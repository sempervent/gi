#!/usr/bin/env python3
"""Release script for creating and managing gi releases."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def get_version():
    """Get the current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    content = pyproject_path.read_text()
    for line in content.split('\n'):
        if line.strip().startswith('version = '):
            version = line.split('=')[1].strip().strip('"\'')
            return version
    
    raise ValueError("Version not found in pyproject.toml")


def create_tag(version, message=None):
    """Create a git tag for the version."""
    if message is None:
        message = f"Release v{version}"
    
    # Check if tag already exists
    result = run_command(["git", "tag", "-l", f"v{version}"], check=False)
    if result.stdout.strip():
        print(f"Tag v{version} already exists!")
        return False
    
    # Create and push tag
    run_command(["git", "tag", "-a", f"v{version}", "-m", message])
    run_command(["git", "push", "origin", f"v{version}"])
    print(f"Created and pushed tag v{version}")
    return True


def build_local():
    """Build executables locally for testing."""
    print("Building executables locally...")
    run_command([sys.executable, "scripts/build.py"])
    
    # Show results
    dist_dir = Path("dist")
    if dist_dir.exists():
        print("\nBuilt executables:")
        for platform_dir in dist_dir.iterdir():
            if platform_dir.is_dir():
                for exe in platform_dir.glob("gi*"):
                    print(f"  {exe}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Release management for gi")
    parser.add_argument("command", choices=["tag", "build", "help"], 
                       help="Command to run")
    parser.add_argument("--version", help="Version to tag (default: from pyproject.toml)")
    parser.add_argument("--message", help="Tag message")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without doing it")
    
    args = parser.parse_args()
    
    if args.command == "help":
        print("""
Release Commands:

1. Build locally (for testing):
   python scripts/release.py build

2. Create a release tag (triggers GitHub Actions):
   python scripts/release.py tag
   python scripts/release.py tag --version 1.0.0
   python scripts/release.py tag --message "Major release with new features"

3. Manual release process:
   # 1. Update version in pyproject.toml
   # 2. Commit changes
   git add pyproject.toml
   git commit -m "Bump version to 1.0.0"
   git push origin main
   
   # 3. Create and push tag (triggers release)
   python scripts/release.py tag --version 1.0.0
   
   # 4. GitHub Actions will automatically:
   #    - Build executables for all platforms
   #    - Create GitHub release with artifacts
   #    - Upload to PyPI (if configured)

Platforms supported:
- Linux x86_64
- Windows x86_64  
- macOS x86_64
- macOS ARM64 (Apple Silicon)
        """)
        return
    
    if args.command == "build":
        build_local()
        return
    
    if args.command == "tag":
        version = args.version or get_version()
        
        if args.dry_run:
            print(f"Would create tag v{version}")
            if args.message:
                print(f"With message: {args.message}")
            return
        
        # Check if we're on main branch
        result = run_command(["git", "branch", "--show-current"], check=False)
        current_branch = result.stdout.strip()
        if current_branch != "main":
            print(f"Warning: Not on main branch (currently on {current_branch})")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                return
        
        # Check if working directory is clean
        result = run_command(["git", "status", "--porcelain"], check=False)
        if result.stdout.strip():
            print("Working directory is not clean!")
            print("Uncommitted changes:")
            print(result.stdout)
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                return
        
        create_tag(version, args.message)


if __name__ == "__main__":
    main()
