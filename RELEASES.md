# Release Process

This document describes how to create and distribute releases of `gi`.

## Overview

The release process is automated using GitHub Actions. When you push a tag starting with `v`, the CI system will:

1. Build executables for all supported platforms
2. Create a GitHub release with downloadable artifacts
3. Generate checksums for verification

## Supported Platforms

- **Linux x86_64**: `gi-{version}-linux-x86_64.tar.gz`
- **Windows x86_64**: `gi-{version}-windows-x86_64.zip`
- **macOS x86_64**: `gi-{version}-macos-x86_64.tar.gz`
- **macOS ARM64**: `gi-{version}-macos-arm64.tar.gz` (Apple Silicon)

## Release Process

### 1. Update Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

### 2. Commit Changes

```bash
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git push origin main
```

### 3. Create Release Tag

Use the release script:

```bash
# Create tag with version from pyproject.toml
python scripts/release.py tag

# Or specify version manually
python scripts/release.py tag --version 1.0.0

# With custom message
python scripts/release.py tag --version 1.0.0 --message "Major release with new features"
```

### 4. Automated Release

GitHub Actions will automatically:

- Build executables for all platforms
- Create a GitHub release
- Upload artifacts with checksums
- Generate release notes

## Manual Release Process

If you need to create a release manually:

### 1. Build Locally

```bash
# Build for current platform
python scripts/release.py build

# Or use the build script directly
python scripts/build.py
```

### 2. Test Executables

```bash
# Test the built executable
./dist/*/gi --help
./dist/*/gi list | head -5
```

### 3. Create GitHub Release

1. Go to [GitHub Releases](https://github.com/sempervent/gi/releases)
2. Click "Create a new release"
3. Choose tag version (e.g., `v1.0.0`)
4. Upload the built artifacts
5. Add release notes
6. Publish release

## Release Script Usage

The `scripts/release.py` script provides several commands:

```bash
# Show help
python scripts/release.py help

# Build locally for testing
python scripts/release.py build

# Create a release tag
python scripts/release.py tag

# Dry run (show what would be done)
python scripts/release.py tag --dry-run

# Specify version and message
python scripts/release.py tag --version 1.0.0 --message "Bug fixes"
```

## Artifact Details

### File Naming Convention

- **Linux**: `gi-{version}-linux-x86_64.tar.gz`
- **Windows**: `gi-{version}-windows-x86_64.zip`
- **macOS Intel**: `gi-{version}-macos-x86_64.tar.gz`
- **macOS Apple Silicon**: `gi-{version}-macos-arm64.tar.gz`

### Checksums

Each release includes a `gi-{version}-checksums.txt` file with SHA256 checksums for all artifacts:

```
a1b2c3d4e5f6...  gi-1.0.0-linux-x86_64.tar.gz
f6e5d4c3b2a1...  gi-1.0.0-windows-x86_64.zip
...
```

### Installation from Release

Users can download and install from releases:

```bash
# Download and extract
wget https://github.com/sempervent/gi/releases/download/v1.0.0/gi-1.0.0-linux-x86_64.tar.gz
tar -xzf gi-1.0.0-linux-x86_64.tar.gz

# Make executable and move to PATH
chmod +x gi
sudo mv gi /usr/local/bin/

# Verify installation
gi --help
```

## Troubleshooting

### Build Failures

If builds fail in GitHub Actions:

1. Check the [Actions tab](https://github.com/sempervent/gi/actions)
2. Look for specific platform failures
3. Test locally with `python scripts/release.py build`
4. Check PyInstaller compatibility with dependencies

### Tag Already Exists

If you get "Tag already exists" error:

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Create new tag
python scripts/release.py tag --version 1.0.0
```

### Working Directory Not Clean

The release script checks for uncommitted changes. Either:

1. Commit your changes first:
   ```bash
   git add .
   git commit -m "Your changes"
   ```

2. Or force the release:
   ```bash
   python scripts/release.py tag --version 1.0.0
   # Answer 'y' when prompted
   ```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fixes
- `1.1.0` - New features
- `2.0.0` - Breaking changes

## Pre-release Versions

For pre-releases, use version suffixes:

- `1.0.0-alpha.1` - Alpha release
- `1.0.0-beta.1` - Beta release
- `1.0.0-rc.1` - Release candidate

These will be marked as pre-releases on GitHub.
