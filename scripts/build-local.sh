#!/bin/bash
# Local build script for gi executables

set -e

echo "Building gi executable for local platform..."

# Install build dependencies
echo "Installing build dependencies..."
pip install -e ".[build]"

# Build executable
echo "Building executable..."
python scripts/build.py

# Show results
echo "Build completed! Executables created in:"
find dist -name "gi*" -type f 2>/dev/null || echo "No executables found in dist/"

echo ""
echo "To test the executable:"
echo "  ./dist/*/gi --help"
