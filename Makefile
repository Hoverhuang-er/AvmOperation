# Makefile for avmoperation project
# This is optional and provided for convenience - not required for the package to work

.PHONY: help install install-dev clean lint format test test-cov build upload check pre-commit

help:
	@echo "Available commands:"
	@echo "  make install       - Install package in current environment"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make clean         - Remove build artifacts and caches"
	@echo "  make lint          - Run linting checks (ruff)"
	@echo "  make format        - Format code (ruff format)"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make build         - Build wheel and sdist packages"
	@echo "  make check         - Check package integrity"
	@echo "  make pre-commit    - Install pre-commit hooks"
	@echo "  make all           - Run format, lint, test, and build"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	@echo "Running ruff linter..."
	ruff check .

format:
	@echo "Formatting code with ruff..."
	ruff format .
	ruff check --fix .

test:
	@echo "Running tests..."
	pytest -v

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=avmoperation --cov=main --cov-report=html --cov-report=term

build: clean
	@echo "Building package..."
	python -m build

check: build
	@echo "Checking package integrity..."
	twine check dist/*

pre-commit:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed!"

all: format lint test build
	@echo "All tasks completed successfully!"
