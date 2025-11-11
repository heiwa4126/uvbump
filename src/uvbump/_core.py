import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import git
from packaging.version import Version, InvalidVersion

try:
    import tomllib
except ImportError:
    import tomli as tomllib
import tomli_w


@dataclass
class VersionInfo:
    path: str
    old_version: str
    new_version: str
    commit_message: str
    tag: str


class UvbumpError(Exception):
    pass


def load_pyproject_toml(path: Path) -> dict:
    """Load pyproject.toml and return parsed content."""
    if not path.exists():
        raise UvbumpError(f"pyproject.toml not found in {path.parent}")
    
    with open(path, "rb") as f:
        data = tomllib.load(f)
    
    if "project" not in data or "version" not in data["project"]:
        raise UvbumpError("project.version not found in pyproject.toml")
    
    return data


def save_pyproject_toml(path: Path, data: dict) -> None:
    """Save data to pyproject.toml."""
    with open(path, "wb") as f:
        tomli_w.dump(data, f)


def validate_version(version_str: str) -> Version:
    """Validate version string according to PEP 440."""
    try:
        return Version(version_str)
    except InvalidVersion:
        raise UvbumpError(f"Invalid version format: {version_str}")


def bump_version(current: Version, bump_type: str) -> Version:
    """Bump version according to type."""
    if bump_type == "major":
        return Version(f"{current.major + 1}.0.0")
    elif bump_type == "minor":
        return Version(f"{current.major}.{current.minor + 1}.0")
    elif bump_type == "patch":
        return Version(f"{current.major}.{current.minor}.{current.micro + 1}")
    elif bump_type == "bump":
        if current.is_prerelease:
            # Increment pre-release number
            pre = current.pre
            if pre:
                pre_type, pre_num = pre
                return Version(f"{current.base_version}{pre_type}{pre_num + 1}")
            else:
                raise UvbumpError("Cannot bump pre-release version without pre-release number")
        else:
            # Same as patch
            return Version(f"{current.major}.{current.minor}.{current.micro + 1}")
    else:
        raise UvbumpError(f"Unknown bump type: {bump_type}")


def check_git_status(repo: git.Repo) -> None:
    """Check git repository status."""
    if repo.is_dirty(untracked_files=False):
        raise UvbumpError("Repository has unstaged changes")
    
    if repo.index.diff("HEAD"):
        raise UvbumpError("Repository has staged changes")


def update_version(new_version: str, test_tag: bool = False, dry_run: bool = False) -> VersionInfo:
    """Update version in pyproject.toml and create git commit and tag."""
    # Find pyproject.toml
    pyproject_path = Path.cwd() / "pyproject.toml"
    
    # Load and validate current version
    data = load_pyproject_toml(pyproject_path)
    current_version_str = data["project"]["version"]
    current_version = validate_version(current_version_str)
    
    # Validate new version
    if isinstance(new_version, str):
        if new_version in ["major", "minor", "patch", "bump"]:
            new_version_obj = bump_version(current_version, new_version)
        else:
            new_version_obj = validate_version(new_version)
    else:
        new_version_obj = new_version
    
    # Check version progression
    if new_version_obj <= current_version:
        raise UvbumpError(f"New version {new_version_obj} must be greater than current version {current_version}")
    
    # Check git repository
    try:
        repo = git.Repo(".")
    except git.InvalidGitRepositoryError:
        raise UvbumpError("Not a git repository")
    
    check_git_status(repo)
    
    # Prepare version info
    new_version_str = str(new_version_obj)
    commit_message = new_version_str
    tag = f"test-{new_version_str}" if test_tag else f"v{new_version_str}"
    
    version_info = VersionInfo(
        path=str(pyproject_path.absolute()),
        old_version=current_version_str,
        new_version=new_version_str,
        commit_message=commit_message,
        tag=tag
    )
    
    if not dry_run:
        # Update pyproject.toml
        data["project"]["version"] = new_version_str
        save_pyproject_toml(pyproject_path, data)
        
        # Git commit and tag
        repo.index.add([str(pyproject_path)])
        repo.index.commit(commit_message)
        repo.create_tag(tag)
    
    return version_info


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="uvbump",
        description="Version bumping tool for Python projects using pyproject.toml"
    )
    parser.add_argument(
        "version",
        nargs="?",
        default="bump",
        help="Version to set or bump type (major|minor|patch|bump)"
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Use test- prefix for tag instead of v"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    try:
        version_info = update_version(args.version, args.test, args.dry_run)
        
        # Display results
        print(f"Updated: {version_info.path}")
        print(f"Version: {version_info.old_version} → {version_info.new_version}")
        print(f"Commit: {version_info.commit_message}")
        print(f"Tag: {version_info.tag}")
        
        if args.dry_run:
            print("(dry run - no changes made)")
            
    except UvbumpError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)