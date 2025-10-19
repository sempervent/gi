"""Utility functions for gi."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import platformdirs


def get_cache_dir() -> Path:
    """Get the cache directory for gi."""
    if platform.system() == "Windows":
        # Use %LOCALAPPDATA%\gi\cache on Windows
        cache_dir = platformdirs.user_cache_dir("gi", "gi")
    else:
        # Use ~/.cache/gi on POSIX systems
        cache_dir = platformdirs.user_cache_dir("gi")

    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


def get_index_cache_path() -> Path:
    """Get the path to the cached index file."""
    return get_cache_dir() / "index.json"


def get_template_cache_path(template_name: str) -> Path:
    """Get the cache path for a specific template."""
    return get_cache_dir() / f"{template_name}.gitignore"


def normalize_line_endings(text: str) -> str:
    """Normalize line endings to Unix style."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def ensure_trailing_newline(text: str) -> str:
    """Ensure text ends with exactly one newline."""
    text = text.rstrip("\n")
    return text + "\n" if text else ""


def is_stale_cache(cache_path: Path, max_age_hours: int = 24) -> bool:
    """Check if a cache file is stale."""
    if not cache_path.exists():
        return True

    import time  # noqa: PLC0415

    cache_age = time.time() - cache_path.stat().st_mtime
    return cache_age > (max_age_hours * 3600)


def safe_write_file(path: Path, content: str, *, force: bool = False) -> bool:
    """Safely write content to a file, with optional force overwrite."""
    if path.exists() and not force:
        return False

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    with path.open("w", encoding="utf-8") as f:
        f.write(content)

    return True


def read_existing_gitignore(path: Path) -> str | None:
    """Read existing .gitignore file if it exists."""
    if not path.exists():
        return None

    try:
        with path.open(encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def detect_operating_system() -> str:
    """Detect the current operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        # Fallback for other systems
        return "linux"


def get_os_specific_templates() -> list[str]:
    """Get OS-specific .gitignore templates based on the current OS."""
    os_type = detect_operating_system()
    
    # OS-specific template mappings
    os_templates = {
        "windows": [
            "Windows",
        ],
        "macos": [
            "macOS",
        ],
        "linux": [
            "Linux",
        ],
    }
    
    return os_templates.get(os_type, ["Linux"])


def detect_development_environment() -> list[str]:
    """Detect common development environments and return appropriate templates."""
    templates = []
    
    # Check for common development tools
    try:
        import subprocess
        
        # Check for Node.js/npm
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
            subprocess.run(["npm", "--version"], capture_output=True, check=True)
            templates.append("Node")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        # Check for Python
        if sys.executable:
            templates.append("Python")
            
        # Check for Git
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            # Git is always available if we're using gi, so don't add a template
            pass
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
    except ImportError:
        # Fallback if subprocess is not available
        pass
    
    return templates


def get_auto_detect_templates() -> list[str]:
    """Get automatically detected templates based on OS and development environment."""
    templates = []
    
    # Add OS-specific templates
    templates.extend(get_os_specific_templates())
    
    # Add development environment templates
    templates.extend(detect_development_environment())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_templates = []
    for template in templates:
        if template not in seen:
            seen.add(template)
            unique_templates.append(template)
    
    return unique_templates
