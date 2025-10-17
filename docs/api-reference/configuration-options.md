# Configuration Options

The `gi` tool supports various configuration options through environment variables and command-line arguments.

## Environment Variables

### `GI_CACHE_DIR`

Override the default cache directory location.

**Default:** Platform-specific cache directory
- **Linux/macOS:** `~/.cache/gi`
- **Windows:** `%LOCALAPPDATA%\gi\cache`

**Example:**
```bash
export GI_CACHE_DIR="/custom/cache/path"
gi python
```

### `GI_TIMEOUT`

Set the network request timeout in seconds.

**Default:** `30`

**Example:**
```bash
export GI_TIMEOUT=60
gi python
```

### `GI_OFFLINE`

Force offline mode, using only cached templates.

**Default:** `false`

**Example:**
```bash
export GI_OFFLINE=true
gi python  # Will only work if Python template is cached
```

## Command-Line Options

### Global Options

These options are available for all commands:

#### `--help`, `-h`

Show help message and exit.

```bash
gi --help
gi list --help
gi search --help
```

#### `--version`, `-v`

Show version information and exit.

```bash
gi --version
```

### Main Command Options

#### `--output`, `-o`

Specify the output file path.

**Default:** `.gitignore`

**Example:**
```bash
gi python -o my-project.gitignore
gi python node -o .gitignore.backup
```

#### `--force`, `-f`

Overwrite existing files without confirmation.

**Default:** `false` (prompts for confirmation)

**Example:**
```bash
gi python --force
gi python -o .gitignore -f
```

#### `--dry-run`

Show what would be done without actually creating files.

**Example:**
```bash
gi python node --dry-run
```

#### `--verbose`, `-V`

Enable verbose output.

**Example:**
```bash
gi python --verbose
```

### Search Command Options

#### `--exact`

Perform exact name matching instead of partial matching.

**Example:**
```bash
gi search python --exact  # Only matches "Python", not "Python.gitignore"
```

#### `--limit`

Limit the number of search results.

**Default:** `50`

**Example:**
```bash
gi search python --limit 10
```

## Configuration File

You can create a configuration file to set default options.

### Location

The configuration file is looked for in the following locations (in order):

1. `GI_CONFIG_FILE` environment variable
2. `~/.config/gi/config.toml`
3. `~/.gi/config.toml`
4. `./gi.toml` (project-local)

### Format

The configuration file uses TOML format:

```toml
# gi.toml

[defaults]
output = ".gitignore"
force = false
timeout = 30
cache_dir = "~/.cache/gi"

[search]
exact = false
limit = 50

[format]
include_headers = true
sort_templates = true
```

### Example Configuration

```toml
# ~/.config/gi/config.toml

[defaults]
# Always overwrite existing files
force = true

# Use a custom cache directory
cache_dir = "~/Documents/gi-cache"

# Longer timeout for slow connections
timeout = 60

[search]
# Show more results
limit = 100

[format]
# Include section headers in output
include_headers = true

# Sort templates alphabetically
sort_templates = true
```

## Template Aliases

You can define custom aliases for template names in your configuration:

```toml
# ~/.config/gi/config.toml

[aliases]
# Custom aliases
py = "Python"
js = "Node"
ts = "TypeScript"
react = "React"
vue = "Vue"
```

**Usage:**
```bash
gi py js  # Equivalent to: gi Python Node
```

## Cache Management

### Cache Directory Structure

```
~/.cache/gi/
├── index.json          # Template index
├── templates/          # Cached templates
│   ├── Python.gitignore
│   ├── Node.gitignore
│   └── ...
└── metadata.json       # Cache metadata
```

### Cache Commands

#### `gi cache clear`

Clear all cached templates and index.

```bash
gi cache clear
```

#### `gi cache list`

List cached templates.

```bash
gi cache list
```

#### `gi cache info`

Show cache statistics.

```bash
gi cache info
```

## Network Configuration

### Proxy Support

The tool respects standard proxy environment variables:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1
```

### Custom User Agent

Set a custom User-Agent string:

```bash
export GI_USER_AGENT="MyApp/1.0 (https://example.com)"
```

## Debugging

### Debug Mode

Enable debug output:

```bash
export GI_DEBUG=true
gi python
```

### Verbose Logging

Enable verbose logging:

```bash
export GI_LOG_LEVEL=DEBUG
gi python
```

### Log File

Specify a log file:

```bash
export GI_LOG_FILE=/tmp/gi.log
gi python
```

## Platform-Specific Configuration

### Windows

On Windows, you can use the registry or environment variables:

```cmd
REM Set cache directory
set GI_CACHE_DIR=C:\Users\%USERNAME%\AppData\Local\gi\cache

REM Set timeout
set GI_TIMEOUT=45
```

### macOS

On macOS, you can use `defaults` or environment variables:

```bash
# Using defaults (requires custom implementation)
defaults write com.example.gi cache_dir "~/Library/Caches/gi"

# Using environment variables
export GI_CACHE_DIR="~/Library/Caches/gi"
```

### Linux

On Linux, follow the XDG Base Directory specification:

```bash
# Cache directory
export XDG_CACHE_HOME="$HOME/.cache"
export GI_CACHE_DIR="$XDG_CACHE_HOME/gi"

# Config directory
export XDG_CONFIG_HOME="$HOME/.config"
```

## Examples

### Basic Configuration

```bash
# Set up basic configuration
export GI_CACHE_DIR="~/.cache/gi"
export GI_TIMEOUT=30

# Use the tool
gi python node
```

### Advanced Configuration

```toml
# ~/.config/gi/config.toml

[defaults]
force = true
timeout = 60
cache_dir = "~/Documents/gi-cache"

[aliases]
py = "Python"
js = "Node"
react = "React"

[search]
limit = 100
exact = false

[format]
include_headers = true
sort_templates = true
```

### CI/CD Configuration

```bash
# In CI environment
export GI_CACHE_DIR="/tmp/gi-cache"
export GI_TIMEOUT=10
export GI_OFFLINE=false

# Create .gitignore
gi python node --force
```
