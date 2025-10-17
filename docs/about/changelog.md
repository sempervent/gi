# Changelog

All notable changes to `gi` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation with MkDocs
- GitHub Pages deployment
- Enhanced release system with cross-platform executables

### Changed
- Improved test coverage and reliability
- Enhanced CLI interface with better error handling

## [0.1.0] - 2024-01-XX

### Added
- Initial release of `gi` CLI tool
- Support for 200+ official `.gitignore` templates
- Intelligent template combination and deduplication
- Local caching for offline usage
- Template aliases for common languages and tools
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive test suite with 74 test cases
- GitHub Actions CI/CD pipeline
- Automated cross-platform executable builds
- Professional documentation site

### Features
- **Main Command**: Combine multiple templates into single `.gitignore`
- **List Command**: Browse all available templates
- **Search Command**: Find templates by name
- **Show Command**: Display raw template content
- **Doctor Command**: Diagnostic information and cache status

### Supported Platforms
- Linux x86_64
- Windows x86_64
- macOS x86_64 (Intel)
- macOS ARM64 (Apple Silicon)

### Template Categories
- **Languages**: Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, PHP, Ruby, Swift, Kotlin
- **Frameworks**: React, Vue, Angular, Django, Flask, Express, Spring, Laravel
- **Tools**: VS Code, JetBrains, Vim, Emacs, Docker, Kubernetes
- **Platforms**: macOS, Windows, Linux, Android, iOS

### Aliases
- **Languages**: `cpp`, `csharp`, `python`, `node`, `java`, `rust`, `go`, `php`, `ruby`, `swift`, `kotlin`
- **Frameworks**: `django`, `flask`, `react`, `vue`, `angular`, `express`, `spring`, `laravel`
- **Tools**: `vscode`, `jetbrains`, `vim`, `emacs`, `docker`, `kubernetes`
- **Platforms**: `macos`, `windows`, `linux`, `android`, `ios`

## [0.0.1] - 2024-01-XX

### Added
- Initial development version
- Basic CLI functionality
- Core template fetching and combining
- Simple caching mechanism
- Basic test suite

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner  
- **PATCH** version for backwards compatible bug fixes

## Release Process

Releases are created automatically when version tags are pushed:

```bash
# Create a new release
python scripts/release.py tag --version 1.0.0
```

This triggers:
1. Cross-platform executable builds
2. GitHub release creation
3. Artifact upload with checksums
4. Documentation deployment

## Breaking Changes

### Version 0.1.0
- Initial public release
- No breaking changes (first release)

## Migration Guide

### From Development Versions

If you were using development versions:

1. **Update installation**:
   ```bash
   pip install --upgrade gi
   ```

2. **Clear cache** (optional):
   ```bash
   rm -rf ~/.cache/gi  # Linux/macOS
   rmdir /s %LOCALAPPDATA%\gi\cache  # Windows
   ```

3. **Verify installation**:
   ```bash
   gi --version
   gi doctor
   ```

## Known Issues

### Version 0.1.0
- None currently known

## Security

### Version 0.1.0
- All templates are fetched from official GitHub repository
- HTTPS is used for all network requests
- Local cache is stored securely
- No sensitive data is collected or transmitted

## Performance

### Version 0.1.0
- Initial template fetch: ~2-3 seconds
- Subsequent usage: <1 second (cached)
- Memory usage: <50MB
- Disk usage: ~10MB (cache)

## Dependencies

### Version 0.1.0
- **Python**: 3.9+
- **requests**: HTTP requests
- **typer**: CLI framework
- **rich**: Terminal formatting
- **platformdirs**: Cross-platform paths

## Contributors

### Version 0.1.0
- Joshua Grant - Initial development and release

## Acknowledgments

### Version 0.1.0
- [github/gitignore](https://github.com/github/gitignore) for comprehensive template collection
- Python community for excellent tooling
- All contributors and testers

---

**For more information, see our [Release Process](developer-guide/release-process.md) documentation.**
