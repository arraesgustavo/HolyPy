# HolyPy Compiler Architecture

## Overview

HolyPy is a hybrid programming language compiler that targets C. This document outlines the overall architecture and compilation pipeline of the HolyPy compiler.

## Compilation Pipeline

```
Source (.hpy)
    ↓
[Lexer] → Tokenization
    ↓
[Parser] → Syntax Analysis & AST Construction
    ↓
[Semantic Analyzer] → Type Checking & Scope Analysis
    ↓
[Code Generator] → C Code Generation
    ↓
Output (.c) → C Backend (GCC/Clang)
    ↓
Binary Executable
```

## Module Organization

### Lexer (`src/lexer/`)
- **Purpose**: Tokenizes raw source code into a stream of tokens
- **Key Files**: `tokens.py`, `lexer.py`
- **Interface**: `Lexer.tokenize(source: str) -> List[Token]`

### Parser (`src/parser/`)
- **Purpose**: Performs syntax analysis and constructs Abstract Syntax Tree
- **Key Files**: `parser.py`
- **Interface**: `Parser.parse(tokens: List[Token]) -> Program`
- **Strategy**: Recursive descent parsing

### AST (`src/ast/`)
- **Purpose**: Defines all Abstract Syntax Tree node types
- **Key Files**: `nodes.py`
- **Node Types**: Program, FnDecl, VarDecl, IfStmt, CycleStmt, BinOp, Literal, etc.

### Semantic Analyzer (`src/semantic/`)
- **Purpose**: Type checking, scope analysis, and semantic validation
- **Key Files**: `analyzer.py`, `symbol_table.py`
- **Responsibilities**:
  - Symbol table management
  - Type inference and checking
  - Scope validation
  - Function/variable validation

### Code Generator (`src/codegen/`)
- **Purpose**: Generates valid C code from annotated AST
- **Key Files**: `c_generator.py`
- **Interface**: `CGenerator.generate(ast: Program) -> str`
- **Output**: Valid C source code

### Runtime (`src/runtime/`)
- **Purpose**: Minimal runtime support for compiled programs
- **Key Files**: `runtime.h`
- **Provides**: print(), input(), chain/unchain stubs

## Design Patterns

### Visitor Pattern
The semantic analyzer and code generator use the visitor pattern to traverse the AST.

### Symbol Table
A hierarchical symbol table manages variable/function declarations across nested scopes.

### Error Handling
All phases collect and report errors before aborting compilation.

## Key Data Structures

### Token
```
Token(type: TokenType, lexeme: str, literal: Optional[str], line: int, column: int)
```

### AST Nodes
All AST nodes inherit from `ASTNode` and use Python `@dataclass` decorators for clean structure.

## Compilation Modes

- **Default**: Compile source → Generate C → Output .c file
- **`--emit-tokens`**: Stop after lexer, output token list
- **`--emit-ast`**: Stop after parser, output AST
- **`--emit-c`**: Show generated C code
- **`--run`**: Compile and execute immediately

## Type System

HolyPy supports explicit and inferred types:

- **Explicit**: `let x: i32 = 42`
- **Inferred**: `let y = 3.14`

### Supported Types
- Integers: `i8, i16, i32, i64, u8, u16, u32, u64`
- Floats: `f32, f64`
- Characters: `char`
- Booleans: `bool`
- Void: `void` (for functions with no return value)

## Error Handling

All compiler phases collect errors and continue analysis when possible, allowing multiple errors to be reported simultaneously.

---

See also:
- [`docs/regex/`](docs/regex/) — Token regular expressions
- [`docs/automata/`](docs/automata/) — DFA/NFA diagrams
- [`docs/grammar/`](docs/grammar/) — Grammar productions
