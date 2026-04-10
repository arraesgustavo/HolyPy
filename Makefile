.PHONY: all test clean build run help

PYTHON := python
PYTHON_VERSION := 3.9

# Default target
all: test

# Help target
help:
	@echo "HolyPy Compiler - Build Targets"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Run all tests (default)"
	@echo "  test         - Run all unit tests"
	@echo "  test-lexer   - Run lexer tests only"
	@echo "  test-parser  - Run parser tests only"
	@echo "  test-semantic - Run semantic analyzer tests only"
	@echo "  test-codegen - Run code generator tests only"
	@echo "  coverage     - Run tests with coverage report"
	@echo "  clean        - Remove build artifacts and cache"
	@echo "  run FILE=<path> - Compile and run a .hpy file"
	@echo "  build FILE=<path> - Compile a .hpy file to C"
	@echo "  lint         - Run code linter"
	@echo "  fmt          - Format code (placeholder)"
	@echo "  docs         - Generate documentation (placeholder)"
	@echo ""

# Test target
test:
	$(PYTHON) -m pytest tests/ -v

# Specific test suites
test-lexer:
	$(PYTHON) -m pytest tests/lexer/ -v

test-parser:
	$(PYTHON) -m pytest tests/parser/ -v

test-semantic:
	$(PYTHON) -m pytest tests/semantic/ -v

test-codegen:
	$(PYTHON) -m pytest tests/codegen/ -v

# Coverage report
coverage:
	$(PYTHON) -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Clean artifacts
clean:
	@bash scripts/clean.sh

# Run a specific HolyPy file
run:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make run FILE=<path>"; \
		echo "Example: make run FILE=examples/io_example.hpy"; \
		exit 1; \
	fi
	@bash scripts/run.sh $(FILE)

# Compile a HolyPy file to C
build:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make build FILE=<path>"; \
		echo "Example: make build FILE=examples/io_example.hpy"; \
		exit 1; \
	fi
	@mkdir -p output
	@$(PYTHON) main.py $(FILE) --output output/$$(basename $(FILE) .hpy).c

# Run all three examples
run-all-examples: run-io run-conditional run-loop

run-io:
	@echo "Running I/O example..."
	@bash scripts/run.sh examples/io_example.hpy || true

run-conditional:
	@echo "Running conditional example..."
	@bash scripts/run.sh examples/conditional_example.hpy || true

run-loop:
	@echo "Running loop example..."
	@bash scripts/run.sh examples/loop_example.hpy || true

# Linter (placeholder)
lint:
	@echo "[LINT] Checking code style..."
	@$(PYTHON) -m flake8 src/ main.py --max-line-length=100 || true

# Format code (placeholder)
fmt:
	@echo "[FMT] Formatting code..."
	@$(PYTHON) -m black src/ main.py --line-length=100 || true

# Generate documentation (placeholder)
docs:
	@echo "[DOCS] Documentation is in docs/ directory"
	@echo "       See: docs/ARCHITECTURE.md, docs/regex/, docs/automata/, docs/grammar/"

# Version check
version:
	@$(PYTHON) --version

# Install dependencies
install:
	@$(PYTHON) -m pip install -r requirements.txt

# Development mode install
install-dev:
	@$(PYTHON) -m pip install -r requirements.txt -e .
