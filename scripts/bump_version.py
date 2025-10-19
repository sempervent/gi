#!/usr/bin/env python3
"""Version bumping script for gi."""

import argparse
import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get the current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    
    return match.group(1)


def bump_version(version: str, bump_type: str) -> str:
    """Bump version based on type (major, minor, patch)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    
    major, minor, patch = map(int, parts)
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_in_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace version line
    new_content = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_path.write_text(new_content)
    print(f"Updated pyproject.toml version to {new_version}")


def update_version_in_init(new_version: str) -> None:
    """Update version in __init__.py if it exists."""
    init_path = Path("gi/__init__.py")
    if not init_path.exists():
        return
    
    content = init_path.read_text()
    
    # Look for __version__ = "..." pattern
    if '__version__' in content:
        new_content = re.sub(
            r'__version__\s*=\s*["\'][^"\']+["\']',
            f'__version__ = "{new_version}"',
            content
        )
        init_path.write_text(new_content)
        print(f"Updated gi/__init__.py version to {new_version}")


def update_version_in_readme(new_version: str) -> None:
    """Update version references in README.md."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        return
    
    content = readme_path.read_text()
    
    # Update version badges and references
    new_content = re.sub(
        r'v\d+\.\d+\.\d+',
        f'v{new_version}',
        content
    )
    
    if new_content != content:
        readme_path.write_text(new_content)
        print(f"Updated README.md version references to {new_version}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Bump version for gi")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    
    args = parser.parse_args()
    
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        
        new_version = bump_version(current_version, args.bump_type)
        print(f"New version: {new_version}")
        
        if args.dry_run:
            print("Dry run - no changes made")
            return
        
        # Update files
        update_version_in_pyproject(new_version)
        update_version_in_init(new_version)
        update_version_in_readme(new_version)
        
        print(f"Successfully bumped version from {current_version} to {new_version}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
