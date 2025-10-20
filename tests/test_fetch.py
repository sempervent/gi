"""Tests for the fetch module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import responses

from gi.fetch import GitIgnoreFetcher, get_fetcher, set_fetcher


class TestGitIgnoreFetcher:
    """Test the GitIgnoreFetcher class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fetcher = GitIgnoreFetcher("https://example.com")

    def test_init(self):
        """Test fetcher initialization."""
        assert self.fetcher.base_url == "https://example.com"
        assert (
            self.fetcher.api_base
            == "https://api.github.com/repos/github/gitignore/contents"
        )

    @responses.activate
    def test_get_template_success(self):
        """Test successful template fetching."""
        template_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
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
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#   Usually these files are written by a python script from a template
#   before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
# Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
# uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
# pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#   JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#   be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#   and can be added to the global gitignore or merged into this file.  For a more nuclear
#   option (not recommended) you can uncomment the following to ignore the entire idea folder.
# .idea/

# Abstra
#   Abstra is an AI-powered process automation framework.
#   Ignore directories containing user credentials, local state, and settings.
#   Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#   Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#   that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#   and can be added to the global gitignore or merged into this file. However, if you prefer, 
#   you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml"""
        responses.add(
            responses.GET,
            "https://example.com/Python.gitignore",
            body=template_content,
            status=200,
        )

        result = self.fetcher.get_template("Python")
        assert result == template_content

    @responses.activate
    def test_get_template_not_found(self):
        """Test template not found."""
        responses.add(
            responses.GET,
            "https://example.com/Nonexistent.gitignore",
            status=404,
        )

        with pytest.raises(RuntimeError, match="Failed to fetch template"):
            self.fetcher.get_template("Nonexistent")

    @responses.activate
    def test_get_template_with_cache(self):
        """Test template fetching with cache."""
        template_content = "*.py\n__pycache__/\n"
        responses.add(
            responses.GET,
            "https://example.com/Python.gitignore",
            body=template_content,
            status=200,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "Python.gitignore"

            with patch("gi.fetch.get_template_cache_path") as mock_cache_path:
                mock_cache_path.return_value = cache_path

                # First fetch should hit the network
                result1 = self.fetcher.get_template("Python")
                assert result1 == template_content

                # Second fetch should use cache (no additional network request)
                result2 = self.fetcher.get_template("Python")
                assert result2 == template_content

                # Should only have made one network request
                assert len(responses.calls) == 1

    @responses.activate
    def test_get_template_no_cache(self):
        """Test template fetching with no_cache=True."""
        template_content = "*.py\n__pycache__/\n"
        responses.add(
            responses.GET,
            "https://example.com/Python.gitignore",
            body=template_content,
            status=200,
        )

        # First fetch
        result1 = self.fetcher.get_template("Python", no_cache=True)
        assert result1 == template_content

        # Second fetch with no_cache should hit network again
        result2 = self.fetcher.get_template("Python", no_cache=True)
        assert result2 == template_content

        # Should have made two network requests
        expected_calls = 2
        assert len(responses.calls) == expected_calls

    @responses.activate
    def test_get_index_success(self):
        """Test successful index fetching."""
        # Mock GitHub API response
        api_response = [
            {
                "name": "Python.gitignore",
                "path": "Python.gitignore",
                "type": "file",
                "download_url": "https://raw.githubusercontent.com/github/gitignore/HEAD/Python.gitignore",
                "size": 1234,
            },
            {
                "name": "Global",
                "path": "Global",
                "type": "dir",
                "url": "https://api.github.com/repos/github/gitignore/contents/Global",
            },
        ]

        global_response = [
            {
                "name": "JetBrains.gitignore",
                "path": "Global/JetBrains.gitignore",
                "type": "file",
                "download_url": "https://raw.githubusercontent.com/github/gitignore/HEAD/Global/JetBrains.gitignore",
                "size": 567,
            },
        ]

        responses.add(
            responses.GET,
            "https://api.github.com/repos/github/gitignore/contents",
            json=api_response,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://api.github.com/repos/github/gitignore/contents/Global",
            json=global_response,
            status=200,
        )

        result = self.fetcher.get_index()

        assert "fetched_at" in result
        assert "source" in result
        assert "templates" in result
        min_templates = 2
        assert len(result["templates"]) >= min_templates

        # Check template names
        template_names = [t["name"] for t in result["templates"]]
        assert "Python.gitignore" in template_names
        assert "JetBrains.gitignore" in template_names

    @responses.activate
    def test_get_index_network_error_with_cache(self):
        """Test index fetching with network error but cached data available."""
        # First, create some cached data
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            index_path = cache_dir / "index.json"

            cached_data = {
                "fetched_at": "2023-01-01T00:00:00Z",
                "source": "https://api.github.com/repos/github/gitignore/contents/",
                "templates": [
                    {
                        "name": "Python.gitignore",
                        "path": "Python.gitignore",
                        "download_url": "https://raw.githubusercontent.com/github/gitignore/HEAD/Python.gitignore",
                        "size": 1234,
                    },
                ],
            }

            with index_path.open("w") as f:
                json.dump(cached_data, f)

            # Mock the cache directory
            with patch("gi.fetch.get_index_cache_path", return_value=index_path):
                # Mock network failure
                responses.add(
                    responses.GET,
                    "https://api.github.com/repos/github/gitignore/contents/",
                    status=500,
                )

                # Should return cached data despite network error
                result = self.fetcher.get_index()
                assert result == cached_data

    def test_list_templates(self):
        """Test listing templates."""
        # Mock the get_index method
        mock_index = {
            "templates": [
                {"name": "Python.gitignore"},
                {"name": "Rust.gitignore"},
                {"name": "Global/JetBrains.gitignore"},
            ],
        }

        with patch.object(self.fetcher, "get_index", return_value=mock_index):
            templates = self.fetcher.list_templates()
            assert templates == ["Python", "Rust", "Global/JetBrains"]

    def test_search_templates(self):
        """Test searching templates."""
        # Mock the list_templates method
        with patch.object(
            self.fetcher,
            "list_templates",
            return_value=["Python", "Rust", "Global/JetBrains"],
        ):
            # Search for "python" (case insensitive)
            matches = self.fetcher.search_templates("python")
            assert matches == ["Python"]

            # Search for "global" (case insensitive)
            matches = self.fetcher.search_templates("global")
            assert matches == ["Global/JetBrains"]

            # Search for "jetbrains" (case insensitive)
            matches = self.fetcher.search_templates("jetbrains")
            assert matches == ["Global/JetBrains"]

    def test_get_template_info(self):
        """Test getting template info."""
        # Mock the get_index method
        mock_index = {
            "templates": [
                {
                    "name": "Python.gitignore",
                    "path": "Python.gitignore",
                    "download_url": "https://raw.githubusercontent.com/github/gitignore/HEAD/Python.gitignore",
                    "size": 1234,
                },
            ],
        }

        with patch.object(self.fetcher, "get_index", return_value=mock_index):
            info = self.fetcher.get_template_info("Python")
            assert info is not None
            assert info["name"] == "Python.gitignore"
            expected_size = 1234
            assert info["size"] == expected_size

            # Test non-existent template
            info = self.fetcher.get_template_info("Nonexistent")
            assert info is None


class TestGlobalFetcher:
    """Test the global fetcher functionality."""

    def test_get_fetcher(self):
        """Test getting the global fetcher."""
        fetcher = get_fetcher()
        assert isinstance(fetcher, GitIgnoreFetcher)

    def test_set_fetcher(self):
        """Test setting the global fetcher."""
        original_fetcher = get_fetcher()
        new_fetcher = GitIgnoreFetcher("https://example.com")

        try:
            set_fetcher(new_fetcher)
            assert get_fetcher() is new_fetcher
        finally:
            set_fetcher(original_fetcher)
