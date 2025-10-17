#!/usr/bin/env python3
"""Standalone entry point for gi executable."""

import sys
from pathlib import Path

# Add the gi package to the path
if getattr(sys, "frozen", False):
    # Running as PyInstaller bundle
    gi_path = Path(sys._MEIPASS) / "gi"
else:
    # Running as script
    gi_path = Path(__file__).parent / "gi"

sys.path.insert(0, str(gi_path))

# Import and run the CLI
from gi.cli import app

if __name__ == "__main__":
    app()
