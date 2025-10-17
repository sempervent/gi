#!/usr/bin/env python3
"""Build script for creating cross-platform executables."""

import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        sys.exit(1)
    return result


def build_with_pyinstaller():
    """Build executable using PyInstaller."""

    # Clean previous builds
    if Path("dist").exists():
        shutil.rmtree("dist")
    if Path("build").exists():
        shutil.rmtree("build")

    # PyInstaller command using spec file
    cmd = ["pyinstaller", "--clean", "gi.spec"]

    run_command(cmd)

    # Move to platform-specific directory
    platform_name = f"{platform.system().lower()}-{platform.machine().lower()}"
    platform_dir = Path("dist") / platform_name
    platform_dir.mkdir(parents=True, exist_ok=True)

    exe_name = "gi.exe" if platform.system() == "Windows" else "gi"

    if Path("dist", exe_name).exists():
        shutil.move(f"dist/{exe_name}", platform_dir / exe_name)


def build_with_cx_freeze():
    """Build executable using cx_Freeze."""

    # Create setup script for cx_Freeze
    setup_content = """
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    "packages": ["gi", "typer", "rich", "requests", "platformdirs"],
    "excludes": ["tkinter", "unittest", "pydoc", "doctest"],
    "include_files": []
}

base = None
if sys.platform == "win32":
    base = "Console"

executables = [
    Executable("gi/__main__.py", base=base, target_name="gi")
]

setup(
    name="gi",
    version="0.0.1",
    description="A CLI tool to combine .gitignore templates",
    options={"build_exe": build_options},
    executables=executables
)
"""

    setup_path = Path("setup_cx_freeze.py")
    setup_path.write_text(setup_content)

    try:
        # Build with cx_Freeze
        run_command([sys.executable, "setup_cx_freeze.py", "build"])

        # Find the built executable
        build_dir = Path("build")
        exe_dir = None
        for item in build_dir.iterdir():
            if item.is_dir():
                exe_dir = item
                break

        if exe_dir:
            platform_name = f"{platform.system().lower()}-{platform.machine().lower()}"
            platform_dir = Path("dist") / platform_name
            platform_dir.mkdir(parents=True, exist_ok=True)

            exe_name = "gi.exe" if platform.system() == "Windows" else "gi"

            exe_path = exe_dir / exe_name
            if exe_path.exists():
                shutil.move(str(exe_path), platform_dir / exe_name)

    finally:
        # Clean up
        if setup_path.exists():
            setup_path.unlink()
        if build_dir.exists():
            shutil.rmtree(build_dir)


def main():
    """Main build function."""
    # Install build dependencies
    run_command([sys.executable, "-m", "pip", "install", ".[build]"])

    # Try PyInstaller first, fall back to cx_Freeze
    try:
        build_with_pyinstaller()
    except Exception:
        try:
            build_with_cx_freeze()
        except Exception:
            sys.exit(1)


if __name__ == "__main__":
    main()
