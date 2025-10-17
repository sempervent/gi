# Python API

The `gi` package provides a Python API for programmatically fetching and combining `.gitignore` templates.

## Core Modules

### `gi.fetch`

Handles fetching templates and the index from GitHub.

#### `TemplateFetcher`

Main class for fetching `.gitignore` templates.

```python
from gi.fetch import TemplateFetcher

fetcher = TemplateFetcher()
```

**Methods:**

- `get_template(template_name: str) -> str` - Fetch a single template
- `get_index() -> dict` - Fetch the complete template index
- `get_template_info(template_name: str) -> dict | None` - Get template metadata

**Example:**
```python
from gi.fetch import TemplateFetcher

fetcher = TemplateFetcher()

# Fetch a template
python_template = fetcher.get_template("Python")

# Get template information
info = fetcher.get_template_info("Python")
print(f"Template: {info['name']}")
print(f"Description: {info.get('description', 'No description')}")
```

### `gi.combine`

Handles combining multiple templates into a single `.gitignore` file.

#### `TemplateCombiner`

Main class for combining templates.

```python
from gi.combine import TemplateCombiner

combiner = TemplateCombiner()
```

**Methods:**

- `combine_templates(templates: dict[str, str]) -> str` - Combine multiple templates
- `parse_lines(content: str) -> list[str]` - Parse template content into lines
- `normalize_line(line: str) -> str` - Normalize a single line
- `deduplicate_lines(lines: list[str]) -> list[str]` - Remove duplicate lines

**Example:**
```python
from gi.combine import TemplateCombiner
from gi.fetch import TemplateFetcher

fetcher = TemplateFetcher()
combiner = TemplateCombiner()

# Fetch multiple templates
templates = {
    "Python": fetcher.get_template("Python"),
    "Node": fetcher.get_template("Node"),
}

# Combine them
combined = combiner.combine_templates(templates)
print(combined)
```

### `gi.names`

Handles template name normalization and aliases.

#### Functions

- `normalize_template_name(name: str) -> str` - Normalize a template name
- `resolve_template_name(name: str) -> str` - Resolve aliases to canonical names

**Example:**
```python
from gi.names import normalize_template_name, resolve_template_name

# Normalize names
print(normalize_template_name("python.gitignore"))  # "Python"
print(normalize_template_name("csharp"))  # "VisualStudio"

# Resolve aliases
print(resolve_template_name("c#"))  # "VisualStudio"
print(resolve_template_name("js"))  # "Node"
```

### `gi.util`

Utility functions for file operations and caching.

#### Functions

- `get_cache_dir() -> Path` - Get the cache directory path
- `read_gitignore(path: Path) -> str` - Read a `.gitignore` file
- `write_gitignore(path: Path, content: str) -> None` - Write a `.gitignore` file
- `normalize_line_endings(content: str) -> str` - Normalize line endings

**Example:**
```python
from gi.util import get_cache_dir, read_gitignore, write_gitignore
from pathlib import Path

# Get cache directory
cache_dir = get_cache_dir()
print(f"Cache directory: {cache_dir}")

# Read existing .gitignore
gitignore_path = Path(".gitignore")
if gitignore_path.exists():
    content = read_gitignore(gitignore_path)
    print(f"Current .gitignore has {len(content.splitlines())} lines")

# Write new .gitignore
new_content = "# Python\n__pycache__/\n*.pyc\n"
write_gitignore(gitignore_path, new_content)
```

## Complete Example

Here's a complete example that demonstrates the Python API:

```python
#!/usr/bin/env python3
"""Example script using the gi Python API."""

from gi.fetch import TemplateFetcher
from gi.combine import TemplateCombiner
from gi.names import normalize_template_name
from gi.util import write_gitignore
from pathlib import Path

def create_gitignore(template_names: list[str], output_path: str = ".gitignore"):
    """Create a .gitignore file from multiple templates."""
    
    # Initialize components
    fetcher = TemplateFetcher()
    combiner = TemplateCombiner()
    
    # Fetch templates
    templates = {}
    for name in template_names:
        normalized_name = normalize_template_name(name)
        try:
            content = fetcher.get_template(normalized_name)
            templates[normalized_name] = content
            print(f"✓ Fetched {normalized_name}")
        except Exception as e:
            print(f"✗ Failed to fetch {normalized_name}: {e}")
    
    if not templates:
        print("No templates were successfully fetched")
        return False
    
    # Combine templates
    combined_content = combiner.combine_templates(templates)
    
    # Write to file
    output_path_obj = Path(output_path)
    write_gitignore(output_path_obj, combined_content)
    
    print(f"✓ Created {output_path} with {len(templates)} templates")
    return True

if __name__ == "__main__":
    # Example usage
    templates = ["python", "node", "rust"]
    create_gitignore(templates, "my-project.gitignore")
```

## Error Handling

The API raises appropriate exceptions for different error conditions:

```python
from gi.fetch import TemplateFetcher
from gi.exceptions import TemplateNotFoundError, NetworkError

fetcher = TemplateFetcher()

try:
    template = fetcher.get_template("NonExistentTemplate")
except TemplateNotFoundError:
    print("Template not found")
except NetworkError:
    print("Network error occurred")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Caching

The API automatically caches templates and the index to improve performance and enable offline usage:

```python
from gi.fetch import TemplateFetcher
from gi.util import get_cache_dir

# Cache directory is automatically managed
cache_dir = get_cache_dir()
print(f"Templates are cached in: {cache_dir}")

# First call fetches from network
fetcher = TemplateFetcher()
template1 = fetcher.get_template("Python")  # Network request

# Subsequent calls use cache
template2 = fetcher.get_template("Python")  # From cache
```

## Thread Safety

The API is thread-safe and can be used in multi-threaded applications:

```python
import threading
from gi.fetch import TemplateFetcher

def fetch_template(name: str):
    fetcher = TemplateFetcher()
    template = fetcher.get_template(name)
    print(f"Fetched {name}: {len(template)} characters")

# Fetch multiple templates concurrently
threads = []
for name in ["Python", "Node", "Rust"]:
    thread = threading.Thread(target=fetch_template, args=(name,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```
