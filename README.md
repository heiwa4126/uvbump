# uvbump

[![PyPI - Version](https://img.shields.io/pypi/v/uvbump.svg)](https://pypi.org/project/uvbump)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvbump.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/uvbump)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

English | [日本語](https://github.com/heiwa4126/uvbump/blob/main/README-ja.md)

A CLI tool similar to `npm version` written in Python. Reference: [npm-version](https://docs.npmjs.com/cli/v11/commands/npm-version)

Performs `npm version`-like operations on pyproject.toml files for Astral uv (and poetry, etc. PEP 621 compliant tools). Primarily used for triggering GitHub Actions.

## Installation and Usage

```sh
# Using uv
uv add uvbump --dev
uv run uvbump <options>

# Or
uvx uvbump <options>

# Or
uv tool install uvbump
uvbump

# Using pip
pip install uvbump
uvbump

# Using poetry
poetry add --group dev uvbump
poetry run uvbump
```

## Usage

```console
uvbump [<newversion> | major | minor | patch | bump] [-n|--dry-run] [-h|--help]
```

### Version Update Types

- `major`: Increment major version by 1 (1.2.3 → 2.0.0)
- `minor`: Increment minor version by 1 (1.2.3 → 1.3.0)
- `patch`: Increment patch version by 1 (1.2.3 → 1.2.4)
- `bump`: Default. Same as patch for normal versions, increment number by 1 for pre-release versions (1.2.3a1 → 1.2.3a2)
- `<newversion>`: Explicit version specification (converted to PEP 440 compliant format)

### Options

- `-n, --dry-run`: Show what would be done without making changes. No prior commit required
- `-h, --help`: Show help message

## Examples

### Basic Usage

```sh
# Increment patch version (1.0.0 → 1.0.1)
uvbump patch

# Increment minor version (1.0.1 → 1.1.0)
uvbump minor

# Increment major version (1.1.0 → 2.0.0)
uvbump major

# Default behavior (same as bump)
uvbump
```

### Explicit Version Specification

```sh
# Set to specific version
uvbump 1.5.0

# Set to pre-release version
uvbump 2.0.0a1

# Release candidate
uvbump 1.0.0rc1
```

### Pre-release Version Management

```sh
# Increment pre-release number (1.0.0a1 → 1.0.0a2)
uvbump bump

# From pre-release to stable (explicit specification)
uvbump 1.0.0
```

### Dry-run Mode

```sh
# Check changes (no actual changes made)
uvbump patch -n
uvbump minor --dry-run
```

### Output Examples

```console
$ uvbump patch
Updated: /path/to/project/pyproject.toml
Version: 1.0.0 → 1.0.1
Commit: 1.0.1
Tag: v1.0.1

$ uvbump 2.0.0a1
Updated: /path/to/project/pyproject.toml
Version: 1.0.1 → 2.0.0a1
Commit: 2.0.0a1
Tag: test-2.0.0a1
```

## Specification

### Basic Behavior

- Default is equivalent to `uvbump bump`
- PEP 440 compliant version management
- Same version and downgrades are not allowed
  - Downgrade example: `1.0.0` > `1.0.0a1`
- Switching between pre-release and normal versions requires explicit version specification
  - Example: `1.0.0` → `1.1.0a1` requires `uvbump 1.1.0a1`
  - Example: `1.0.0a1` → `1.0.0` requires `uvbump 1.0.0`

### Git Integration

- **Important**: All changes must be committed beforehand
- After updating pyproject.toml in current directory, automatically commits and creates tags
  - Commit message: New version number
  - Tag: `v{version}` for normal versions, `test-{version}` for pre-release versions
- Does not perform `git push`. You must manually run `git push` and `git push --tags`

### Error Conditions

- pyproject.toml does not exist in current directory
- project.version does not exist or is not PEP 440 compliant
- Not a git repository
- Uncommitted changes exist (warning only in dry-run mode)

### Limitations

- Configuration files not supported
- Monorepo support not implemented

## Similar Tools

- [npm-version](https://docs.npmjs.com/cli/v11/commands/npm-version)
- [pybump](https://pypi.org/project/pybump/)
- [bump2version](https://pypi.org/project/bump2version/)
- [bump-my-version](https://pypi.org/project/bump-my-version/)
- [bumpver](https://pypi.org/project/bumpver/)

## Development

### Setup

```bash
uv sync
```

### Task Execution

```bash
# Run tests
poe test

# Lint
poe check

# Type check
poe mypy

# Run all checks & build & smoke test
poe build
```

### Development Requirements

- uv
- Python == 3.12, 3.10 (for test)

## License

MIT
