# Release Process

Learn how to create and manage releases for `gi`.

## Release Workflow

### Automated Releases

Releases are automated through GitHub Actions:

1. **Create a Git tag** with the version number
2. **Push the tag** to trigger the build workflow
3. **GitHub Actions** builds executables for all platforms
4. **GitHub Release** is created with all artifacts

### Manual Release Process

For manual releases:

```bash
# 1. Update version in pyproject.toml
# 2. Create and push tag
git tag v1.0.0
git push origin v1.0.0

# 3. GitHub Actions will handle the rest
```

## Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Bumping

Update version in `pyproject.toml`:

```toml
[project]
name = "gi"
version = "1.0.0"  # Update this
```

### Release Scripts

Use the provided release scripts:

```bash
# Create a new release
python scripts/release.py tag --version 1.0.0

# Or with custom message
python scripts/release.py tag --version 1.0.0 --message "Major release with new features"
```

## Pre-Release Checklist

### Code Quality

Ensure code quality before release:

```bash
# Run all tests
pytest

# Check code formatting
ruff format --check gi/ tests/

# Run linting
ruff check gi/ tests/

# Check type hints (if using mypy)
mypy gi/
```

### Documentation

Update documentation:

```bash
# Update CHANGELOG.md
# Update README.md if needed
# Update version in docs

# Build documentation
mkdocs build
```

### Testing

Test the release:

```bash
# Test installation
pip install -e .

# Test CLI
gi --help
gi list | head -5

# Test basic functionality
gi python node -o test.gitignore
cat test.gitignore
rm test.gitignore
```

## Release Automation

### GitHub Actions Workflow

The release workflow (`.github/workflows/build.yml`) handles:

1. **Building executables** for all platforms
2. **Creating archives** (tar.gz, zip)
3. **Generating checksums**
4. **Creating GitHub release**

### Build Matrix

Builds for multiple platforms:

```yaml
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

### Release Artifacts

Each release includes:

- **Source distribution** (`.tar.gz`)
- **Wheel package** (`.whl`)
- **Executables** for all platforms
- **Checksums** for verification

## Local Release Testing

### Build Executables Locally

Test the build process locally:

```bash
# Build for current platform
python scripts/build.py

# Or use the shell script
./scripts/build-local.sh
```

### Test Executables

Test the built executables:

```bash
# Test the executable
./dist/gi --help

# Test functionality
./dist/gi list | head -5
./dist/gi python node -o test.gitignore
```

## Release Notes

### Changelog

Maintain a changelog in `CHANGELOG.md`:

```markdown
# Changelog

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Support for combining .gitignore templates
- CLI interface with list, search, show commands
- Caching for offline usage
- Cross-platform executables

### Changed
- Nothing

### Fixed
- Nothing

### Removed
- Nothing
```

### Release Summary

Create a release summary:

```markdown
# Release Summary

## Version 1.0.0

### What's New
- First public release
- Complete CLI tool for .gitignore management
- Cross-platform support

### Installation
```bash
pip install gi
```

### Quick Start
```bash
gi python node
```

### Full Changelog
See [CHANGELOG.md](CHANGELOG.md)
```

## Post-Release Tasks

### PyPI Upload

Upload to PyPI (if not automated):

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*

# Or upload to Test PyPI first
twine upload --repository testpypi dist/*
```

### Documentation Update

Update documentation:

```bash
# Update version in docs
# Update installation instructions
# Update examples

# Deploy documentation
mkdocs gh-deploy
```

### Announcement

Announce the release:

- **GitHub Release**: Automatic
- **Social Media**: Twitter, LinkedIn
- **Community**: Reddit, Discord
- **Blog**: If you have one

## Rollback Process

### If Release Fails

If a release has issues:

1. **Delete the GitHub release**
2. **Delete the Git tag**
3. **Fix the issues**
4. **Create a new release**

```bash
# Delete tag locally
git tag -d v1.0.0

# Delete tag on remote
git push origin :refs/tags/v1.0.0

# Fix issues and create new release
git tag v1.0.1
git push origin v1.0.1
```

### Hotfix Releases

For critical bugs:

```bash
# Create hotfix branch
git checkout -b hotfix/1.0.1

# Fix the bug
# ... make changes ...

# Commit and tag
git commit -m "fix: critical bug in template fetching"
git tag v1.0.1
git push origin hotfix/1.0.1
git push origin v1.0.1
```

## Release Monitoring

### Health Checks

Monitor release health:

```bash
# Check PyPI package
pip install gi --upgrade
gi --version

# Check GitHub release
# Visit: https://github.com/sempervent/gi/releases

# Check documentation
# Visit: https://sempervent.github.io/gi
```

### User Feedback

Monitor user feedback:

- **GitHub Issues**: Bug reports
- **GitHub Discussions**: Feature requests
- **PyPI**: Download statistics
- **Social Media**: User reactions

## Release Schedule

### Regular Releases

Plan regular releases:

- **Major releases**: Every 6 months
- **Minor releases**: Every 2 months
- **Patch releases**: As needed

### Release Calendar

```markdown
# Release Calendar 2024

## Q1 2024
- v1.0.0 (January) - Initial release
- v1.1.0 (March) - New features

## Q2 2024
- v1.2.0 (May) - Performance improvements
- v2.0.0 (June) - Major refactor

## Q3 2024
- v2.1.0 (August) - New templates
- v2.2.0 (September) - CLI improvements

## Q4 2024
- v2.3.0 (November) - Bug fixes
- v3.0.0 (December) - Major features
```

## Release Tools

### Release Script

The `scripts/release.py` script provides:

```bash
# Show help
python scripts/release.py help

# Build locally
python scripts/release.py build

# Create tag
python scripts/release.py tag --version 1.0.0

# Dry run
python scripts/release.py tag --version 1.0.0 --dry-run
```

### Build Script

The `scripts/build.py` script handles:

```bash
# Build executables
python scripts/build.py

# Build for specific platform
python scripts/build.py --platform linux --arch x86_64
```

## Best Practices

### Release Checklist

Before each release:

- [ ] All tests pass
- [ ] Code is formatted and linted
- [ ] Documentation is updated
- [ ] Version is bumped
- [ ] Changelog is updated
- [ ] Release notes are written
- [ ] Executables are tested locally

### Communication

Communicate releases effectively:

- **Clear release notes**: What's new, what's fixed
- **Migration guides**: For breaking changes
- **Examples**: How to use new features
- **Timeline**: When to expect the release

### Quality Assurance

Ensure release quality:

- **Automated testing**: CI/CD pipeline
- **Manual testing**: Test executables locally
- **User testing**: Beta releases for major changes
- **Performance testing**: Ensure no regressions

This comprehensive guide covers all aspects of the release process for `gi`, from planning to execution to monitoring.
