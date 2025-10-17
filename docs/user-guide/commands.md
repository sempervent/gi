# Commands

Complete reference for all `gi` commands and options.

## 📋 Command Overview

```bash
gi [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message and exit |
| `--version` | Show version and exit |
| `--install-completion` | Install shell completion |
| `--show-completion` | Show completion script |

## 🎯 Main Command

### `gi main`

Combine `.gitignore` templates into a single file.

```bash
gi main TEMPLATES... [OPTIONS]
```

#### Arguments

- `TEMPLATES`: Space or comma-separated template names

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `.gitignore` |
| `--append` | `-a` | Append to existing file | `False` |
| `--force` | `-f` | Overwrite without prompting | `False` |
| `--no-cache` | | Ignore cache for this run | `False` |
| `--update-index` | | Refresh template list | `False` |
| `--from` | | Override source repository URL | `github/gitignore` |

#### Examples

```bash
# Basic usage
gi main python rust

# Custom output location
gi main python rust -o my-project/.gitignore

# Append to existing file
gi main python -a existing/.gitignore

# Force overwrite
gi main python node --force

# Use aliases
gi main cpp csharp vscode

# Comma-separated templates
gi main python,rust,node
```

## 📋 List Command

### `gi list`

List all available `.gitignore` templates.

```bash
gi list [OPTIONS]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--category` | Filter by category | All |
| `--limit` | Limit number of results | All |
| `--format` | Output format (table, json) | `table` |

#### Examples

```bash
# List all templates
gi list

# Filter by category
gi list --category "Language/Framework"

# Limit results
gi list --limit 10

# JSON output
gi list --format json
```

## 🔍 Search Command

### `gi search`

Search for `.gitignore` templates by name.

```bash
gi search QUERY [OPTIONS]
```

#### Arguments

- `QUERY`: Search term (case-insensitive)

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--category` | Filter by category | All |
| `--limit` | Limit number of results | All |
| `--format` | Output format (table, json) | `table` |

#### Examples

```bash
# Search for Python-related templates
gi search python

# Search for IDE templates
gi search studio

# Search with category filter
gi search python --category "Language/Framework"

# JSON output
gi search python --format json
```

## 👀 Show Command

### `gi show`

Display the raw content of a `.gitignore` template.

```bash
gi show TEMPLATE [OPTIONS]
```

#### Arguments

- `TEMPLATE`: Template name to display

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lines` | Number of lines to show | All |
| `--format` | Output format (text, json) | `text` |

#### Examples

```bash
# Show Python template
gi show Python

# Show first 20 lines
gi show Python --lines 20

# Show VS Code template
gi show Global/VisualStudioCode

# JSON format
gi show Python --format json
```

## 🩺 Doctor Command

### `gi doctor`

Show diagnostic information about `gi`'s cache and configuration.

```bash
gi doctor [OPTIONS]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--verbose` | Show detailed information | `False` |
| `--format` | Output format (table, json) | `table` |

#### Examples

```bash
# Basic diagnostics
gi doctor

# Detailed information
gi doctor --verbose

# JSON output
gi doctor --format json
```

## 🎨 Template Aliases

`gi` includes convenient aliases for common templates:

### Language Aliases

| Alias | Maps to | Description |
|-------|---------|-------------|
| `cpp` | `C++` | C++ development |
| `csharp` | `VisualStudio` | C# development |
| `python` | `Python` | Python development |
| `node` | `Node` | Node.js development |
| `java` | `Java` | Java development |
| `rust` | `Rust` | Rust development |
| `go` | `Go` | Go development |
| `php` | `PHP` | PHP development |
| `ruby` | `Ruby` | Ruby development |
| `swift` | `Swift` | Swift development |
| `kotlin` | `Kotlin` | Kotlin development |

### Framework Aliases

| Alias | Maps to | Description |
|-------|---------|-------------|
| `django` | `Django` | Django framework |
| `flask` | `Flask` | Flask framework |
| `react` | `React` | React framework |
| `vue` | `Vue` | Vue.js framework |
| `angular` | `Angular` | Angular framework |
| `express` | `Express` | Express.js framework |
| `spring` | `Spring` | Spring framework |
| `laravel` | `Laravel` | Laravel framework |

### Tool Aliases

| Alias | Maps to | Description |
|-------|---------|-------------|
| `vscode` | `Global/VisualStudioCode` | VS Code settings |
| `jetbrains` | `Global/JetBrains` | JetBrains IDEs |
| `vim` | `Global/Vim` | Vim editor |
| `emacs` | `Global/Emacs` | Emacs editor |
| `docker` | `Docker` | Docker containers |
| `kubernetes` | `Kubernetes` | Kubernetes |

### Platform Aliases

| Alias | Maps to | Description |
|-------|---------|-------------|
| `macos` | `Global/macOS` | macOS system files |
| `windows` | `Global/Windows` | Windows system files |
| `linux` | `Global/Linux` | Linux system files |
| `android` | `Android` | Android development |
| `ios` | `iOS` | iOS development |

## 🔧 Configuration

### Cache Directory

`gi` caches templates locally for offline use:

- **Linux/macOS**: `~/.cache/gi`
- **Windows**: `%LOCALAPPDATA%\gi\cache`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GI_CACHE_DIR` | Custom cache directory | Platform default |
| `GI_SOURCE_URL` | Custom source repository | `github/gitignore` |
| `GI_NO_CACHE` | Disable caching | `False` |

### Configuration File

Create a `gi.yml` file in your home directory:

```yaml
cache:
  directory: ~/.cache/gi
  ttl: 86400  # 24 hours

source:
  url: github/gitignore
  branch: main

output:
  format: gitignore
  header: true
  comments: true
```

## 🚨 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Template not found` | Invalid template name | Use `gi list` to see available templates |
| `Network error` | No internet connection | Use cached templates or check connection |
| `Permission denied` | No write access | Check directory permissions |
| `Cache error` | Corrupted cache | Run `gi doctor` to check cache status |

### Troubleshooting

```bash
# Check system status
gi doctor

# Clear cache
rm -rf ~/.cache/gi  # Linux/macOS
rmdir /s %LOCALAPPDATA%\gi\cache  # Windows

# Update templates
gi main python --update-index
```

## 💡 Tips and Tricks

### 1. Use Aliases
```bash
# Instead of full names
gi main "Global/VisualStudioCode" "Global/JetBrains"

# Use aliases
gi main vscode jetbrains
```

### 2. Preview Before Using
```bash
# Check template content
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

### 4. Use Output Options
```bash
# Save to specific location
gi main python -o my-project/.gitignore

# Append to existing file
gi main python -a existing/.gitignore
```

### 5. Batch Operations
```bash
# Create multiple .gitignore files
for project in frontend backend; do
  gi main python node -o $project/.gitignore
done
```

---

**Next:** [Templates Guide](templates.md) to learn about available templates!
