import pytest
from packaging.version import Version
from ._core import validate_version, bump_version, UvbumpError


def test_validate_version():
    """Test version validation."""
    # Valid versions
    assert validate_version("1.0.0") == Version("1.0.0")
    assert validate_version("1.2.3a1") == Version("1.2.3a1")
    assert validate_version("2.0.0rc1") == Version("2.0.0rc1")
    
    # Invalid versions
    with pytest.raises(UvbumpError):
        validate_version("invalid")


def test_bump_version():
    """Test version bumping."""
    v = Version("1.2.3")
    
    # Test major bump
    assert bump_version(v, "major") == Version("2.0.0")
    
    # Test minor bump
    assert bump_version(v, "minor") == Version("1.3.0")
    
    # Test patch bump
    assert bump_version(v, "patch") == Version("1.2.4")
    
    # Test bump (same as patch for non-prerelease)
    assert bump_version(v, "bump") == Version("1.2.4")


def test_bump_prerelease():
    """Test pre-release version bumping."""
    v = Version("1.2.3a4")
    
    # Test bump for pre-release
    assert bump_version(v, "bump") == Version("1.2.3a5")
    
    # Test other bumps for pre-release
    assert bump_version(v, "major") == Version("2.0.0")
    assert bump_version(v, "minor") == Version("1.3.0")
    assert bump_version(v, "patch") == Version("1.2.4")


def test_bump_invalid_type():
    """Test invalid bump type."""
    v = Version("1.0.0")
    with pytest.raises(UvbumpError):
        bump_version(v, "invalid")