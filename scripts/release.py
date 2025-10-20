#!/usr/bin/env python3
"""Release script for creating and managing gi releases."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, *, check=True):
    """Run a command and return the result."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        sys.exit(1)
    return result


def get_version():
    """Get the current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        error_msg = "pyproject.toml not found"
        raise FileNotFoundError(error_msg)

    content = pyproject_path.read_text()
    for line in content.split("\n"):
        if line.strip().startswith("version = "):
            return line.split("=")[1].strip().strip("\"'")

    error_msg = "Version not found in pyproject.toml"
    raise ValueError(error_msg)


def create_tag(version, message=None):
    """Create a git tag for the version."""
    if message is None:
        message = f"Release v{version}"

    # Check if tag already exists
    result = run_command(["git", "tag", "-l", f"v{version}"], check=False)
    if result.stdout.strip():
        return False

    # Create and push tag
    run_command(["git", "tag", "-a", f"v{version}", "-m", message])
    run_command(["git", "push", "origin", f"v{version}"])
    return True


def build_local():
    """Build executables locally for testing."""
    run_command([sys.executable, "scripts/build.py"])


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Release management for gi")
    parser.add_argument(
        "command",
        choices=["tag", "build", "help"],
        help="Command to run",
    )
    parser.add_argument(
        "--version",
        help="Version to tag (default: from pyproject.toml)",
    )
    parser.add_argument("--message", help="Tag message")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without doing it",
    )

    args = parser.parse_args()

    if args.command == "help":
        return

    if args.command == "build":
        build_local()
        return

    if args.command == "tag":
        version = args.version or get_version()

        if args.dry_run:
            return

        # Check if we're on main branch
        result = run_command(["git", "branch", "--show-current"], check=False)
        current_branch = result.stdout.strip()
        if current_branch != "main":
            return

        # Check if working directory is clean
        result = run_command(["git", "status", "--porcelain"], check=False)
        if result.stdout.strip():
            return

        create_tag(version, args.message)


if __name__ == "__main__":
    main()
