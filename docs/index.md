# Welcome to gi

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/sempervent/gi/workflows/CI/badge.svg)](https://github.com/sempervent/gi/actions/workflows/ci.yml)
[![Build](https://github.com/sempervent/gi/workflows/Build%20Cross-Platform%20Executables/badge.svg)](https://github.com/sempervent/gi/actions/workflows/build.yml)
[![Coverage](https://codecov.io/gh/sempervent/gi/branch/main/graph/badge.svg)](https://codecov.io/gh/sempervent/gi)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/gi.svg)](https://pypi.org/project/gi/)
[![Downloads](https://pepy.tech/badge/gi)](https://pepy.tech/project/gi)

A fast, intelligent CLI tool that fetches and combines official `.gitignore` templates from [github/gitignore](https://github.com/github/gitignore) into a single, deduplicated `.gitignore` file.

## ✨ Features

- 🚀 **Fast**: Caches templates locally for offline use
- 🧠 **Smart**: Deduplicates rules across templates while preserving comments
- 🔍 **Searchable**: List and search through 200+ available templates
- 🎯 **Flexible**: Support for aliases, case-insensitive names, and custom output paths
- 💪 **Robust**: Graceful fallback to cached content when offline
- 🖥️ **Cross-platform**: Works on macOS, Linux, and Windows

## 🚀 Quick Start

### Installation

**Recommended (using pipx):**
```bash
pipx install gi
```

**Alternative (using pip):**
```bash
pip install gi
```

**From source:**
```bash
git clone https://github.com/sempervent/gi.git
cd gi
pip install -e .
```

### Basic Usage

```bash
# Combine multiple templates
gi main python rust node

# List available templates
gi list

# Search for templates
gi search studio

# Show template content
gi show Global/JetBrains
```

## 📖 Documentation

This documentation covers everything you need to know about `gi`:

- **[Getting Started](getting-started/installation.md)** - Installation and setup
- **[User Guide](user-guide/commands.md)** - Complete command reference
- **[Tutorials](tutorials/basic-usage.md)** - Step-by-step guides
- **[Developer Guide](developer-guide/contributing.md)** - Contributing and development

## 🎯 Use Cases

### For Developers
- Quickly set up `.gitignore` files for new projects
- Combine multiple language-specific templates
- Maintain consistent ignore patterns across projects

### For Teams
- Standardize `.gitignore` files across team projects
- Automate `.gitignore` generation in CI/CD pipelines
- Share common ignore patterns between projects

### For Open Source
- Generate comprehensive `.gitignore` files for multi-language projects
- Maintain up-to-date ignore patterns from official templates
- Reduce maintenance overhead of custom `.gitignore` files

## 🔧 Advanced Features

### Template Aliases
```bash
# Use convenient aliases
gi main cpp csharp vscode  # C++, C#, VS Code
gi main python django      # Python with Django
gi main node react         # Node.js with React
```

### Custom Output
```bash
# Specify output file
gi main python rust -o my-project/.gitignore

# Append to existing file
gi main python -a existing/.gitignore
```

### Offline Usage
```bash
# Works offline with cached templates
gi main python rust  # Uses cached templates if network unavailable
```

## 📊 Supported Templates

`gi` supports 200+ official templates including:

- **Languages**: Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, PHP, Ruby, Swift, Kotlin
- **Frameworks**: React, Vue, Angular, Django, Flask, Express, Spring, Laravel
- **Tools**: VS Code, JetBrains, Vim, Emacs, Docker, Kubernetes
- **Platforms**: macOS, Windows, Linux, Android, iOS
- **And many more...**

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](developer-guide/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](about/license.md) file for details.

## 🙏 Acknowledgments

- [github/gitignore](https://github.com/github/gitignore) for the comprehensive template collection
- The Python community for excellent tooling and libraries
- All contributors who help make `gi` better

---

**Ready to get started?** Check out our [Installation Guide](getting-started/installation.md)!
