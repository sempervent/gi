"""Fetch .gitignore templates from GitHub and manage caching."""

from __future__ import annotations

import json
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .util import (
    get_index_cache_path,
    get_template_cache_path,
    is_stale_cache,
)


class GitIgnoreFetcher:
    """Handles fetching and caching .gitignore templates."""

    def __init__(
        self, base_url: str = "https://raw.githubusercontent.com/github/gitignore/HEAD",
    ):
        self.base_url = base_url.rstrip("/")
        self.api_base = "https://api.github.com/repos/github/gitignore/contents"

        # Set up requests session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set a reasonable timeout
        self.session.timeout = 30

    def get_index(self, *, force: bool = False) -> dict:
        """Get the list of available templates from GitHub API."""
        cache_path = get_index_cache_path()

        # Check cache first (unless forced or stale)
        if not force and cache_path.exists() and not is_stale_cache(cache_path):
            try:
                with cache_path.open(encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                # Cache is corrupted, fetch fresh
                pass

        # Fetch from GitHub API
        try:
            response = self.session.get(self.api_base)
            response.raise_for_status()

            # Parse the response to find all .gitignore files
            templates = []
            for item in response.json():
                if item["type"] == "file" and item["name"].endswith(".gitignore"):
                    templates.append(
                        {
                            "name": item["name"],
                            "path": item["path"],
                            "download_url": item["download_url"],
                            "size": item["size"],
                        },
                    )
                elif item["type"] == "dir" and item["name"] == "Global":
                    # Fetch Global directory contents
                    global_response = self.session.get(item["url"])
                    global_response.raise_for_status()

                    for global_item in global_response.json():
                        if global_item["type"] == "file" and global_item[
                            "name"
                        ].endswith(".gitignore"):
                            templates.append(
                                {
                                    "name": global_item["name"],
                                    "path": global_item["path"],
                                    "download_url": global_item["download_url"],
                                    "size": global_item["size"],
                                },
                            )

            # Create index data
            index_data = {
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": self.api_base,
                "templates": templates,
            }

            # Cache the result
            try:
                with cache_path.open("w", encoding="utf-8") as f:
                    json.dump(index_data, f, indent=2)
            except OSError:
                # Cache write failed, but we can still return the data
                pass
            else:
                return index_data

        except requests.RequestException as e:
            # If we have cached data, use it even if stale
            if cache_path.exists():
                try:
                    with cache_path.open(encoding="utf-8") as f:
                        return json.load(f)
                except (json.JSONDecodeError, OSError):
                    pass

            error_msg = f"Failed to fetch template index: {e}"
            raise RuntimeError(error_msg) from e

    def get_template(self, template_name: str, *, no_cache: bool = False) -> str:
        """Get a specific template, using cache when possible."""
        cache_path = get_template_cache_path(template_name)

        # Try cache first (unless no_cache is specified)
        if not no_cache and cache_path.exists():
            try:
                with cache_path.open(encoding="utf-8") as f:
                    return f.read()
            except OSError:
                # Cache read failed, continue to fetch
                pass

        # Fetch from GitHub
        url = f"{self.base_url}/{template_name}.gitignore"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            content = response.text

            # Cache the result
            try:
                with cache_path.open("w", encoding="utf-8") as f:
                    f.write(content)
            except OSError:
                # Cache write failed, but we can still return the content
                pass
            else:
                return content

        except requests.RequestException as e:
            # If we have cached content, use it
            if cache_path.exists():
                try:
                    with cache_path.open(encoding="utf-8") as f:
                        return f.read()
                except OSError:
                    pass

            error_msg = f"Failed to fetch template '{template_name}': {e}"
            raise RuntimeError(error_msg) from e

    def get_template_info(self, template_name: str) -> dict | None:
        """Get information about a specific template from the index."""
        try:
            index = self.get_index()
            for template in index["templates"]:
                if template["name"] == f"{template_name}.gitignore":
                    return template
        except RuntimeError:
            pass

        return None

    def list_templates(self) -> list[str]:
        """Get a list of all available template names."""
        try:
            index = self.get_index()
            return [
                template["name"][:-10] for template in index["templates"]
            ]  # Remove .gitignore suffix
        except RuntimeError:
            return []

    def search_templates(self, query: str) -> list[str]:
        """Search for templates matching a query."""
        query_lower = query.lower()
        templates = self.list_templates()

        # Simple substring search
        return [template for template in templates if query_lower in template.lower()]


# Global fetcher instance
_fetcher = GitIgnoreFetcher()


def get_fetcher() -> GitIgnoreFetcher:
    """Get the global fetcher instance."""
    return _fetcher


def set_fetcher(fetcher: GitIgnoreFetcher) -> None:
    """Set the global fetcher instance (mainly for testing)."""
    global _fetcher
    _fetcher = fetcher
