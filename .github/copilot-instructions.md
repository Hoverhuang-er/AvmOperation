# GitHub Copilot Instructions for AvmOperation

## Project Overview
Azure Virtual Machine operations library with webhook notifications. Supports Python 3.11+ including free-threaded Python 3.14.

## Development Commands
- Install: `uv pip install -e .` or `pip install -e .`
- Install dev dependencies: `uv pip install -e ".[dev]"` or `pip install -e ".[dev]"`
- Run tests: `pytest -v` or `make test`
- Run single test: `pytest -v path/to/test_file.py::test_function_name`
- Test with coverage: `pytest --cov=avmoperation --cov=main --cov-report=html --cov-report=term`
- Lint code: `ruff check .` or `make lint`
- Format code: `ruff format .` or `make format`
- Build package: `python -m build` or `make build`
- Clean artifacts: `make clean`

## Code Style Requirements

### Python Standards
- **Python version**: 3.11+ (test compatibility up to 3.14 free-threaded)
- **Line length**: 88 characters (Ruff default)
- **Indentation**: 4 spaces (never tabs)
- **Line endings**: LF (Unix style)
- **String quotes**: Single quotes preferred (use double quotes only to avoid escaping)

### Import Organization
Order imports in three groups, sorted alphabetically within each group:
1. Standard library imports
2. Third-party imports (azure-identity, azure-mgmt-compute, requests)
3. Local application imports

Example:
```python
import os
from typing import Optional

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
import requests

from avmoperation import helper_function
```

### Type Hints
- Required for all public functions and methods
- Use `Optional`, `List`, `Dict`, `Tuple` from typing module
- Example: `def start_vm(...) -> bool:`
- Example: `def get_status(...) -> Optional[str]:`

### Naming Conventions
- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: prefix with single underscore `_private_method`

### Docstrings
Use Google style docstrings for all public functions and classes:

```python
def start_vm(subscription_id: str, vm_name: str) -> bool:
    """Start an Azure virtual machine.
    
    Args:
        subscription_id: Azure subscription ID
        vm_name: Name of the virtual machine
        
    Returns:
        True if VM started successfully, False otherwise
    """
```

### Error Handling
- **User-facing functions**: Return `bool` for success/failure
- **Internal functions**: May raise exceptions
- Log errors using print() or logging module, don't raise for user-facing operations
- Example:
```python
def start_vm(...) -> bool:
    try:
        # operation
        return True
    except Exception as e:
        print(f'Error starting VM: {e}')
        return False
```

### Function Design
- Keep functions focused and single-purpose
- Return boolean for success/failure operations
- Return `Optional[str]` for status queries (None on failure)
- Accept all Azure credentials as explicit parameters

## Testing
- Write tests for all new features and bug fixes
- Use pytest framework
- Test files should be named `test_*.py` or `*_test.py`
- Mock Azure API calls to avoid live API dependencies
- Ensure compatibility across Python 3.11, 3.12, 3.13, and 3.14

## Dependencies
Core dependencies (keep versions aligned with pyproject.toml):
- `requests>=2.31.0`
- `azure-identity>=1.15.0`
- `azure-mgmt-compute>=30.0.0`

Dev dependencies:
- `pytest>=7.0.0`
- `pytest-cov>=4.0.0` (for test coverage)
- `ruff>=0.1.0` (linting and formatting)

## Project Structure
```
avmoperation/
├── avmoperation/          # Main package directory
│   ├── __init__.py       # Exports: start_vm, stop_vm, check_status, AvmOperation
│   └── ...               # Implementation modules
├── tests/                # Test files
├── example.py            # Usage examples
├── pyproject.toml        # Project configuration
└── README.md             # Documentation
```

## API Design Guidelines
The library provides both functional and object-oriented interfaces:

### Functional Interface
```python
from avmoperation import start_vm, stop_vm, check_status

start_vm(subscription_id=..., vm_name=..., resource_group=..., ...)
stop_vm(subscription_id=..., vm_name=..., resource_group=..., ...)
status = check_status(subscription_id=..., vm_name=..., resource_group=..., ...)
```

### Object-Oriented Interface
```python
from avmoperation import AvmOperation

operator = AvmOperation(subscription_id=..., vm_name=..., ...)
operator.start_vm()
operator.stop_vm()
status = operator.get_status()
```

## Webhook Integration
- Support webhook notifications for VM operations
- Default format: Feishu/Lark compatible
- Allow mode parameter: 'dev' for local logging, other values for webhook
- Webhook messages should include: action, VM name, resource group, status, timestamp

## Pre-commit Hooks
Optional but recommended. Install with: `pre-commit install`
- YAML syntax checking
- End of file fixes
- Trailing whitespace trimming
- Large file detection
- Merge conflict detection
- Ruff linting and formatting

## Best Practices
- Use environment variables for credentials, never hardcode
- Implement proper credential handling with Service Principal authentication
- Support both uv and pip package managers
- Keep backward compatibility with Python 3.11+
- Write clear, descriptive commit messages
- Update tests when changing functionality
- Run `make format` and `make lint` before committing
