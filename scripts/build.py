#!/usr/bin/env python3
"""Build script for creating cross-platform executables."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def build_with_pyinstaller():
    """Build executable using PyInstaller."""
    print("Building with PyInstaller...")
    
    # Clean previous builds
    if Path("dist").exists():
        shutil.rmtree("dist")
    if Path("build").exists():
        shutil.rmtree("build")
    
    # PyInstaller command using spec file
    cmd = [
        "pyinstaller",
        "--clean",
        "gi.spec"
    ]
    
    run_command(cmd)
    
    # Move to platform-specific directory
    platform_name = f"{platform.system().lower()}-{platform.machine().lower()}"
    platform_dir = Path("dist") / platform_name
    platform_dir.mkdir(parents=True, exist_ok=True)
    
    if platform.system() == "Windows":
        exe_name = "gi.exe"
    else:
        exe_name = "gi"
    
    if Path("dist", exe_name).exists():
        shutil.move(f"dist/{exe_name}", platform_dir / exe_name)
        print(f"Created executable: {platform_dir / exe_name}")
    else:
        print(f"Error: Executable not found at dist/{exe_name}")


def build_with_cx_freeze():
    """Build executable using cx_Freeze."""
    print("Building with cx_Freeze...")
    
    # Create setup script for cx_Freeze
    setup_content = '''
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
'''
    
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
            
            if platform.system() == "Windows":
                exe_name = "gi.exe"
            else:
                exe_name = "gi"
            
            exe_path = exe_dir / exe_name
            if exe_path.exists():
                shutil.move(str(exe_path), platform_dir / exe_name)
                print(f"Created executable: {platform_dir / exe_name}")
            else:
                print(f"Error: Executable not found at {exe_path}")
        else:
            print("Error: Build directory not found")
    
    finally:
        # Clean up
        if setup_path.exists():
            setup_path.unlink()
        if build_dir.exists():
            shutil.rmtree(build_dir)


def main():
    """Main build function."""
    print(f"Building gi for {platform.system()} {platform.machine()}")
    
    # Install build dependencies
    print("Installing build dependencies...")
    run_command([sys.executable, "-m", "pip", "install", ".[build]"])
    
    # Try PyInstaller first, fall back to cx_Freeze
    try:
        build_with_pyinstaller()
    except Exception as e:
        print(f"PyInstaller failed: {e}")
        print("Trying cx_Freeze...")
        try:
            build_with_cx_freeze()
        except Exception as e2:
            print(f"cx_Freeze also failed: {e2}")
            print("Both build methods failed!")
            sys.exit(1)
    
    print("Build completed successfully!")


if __name__ == "__main__":
    main()
