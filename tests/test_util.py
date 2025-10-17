"""Tests for the util module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from gi.util import (
    ensure_trailing_newline,
    get_cache_dir,
    get_index_cache_path,
    get_template_cache_path,
    is_stale_cache,
    normalize_line_endings,
    read_existing_gitignore,
    safe_write_file,
)


class TestGetCacheDir:
    """Test cache directory functionality."""

    def test_get_cache_dir_windows(self):
        """Test cache directory on Windows."""
        with (
            patch("platform.system", return_value="Windows"),
            patch("platformdirs.user_cache_dir", return_value="/mock/cache/gi") as mock_cache_dir,
            patch("pathlib.Path.mkdir"),
        ):
            cache_dir = get_cache_dir()
            assert cache_dir == Path("/mock/cache/gi")
            mock_cache_dir.assert_called_once_with("gi", "gi")

    def test_get_cache_dir_posix(self):
        """Test cache directory on POSIX systems."""
        with (
            patch("platform.system", return_value="Linux"),
            patch("platformdirs.user_cache_dir", return_value="/home/user/.cache/gi") as mock_cache_dir,
            patch("pathlib.Path.mkdir"),
        ):
            cache_dir = get_cache_dir()
            assert cache_dir == Path("/home/user/.cache/gi")
            mock_cache_dir.assert_called_once_with("gi")

    def test_get_cache_dir_creates_directory(self):
        """Test that cache directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "test_cache"

            with patch(
                "gi.util.platformdirs.user_cache_dir", return_value=str(cache_path),
            ):
                cache_dir = get_cache_dir()
                assert cache_dir.exists()
                assert cache_dir.is_dir()


class TestCachePaths:
    """Test cache path generation."""

    def test_get_index_cache_path(self):
        """Test getting index cache path."""
        with patch("gi.util.get_cache_dir", return_value=Path("/mock/cache")):
            path = get_index_cache_path()
            assert path == Path("/mock/cache/index.json")

    def test_get_template_cache_path(self):
        """Test getting template cache path."""
        with patch("gi.util.get_cache_dir", return_value=Path("/mock/cache")):
            path = get_template_cache_path("Python")
            assert path == Path("/mock/cache/Python.gitignore")


class TestNormalizeLineEndings:
    """Test line ending normalization."""

    def test_normalize_unix(self):
        """Test Unix line endings (no change)."""
        text = "line1\nline2\nline3"
        result = normalize_line_endings(text)
        assert result == text

    def test_normalize_windows(self):
        """Test Windows line endings."""
        text = "line1\r\nline2\r\nline3"
        result = normalize_line_endings(text)
        assert result == "line1\nline2\nline3"

    def test_normalize_mixed(self):
        """Test mixed line endings."""
        text = "line1\r\nline2\nline3\r"
        result = normalize_line_endings(text)
        assert result == "line1\nline2\nline3\n"

    def test_normalize_empty(self):
        """Test empty string."""
        result = normalize_line_endings("")
        assert result == ""


class TestEnsureTrailingNewline:
    """Test trailing newline functionality."""

    def test_ensure_trailing_newline_with_newline(self):
        """Test text that already has trailing newline."""
        text = "line1\nline2\n"
        result = ensure_trailing_newline(text)
        assert result == text

    def test_ensure_trailing_newline_without_newline(self):
        """Test text without trailing newline."""
        text = "line1\nline2"
        result = ensure_trailing_newline(text)
        assert result == "line1\nline2\n"

    def test_ensure_trailing_newline_empty(self):
        """Test empty string."""
        result = ensure_trailing_newline("")
        assert result == ""

    def test_ensure_trailing_newline_multiple_newlines(self):
        """Test text with multiple trailing newlines."""
        text = "line1\nline2\n\n\n"
        result = ensure_trailing_newline(text)
        assert result == "line1\nline2\n"


class TestIsStaleCache:
    """Test cache staleness checking."""

    def test_is_stale_cache_nonexistent(self):
        """Test non-existent cache file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "nonexistent.json"
            assert is_stale_cache(cache_path) is True

    def test_is_stale_cache_fresh(self):
        """Test fresh cache file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "fresh.json"
            cache_path.write_text("{}")

            # File was just created, so it should not be stale
            assert is_stale_cache(cache_path, max_age_hours=24) is False

    def test_is_stale_cache_old(self):
        """Test old cache file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "old.json"
            cache_path.write_text("{}")

            # Mock the file to be old
            with patch("pathlib.Path.stat") as mock_stat:
                import time  # noqa: PLC0415

                old_time = time.time() - (25 * 3600)  # 25 hours ago
                mock_stat.return_value.st_mtime = old_time

                assert is_stale_cache(cache_path, max_age_hours=24) is True


class TestSafeWriteFile:
    """Test safe file writing functionality."""

    def test_safe_write_file_new_file(self):
        """Test writing to a new file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            content = "test content"

            result = safe_write_file(file_path, content)
            assert result is True
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_safe_write_file_existing_file_no_force(self):
        """Test writing to existing file without force."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            file_path.write_text("original content")

            result = safe_write_file(file_path, "new content", force=False)
            assert result is False
            assert file_path.read_text() == "original content"

    def test_safe_write_file_existing_file_with_force(self):
        """Test writing to existing file with force."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            file_path.write_text("original content")

            result = safe_write_file(file_path, "new content", force=True)
            assert result is True
            assert file_path.read_text() == "new content"

    def test_safe_write_file_creates_parent_dirs(self):
        """Test that parent directories are created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "subdir" / "test.txt"
            content = "test content"

            result = safe_write_file(file_path, content)
            assert result is True
            assert file_path.exists()
            assert file_path.read_text() == content


class TestReadExistingGitignore:
    """Test reading existing .gitignore files."""

    def test_read_existing_gitignore_exists(self):
        """Test reading existing .gitignore file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / ".gitignore"
            content = "*.py\n__pycache__/\n"
            file_path.write_text(content)

            result = read_existing_gitignore(file_path)
            assert result == content

    def test_read_existing_gitignore_nonexistent(self):
        """Test reading non-existent .gitignore file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "nonexistent.gitignore"

            result = read_existing_gitignore(file_path)
            assert result is None

    def test_read_existing_gitignore_encoding_error(self):
        """Test reading file with encoding error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / ".gitignore"
            # Write binary data that can't be decoded as UTF-8
            file_path.write_bytes(b"\xff\xfe\x00\x00")

            result = read_existing_gitignore(file_path)
            assert result is None
