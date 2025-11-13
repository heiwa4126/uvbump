# bumpuv Project Rules

## Project Overview

- This is a Python CLI tool for version bumping in pyproject.toml files, similar to npm version
- Package name: bumpuv
- Target Python version: >=3.10
- Build system: uv_build
- License: MIT
- Virtual environment: Uses uv's built-in venv management

## Core Functionality

- Version bumping: major, minor, patch, bump operations
- Git integration: automatic commits and tagging
- PEP 440 compliant version validation
- Pre-release version support
- Dry-run mode for safe testing
- Safety checks for git repository state

## Code Style

- Use dataclasses for structured data
- Keep functions minimal and focused
- Follow Python naming conventions
- Use type hints where appropriate
- Separate core logic from CLI interface

## Testing

- Test files should be named `*_test.py`
- Use pytest for testing
- Unit tests for core functions (`_core_test.py`)
- Integration tests using temporary directories (`_integration_test.py`)
- Test both functionality and error conditions

## Dependencies

- Runtime dependencies: GitPython, packaging, tomli/tomli-w
- Development dependencies: mypy, pytest, ruff, poethepoet
- Use uv for dependency management and virtual environments

## Development Environment

- Use `uv run` for executing commands in the virtual environment
- Use `poe` (poethepoet) for task automation
- Support multiple Python versions (3.10+) for testing
- Use `uv python install` to manage Python versions

## File Structure

- Source code in `src/bumpuv/`
- Tests alongside source files with `_test.py` suffix
- CLI entry point in `__main__.py`
- Core functionality in `_core.py`
- Exclude test files from wheel distribution

## Git Workflow

- Clean working directory required before version bumping
- Automatic commit with version number as message
- Automatic tagging (v{version} or test-{version})
- No automatic pushing to remote

## Code Review Rules

- Exclude files and directories specified in .gitignore from code reviews
- Skip scanning: __pycache__/, *.py[oc], build/, dist/, wheels/, *.egg-info, .venv, .env*, .ruff_cache/, .mypy_cache/, .pytest_cache/, tmp/, *.tmp, *.dump
