# Testing

Learn how to run tests, write new tests, and maintain test coverage for `gi`.

## Running Tests

### Basic Test Execution

Run all tests:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=gi --cov-report=html
```

### Specific Test Categories

Run specific test categories:

```bash
# Run only unit tests
pytest tests/test_*.py

# Run tests for specific module
pytest tests/test_fetch.py

# Run specific test function
pytest tests/test_fetch.py::test_get_template_success
```

### Test Configuration

The test configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## Test Structure

### Test Organization

Tests are organized by module:

```
tests/
├── __init__.py
├── fixtures/
│   ├── Python.gitignore
│   └── Rust.gitignore
├── test_combine.py
├── test_fetch.py
├── test_names.py
└── test_util.py
```

### Test Fixtures

Test fixtures provide sample data:

```python
# tests/fixtures/Python.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
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
*.egg-info/
.installed.cfg
*.egg
```

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Example Test

```python
# tests/test_names.py
import pytest
from gi.names import normalize_template_name

def test_normalize_template_name():
    """Test template name normalization."""
    # Test basic normalization
    assert normalize_template_name("python") == "Python"
    assert normalize_template_name("PYTHON") == "Python"
    
    # Test with .gitignore suffix
    assert normalize_template_name("python.gitignore") == "Python"
    
    # Test aliases
    assert normalize_template_name("csharp") == "VisualStudio"
```

### Mocking External Dependencies

Use `responses` for mocking HTTP requests:

```python
# tests/test_fetch.py
import responses
import pytest
from gi.fetch import TemplateFetcher

@responses.activate
def test_get_template_success():
    """Test successful template fetching."""
    # Mock the HTTP response
    responses.add(
        responses.GET,
        "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore",
        body="# Python template\n__pycache__/\n*.pyc",
        status=200
    )
    
    # Test the function
    fetcher = TemplateFetcher()
    result = fetcher.get_template("Python")
    
    assert result == "# Python template\n__pycache__/\n*.pyc"
```

### Testing CLI Commands

Test CLI commands using `typer.testing`:

```python
# tests/test_cli.py
from typer.testing import CliRunner
from gi.cli import app

def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "gi" in result.output
    assert "help" in result.output

def test_cli_list():
    """Test CLI list command."""
    runner = CliRunner()
    result = runner.invoke(app, ["list"])
    
    assert result.exit_code == 0
    assert "Python" in result.output
```

## Test Coverage

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["gi"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Running Coverage

```bash
# Run tests with coverage
pytest --cov=gi --cov-report=html

# Generate coverage report
coverage html

# View coverage report
open htmlcov/index.html
```

### Coverage Goals

Maintain high test coverage:

- **Overall coverage**: > 90%
- **Critical modules**: > 95%
- **New code**: 100%

## Test Categories

### Unit Tests

Test individual functions and methods:

```python
def test_parse_lines():
    """Test line parsing functionality."""
    content = "line1\nline2\n\nline3"
    result = parse_lines(content)
    
    assert result == ["line1", "line2", "", "line3"]
```

### Integration Tests

Test module interactions:

```python
def test_fetch_and_combine():
    """Test fetching and combining templates."""
    fetcher = TemplateFetcher()
    combiner = TemplateCombiner()
    
    # Fetch templates
    python_template = fetcher.get_template("Python")
    node_template = fetcher.get_template("Node")
    
    # Combine templates
    combined = combiner.combine_templates({
        "Python": python_template,
        "Node": node_template
    })
    
    assert "Python" in combined
    assert "Node" in combined
```

### End-to-End Tests

Test complete workflows:

```python
def test_cli_workflow():
    """Test complete CLI workflow."""
    runner = CliRunner()
    
    # Test list command
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    
    # Test search command
    result = runner.invoke(app, ["search", "python"])
    assert result.exit_code == 0
    
    # Test main command
    result = runner.invoke(app, ["python", "node", "-o", "test.gitignore"])
    assert result.exit_code == 0
    assert Path("test.gitignore").exists()
    
    # Cleanup
    Path("test.gitignore").unlink()
```

## Test Utilities

### Custom Fixtures

Create reusable test fixtures:

```python
# tests/conftest.py
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_gitignore():
    """Provide sample .gitignore content."""
    return "# Python\n__pycache__/\n*.pyc\n\n# Node\nnode_modules/\n"

@pytest.fixture
def mock_fetcher():
    """Provide a mock template fetcher."""
    from unittest.mock import Mock
    fetcher = Mock()
    fetcher.get_template.return_value = "# Mock template\n*.mock"
    return fetcher
```

### Test Helpers

Create helper functions for common test operations:

```python
# tests/helpers.py
def create_test_file(path: Path, content: str) -> None:
    """Create a test file with content."""
    path.write_text(content)

def assert_file_contains(path: Path, content: str) -> None:
    """Assert that a file contains specific content."""
    assert path.exists()
    assert content in path.read_text()

def assert_gitignore_valid(path: Path) -> None:
    """Assert that a .gitignore file is valid."""
    assert path.exists()
    content = path.read_text()
    assert content.strip()  # Not empty
    assert not content.endswith("\n\n")  # No trailing newlines
```

## Continuous Integration

### GitHub Actions

Tests run automatically on GitHub Actions:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest --cov=gi --cov-report=xml
    
    - name: Upload coverage to Codecov
      if: matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Local CI Testing

Test the CI process locally:

```bash
# Install act (GitHub Actions runner)
# https://github.com/nektos/act

# Run the CI workflow
act -j test

# Run with specific Python version
act -j test --matrix python-version:3.11
```

## Test Best Practices

### Naming Conventions

Use descriptive test names:

```python
# Good
def test_normalize_template_name_with_gitignore_suffix():
    """Test that .gitignore suffix is removed from template names."""

# Avoid
def test_normalize():
    """Test normalization."""
```

### Test Isolation

Ensure tests are independent:

```python
def test_function():
    """Test that doesn't depend on other tests."""
    # Use fresh data for each test
    input_data = create_test_data()
    result = function_under_test(input_data)
    assert result is not None
```

### Error Testing

Test error conditions:

```python
def test_invalid_template_name():
    """Test handling of invalid template names."""
    with pytest.raises(ValueError, match="Invalid template name"):
        normalize_template_name("")

def test_network_error():
    """Test handling of network errors."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://api.github.com/repos/github/gitignore/contents/",
            status=500
        )
        
        fetcher = TemplateFetcher()
        with pytest.raises(NetworkError):
            fetcher.get_index()
```

### Performance Testing

Test performance characteristics:

```python
import time

def test_template_fetching_performance():
    """Test that template fetching is reasonably fast."""
    fetcher = TemplateFetcher()
    
    start_time = time.time()
    result = fetcher.get_template("Python")
    end_time = time.time()
    
    assert result is not None
    assert (end_time - start_time) < 5.0  # Should complete within 5 seconds
```

## Debugging Tests

### Verbose Output

Get detailed test output:

```bash
# Verbose output
pytest -v

# Extra verbose
pytest -vv

# Show local variables on failure
pytest -l
```

### Debug Mode

Run tests in debug mode:

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb
```

### Test Discovery

Debug test discovery:

```bash
# Show which tests would be run
pytest --collect-only

# Show test collection errors
pytest --collect-only -v
```

## Maintenance

### Regular Updates

Keep tests up to date:

```bash
# Run tests before committing
pytest

# Run tests with coverage
pytest --cov=gi

# Update test fixtures if needed
# Edit tests/fixtures/*.gitignore
```

### Test Documentation

Document test strategies:

```python
class TestTemplateFetcher:
    """Test suite for TemplateFetcher class."""
    
    def test_get_template_success(self):
        """Test successful template fetching.
        
        This test verifies that:
        1. HTTP requests are made correctly
        2. Response content is returned
        3. Caching works properly
        """
        # Test implementation
```

This comprehensive guide covers all aspects of testing `gi`, from writing tests to maintaining test coverage and debugging test issues.
