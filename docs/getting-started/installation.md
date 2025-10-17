# Installation

This guide covers different ways to install `gi` on your system.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation Methods

### 🎯 Recommended: pipx (Isolated Environment)

**pipx** is the recommended way to install `gi` as it creates an isolated environment, preventing dependency conflicts.

```bash
# Install pipx if you don't have it
python -m pip install --user pipx
python -m pipx ensurepath

# Install gi
pipx install gi
```

**Benefits:**
- ✅ Isolated from other Python packages
- ✅ No dependency conflicts
- ✅ Easy to update and uninstall
- ✅ Works on all platforms

### 📦 Standard: pip

Install directly with pip:

```bash
# Install globally
pip install gi

# Or install for current user only
pip install --user gi
```

### 🐍 Virtual Environment

For development or if you prefer isolated environments:

```bash
# Create virtual environment
python -m venv gi-env

# Activate (Linux/macOS)
source gi-env/bin/activate

# Activate (Windows)
gi-env\Scripts\activate

# Install gi
pip install gi
```

### 🏗️ From Source

For development or latest features:

```bash
# Clone repository
git clone https://github.com/sempervent/gi.git
cd gi

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 📱 Platform-Specific

#### macOS

```bash
# Using Homebrew (if available)
brew install python
pipx install gi

# Or using MacPorts
sudo port install python39
pipx install gi
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install gi
pipx install gi
```

#### Windows

```powershell
# Using Chocolatey
choco install python
pipx install gi

# Or download Python from python.org
# Then run: pipx install gi
```

## 🚀 Download Executables

For users who prefer not to install Python, we provide pre-built executables:

### Download from GitHub Releases

Visit our [Releases page](https://github.com/sempervent/gi/releases) and download the appropriate executable for your platform:

- **Linux x86_64**: `gi-{version}-linux-x86_64.tar.gz`
- **Windows x86_64**: `gi-{version}-windows-x86_64.zip`
- **macOS x86_64**: `gi-{version}-macos-x86_64.tar.gz`
- **macOS ARM64**: `gi-{version}-macos-arm64.tar.gz`

### Installation from Executables

#### Linux/macOS

```bash
# Download and extract
wget https://github.com/sempervent/gi/releases/download/v0.1.0/gi-0.1.0-linux-x86_64.tar.gz
tar -xzf gi-0.1.0-linux-x86_64.tar.gz

# Make executable and move to PATH
chmod +x gi
sudo mv gi /usr/local/bin/

# Verify installation
gi --help
```

#### Windows

```powershell
# Download and extract
Invoke-WebRequest -Uri "https://github.com/sempervent/gi/releases/download/v0.1.0/gi-0.1.0-windows-x86_64.zip" -OutFile "gi.zip"
Expand-Archive -Path "gi.zip" -DestinationPath "gi"

# Add to PATH (optional)
# Move gi.exe to a directory in your PATH
```

## ✅ Verify Installation

After installation, verify that `gi` is working:

```bash
# Check version
gi --version

# Show help
gi --help

# Test basic functionality
gi list | head -5
```

Expected output:
```
gi version 0.1.0
Usage: gi [OPTIONS] COMMAND [ARGS]...

A CLI tool to combine .gitignore templates from github/gitignore

Commands:
  main     Combine .gitignore templates into a single file.
  list     List all available .gitignore templates.
  search   Search for .gitignore templates by name.
  show     Show the raw content of a .gitignore template.
  doctor   Show diagnostic information about gi's cache and configuration.
```

## 🔄 Updating

### Using pipx

```bash
pipx upgrade gi
```

### Using pip

```bash
pip install --upgrade gi
```

### Using Executables

Download the latest release from [GitHub Releases](https://github.com/sempervent/gi/releases).

## 🗑️ Uninstalling

### pipx

```bash
pipx uninstall gi
```

### pip

```bash
pip uninstall gi
```

### Manual Cleanup

If you installed manually, you may need to:

1. Remove the executable from your PATH
2. Delete cache directory:
   - **Linux/macOS**: `~/.cache/gi`
   - **Windows**: `%LOCALAPPDATA%\gi\cache`

## 🐛 Troubleshooting

### Command Not Found

If `gi` command is not found after installation:

1. **Check PATH**: Ensure the installation directory is in your PATH
2. **Restart terminal**: Close and reopen your terminal
3. **Check installation**: Verify with `pip list | grep gi` or `pipx list`

### Permission Errors

If you get permission errors:

```bash
# Install for current user only
pip install --user gi

# Or use pipx (recommended)
pipx install gi
```

### Python Version Issues

Ensure you have Python 3.9 or higher:

```bash
python --version
# Should show Python 3.9.x or higher
```

### Network Issues

If you have network restrictions:

1. Use cached templates (works offline)
2. Configure proxy settings if needed
3. Check firewall settings

## 📞 Getting Help

If you encounter issues:

1. Check our [Troubleshooting Guide](user-guide/configuration.md#troubleshooting)
2. Search [GitHub Issues](https://github.com/sempervent/gi/issues)
3. Create a new issue with details about your problem

---

**Next:** [Quick Start Guide](quick-start.md) to get up and running with `gi`!
