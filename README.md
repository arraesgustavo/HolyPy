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
- Void (functions)
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
print     - Output
input     - Input
```

### Example Program

```holypy
let x: i32
let y: i32

fn add(a: i32, b: i32) -> i32 {
    return a + b
}

fn main() -> i32 {
    print("Enter two numbers:")
    input(x)
    input(y)
    
    let sum: i32 = add(x, y)
    print("Sum: ", sum)
    
    return 0
}
```

---

## Architecture

The HolyPy compiler follows a classic multi-phase architecture:

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

### Compiler Phases

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

## Project Structure

```
HolyPy/
├── src/                          # Compiler source
│   ├── __init__.py
│   ├── lexer/                    # Lexical analyzer
│   │   ├── __init__.py
│   │   ├── tokens.py             # Token definitions
│   │   └── lexer.py              # Lexer implementation
│   ├── parser/                   # Syntax analyzer
│   │   ├── __init__.py
│   │   └── parser.py             # Parser implementation
│   ├── ast/                      # AST node definitions
│   │   ├── __init__.py
│   │   └── nodes.py              # Dataclass AST nodes
│   ├── semantic/                 # Semantic analysis
│   │   ├── __init__.py
│   │   ├── analyzer.py           # Semantic analyzer
│   │   └── symbol_table.py       # Symbol table & scopes
│   ├── codegen/                  # Code generation
│   │   ├── __init__.py
│   │   └── c_generator.py        # C code generator
│   └── runtime/                  # Runtime support
│       └── runtime.h             # Runtime stubs
├── examples/                     # Example .hpy programs
│   ├── io_example.hpy            # I/O example
│   ├── conditional_example.hpy   # Conditional example
│   ├── loop_example.hpy          # Loop example
│   └── expected_output/          # Expected C output
├── tests/                        # Unit tests
│   ├── conftest.py               # Pytest configuration
│   ├── lexer/
│   ├── parser/
│   ├── semantic/
│   └── codegen/
├── docs/                         # Academic documentation
│   ├── ARCHITECTURE.md           # Compiler architecture
│   ├── regex/                    # Token regexes
│   │   └── token_regex.md
│   ├── automata/                 # DFA/NFA diagrams
│   │   └── dfa_overview.md
│   └── grammar/                  # Grammar & derivations
│       ├── productions.md
│       └── derivation_tree.md
├── scripts/                      # Utility scripts
│   ├── build.sh                  # Build generated C
│   ├── run.sh                    # Compile & run
│   └── clean.sh                  # Clean artifacts
├── output/                       # Generated C files (gitignored)
├── main.py                       # CLI entry point
├── Makefile                      # Build targets
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md                     # This file
```

---

## Documentation

### Academic Requirements

#### Part 1 (Theory & Documentation)

- **Token Regular Expressions**: [docs/regex/token_regex.md](docs/regex/token_regex.md)
  - Regular expressions for each token category
  - Examples and lexical rules

- **Finite Automata**: [docs/automata/dfa_overview.md](docs/automata/dfa_overview.md)
  - DFAs derived from regular expressions
  - NFA → NFA-ε → DFA conversion (Thompson's method)
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

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for:
- Compilation pipeline overview
- Module organization and responsibilities
- Design patterns (Visitor, Symbol Table)
- Type system
- Error handling

---

## License

Academic project for UNIFEI, ECOM06 course.

---

## References

### Compiler Books
- *Compilers: Principles, Techniques, and Tools* (Dragon Book), 2nd Edition
  - Aho, Sethi, Ullman
  - Chapters 1-6: Lexing, Parsing, Semantic Analysis
  
- *Crafting Interpreters* — https://craftinginterpreters.com
  - Excellent for practical compiler implementation

### Tools & Frameworks
- **PLY** (Python Lex-Yacc) — https://www.dabeaz.com/ply/
- **LLVM** — https://llvm.org (for future phases)
- **GCC** — https://gcc.gnu.org (C backend target)

