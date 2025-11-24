# Contributing to AvmOperation

Thank you for your interest in contributing to AvmOperation!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Hoverhuang-er/AvmOperation.git
cd AvmOperation
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
# or using uv
uv pip install -e ".[dev]"
```

3. (Optional) Install pre-commit hooks:
```bash
pre-commit install
```

## Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: For linting and formatting
- **pytest**: For testing
- **mypy**: For type checking (optional)
- **pre-commit**: For automated checks before commits (optional)

### Running Quality Checks

```bash
# Format code
make format
# or
ruff format .

# Lint code
make lint
# or
ruff check .

# Run tests
make test
# or
pytest

# Run tests with coverage
make test-cov
# or
pytest --cov=avmoperation --cov-report=html
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and maintainable
- Add tests for new features

## Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting PR
- Aim for good test coverage

## Questions?

Feel free to open an issue for any questions or concerns!
