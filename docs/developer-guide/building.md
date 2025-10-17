# Building

Learn how to build `gi` from source and create distributable packages.

## Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **Build Tools**: 
  - `pip` (latest version)
  - `setuptools` and `wheel`
  - `build` (for PEP 517 builds)

### Development Dependencies

Install development dependencies:

```bash
# Clone the repository
git clone https://github.com/sempervent/gi.git
cd gi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Building from Source

### Standard Build

Build the package using the standard Python build tools:

```bash
# Install build dependencies
pip install build

# Build the package
python -m build

# The built packages will be in dist/
ls dist/
# gi-0.1.0-py3-none-any.whl
# gi-0.1.0.tar.gz
```

### Development Build

For development and testing:

```bash
# Install in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Creating Executables

### Using PyInstaller

Create standalone executables for distribution:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller gi.spec

# The executable will be in dist/gi
ls dist/
# gi  (executable)
```

### Using the Build Script

Use the provided build script for convenience:

```bash
# Make the script executable
chmod +x scripts/build-local.sh

# Run the build
./scripts/build-local.sh
```

### Cross-Platform Builds

Build for multiple platforms:

```bash
# Build for current platform
python scripts/build.py

# The script will create platform-specific executables
ls dist/
# darwin-arm64/gi
# linux-x86_64/gi
# windows-x86_64/gi.exe
```

## Build Configuration

### PyInstaller Spec File

The `gi.spec` file configures PyInstaller:

```python
# gi.spec
a = Analysis(
    ['gi_standalone.py'],
    pathex=[],
    binaries=[],
    datas=[('gi', 'gi')],
    hiddenimports=[
        'gi.cli',
        'gi.combine', 
        'gi.fetch',
        'gi.names',
        'gi.util',
        'typer',
        'rich',
        'requests',
        'platformdirs',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['gi'],  # Exclude PyGObject
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

### Build Script Configuration

The `scripts/build.py` script handles the build process:

```python
# scripts/build.py
def build_executables():
    """Build executables for all platforms."""
    platforms = [
        ("linux", "x86_64"),
        ("windows", "x86_64"), 
        ("darwin", "x86_64"),
        ("darwin", "arm64"),
    ]
    
    for platform, arch in platforms:
        build_for_platform(platform, arch)
```

## Testing Builds

### Local Testing

Test the built executable locally:

```bash
# Test the executable
./dist/gi --help

# Test basic functionality
./dist/gi list | head -5

# Test template combination
./dist/gi python node -o test.gitignore
cat test.gitignore
rm test.gitignore
```

### Automated Testing

Run automated tests on built packages:

```bash
# Test the wheel package
pip install dist/gi-*.whl
gi --help

# Test the source distribution
pip install dist/gi-*.tar.gz
gi --help

# Run the test suite
pytest tests/
```

## Distribution

### PyPI Upload

Upload to PyPI (requires PyPI account):

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*

# Or upload to Test PyPI first
twine upload --repository testpypi dist/*
```

### GitHub Releases

Create GitHub releases with executables:

```bash
# Use the release script
python scripts/release.py tag --version 1.0.0

# This will:
# 1. Build executables for all platforms
# 2. Create a Git tag
# 3. Push to GitHub
# 4. Trigger GitHub Actions to create a release
```

## Build Optimization

### Size Optimization

Optimize executable size:

```python
# In gi.spec
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols
    upx=True,    # Compress with UPX
    upx_exclude=[],
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Performance Optimization

Optimize for performance:

```python
# In gi.spec
a = Analysis(
    ['gi_standalone.py'],
    pathex=[],
    binaries=[],
    datas=[('gi', 'gi')],
    hiddenimports=[
        # Only include necessary modules
        'gi.cli',
        'gi.combine',
        'gi.fetch', 
        'gi.names',
        'gi.util',
        'typer',
        'rich',
        'requests',
        'platformdirs',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'gi',           # PyGObject
        'tkinter',      # GUI toolkit
        'matplotlib',   # Plotting library
        'numpy',        # Scientific computing
        'pandas',       # Data analysis
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

## Troubleshooting

### Common Build Issues

#### Import Errors

If you get import errors in the built executable:

```python
# Add missing modules to hiddenimports in gi.spec
hiddenimports=[
    'gi.cli',
    'gi.combine',
    'gi.fetch',
    'gi.names', 
    'gi.util',
    'typer',
    'rich',
    'requests',
    'platformdirs',
    'pkg_resources',  # Add if needed
    'importlib_metadata',  # Add if needed
]
```

#### Missing Dependencies

If dependencies are missing:

```bash
# Check what's included
pyinstaller --debug=all gi.spec

# Add missing packages to datas
datas=[
    ('gi', 'gi'),
    ('typer', 'typer'),  # Add if needed
    ('rich', 'rich'),    # Add if needed
]
```

#### Large Executable Size

To reduce executable size:

```bash
# Use UPX compression
pip install upx-ucl

# Enable UPX in spec file
upx=True

# Exclude unnecessary modules
excludes=['tkinter', 'matplotlib', 'numpy', 'pandas']
```

### Debug Builds

Create debug builds for troubleshooting:

```python
# In gi.spec
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gi-debug',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,  # Don't strip symbols
    upx=False,    # Don't compress
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

## Continuous Integration

### GitHub Actions

The project includes GitHub Actions workflows for automated building:

```yaml
# .github/workflows/build.yml
name: Build Cross-Platform Executables

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            platform: linux
            arch: x86_64
          - os: windows-latest
            platform: windows
            arch: x86_64
          - os: macos-latest
            platform: macos
            arch: x86_64
          - os: macos-latest
            platform: macos
            arch: arm64
```

### Local CI Testing

Test the CI build process locally:

```bash
# Install act (GitHub Actions runner)
# https://github.com/nektos/act

# Run the build workflow
act -j build

# Run specific job
act -j build --matrix os:ubuntu-latest,platform:linux,arch:x86_64
```

## Advanced Build Options

### Custom Entry Points

Create custom entry points:

```python
# In pyproject.toml
[project.scripts]
gi = "gi.__main__:main"
gi-debug = "gi.__main__:main_debug"

# In gi/__main__.py
def main_debug():
    """Debug entry point with verbose logging."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
    main()
```

### Plugin System

Build with plugin support:

```python
# In gi.spec
datas=[
    ('gi', 'gi'),
    ('gi/plugins', 'gi/plugins'),  # Include plugins
]

hiddenimports=[
    'gi.cli',
    'gi.combine',
    'gi.fetch',
    'gi.names',
    'gi.util',
    'gi.plugins',  # Include plugin system
]
```

This comprehensive guide covers all aspects of building `gi` from source, creating executables, and distributing the package.
