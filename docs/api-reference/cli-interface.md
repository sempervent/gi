# CLI Interface

The `gi` command-line interface provides a simple and intuitive way to combine `.gitignore` templates from the official GitHub repository.

## Command Structure

```bash
gi [OPTIONS] [TEMPLATES]...
```

## Main Command

### `gi <templates>`

Combine multiple `.gitignore` templates into a single file.

**Arguments:**
- `templates` - One or more template names to combine

**Options:**
- `-o, --output PATH` - Output file path (default: `.gitignore`)
- `-f, --force` - Overwrite existing files without confirmation
- `--help` - Show help message and exit

**Examples:**
```bash
# Combine Python and Node.js templates
gi python node

# Save to custom file
gi python rust scala -o my-project.gitignore

# Overwrite existing file
gi python -o .gitignore --force
```

## Subcommands

### `gi list`

List all available `.gitignore` templates.

**Options:**
- `--help` - Show help message and exit

**Example:**
```bash
gi list
```

### `gi search <query>`

Search for templates by name or description.

**Arguments:**
- `query` - Search term to match against template names

**Options:**
- `--help` - Show help message and exit

**Examples:**
```bash
# Search for Python-related templates
gi search python

# Search for IDE templates
gi search jetbrains
```

### `gi show <template>`

Display the contents of a specific template.

**Arguments:**
- `template` - Name of the template to display

**Options:**
- `--help` - Show help message and exit

**Examples:**
```bash
# Show Python template
gi show python

# Show Global template
gi show Global/JetBrains
```

### `gi doctor`

Check system health and diagnose common issues.

**Options:**
- `--help` - Show help message and exit

**Example:**
```bash
gi doctor
```

## Template Names

Template names are case-insensitive and support several formats:

- **Simple names**: `python`, `node`, `rust`
- **With .gitignore suffix**: `Python.gitignore`, `Node.gitignore`
- **Global templates**: `Global/JetBrains`, `Global/VisualStudioCode`
- **Aliases**: `csharp` → `VisualStudio`, `js` → `Node`

## Exit Codes

- `0` - Success
- `1` - General error (invalid arguments, network issues, etc.)
- `2` - Template not found
- `3` - File system error (permission denied, disk full, etc.)

## Environment Variables

- `GI_CACHE_DIR` - Override default cache directory location
- `GI_TIMEOUT` - Network request timeout in seconds (default: 30)

## Examples

### Basic Usage
```bash
# Create a .gitignore for a Python project
gi python

# Create a .gitignore for a full-stack project
gi python node react

# List available templates
gi list | grep -i python
```

### Advanced Usage
```bash
# Search and combine templates
gi search python | head -5
gi python django pytest

# Show template before using
gi show python
gi python -o .gitignore

# Check system status
gi doctor
```

### CI/CD Integration
```bash
# In a CI script
gi python node -o .gitignore --force
git add .gitignore
git commit -m "Update .gitignore"
```
