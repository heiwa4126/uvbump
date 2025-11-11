import os
import tempfile
from pathlib import Path

import git
import pytest

from ._core import UvbumpError, update_version

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]


@pytest.fixture
def temp_project():
    """Create a temporary project with pyproject.toml and git repo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()

        # Create pyproject.toml
        pyproject_content = """[project]
name = "test-project"
version = "1.0.0"
description = "Test project"
"""
        pyproject_path = project_dir / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        # Initialize git repo
        repo = git.Repo.init(project_dir)
        repo.index.add([str(pyproject_path)])
        repo.index.commit("Initial commit")

        # Change to project directory
        original_cwd = os.getcwd()
        os.chdir(project_dir)

        try:
            yield project_dir, repo
        finally:
            os.chdir(original_cwd)


def test_patch_version_bump(temp_project):
    """Test patch version bump."""
    project_dir, repo = temp_project

    result = update_version("patch")

    assert result.old_version == "1.0.0"
    assert result.new_version == "1.0.1"
    assert result.commit_message == "1.0.1"
    assert result.tag == "v1.0.1"

    # Verify pyproject.toml was updated
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    assert data["project"]["version"] == "1.0.1"

    # Verify git commit and tag
    assert repo.head.commit.message.strip() == "1.0.1"
    assert "v1.0.1" in [tag.name for tag in repo.tags]


def test_minor_version_bump(temp_project):
    """Test minor version bump."""
    project_dir, repo = temp_project

    result = update_version("minor")

    assert result.old_version == "1.0.0"
    assert result.new_version == "1.1.0"
    assert result.tag == "v1.1.0"


def test_major_version_bump(temp_project):
    """Test major version bump."""
    project_dir, repo = temp_project

    result = update_version("major")

    assert result.old_version == "1.0.0"
    assert result.new_version == "2.0.0"
    assert result.tag == "v2.0.0"


def test_explicit_version_set(temp_project):
    """Test setting explicit version."""
    project_dir, repo = temp_project

    result = update_version("1.5.0")

    assert result.old_version == "1.0.0"
    assert result.new_version == "1.5.0"
    assert result.tag == "v1.5.0"


def test_test_tag_option(temp_project):
    """Test -t option for test tag."""
    project_dir, repo = temp_project

    result = update_version("patch", test_tag=True)

    assert result.tag == "test-1.0.1"
    assert "test-1.0.1" in [tag.name for tag in repo.tags]


def test_dry_run_mode(temp_project):
    """Test dry-run mode doesn't make changes."""
    project_dir, repo = temp_project

    result = update_version("patch", dry_run=True)

    assert result.old_version == "1.0.0"
    assert result.new_version == "1.0.1"

    # Verify no changes were made
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    assert data["project"]["version"] == "1.0.0"

    # Verify no new commit or tag
    assert repo.head.commit.message.strip() == "Initial commit"
    assert len(list(repo.tags)) == 0


def test_prerelease_bump(temp_project):
    """Test bump on pre-release version."""
    project_dir, repo = temp_project

    # First set to pre-release (higher than 1.0.0)
    update_version("1.1.0a1")

    # Then bump
    result = update_version("bump")

    assert result.old_version == "1.1.0a1"
    assert result.new_version == "1.1.0a2"


def test_normal_version_bump(temp_project):
    """Test bump on normal version (should be same as patch)."""
    project_dir, repo = temp_project

    result = update_version("bump")

    assert result.old_version == "1.0.0"
    assert result.new_version == "1.0.1"


def test_version_downgrade_error(temp_project):
    """Test error on version downgrade."""
    project_dir, repo = temp_project

    with pytest.raises(UvbumpError, match="must be greater than"):
        update_version("0.9.0")


def test_same_version_error(temp_project):
    """Test error on same version."""
    project_dir, repo = temp_project

    with pytest.raises(UvbumpError, match="must be greater than"):
        update_version("1.0.0")


def test_unstaged_changes_error(temp_project):
    """Test error with unstaged changes."""
    project_dir, repo = temp_project

    # Modify existing file to create unstaged change
    with open("pyproject.toml", "a") as f:
        f.write("\n# test comment\n")

    with pytest.raises(UvbumpError, match="unstaged changes"):
        update_version("patch")


def test_staged_changes_error(temp_project):
    """Test error with staged changes."""
    project_dir, repo = temp_project

    # Create and stage change
    Path("test_file.txt").write_text("test")
    repo.index.add(["test_file.txt"])

    with pytest.raises(UvbumpError, match="staged changes"):
        update_version("patch")


def test_no_pyproject_toml_error():
    """Test error when pyproject.toml doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "empty_project"
        project_dir.mkdir()

        # Initialize git repo but no pyproject.toml
        # repo = git.Repo.init(project_dir)

        original_cwd = os.getcwd()
        os.chdir(project_dir)

        try:
            with pytest.raises(UvbumpError, match="pyproject.toml not found"):
                update_version("patch")
        finally:
            os.chdir(original_cwd)


def test_no_project_version_error():
    """Test error when project.version doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "no_version_project"
        project_dir.mkdir()

        # Create pyproject.toml without version
        pyproject_content = """[project]
name = "test-project"
description = "Test project"
"""
        pyproject_path = project_dir / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        # Initialize git repo
        repo = git.Repo.init(project_dir)
        repo.index.add([str(pyproject_path)])
        repo.index.commit("Initial commit")

        original_cwd = os.getcwd()
        os.chdir(project_dir)

        try:
            with pytest.raises(UvbumpError, match="project.version not found"):
                update_version("patch")
        finally:
            os.chdir(original_cwd)


def test_not_git_repo_error():
    """Test error when not in git repository."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "not_git_project"
        project_dir.mkdir()

        # Create pyproject.toml but no git repo
        pyproject_content = """[project]
name = "test-project"
version = "1.0.0"
description = "Test project"
"""
        pyproject_path = project_dir / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        original_cwd = os.getcwd()
        os.chdir(project_dir)

        try:
            with pytest.raises(UvbumpError, match="Not a git repository"):
                update_version("patch")
        finally:
            os.chdir(original_cwd)


def test_invalid_version_error(temp_project):
    """Test error with invalid version format."""
    project_dir, repo = temp_project

    with pytest.raises(UvbumpError, match="Invalid version format"):
        update_version("invalid-version")
