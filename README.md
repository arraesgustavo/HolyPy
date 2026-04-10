# HolyPy Compiler

A hybrid programming language compiler project for **ECOM06 – Compiladores** at **UNIFEI** (Universidade Federal de Itajubá).

HolyPy is a high-level to low-level hybrid language with Python-like syntax that compiles to C code and eventually to LLVM IR. This project implements a complete compiler pipeline including lexical analysis, parsing, semantic analysis, and code generation.

---

## Table of Contents

- [Project Context](#project-context)
- [Language Features](#language-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Building & Running](#building--running)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Deliverables](#deliverables)
- [Contributing](#contributing)

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

## Setup & Installation

### Prerequisites

- **Python 3.9+**
- **GCC or Clang** (for compiling generated C code)
- **pip** (Python package manager)

### Installation Steps

1. **Clone or extract the project**
   ```bash
   cd HolyPy
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make scripts executable** (Linux/macOS)
   ```bash
   chmod +x scripts/*.sh
   ```

4. **Verify installation**
   ```bash
   python main.py --help
   ```

---

## Building & Running

### Using Makefile

```bash
# Show all targets
make help

# Run all tests
make test

# Test specific module
make test-lexer
make test-parser
make test-semantic
make test-codegen

# Run with coverage
make coverage

# Compile a .hpy file
make build FILE=examples/io_example.hpy

# Compile and run
make run FILE=examples/io_example.hpy

# Run all examples
make run-all-examples

# Clean artifacts
make clean
```

### Using CLI Directly

```bash
# Compile to C output
python main.py examples/io_example.hpy

# Show tokenization
python main.py examples/io_example.hpy --emit-tokens

# Show AST
python main.py examples/io_example.hpy --emit-ast

# Show generated C
python main.py examples/io_example.hpy --emit-c

# Compile and run
python main.py examples/io_example.hpy --run

# Specify output file
python main.py examples/io_example.hpy --output my_program.c
```

### Using Shell Scripts

```bash
# Build generated C code
./scripts/build.sh output/program.c

# Full pipeline: compile and run
./scripts/run.sh examples/io_example.hpy

# Clean build artifacts
./scripts/clean.sh
```

---

## Testing

### Run All Tests

```bash
make test
```

### Run Specific Test Suite

```bash
make test-lexer      # Lexer unit tests
make test-parser     # Parser unit tests
make test-semantic   # Semantic analyzer tests
make test-codegen    # Code generator tests
```

### Coverage Report

```bash
make coverage
```

Generates an HTML coverage report in `htmlcov/`.

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── lexer/test_lexer.py      # Lexer tests
├── parser/test_parser.py    # Parser tests
├── semantic/test_semantic.py  # Semantic analyzer tests
└── codegen/test_codegen.py  # Code generator tests
```

Each test module contains placeholder test functions (docstrings with TODO comments) ready for implementation.

---

## Examples

Three complete example programs are provided in the `examples/` directory:

### 1. I/O Example (`io_example.hpy`)

Demonstrates reading input and printing output.

```holypy
let num1: i32
let num2: i32

fn main() -> i32 {
    print("Enter first number: ")
    input(num1)
    
    print("Enter second number: ")
    input(num2)
    
    let sum: i32 = num1 + num2
    print("Sum: ", sum)
    
    return 0
}
```

**Run**: `make run FILE=examples/io_example.hpy`

---

### 2. Conditional Example (`conditional_example.hpy`)

Demonstrates if/else conditional logic.

```holypy
fn is_positive(x: i32) -> i32 {
    if (x > 0) {
        print("Number is positive")
        return 1
    }
    
    if (x < 0) {
        print("Number is negative")
        return -1
    }
    
    print("Number is zero")
    return 0
}

fn main() -> i32 {
    let number: i32 = 42
    is_positive(number)
    return 0
}
```

**Run**: `make run FILE=examples/conditional_example.hpy`

---

### 3. Loop Example (`loop_example.hpy`)

Demonstrates cycle (loop) constructs.

```holypy
fn sum_range(n: i32) -> i32 {
    let sum: i32 = 0
    let i: i32 = 1
    
    cycle {
        if (i > n) {
            break
        }
        
        sum = sum + i
        i = i + 1
    }
    
    return sum
}

fn main() -> i32 {
    let result: i32 = sum_range(10)
    print("Sum of 1..10: ", result)
    return 0
}
```

**Run**: `make run FILE=examples/loop_example.hpy`

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

## Deliverables

### Part 1 (Theory)
- [x] Regular expressions for tokens
- [x] DFAs from regex (Thompson's method)
- [x] BNF/EBNF grammar with detailed explanation
- [x] Derivation trees with worked examples

### Part 2 (Implementation) — WIP
- [ ] Full lexer implementation
- [ ] Full parser implementation
- [ ] AST construction
- [ ] Semantic analysis (type checking, scopes, validation)
- [ ] C code generation backend
- [ ] Three example programs with working output
- [ ] Token recognition log file generation
- [ ] README with build/run instructions
- [ ] Source compiles without errors

---

## Building the Project

### Development Build

```bash
# Install dev dependencies
make install

# Run tests
make test

# Generate coverage report
make coverage

# Format code (placeholder)
make fmt

# Lint code (placeholder)
make lint
```

### Clean Build

```bash
# Remove all artifacts
make clean

# Rebuild everything
make test
```

---

## Error Handling

The compiler collects errors from all phases and reports them before aborting. Each error includes:
- Source location (line:column)
- Error type (lexical, syntax, semantic)
- Descriptive message

Example:
```
Semantic Error at 5:12: Undefined variable 'foo'
Type Error at 10:5: Expected i32, got f64
```

---

## Contributing

This is an academic project for ECOM06. Team members should:

1. Follow the architecture defined in `docs/ARCHITECTURE.md`
2. Write tests for new features in `tests/`
3. Keep docstrings comprehensive and up-to-date
4. Use type hints in Python code
5. Follow PEP 8 style guidelines

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

---

## Contact

**Project**: HolyPy Compiler  
**Course**: ECOM06 – Compiladores  
**Institution**: UNIFEI  

---

**Last Updated**: April 10, 2026  
**Status**: Scaffolding Complete ✓
