# Agent Guidelines for AvmOperation

## Build/Test Commands
- **Install**: `uv pip install -e .` or `pip install -e .`
- **Install dev**: `uv pip install -e ".[dev]"` or `pip install -e ".[dev]"`
- **Test all**: `pytest -v` or `make test`
- **Test single**: `pytest -v path/to/test_file.py::test_function_name`
- **Test with coverage**: `pytest --cov=avmoperation --cov=main --cov-report=html --cov-report=term`
- **Lint**: `ruff check .` or `make lint`
- **Format**: `ruff format .` or `make format`
- **Build**: `python -m build` or `make build`
- **Clean**: `make clean`

## Code Style
- **Python version**: 3.11+ (supports up to 3.14 free-threaded)
- **Formatter**: Ruff (88 char line length)
- **Imports**: Group standard lib, third-party, then local; sort alphabetically
- **Type hints**: Required for public APIs; use Optional, List, Dict from typing
- **Indentation**: 4 spaces (never tabs) for .py files
- **Line endings**: LF (Unix style)
- **Docstrings**: Use for all public functions/classes; follow Google style
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Error handling**: Return bool for success/failure; log errors, don't raise for user-facing functions
- **String quotes**: Single quotes preferred unless double quotes avoid escaping
