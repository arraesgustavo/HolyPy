# HolyPy Compiler

A hybrid programming language compiler project for **ECOM06 – Compiladores** at **UNIFEI** (Universidade Federal de Itajubá).

HolyPy is a high-level to low-level hybrid language with Python-like syntax that compiles to C code and eventually to LLVM IR. This project implements a complete compiler pipeline including lexical analysis, parsing, semantic analysis, and code generation.

---

## Table of Contents

- [Project Context](#project-context)
- [Language Features](#language-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)

---

## Project Context

**Course**: ECOM06 – Compiladores  
**Institution**: UNIFEI (Universidade Federal de Itajubá)  
**Semester**: Nono Semestre  
**Project Name**: HolyPy Compiler  

### MVP (Part 1) Features

- Data types: integer, real/float, char
- Commands: assignment, input/output, conditionals (if), loops (cycle)
- Operators: relational, logical, arithmetic
- Variable declarations with `let` and optional explicit types
- Function declarations with `fn`
- Built-in `print()` function

### Phase 2+ Features (Future)

- Hybrid typing (inferred + explicit)
- Inline assembly: `asm { }`
- Execution modes: `!kernel`, `!embedded`
- Infinite loops: `cycle { }`
- Manual memory: `chain(n)` / `unchain(ptr)`
- Pointers: `let ptr: *u32 = 0x1000`

---

## Language Features

### Data Types

```
- Signed Integers: i8, i16, i32, i64
- Unsigned Integers: u8, u16, u32, u64
- Floating Point: f32, f64
- Characters: char
- Booleans: bool
```

### Operators

**Arithmetic**: `+`, `-`, `*`, `/`, `mod`  
**Relational**: `=`, `!=`, `<`, `>`, `<=`, `>=`  
**Logical**: `and`, `or`, `not`  

### Keywords

```
let       - Variable declaration
fn        - Function declaration
if        - Conditional
cycle     - Loop
return    - Return from function
speak     - Output
receive     - Input
```

### Example Program

```holypy
let x: i32
let y: i32

fn add(a: i32, b: i32) -> i32 {
    return a + b
}

fn main() -> i32 {
    speak("Enter two numbers:")
    input(x)
    input(y)
    
    let sum: i32 = add(x, y)
    speak("Sum: ", sum)
    
    return 0
}
```

---

## Architecture

The HolyPy compiler is designed to follow, in the future, a classic multi-phase architecture:

```
Source (.hpy)
    ↓
[Lexer] ──→ Tokenization
    ↓
[Parser] ──→ AST Construction
    ↓
[Semantic Analyzer] ──→ Type Checking & Validation
    ↓
[Code Generator] ──→ C Code Emission
    ↓
Output (.c) ──→ C Backend (GCC/Clang)
    ↓
Binary Executable
```

### Compiler Phases (For future implementation)

1. **Lexical Analysis (Lexer)**
   - Tokenizes source into a stream of tokens
   - Recognizes keywords, identifiers, operators, literals
   - Maintains line/column information for error reporting

2. **Syntax Analysis (Parser)**
   - Implements recursive descent parsing
   - Constructs Abstract Syntax Tree (AST)
   - Enforces grammar rules and syntax

3. **Semantic Analysis**
   - Type checking and inference
   - Scope management and symbol table
   - Function/variable validation

4. **Code Generation**
   - Traverses annotated AST
   - Emits equivalent C code
   - Handles type mapping and runtime calls

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

## Documentation

### Academic Requirements

#### Part 1 (Theory & Documentation)

- **Token Regular Expressions**: [docs/regex/token_regex.md](docs/regex/token_regex.md)
  - Regular expressions for each token category
  - Examples and lexical rules

- **Finite Automata**: [docs/automata/](docs/automata/)
  - DFAs derived from regular expressions
  - State diagrams and descriptions

- **Grammar Productions**: [docs/grammar/productions.md](docs/grammar/productions.md)
  - BNF/EBNF grammar rules for all language constructs
  - Operator precedence and associativity

- **Derivation Trees**: [docs/grammar/derivation_tree.md](docs/grammar/derivation_tree.md)
  - Complete worked examples showing derivation trees
  - Demonstrates grammar usage

#### Part 2 (Implementation)

- Compiler source code in `src/`
- Unit tests in `tests/`
- Three example programs in `examples/` with expected C output

### Architecture Documentation

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for future resolutions on the architecture and development.

---

## License

Academic project for UNIFEI, ECOM06 course.

---

## References

### Compiler Books
- *Compilers: Principles, Techniques, and Tools* (Dragon Book), 2nd Edition
  - Aho, Sethi, Ullman
  - Chapters 1-6: Lexing, Parsing, Semantic Analysis

### Tools & Frameworks
- **PLY** (Python Lex-Yacc) — https://www.dabeaz.com/ply/
- **LLVM** — https://llvm.org (for future phases)
- **GCC** — https://gcc.gnu.org (C backend target)

