"""Tests for the names module."""

from gi.names import (
    ALIASES,
    normalize_template_name,
    parse_template_names,
    resolve_template_names,
)


class TestNormalizeTemplateName:
    """Test template name normalization."""

    def test_remove_gitignore_suffix(self):
        """Test removing .gitignore suffix."""
        assert normalize_template_name("Python.gitignore") == "Python"
        assert normalize_template_name("Rust.gitignore") == "Rust"

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        assert normalize_template_name("python") == "Python"
        assert normalize_template_name("PYTHON") == "Python"
        assert normalize_template_name("Python") == "Python"

    def test_aliases(self):
        """Test alias resolution."""
        assert normalize_template_name("cpp") == "C++"
        assert normalize_template_name("csharp") == "VisualStudio"
        assert normalize_template_name("vscode") == "Global/VisualStudioCode"
        assert normalize_template_name("macos") == "macOS"
        assert normalize_template_name("jetbrains") == "Global/JetBrains"

    def test_underscore_dash_normalization(self):
        """Test underscore and dash normalization."""
        assert normalize_template_name("visual_studio_code") == "Visual Studio Code"
        assert normalize_template_name("visual-studio-code") == "Visual Studio Code"
        assert normalize_template_name("visual_studio-code") == "Visual Studio Code"

    def test_global_paths(self):
        """Test Global/ path handling."""
        assert normalize_template_name("Global/JetBrains") == "Global/Jetbrains"
        assert normalize_template_name("global/jetbrains") == "Global/Jetbrains"
        assert normalize_template_name("GLOBAL/JETBRAINS") == "Global/Jetbrains"

    def test_title_case_conversion(self):
        """Test title case conversion."""
        assert normalize_template_name("python") == "Python"
        assert normalize_template_name("rust") == "Rust"
        assert normalize_template_name("c++") == "C++"
        assert normalize_template_name("csharp") == "VisualStudio"


class TestParseTemplateNames:
    """Test parsing template names from input strings."""

    def test_space_separated(self):
        """Test space-separated names."""
        result = parse_template_names("python rust c++")
        assert result == ["python", "rust", "c++"]

    def test_comma_separated(self):
        """Test comma-separated names."""
        result = parse_template_names("python,rust,c++")
        assert result == ["python", "rust", "c++"]

    def test_mixed_separators(self):
        """Test mixed separators."""
        result = parse_template_names("python, rust c++")
        assert result == ["python", "rust", "c++"]

    def test_extra_whitespace(self):
        """Test handling extra whitespace."""
        result = parse_template_names("  python  ,  rust  ,  c++  ")
        assert result == ["python", "rust", "c++"]

    def test_empty_string(self):
        """Test empty string input."""
        result = parse_template_names("")
        assert result == []

    def test_whitespace_only(self):
        """Test whitespace-only input."""
        result = parse_template_names("   ")
        assert result == []


class TestResolveTemplateNames:
    """Test resolving template names to canonical forms."""

    def test_resolve_simple(self):
        """Test resolving simple names."""
        result = resolve_template_names(["python", "rust"])
        assert result == ["Python", "Rust"]

    def test_resolve_with_aliases(self):
        """Test resolving names with aliases."""
        result = resolve_template_names(["cpp", "csharp", "vscode"])
        assert result == ["C++", "VisualStudio", "Global/VisualStudioCode"]

    def test_resolve_duplicates(self):
        """Test resolving duplicate names."""
        result = resolve_template_names(["python", "Python", "PYTHON"])
        assert result == ["Python"]  # Should deduplicate

    def test_resolve_mixed_case(self):
        """Test resolving mixed case names."""
        result = resolve_template_names(["python", "RUST", "C++"])
        assert result == ["Python", "Rust", "C++"]

    def test_resolve_empty_list(self):
        """Test resolving empty list."""
        result = resolve_template_names([])
        assert result == []


class TestAliases:
    """Test the ALIASES dictionary."""

    def test_aliases_are_strings(self):
        """Test that all aliases are strings."""
        for alias, canonical in ALIASES.items():
            assert isinstance(alias, str)
            assert isinstance(canonical, str)

    def test_aliases_are_not_empty(self):
        """Test that aliases are not empty."""
        for alias, canonical in ALIASES.items():
            assert alias.strip() != ""
            assert canonical.strip() != ""

    def test_common_aliases_exist(self):
        """Test that common aliases exist."""
        assert "cpp" in ALIASES
        assert "csharp" in ALIASES
        assert "vscode" in ALIASES
        assert "macos" in ALIASES
        assert "jetbrains" in ALIASES
        assert "python" in ALIASES
        assert "rust" in ALIASES
        assert "java" in ALIASES
        assert "javascript" in ALIASES
        assert "typescript" in ALIASES

    def test_aliases_are_case_insensitive(self):
        """Test that aliases work case-insensitively."""
        # This is tested indirectly through normalize_template_name
        assert normalize_template_name("CPP") == "C++"
        assert normalize_template_name("CSharp") == "VisualStudio"
        assert normalize_template_name("VSCode") == "Global/VisualStudioCode"
