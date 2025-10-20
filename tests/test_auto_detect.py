"""Tests for auto-detect functionality."""

from unittest.mock import patch

import pytest

from gi.util import (
    detect_development_environment,
    detect_operating_system,
    get_auto_detect_templates,
    get_os_specific_templates,
)


class TestDetectOperatingSystem:
    """Test OS detection functionality."""

    def test_detect_windows(self):
        """Test Windows detection."""
        with patch("platform.system", return_value="Windows"):
            result = detect_operating_system()
            assert result == "windows"

    def test_detect_macos(self):
        """Test macOS detection."""
        with patch("platform.system", return_value="Darwin"):
            result = detect_operating_system()
            assert result == "macos"

    def test_detect_linux(self):
        """Test Linux detection."""
        with patch("platform.system", return_value="Linux"):
            result = detect_operating_system()
            assert result == "linux"

    def test_detect_unknown_fallback(self):
        """Test fallback for unknown systems."""
        with patch("platform.system", return_value="Unknown"):
            result = detect_operating_system()
            assert result == "linux"


class TestGetOsSpecificTemplates:
    """Test OS-specific template selection."""

    def test_windows_templates(self):
        """Test Windows template selection."""
        with patch("gi.util.detect_operating_system", return_value="windows"):
            templates = get_os_specific_templates()
            assert "Windows" in templates

    def test_macos_templates(self):
        """Test macOS template selection."""
        with patch("gi.util.detect_operating_system", return_value="macos"):
            templates = get_os_specific_templates()
            assert "macOS" in templates

    def test_linux_templates(self):
        """Test Linux template selection."""
        with patch("gi.util.detect_operating_system", return_value="linux"):
            templates = get_os_specific_templates()
            assert "Linux" in templates


class TestDetectDevelopmentEnvironment:
    """Test development environment detection."""

    def test_detect_python(self):
        """Test Python detection."""
        with patch("sys.executable", "/usr/bin/python"):
            templates = detect_development_environment()
            assert "Python" in templates

    def test_detect_node_success(self):
        """Test Node.js detection when available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            templates = detect_development_environment()
            assert "Node" in templates

    def test_detect_node_failure(self):
        """Test Node.js detection when not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            templates = detect_development_environment()
            assert "Node" not in templates

    def test_detect_git_success(self):
        """Test Git detection when available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            templates = detect_development_environment()
            # Git detection was removed as it's always available when using gi
            assert "Python" in templates

    def test_detect_git_failure(self):
        """Test Git detection when not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            templates = detect_development_environment()
            assert "Global/Git" not in templates

    def test_detect_multiple_tools(self):
        """Test detection of multiple development tools."""
        with (
            patch("subprocess.run") as mock_run,
            patch("sys.executable", "/usr/bin/python"),
        ):
            mock_run.return_value.returncode = 0
            templates = detect_development_environment()
            assert "Python" in templates
            assert "Node" in templates


class TestGetAutoDetectTemplates:
    """Test auto-detect template combination."""

    def test_auto_detect_combines_os_and_dev(self):
        """Test that auto-detect combines OS and development templates."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=["Windows"]),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python", "Node"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "Windows" in templates
            assert "Python" in templates
            assert "Node" in templates

    def test_auto_detect_removes_duplicates(self):
        """Test that auto-detect removes duplicate templates."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=["Python"]),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python", "Node"],
            ),
        ):
            templates = get_auto_detect_templates()
            # Should only have one "Python" entry
            assert templates.count("Python") == 1
            assert "Node" in templates

    def test_auto_detect_preserves_order(self):
        """Test that auto-detect preserves template order."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=["A", "B"]),
            patch(
                "gi.util.detect_development_environment",
                return_value=["C", "D"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert templates == ["A", "B", "C", "D"]

    def test_auto_detect_empty_os_templates(self):
        """Test auto-detect with empty OS templates."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=[]),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert templates == ["Python"]

    def test_auto_detect_empty_dev_templates(self):
        """Test auto-detect with empty development templates."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=["Windows"]),
            patch(
                "gi.util.detect_development_environment",
                return_value=[],
            ),
        ):
            templates = get_auto_detect_templates()
            assert templates == ["Windows"]

    def test_auto_detect_both_empty(self):
        """Test auto-detect with both OS and dev templates empty."""
        with (
            patch("gi.util.get_os_specific_templates", return_value=[]),
            patch(
                "gi.util.detect_development_environment",
                return_value=[],
            ),
        ):
            templates = get_auto_detect_templates()
            assert templates == []


class TestCrossPlatformAutoDetect:
    """Test auto-detect functionality across all supported operating systems."""

    def test_windows_auto_detect(self):
        """Test auto-detect on Windows system."""
        with (
            patch("platform.system", return_value="Windows"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python", "Node"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "Windows" in templates
            assert "Python" in templates
            assert "Node" in templates
            # Windows should be first (OS templates come before dev templates)
            assert templates[0] == "Windows"

    def test_linux_auto_detect(self):
        """Test auto-detect on Linux system."""
        with (
            patch("platform.system", return_value="Linux"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "Linux" in templates
            assert "Python" in templates
            assert templates[0] == "Linux"

    def test_macos_auto_detect(self):
        """Test auto-detect on macOS system."""
        with (
            patch("platform.system", return_value="Darwin"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python", "Node"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "macOS" in templates
            assert "Python" in templates
            assert "Node" in templates
            assert templates[0] == "macOS"

    def test_unknown_os_auto_detect(self):
        """Test auto-detect on unknown system (fallback to Linux)."""
        with (
            patch("platform.system", return_value="Unknown"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "Linux" in templates  # Fallback to Linux
            assert "Python" in templates

    def test_windows_with_no_dev_tools(self):
        """Test Windows auto-detect when no development tools are detected."""
        with (
            patch("platform.system", return_value="Windows"),
            patch(
                "gi.util.detect_development_environment",
                return_value=[],
            ),
        ):
            templates = get_auto_detect_templates()
            assert templates == ["Windows"]

    def test_linux_with_node_detection(self):
        """Test Linux auto-detect with Node.js detection."""
        with (
            patch("platform.system", return_value="Linux"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python", "Node"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "Linux" in templates
            assert "Python" in templates
            assert "Node" in templates
            assert templates == ["Linux", "Python", "Node"]

    def test_macos_with_python_only(self):
        """Test macOS auto-detect with only Python detected."""
        with (
            patch("platform.system", return_value="Darwin"),
            patch(
                "gi.util.detect_development_environment",
                return_value=["Python"],
            ),
        ):
            templates = get_auto_detect_templates()
            assert "macOS" in templates
            assert "Python" in templates
            assert "Node" not in templates
            assert templates == ["macOS", "Python"]

    def test_all_os_templates_are_valid(self):
        """Test that all OS-specific templates are valid template names."""
        from gi.fetch import get_fetcher

        fetcher = get_fetcher()
        os_templates = ["Windows", "Linux", "macOS"]

        for template in os_templates:
            try:
                # Test that the template can be resolved
                resolved = fetcher.resolve_template_path(template)
                assert resolved is not None
                assert resolved != template  # Should be resolved to a different path
            except Exception as e:
                pytest.fail(f"Template '{template}' failed to resolve: {e}")

    def test_os_template_resolution_mapping(self):
        """Test that OS template names resolve to correct repository paths."""
        from gi.fetch import get_fetcher

        fetcher = get_fetcher()

        # Test the expected mappings
        expected_mappings = {
            "Windows": "Global/Windows",
            "Linux": "Global/Linux",
            "macOS": "Global/macOS",
        }

        for template_name, expected_path in expected_mappings.items():
            resolved_path = fetcher.resolve_template_path(template_name)
            assert resolved_path == expected_path, (
                f"Expected {template_name} to resolve to {expected_path}, got {resolved_path}"
            )

    def test_cross_platform_consistency(self):
        """Test that auto-detect behavior is consistent across platforms."""
        # Test that all platforms return at least their OS template
        platforms = [
            ("Windows", "Windows"),
            ("Linux", "Linux"),
            ("Darwin", "macOS"),
        ]

        for platform_name, expected_template in platforms:
            with (
                patch("platform.system", return_value=platform_name),
                patch(
                    "gi.util.detect_development_environment",
                    return_value=[],
                ),
            ):
                templates = get_auto_detect_templates()
                assert expected_template in templates
                assert templates[0] == expected_template  # OS template should be first
