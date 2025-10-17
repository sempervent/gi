# Quick Start

Get up and running with `gi` in just a few minutes!

## 🚀 Your First .gitignore

Let's create a `.gitignore` file for a Python project:

```bash
# Create a Python .gitignore
gi main python
```

This will create a `.gitignore` file in your current directory with Python-specific ignore rules.

## 🔍 Explore Available Templates

See what templates are available:

```bash
# List all templates
gi list

# Search for specific templates
gi search python
gi search node
gi search studio
```

## 🎯 Combine Multiple Templates

Create a comprehensive `.gitignore` for a full-stack project:

```bash
# Python backend + Node.js frontend + VS Code
gi main python node vscode

# Or with aliases
gi main python node vscode
```

## 📋 Common Use Cases

### Web Development

```bash
# React + Node.js project
gi main node react

# Django + Python project  
gi main python django

# Full-stack with VS Code
gi main python node react vscode
```

### Mobile Development

```bash
# React Native
gi main node react-native

# Flutter
gi main flutter

# Native iOS/Android
gi main swift kotlin
```

### Data Science

```bash
# Python data science
gi main python jupyter

# R programming
gi main r

# Jupyter notebooks
gi main python jupyter
```

## ⚙️ Advanced Usage

### Custom Output Location

```bash
# Save to specific file
gi main python rust -o my-project/.gitignore

# Append to existing file
gi main python -a existing/.gitignore
```

### Show Template Content

```bash
# Preview a template before using
gi show Python
gi show Global/JetBrains
```

### Get Help

```bash
# General help
gi --help

# Command-specific help
gi main --help
gi list --help
```

## 🎨 Template Aliases

`gi` includes convenient aliases for common templates:

| Alias | Maps to | Description |
|-------|---------|-------------|
| `cpp` | `C++` | C++ development |
| `csharp` | `VisualStudio` | C# development |
| `vscode` | `Global/VisualStudioCode` | VS Code settings |
| `macos` | `Global/macOS` | macOS system files |
| `jetbrains` | `Global/JetBrains` | JetBrains IDEs |
| `node` | `Node` | Node.js projects |
| `python` | `Python` | Python projects |

## 🔄 Workflow Examples

### New Project Setup

```bash
# 1. Create project directory
mkdir my-awesome-project
cd my-awesome-project

# 2. Initialize git
git init

# 3. Create .gitignore
gi main python django vscode

# 4. Start coding!
```

### Team Project

```bash
# Standardize .gitignore across team
gi main python node react vscode -o .gitignore

# Commit to repository
git add .gitignore
git commit -m "Add comprehensive .gitignore"
```

### CI/CD Integration

```bash
# In your build script
gi main python node -o .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

## 🎯 Pro Tips

### 1. Use Aliases
```bash
# Instead of typing full names
gi main cpp csharp vscode  # Much easier!
```

### 2. Preview Before Using
```bash
# Check what's in a template
gi show Python
gi show Global/JetBrains
```

### 3. Combine Related Templates
```bash
# Web development stack
gi main node react typescript vscode

# Data science stack  
gi main python jupyter pandas
```

### 4. Keep Templates Updated
```bash
# Refresh template cache
gi doctor  # Shows cache status
# Templates auto-update when needed
```

## 🚨 Common Mistakes

### ❌ Don't Do This
```bash
# Don't use full template names when aliases exist
gi main "Global/VisualStudioCode"  # Use 'vscode' instead
gi main "C++"                       # Use 'cpp' instead
```

### ✅ Do This Instead
```bash
# Use convenient aliases
gi main vscode cpp
```

## 📚 Next Steps

Now that you know the basics:

1. **[User Guide](user-guide/commands.md)** - Complete command reference
2. **[Tutorials](tutorials/basic-usage.md)** - Detailed step-by-step guides
3. **[Advanced Usage](user-guide/advanced-usage.md)** - Power user features

## 🆘 Need Help?

- **Commands**: `gi --help` or `gi <command> --help`
- **Templates**: `gi list` or `gi search <term>`
- **Issues**: [GitHub Issues](https://github.com/sempervent/gi/issues)
- **Documentation**: This site!

---

**Ready for more?** Check out our [Complete Command Reference](user-guide/commands.md)!
