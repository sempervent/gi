# First Steps

Welcome to `gi`! This guide will walk you through your first steps with the `.gitignore` combiner.

## 🎯 What is gi?

`gi` is a command-line tool that helps you create comprehensive `.gitignore` files by combining official templates from [github/gitignore](https://github.com/github/gitignore). Instead of manually copying and pasting ignore rules, `gi` does it automatically and intelligently.

## 🚀 Why Use gi?

### Before gi
```bash
# Manual process - time consuming and error-prone
# 1. Go to github.com/github/gitignore
# 2. Find Python template
# 3. Copy content
# 4. Find Node.js template  
# 5. Copy content
# 6. Manually combine and deduplicate
# 7. Save as .gitignore
```

### With gi
```bash
# One command - fast and reliable
gi main python node
```

## 📋 Prerequisites

Before we start, make sure you have:

- ✅ `gi` installed (see [Installation Guide](installation.md))
- ✅ Basic familiarity with command line
- ✅ A project directory to work with

## 🏁 Step 1: Verify Installation

First, let's make sure `gi` is working:

```bash
gi --version
```

You should see something like:
```
gi version 0.1.0
```

## 🔍 Step 2: Explore Available Templates

Let's see what templates are available:

```bash
# List all templates
gi list
```

This shows you all 200+ available templates. You'll see output like:
```
Available .gitignore Templates
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Template Name         ┃ Category           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ Python               │ Language/Framework │
│ Node                 │ Language/Framework │
│ React                │ Language/Framework │
│ Django               │ Language/Framework │
│ Flask                │ Language/Framework │
│ ...                  │ ...                │
└──────────────────────┴────────────────────┘
```

## 🔎 Step 3: Search for Templates

Let's search for templates related to Python:

```bash
gi search python
```

This will show templates that match "python":
```
Search Results for "python"
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Template Name         ┃ Category           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ Python               │ Language/Framework │
│ Django               │ Language/Framework │
│ Flask                │ Language/Framework │
│ Jupyter              │ Language/Framework │
└──────────────────────┴────────────────────┘
```

## 👀 Step 4: Preview a Template

Before using a template, let's see what's in it:

```bash
gi show Python
```

This shows the raw content of the Python template:
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
...
```

## 🎯 Step 5: Create Your First .gitignore

Now let's create a `.gitignore` file for a Python project:

```bash
# Create a Python .gitignore
gi main python
```

This creates a `.gitignore` file in your current directory. Let's verify it worked:

```bash
# Check if file was created
ls -la .gitignore

# View the content
head -20 .gitignore
```

## 🔄 Step 6: Combine Multiple Templates

Let's create a more comprehensive `.gitignore` for a full-stack project:

```bash
# Python backend + Node.js frontend
gi main python node
```

This combines both Python and Node.js ignore rules into one file.

## 🎨 Step 7: Use Convenient Aliases

`gi` includes aliases to make common combinations easier:

```bash
# Use aliases instead of full names
gi main python node vscode
```

This is equivalent to:
```bash
gi main Python Node "Global/VisualStudioCode"
```

## ⚙️ Step 8: Customize Output

Let's try some advanced options:

```bash
# Save to a specific file
gi main python rust -o my-project/.gitignore

# Append to existing file
gi main python -a existing/.gitignore

# Force overwrite without prompting
gi main python node --force
```

## 🔍 Step 9: Get Diagnostic Information

Check the status of your `gi` installation:

```bash
gi doctor
```

This shows information about:
- Cache status
- Available templates
- Configuration
- Network connectivity

## 🎯 Step 10: Real-World Example

Let's create a `.gitignore` for a real project. Imagine you're building a web application with:

- Python backend (Django)
- Node.js frontend (React)
- VS Code for development
- Docker for containerization

```bash
# Create comprehensive .gitignore
gi main python django node react vscode docker
```

This creates a `.gitignore` file that covers all these technologies!

## 🎉 Congratulations!

You've successfully:

- ✅ Installed and verified `gi`
- ✅ Explored available templates
- ✅ Created your first `.gitignore` file
- ✅ Combined multiple templates
- ✅ Used aliases and advanced options
- ✅ Created a real-world example

## 🚀 What's Next?

Now that you know the basics, explore more:

1. **[User Guide](user-guide/commands.md)** - Complete command reference
2. **[Tutorials](tutorials/basic-usage.md)** - Detailed guides
3. **[Advanced Usage](user-guide/advanced-usage.md)** - Power user features

## 🆘 Common Issues

### Template Not Found
```bash
# If a template isn't found, search for it
gi search <partial-name>

# Or list all to see exact names
gi list
```

### Permission Errors
```bash
# Make sure you have write permissions in the directory
ls -la .  # Check permissions
```

### Network Issues
```bash
# gi works offline with cached templates
gi doctor  # Check cache status
```

## 💡 Pro Tips

1. **Use aliases**: They're shorter and easier to remember
2. **Preview templates**: Use `gi show <template>` before combining
3. **Check results**: Always review the generated `.gitignore`
4. **Keep it simple**: Start with basic templates, add complexity as needed

---

**Ready for more?** Check out our [Complete Command Reference](user-guide/commands.md)!
