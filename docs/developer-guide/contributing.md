# Contributing

We welcome contributions to `gi`! This guide will help you get started.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Basic familiarity with Python development

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/gi.git
cd gi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check installation
gi --version

# Run tests
python -m pytest tests/ -v
```

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write your code
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_combine.py -v

# Run with coverage
python -m pytest tests/ --cov=gi --cov-report=term-missing
```

### 4. Check Code Quality

```bash
# Format code
ruff format gi/ tests/

# Check linting
ruff check gi/ tests/

# Type checking (if using mypy)
mypy gi/
```

### 5. Commit Changes

```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Submit Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill out the template
4. Submit the PR

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_combine.py::TestCombineTemplates::test_combine_single_template -v

# Run with coverage
python -m pytest tests/ --cov=gi --cov-report=html
```

### Writing Tests

```python
# Example test structure
def test_new_feature():
    """Test description."""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Test Categories

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **CLI Tests**: Test command-line interface
- **Network Tests**: Test HTTP requests (mocked)

## 📚 Documentation

### Code Documentation

```python
def example_function(param1: str, param2: int) -> str:
    """Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### User Documentation

- Update relevant documentation in `docs/`
- Add examples for new features
- Update command reference if needed

## 🎯 Contribution Areas

### 🐛 Bug Fixes

- Fix failing tests
- Resolve issues from GitHub Issues
- Improve error handling
- Fix edge cases

### ✨ New Features

- Add new template aliases
- Improve CLI interface
- Add new commands
- Enhance caching

### 📖 Documentation

- Improve user guides
- Add tutorials
- Update API reference
- Fix typos

### 🧪 Testing

- Add test coverage
- Improve test quality
- Add integration tests
- Performance testing

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement
- [ ] Other (please describe)

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] All existing tests still pass

## Documentation
- [ ] Documentation updated
- [ ] No breaking changes to public API
```

## 🏗️ Building and Testing

### Local Build

```bash
# Build executable locally
python scripts/build.py

# Test built executable
./dist/*/gi --help
```

### CI/CD

Our GitHub Actions will automatically:

- Run tests on multiple Python versions
- Check code quality
- Build executables
- Deploy documentation

## 🐛 Reporting Issues

### Before Reporting

1. Check existing issues
2. Try latest version
3. Reproduce the issue
4. Gather relevant information

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.0]
- gi version: [e.g., 0.1.0]

## Additional Context
Any other relevant information
```

## 💡 Development Tips

### 1. Use Virtual Environment

```bash
# Always use virtual environment
python -m venv .venv
source .venv/bin/activate
```

### 2. Test Frequently

```bash
# Run tests after each change
python -m pytest tests/ -v
```

### 3. Follow Style Guidelines

```bash
# Use ruff for formatting and linting
ruff format gi/ tests/
ruff check gi/ tests/
```

### 4. Write Good Tests

```python
# Test edge cases
def test_edge_case():
    """Test edge case behavior."""
    assert function_under_test("") == expected_result
    assert function_under_test(None) == expected_result
```

### 5. Document Changes

```python
# Update docstrings
def new_function(param: str) -> str:
    """New function description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

## 🎉 Recognition

Contributors will be:

- Listed in the [Credits](about/credits.md) page
- Mentioned in release notes
- Given credit in commit messages

## 📞 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and discussions
- **Code Review**: For feedback on your contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Ready to contribute?** Check out our [Building Guide](building.md) for more technical details!
