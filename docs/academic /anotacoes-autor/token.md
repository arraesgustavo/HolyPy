# Análise Léxica — HolyPy

## Validação de Completude Léxica

### Conflitos e Ambiguidades

- **`=` como `T_ATR` e `T_EQ` é ambíguo no léxico** (mesmo lexema).  
  **Melhor prática:** usar um único token léxico (`T_ASSIGN_OR_EQ`) e desambiguação sintática, ou mudar igualdade para `==`.

- **Sobreposição entre operadores compostos e simples:**

  | Composto | Simples |
  |:--------:|:-------:|
  | `!=`     | `!`     |
  | `>=`     | `>`     |
  | `<=`     | `<`     |
  | `->`     | `-`     |

  Exige **maximal munch** (casar o mais longo primeiro) em `Lexer.tokenize`.

- **Palavras reservadas colidem com `T_ID`** por definição formal (ex.: `if`, `mod`, `i32` também casariam em `T_ID`).  
  Resolver com tabela de reservadas como `RESERVED_WORDS`, priorizando keyword após casar identificador.

---

### Lacunas Prováveis

Com base em `LanguageSpecifications.md`, `README.md` e `enunciadoTrabalho.md`, os seguintes tokens **estão ausentes ou inconsistentes** em `token_regex.md`:

| Token / Construção | Situação |
|:---|:---|
| `;` e `.` | Aparecem no enunciado, mas não estão tokenizados |
| Literal de caractere `'a'` | Não há token definido |
| Número hexadecimal `0x1000` | Citado no README, sem token |
| Expoente em número `1.0E-3` | Não há token definido |
| Escape em string `\"`, `\n` | Não modelado no padrão de `T_STR` |
| Comentário multilinha | Somente `#.*` está modelado |
| `[` `]` (índice/array) e `.` (membro) | Possivelmente necessários para evolução da linguagem |

> **Inconsistência semântica entre documentos:** `print`/`input` vs. `speak`/`receive` e `break` vs. `free`.

---

### Tipos Estruturais: Reservadas vs. `T_ID`

**Mais correto:** tratar `i32`, `u64`, `f32`, etc. como tokens próprios (`T_INT` / `T_UINT` / `T_FLOAT`), **não** como `T_ID`.

**Vantagem:** gramática mais limpa e análise semântica mais previsível.

---

### Ordem de Casamento (Essencial)

Ordem recomendada no lexer para evitar tokenização incorreta:

1. Operadores compostos: `->`, `!=`, `>=`, `<=`
2. Operadores simples: `!`, `-`, `>`, `<`, `=`
3. Identificadores, keywords e tipos

---

## Análise Teórica — Compiladores

### Linguagens Regulares (Tipo 3 de Chomsky)

Sim, as expressões regulares definidas são **linguagens regulares (Tipo 3 de Chomsky)**, pois utilizam apenas concatenação, união e fechamento de Kleene — operações implementáveis por DFA/NFA.

> Não há nenhuma expressão na tabela que exija poder computacional acima de um autômato finito. Não há balanceamento de parênteses, dependências de contagem ou outras construções que exijam gramáticas livres de contexto.

---

### AFD para `T_ID`

| Estado | Tipo | Transições |
|:---|:---|:---|
| `q0` | Inicial | `[A-Za-z_]` → `q1` |
| `q1` | Aceitação | `[A-Za-z0-9_]` → `q1` / outros → fim do token |

```
q0 --[A-Za-z_]--> q1
q1 --[A-Za-z0-9_]--> q1
```

---

### AFD para `T_NUM`

| Estado | Tipo | Transições |
|:---|:---|:---|
| `q0` | Inicial | `[0-9]` → `q1` |
| `q1` | Aceitação (inteiro) | `[0-9]` → `q1` / `.` → `q2` |
| `q2` | Não-aceitação (após ponto) | `[0-9]` → `q3` |
| `q3` | Aceitação (decimal) | `[0-9]` → `q3` |

```
q0 --[0-9]--> q1
q1 --[0-9]--> q1
q1 --[.]--> q2
q2 --[0-9]--> q3
q3 --[0-9]--> q3
```

---

### "O Lexer é LL(1)?"

> **LL(1) é uma propriedade de parser, não de lexer.**

O léxico aqui é implementado como **DFA + prioridade + maximal munch**.

- **Lookahead prático:** 1 caractere é suficiente para operadores compostos (`!`/`!=`, `-`/`->`, etc.).
- **Ponto crítico:** o `=` com dois significados **não se resolve no DFA por lookahead** — exige regra sintática ou contextual para desambiguação.

---

## T\_NUM — Literal Numérico

```
[+-]?(0[xX][0-9A-Fa-f]+|((([0-9]+(\.[0-9]*)?)|(\.[0-9]+))([eE][+-]?[0-9]+)?))
```

O `[+-]?` no início é o sinal opcional — aceita `+`, `-` ou nada.

Depois disso, a expressão se divide em **dois ramos** com `|`:

**Ramo 1 — Hexadecimal:** `0[xX][0-9A-Fa-f]+`
Começa obrigatoriamente com `0x` ou `0X`, seguido de um ou mais dígitos hex (`0-9`, `a-f`, `A-F`). Captura `0x1000`, `0xFF`, `0xABCD`.

**Ramo 2 — Decimal/Float:** `(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))([eE][+-]?[0-9]+)?`

Esse ramo também se subdivide:

- `[0-9]+(\.[0-9]*)?` → inteiro com parte decimal **opcional**: aceita `42`, `3.14`, e até `3.` (ponto sem dígitos depois)
- `\.[0-9]+` → começa com ponto obrigatório: aceita `.5`, `.001`

Por fim, `([eE][+-]?[0-9]+)?` é o **expoente opcional**, aplicado a qualquer um dos dois sub-ramos: `2E10`, `1.5e-3`, `0.1E+2`.

| Lexema | Ramo casado |
|:---|:---|
| `42` | decimal inteiro |
| `-3.14` | sinal + decimal float |
| `+2E10` | sinal + inteiro + expoente |
| `0x1000` | hexadecimal |
| `.5e-2` | ponto inicial + expoente |

---

## T\_CHAR\_LIT — Literal de Caractere

```
'(\\.|[^'\\])'
```

Abre e fecha com aspas simples `' '`. O conteúdo entre elas aceita **exatamente um** dos dois padrões:

- `\\.` → uma barra invertida seguida de **qualquer caractere**: captura sequências de escape como `'\n'`, `'\t'`, `'\\'`, `'\''`
- `[^'\\]` → qualquer caractere que **não seja** `'` nem `\`: captura `'a'`, `'Z'`, `'@'`

O `|` entre eles garante que escape tem prioridade. Como não há `*` ou `+`, a expressão aceita **somente um caractere** (ou um escape), o que é semanticamente correto para um `char`.

| Lexema | Padrão casado |
|:---|:---|
| `'a'` | `[^'\\]` |
| `'\n'` | `\\.` (escape) |
| `'\\'` | `\\.` (barra escapada) |
| `''` | ❌ rejeitado (vazio) |
| `'ab'` | ❌ rejeitado (dois chars) |

---

## T\_STR — Literal de String

```
"(\\.|[^"\\])*"
```

Estrutura quase idêntica ao `T_CHAR_LIT`, com duas diferenças importantes:

- Usa aspas **duplas** `" "` em vez de simples
- O `*` no lugar do implícito "um único" permite **zero ou mais caracteres** — strings vazias `""` são válidas

O conteúdo interno repete o mesmo padrão de dois ramos:

- `\\.` → escape: `\"`, `\n`, `\\`, `\t`
- `[^"\\]` → qualquer caractere exceto `"` e `\`

O `[^"\\]` é essencial: sem ele, uma aspa dupla dentro da string fecharia ela prematuramente, e uma barra invertida isolada quebraria o parser. A alternância com `\\.` garante que `\"` é consumido **antes** de `[^"\\]` tentar casá-lo.

| Lexema | Observação |
|:---|:---|
| `"Ola"` | três chars normais |
| `""` | string vazia, válida |
| `"linha\n"` | escape no meio |
| `"aspas \"aqui\""` | aspas escapadas dentro |
| `"abc` | ❌ sem fechamento |