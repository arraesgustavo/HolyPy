"""
pdf_to_md.py — Converte PDF para Markdown limpo
================================================
Corrige automaticamente:
  • Acentos LaTeX separados como words (´ ˜ ¸ …) → recolados à letra base
  • Acentos em consoante errada (bug OT1/CM fonts) → movidos para vogal seguinte
  • Cabeçalho repetido a cada página → removido
  • (cid:N) glifos sem mapeamento → removidos
  • Palavras coladas sem espaço (bbox gap) → separadas
  • Dotless-i (U+0131) de fontes LaTeX → substituído por 'i'
  • Número de página solto → removido

Uso:
    python pdf_to_md.py documento.pdf
    python pdf_to_md.py documento.pdf -o saida.md

Dependências:
    pip install pdfplumber
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Instale a dependência: pip install pdfplumber")
    sys.exit(1)


# ── Constantes ────────────────────────────────────────────────────────────────

HEADER_Y_THRESHOLD = 110   # px do topo → acima disso é cabeçalho
HEADING_SIZE_H1    = 16.0
HEADING_SIZE_H2    = 13.0
LINE_Y_TOLERANCE   = 3.0   # pts para agrupar words na mesma linha
WORD_GAP_THRESHOLD = 1.5   # pts de gap → insere espaço


# ── Mapa: spacing accents → combining Unicode ─────────────────────────────────

SPACING_TO_COMBINING = {
    "\u00B4": "\u0301",   # ACUTE ACCENT
    "\u0060": "\u0300",   # GRAVE ACCENT
    "\u00B8": "\u0327",   # CEDILLA
    "\u02DC": "\u0303",   # SMALL TILDE
    "\u02C6": "\u0302",   # MODIFIER CIRCUMFLEX
    "\u00A8": "\u0308",   # DIAERESIS
    "\u02DB": "\u0328",   # OGONEK
    "\u02D8": "\u0306",   # BREVE
    "\u02D9": "\u0307",   # DOT ABOVE
    "\u02DA": "\u030A",   # RING ABOVE
    "\u02C7": "\u030C",   # CARON
}

# Letras que não levam acento em português/espanhol
# (usadas para detectar acento na consoante errada — bug LaTeX OT1)
_CONSONANTS_NO_ACCENT = set("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ")
_VOWELS               = set("aeiouAEIOU")

CID_RE  = re.compile(r"\(cid:\d+\)")
LIST_RE = re.compile(r"^(\d+\.)\s+|^[-•●▸*]\s+")


# ── Correção de texto ─────────────────────────────────────────────────────────

def _fix_word_accents(text: str) -> str:
    """
    Percorre o texto char a char tratando:
    - Spacing accents (U+00B4, U+00B8 …) → pending combining → aplicado na próxima letra
    - Combining marks orphãs → aplicadas na letra anterior
    - Dotless-i (U+0131) → 'i'
    """
    chars  = list(text)
    result = []
    pending = ""
    for ch in chars:
        cat = unicodedata.category(ch)
        if ch in SPACING_TO_COMBINING:
            pending += SPACING_TO_COMBINING[ch]
        elif cat.startswith("M"):          # combining mark
            pending += ch
        elif ch == "\u0131":               # dotless i
            base = "i"
            if pending:
                base = unicodedata.normalize("NFC", base + pending)
                pending = ""
            result.append(base)
        else:
            if pending:
                ch = unicodedata.normalize("NFC", ch + pending)
                pending = ""
            result.append(ch)
    return "".join(result)


def _fix_misplaced_accent(text: str) -> str:
    """
    Bug de fontes LaTeX OT1/CM: acento cai na consoante antes da vogal.
    Ex.: ĺexico → léxico, ńisticos → nísticos, Ŕısticas → Rísticas
    Move o acento para a vogal imediatamente seguinte.
    """
    result = list(text)
    for i, ch in enumerate(result):
        decomp = unicodedata.decomposition(ch)
        if not decomp or decomp.startswith("<"):
            continue
        parts = decomp.split()
        if len(parts) != 2:
            continue
        base_char = chr(int(parts[0], 16))
        combining = chr(int(parts[1], 16))
        if (
            base_char in _CONSONANTS_NO_ACCENT
            and unicodedata.category(combining).startswith("M")
            and i + 1 < len(result)
            and result[i + 1] in _VOWELS
        ):
            result[i]     = base_char
            result[i + 1] = unicodedata.normalize("NFC", result[i + 1] + combining)
    return "".join(result)


def fix_text(text: str) -> str:
    text = _fix_word_accents(text)
    text = _fix_misplaced_accent(text)
    return text


# ── Correção de acentos em words separadas (nível word-list) ─────────────────

def fix_accent_words(words: list[dict]) -> list[dict]:
    """
    Trata acentos que chegam como WORDS SEPARADAS no PDF LaTeX.
    Ex.: word "Ministe" + word "´" + word "rio"  →  "Ministério"
    """
    result: list[dict] = []
    i = 0
    while i < len(words):
        w    = words[i]
        text = w["text"]

        # Acento DEPOIS da word atual
        if i + 1 < len(words) and words[i + 1]["text"] in SPACING_TO_COMBINING:
            comb   = SPACING_TO_COMBINING[words[i + 1]["text"]]
            fused  = unicodedata.normalize("NFC", text[-1] + comb)
            w      = dict(w)
            w["text"] = text[:-1] + fused
            i += 2
            result.append(w)
            continue

        # Acento ANTES (word atual É o acento)
        if text in SPACING_TO_COMBINING and i + 1 < len(words):
            comb   = SPACING_TO_COMBINING[text]
            nxt    = words[i + 1]
            fused  = unicodedata.normalize("NFC", nxt["text"][0] + comb)
            merged = dict(nxt)
            merged["text"] = fused + nxt["text"][1:]
            i += 2
            result.append(merged)
            continue

        result.append(w)
        i += 1
    return result


# ── Agrupamento de words em linhas ────────────────────────────────────────────

def group_into_lines(words: list[dict]) -> list[dict]:
    if not words:
        return []
    words = sorted(words, key=lambda w: (w["top"], w["x0"]))
    buckets: list[list[dict]] = [[words[0]]]
    for w in words[1:]:
        if abs(w["top"] - buckets[-1][0]["top"]) <= LINE_Y_TOLERANCE:
            buckets[-1].append(w)
        else:
            buckets.append([w])

    lines = []
    for bucket in buckets:
        bucket.sort(key=lambda w: w["x0"])
        parts = [bucket[0]["text"]]
        for j in range(1, len(bucket)):
            gap = bucket[j]["x0"] - bucket[j - 1]["x1"]
            sep = " " if gap >= WORD_GAP_THRESHOLD else ""
            parts.append(sep + bucket[j]["text"])
        raw_text = "".join(parts)
        avg_size = sum(w.get("size", 10) for w in bucket) / len(bucket)
        lines.append({
            "text": fix_text(raw_text),
            "size": round(avg_size, 1),
            "top":  bucket[0]["top"],
        })
    return lines


# ── Limpeza final ─────────────────────────────────────────────────────────────

def clean(text: str) -> str:
    text = CID_RE.sub("", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


# ── Fingerprint do cabeçalho ──────────────────────────────────────────────────

def get_header_fingerprint(pdf) -> set[str]:
    fp:    set[str] = set()
    page  = pdf.pages[0]
    words = page.extract_words(extra_attrs=["size", "top", "x0", "x1"]) or []
    words = [w for w in words if w["top"] < HEADER_Y_THRESHOLD]
    words = fix_accent_words(words)
    for line in group_into_lines(words):
        t = clean(line["text"])
        if t:
            fp.add(t)
    return fp


# ── Tabelas ───────────────────────────────────────────────────────────────────

def table_to_md(table: list[list]) -> str:
    rows = [[str(c or "").strip() for c in row] for row in table if any(c for c in row)]
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep    = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body   = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join(filter(None, [header, sep, body]))


# ── Conversão principal ───────────────────────────────────────────────────────

def convert(pdf_path: str) -> str:
    out: list[str] = []

    with pdfplumber.open(pdf_path) as pdf:
        header_fp = get_header_fingerprint(pdf)

        for page_num, page in enumerate(pdf.pages, start=1):
            out.append(f"\n<!-- página {page_num} -->\n")

            # Tabelas
            tables      = page.extract_tables() or []
            table_texts: set[str] = set()
            for tbl in tables:
                md = table_to_md(tbl)
                if md:
                    out.append(md + "\n")
                for row in tbl:
                    for cell in row:
                        if cell:
                            table_texts.add(str(cell).strip())

            # Words → fix acentos separados → linhas
            words = page.extract_words(extra_attrs=["size", "top", "x0", "x1"]) or []
            words = [w for w in words if w["top"] >= HEADER_Y_THRESHOLD]
            words = fix_accent_words(words)
            lines = group_into_lines(words)

            for line in lines:
                text = clean(line["text"])
                if not text:
                    continue
                if text in table_texts:
                    continue
                if text in header_fp:
                    continue
                if text == str(page_num):
                    continue

                size = line["size"]

                if size >= HEADING_SIZE_H1:
                    out.append(f"\n# {text}\n")
                elif size >= HEADING_SIZE_H2:
                    out.append(f"\n## {text}\n")
                elif LIST_RE.match(text):
                    m    = LIST_RE.match(text)
                    body = text[m.end():].strip()
                    pfx  = m.group(1)
                    out.append(f"{pfx} {body}" if pfx else f"- {body}")
                else:
                    out.append(text)

    return "\n".join(out)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Converte PDF para Markdown limpo")
    parser.add_argument("pdf", help="Arquivo .pdf de entrada")
    parser.add_argument("-o", "--output", help="Arquivo .md de saída")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    out_path = Path(args.output) if args.output else pdf_path.with_suffix(".md")
    print(f"Convertendo: {pdf_path} → {out_path}")
    md = convert(str(pdf_path))
    out_path.write_text(md, encoding="utf-8")
    print(f"Pronto! {out_path} ({len(md)} chars)")


if __name__ == "__main__":
    main()