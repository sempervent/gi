# PyPI Publishing Guide

This guide explains how to publish the `gi` package to PyPI using GitHub Actions.

## Overview

The `gi` package is automatically published to PyPI when:
1. A new GitHub release is created
2. The workflow is manually triggered

## Setup Instructions

### 1. Create PyPI Account

1. Go to [PyPI](https://pypi.org) and create an account
2. Verify your email address

### 2. Configure Trusted Publishing (Recommended)

Trusted publishing is more secure than API tokens and is the recommended approach.

#### Step 1: Create PyPI Project
1. Go to [PyPI](https://pypi.org) and create a new project named `python-gitignore`
2. Note: The project name must match the name in `pyproject.toml`

#### Step 2: Configure Trusted Publishing
1. In your PyPI project settings, go to "Publishing" → "Trusted publishers"
2. Click "Add a new pending publisher"
3. Configure the publisher:
   - **PyPI project name**: `python-gitignore`
   - **Owner**: `sempervent` (your GitHub username/organization)
   - **Repository name**: `gi`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`
   - **Environment URL**: Leave empty
4. Click "Add pending publisher"
5. The publisher will be pending until the first successful run

### 3. Alternative: API Token Method

If you prefer to use API tokens instead of trusted publishing:

#### Step 1: Create API Token
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Go to "API tokens" section
3. Click "Add API token"
4. Choose "Entire account (all projects)" or "Specific project"
5. Copy the token (it starts with `pypi-`)

#### Step 2: Add Secret to GitHub
1. Go to your GitHub repository
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token

#### Step 3: Update Workflow
If using API tokens, uncomment the environment variables in the workflow:

```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    # ... rest of the command
```

## Publishing Process

### Automatic Publishing (Recommended)

1. **Create a GitHub Release:**
   ```bash
   # The workflow will automatically trigger
   git tag v1.0.0
   git push origin v1.0.0
   
   # Then create a release on GitHub with the same tag
   ```

2. **The workflow will:**
   - Build the package using `python -m build`
   - Upload to PyPI using `twine`
   - Verify the publication

### Manual Publishing

1. Go to your GitHub repository
2. Go to Actions → "Publish to PyPI"
3. Click "Run workflow"
4. Enter the version number
5. Click "Run workflow"

## Verification

After publishing, you can verify the package is available:

1. **Check PyPI**: https://pypi.org/project/python-gitignore/
2. **Install the package**: `pip install python-gitignore`
3. **Test the CLI**: `gi --help`

## Troubleshooting

### Common Issues

1. **"Package already exists"**
   - Make sure the version number in `pyproject.toml` is unique
   - Check if the version was already published

2. **"Authentication failed"**
   - Verify the PyPI API token is correct
   - Check that the token has the right permissions

3. **"Trusted publishing failed"**
   - Ensure the workflow file name matches exactly
   - Check that the environment name is `pypi`
   - Verify the repository name and owner are correct

### Debug Steps

1. **Check workflow logs** in GitHub Actions
2. **Verify package metadata** in `pyproject.toml`
3. **Test locally**:
   ```bash
   python -m build
   python -m twine check dist/*
   ```

## Security Best Practices

1. **Use trusted publishing** instead of API tokens when possible
2. **Never commit API tokens** to the repository
3. **Use environment-specific secrets** for different PyPI accounts
4. **Regularly rotate API tokens** if using token-based authentication

## Package Information

- **Package name**: `python-gitignore`
- **PyPI URL**: https://pypi.org/project/python-gitignore/
- **Installation**: `pip install python-gitignore`
- **CLI command**: `gi`

## Release Checklist

Before publishing a new version:

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `gi/__init__.py`
- [ ] Run tests: `python -m pytest`
- [ ] Run linting: `uv run ruff check`
- [ ] Test build locally: `python -m build`
- [ ] Create GitHub release with proper tag
- [ ] Verify publication on PyPI
- [ ] Test installation: `pip install python-gitignore`
