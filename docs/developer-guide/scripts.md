# Scripts Documentation

This document provides comprehensive documentation for all scripts in the `gi` project. These scripts automate various development, build, and release tasks.

## Overview

The `scripts/` directory contains the following automation scripts:

- [`bump_version.py`](#bump_versionpy) - Automated version management
- [`build.py`](#buildpy) - Cross-platform executable building
- [`release.py`](#releasepy) - Release management and tagging
- [`install.sh`](#installsh) - Installation automation
- [`build-local.sh`](#build-localsh) - Local development builds

## Scripts Reference

### `bump_version.py`

**Purpose**: Automated version bumping with multi-file updates

**Usage**:
```bash
python scripts/bump_version.py [major|minor|patch] [--dry-run]
```

**Features**:
- Supports semantic versioning (major, minor, patch)
- Updates multiple files automatically:
  - `pyproject.toml` version field
  - `gi/__init__.py` `__version__` variable
  - `README.md` version references
- Dry-run mode to preview changes
- Error handling and validation

**Examples**:
```bash
# Preview a minor version bump (0.2.0 → 0.3.0)
python scripts/bump_version.py --dry-run minor

# Bump patch version (0.2.0 → 0.2.1)
python scripts/bump_version.py patch

# Bump major version (0.2.0 → 1.0.0)
python scripts/bump_version.py major
```

**Files Updated**:
- `pyproject.toml`: `version = "X.Y.Z"`
- `gi/__init__.py`: `__version__ = "X.Y.Z"`
- `README.md`: Version references in badges and text

### `build.py`

**Purpose**: Cross-platform executable building using PyInstaller or cx_Freeze

**Usage**:
```bash
python scripts/build.py
```

**Features**:
- **Primary**: PyInstaller with `gi.spec` configuration
- **Fallback**: cx_Freeze if PyInstaller fails
- **Platform Detection**: Automatically detects OS and architecture
- **Clean Builds**: Removes previous build artifacts
- **Organized Output**: Creates platform-specific directories

**Build Process**:
1. Installs build dependencies (`.[build]`)
2. Cleans previous builds (`dist/`, `build/`)
3. Attempts PyInstaller build with `gi.spec`
4. Falls back to cx_Freeze if needed
5. Organizes output by platform (`dist/{platform}-{arch}/`)

**Output Structure**:
```
dist/
├── darwin-arm64/
│   └── gi
├── linux-x86_64/
│   └── gi
└── windows-x86_64/
    └── gi.exe
```

**Dependencies**:
- PyInstaller (primary)
- cx_Freeze (fallback)
- Platform-specific build tools

### `release.py`

**Purpose**: Release management and Git tagging automation

**Usage**:
```bash
python scripts/release.py [command] [options]
```

**Commands**:
- `tag` - Create and push Git tags
- `build` - Build executables locally
- `help` - Show help information

**Options**:
- `--version` - Specify version (default: from pyproject.toml)
- `--message` - Custom tag message
- `--dry-run` - Preview actions without executing

**Examples**:
```bash
# Create tag for current version
python scripts/release.py tag

# Create tag with custom version
python scripts/release.py tag --version 0.3.0

# Create tag with custom message
python scripts/release.py tag --message "Bug fixes and improvements"

# Build locally for testing
python scripts/release.py build
```

**Safety Checks**:
- Verifies working directory is clean
- Confirms on main branch
- Checks for existing tags
- Validates version format

### `install.sh`

**Purpose**: Automated installation with multiple methods

**Usage**:
```bash
bash scripts/install.sh
```

**Installation Methods** (in order of preference):
1. **pipx** - Isolated installation (recommended)
2. **pip** - User installation with `--user` flag
3. **Virtual Environment** - Local development setup

**Features**:
- **Python Version Check**: Validates Python 3.9+ requirement
- **Method Detection**: Automatically chooses best installation method
- **Colored Output**: Status messages with color coding
- **Error Handling**: Graceful fallbacks and clear error messages
- **Path Configuration**: Automatic PATH setup guidance

**Installation Process**:
1. Validates Python version (3.9+)
2. Checks for `pyproject.toml` in current directory
3. Attempts pipx installation (if available)
4. Falls back to pip user installation
5. Creates virtual environment as last resort

**Output Examples**:
```bash
[INFO] Installing gi - .gitignore Combiner
[INFO] Python version: 3.11 ✓
[INFO] Installing gi with pipx...
[SUCCESS] gi installed successfully with pipx!
[INFO] You can now use 'gi' from anywhere in your terminal.
```

### `build-local.sh`

**Purpose**: Simplified local development builds

**Usage**:
```bash
bash scripts/build-local.sh
```

**Features**:
- **Quick Setup**: One-command local builds
- **Dependency Installation**: Automatically installs build dependencies
- **Result Display**: Shows created executables and usage instructions

**Process**:
1. Installs build dependencies (`pip install -e ".[build]"`)
2. Runs the build script (`python scripts/build.py`)
3. Displays results and usage instructions

**Output**:
```bash
Building gi executable for local platform...
Installing build dependencies...
Building executable...
Build completed! Executables created in:
dist/darwin-arm64/gi

To test the executable:
  ./dist/darwin-arm64/gi --help
```

## Workflow Integration

### Development Workflow

```bash
# 1. Install for development
bash scripts/install.sh

# 2. Make changes and test
gi --help

# 3. Run tests
python -m pytest

# 4. Build locally to test
bash scripts/build-local.sh

# 5. Bump version when ready
python scripts/bump_version.py minor

# 6. Create release
python scripts/release.py tag
```

### Release Workflow

```bash
# 1. Update version
python scripts/bump_version.py minor

# 2. Commit changes
git add -A && git commit -m "feat: new features"

# 3. Create and push tag
python scripts/release.py tag

# 4. GitHub Actions will automatically:
#    - Build executables for all platforms
#    - Create GitHub release with artifacts
#    - Deploy documentation
```

### CI/CD Integration

The scripts are designed to work with GitHub Actions:

- **`build.yml`**: Uses `scripts/build.py` for cross-platform builds
- **`scripts/bump_version.py`**: Can be used in automated version bumping
- **`scripts/release.py`**: Integrates with Git tagging workflows

## Error Handling

All scripts include comprehensive error handling:

- **Validation**: Input validation and file existence checks
- **Graceful Failures**: Clear error messages and exit codes
- **Fallbacks**: Alternative methods when primary approaches fail
- **Cleanup**: Automatic cleanup of temporary files

## Dependencies

### Required Dependencies
- Python 3.9+
- Git (for release script)
- Build tools (PyInstaller, cx_Freeze)

### Optional Dependencies
- pipx (for isolated installation)
- Platform-specific build tools

## Troubleshooting

### Common Issues

**Version Bumping Fails**:
```bash
# Check file permissions
ls -la pyproject.toml gi/__init__.py

# Verify version format
python scripts/bump_version.py --dry-run patch
```

**Build Failures**:
```bash
# Install build dependencies
pip install -e ".[build]"

# Try alternative build method
python scripts/build.py
```

**Installation Issues**:
```bash
# Check Python version
python3 --version

# Try manual installation
pip install -e .
```

### Debug Mode

Most scripts support verbose output:
```bash
# Enable debug output
python scripts/build.py  # Check build logs
python scripts/release.py tag --dry-run  # Preview actions
```

## Contributing

When adding new scripts:

1. **Follow Naming**: Use descriptive names with appropriate extensions
2. **Add Documentation**: Update this file with script details
3. **Include Help**: Add `--help` flags and usage information
4. **Error Handling**: Implement proper error handling and validation
5. **Testing**: Test on multiple platforms when possible

## See Also

- [Building Guide](building.md) - Detailed build instructions
- [Release Process](release-process.md) - Release workflow documentation
- [Contributing Guide](contributing.md) - Development guidelines
