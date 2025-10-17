# Basic Usage Tutorial

This tutorial will walk you through the most common use cases for `gi` with step-by-step examples.

## 🎯 Tutorial 1: Python Web Development

Let's create a `.gitignore` file for a Python web application using Django.

### Step 1: Start with Python

```bash
# Create a basic Python .gitignore
gi main python
```

This creates a `.gitignore` file with Python-specific ignore rules.

### Step 2: Add Django Framework

```bash
# Add Django-specific rules
gi main python django
```

Now your `.gitignore` includes both Python and Django ignore patterns.

### Step 3: Add Development Tools

```bash
# Add VS Code settings
gi main python django vscode
```

Your `.gitignore` now covers Python, Django, and VS Code.

### Step 4: Add Deployment Tools

```bash
# Add Docker for containerization
gi main python django vscode docker
```

Perfect! You now have a comprehensive `.gitignore` for a Python Django application.

## 🎯 Tutorial 2: Full-Stack JavaScript

Let's create a `.gitignore` for a React + Node.js application.

### Step 1: Base JavaScript

```bash
# Start with Node.js
gi main node
```

### Step 2: Add React Framework

```bash
# Add React-specific rules
gi main node react
```

### Step 3: Add TypeScript

```bash
# Add TypeScript support
gi main node react typescript
```

### Step 4: Add Development Tools

```bash
# Add VS Code and other tools
gi main node react typescript vscode
```

## 🎯 Tutorial 3: Data Science Project

Let's create a `.gitignore` for a Python data science project.

### Step 1: Python Base

```bash
# Start with Python
gi main python
```

### Step 2: Add Jupyter Notebooks

```bash
# Add Jupyter support
gi main python jupyter
```

### Step 3: Add Data Science Libraries

```bash
# Add common data science tools
gi main python jupyter pandas
```

## 🎯 Tutorial 4: Mobile Development

Let's create a `.gitignore` for a Flutter mobile application.

### Step 1: Flutter Framework

```bash
# Start with Flutter
gi main flutter
```

### Step 2: Add Platform Support

```bash
# Add Android and iOS support
gi main flutter android ios
```

### Step 3: Add Development Tools

```bash
# Add VS Code for Flutter development
gi main flutter android ios vscode
```

## 🎯 Tutorial 5: Multi-Language Project

Let's create a `.gitignore` for a project with multiple languages.

### Step 1: Backend (Python)

```bash
# Start with Python backend
gi main python django
```

### Step 2: Frontend (JavaScript)

```bash
# Add Node.js frontend
gi main python django node react
```

### Step 3: Development Tools

```bash
# Add common development tools
gi main python django node react vscode docker
```

## 🔧 Advanced Techniques

### Custom Output Locations

```bash
# Save to specific directory
gi main python django -o backend/.gitignore
gi main node react -o frontend/.gitignore
```

### Appending to Existing Files

```bash
# Start with existing .gitignore
echo "# Custom rules" > .gitignore
echo "my-secret-file.txt" >> .gitignore

# Append Python rules
gi main python -a .gitignore
```

### Preview Before Using

```bash
# Check what's in a template
gi show Python
gi show Django
gi show Global/VisualStudioCode
```

## 🎨 Using Aliases Effectively

### Language Aliases

```bash
# Use convenient aliases
gi main python node rust go java
```

### Framework Aliases

```bash
# Web frameworks
gi main django flask react vue angular
```

### Tool Aliases

```bash
# Development tools
gi main vscode jetbrains docker
```

## 📋 Common Patterns

### Web Development Stacks

```bash
# Python + Django
gi main python django vscode

# Node.js + React
gi main node react typescript vscode

# PHP + Laravel
gi main php laravel vscode
```

### Mobile Development

```bash
# React Native
gi main node react-native

# Flutter
gi main flutter android ios

# Native iOS
gi main swift xcode
```

### Data Science

```bash
# Python data science
gi main python jupyter pandas

# R development
gi main r rstudio
```

### Desktop Development

```bash
# C++ development
gi main cpp cmake vscode

# C# development
gi main csharp visualstudio
```

## 🚀 Pro Tips

### 1. Start Simple, Add Complexity

```bash
# Start with basic language
gi main python

# Add framework
gi main python django

# Add tools
gi main python django vscode
```

### 2. Use Aliases

```bash
# Good
gi main python django vscode

# Avoid
gi main Python Django "Global/VisualStudioCode"
```

### 3. Preview Templates

```bash
# Always check what you're adding
gi show Django
gi show Global/VisualStudioCode
```

### 4. Combine Related Templates

```bash
# Web development
gi main python django vscode

# Mobile development
gi main flutter android ios
```

## 🔍 Troubleshooting

### Template Not Found

```bash
# Search for templates
gi search python
gi search django

# List all templates
gi list
```

### Too Many Rules

```bash
# Start with fewer templates
gi main python  # Instead of python django flask

# Use specific templates
gi main python django  # Instead of python django flask
```

### Missing Rules

```bash
# Check if template exists
gi show Python
gi show Django

# Combine related templates
gi main python django vscode
```

## 📚 Next Steps

Now that you know the basics:

1. **[Advanced Usage](user-guide/advanced-usage.md)** - Power user features
2. **[Configuration](user-guide/configuration.md)** - Customize your setup
3. **[Best Practices](tutorials/best-practices.md)** - Professional workflows

---

**Ready for more?** Check out our [Advanced Usage Guide](user-guide/advanced-usage.md)!
