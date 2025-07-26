# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses Poetry for dependency management and includes a comprehensive Makefile for development tasks:

### Setup
- `make install` - Install core dependencies
- `make install-dev` - Install all development dependencies
- `make install-all` - Install all dependency groups (dev, test, lint, docs)

### Code Quality
- `make format` - Run all formatters (black, isort)
- `make lint` - Run all linters (flake8, pylint, mypy)
- `make check` - Run format, lint, and test (useful for CI)

### Testing
- `make test` - Run tests with pytest
- `make test-cov` - Run tests with coverage
- `make test-file f=<file>` - Run a specific test file
- `make test-pattern p=<pattern>` - Run tests matching a pattern

### Documentation
- `make docs` - Build documentation with Sphinx
- `make docs-live` - Start live documentation server
- `make docs-check` - Check documentation quality with doc8

### Building and Publishing
- `make build` - Build package with Poetry
- `make publish-test` - Publish to TestPyPI
- `make publish` - Publish to PyPI

### Release Management
- `make release-major` - Create major release
- `make release-minor` - Create minor release  
- `make release-micro` - Create micro release

All commands are proxied through `./run.sh` which handles the Poetry environment.

## Project Architecture

This is a Python CLI tool for finding and replacing text in files using regular expressions.

### Core Structure
- **Entry Point**: `src/find_and_replace/main.py` contains all core functionality
- **CLI Interface**: Uses argparse for command-line argument parsing
- **Command**: `find-and-replace` script is defined in pyproject.toml

### Key Components
- `find_files()` - File discovery using glob patterns with recursive support
- `process_file()` - Core find/replace logic with regex processing
- `show_matches_for_confirmation()` - Interactive confirmation for file changes
- `Colors` enum - ANSI color codes for terminal output

### Features
- Regex pattern matching for find/replace operations
- Glob pattern file matching (*.py, config.*, etc.)
- Recursive directory traversal
- Interactive confirmation with preview
- Dry-run mode for safe testing
- Comprehensive error handling for permissions, encoding, and invalid regex

### Testing
- Comprehensive test suite in `tests/test_find_and_replace.py`
- Uses pytest with extensive mocking for file operations
- Tests cover error conditions, user interactions, and edge cases

### Code Quality Tools
- **Black**: Code formatting (line length 119)
- **isort**: Import sorting  
- **flake8**: Linting with custom ignore rules
- **pylint**: Additional static analysis
- **mypy**: Type checking (strict mode enabled)
- **doc8**: Documentation linting

### Version Management
- Uses semantic-release for automated versioning
- Version is synchronized across pyproject.toml, docs/conf.py, and __init__.py