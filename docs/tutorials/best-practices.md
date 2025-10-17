# Best Practices

Learn the best practices for using `gi` effectively in your projects.

## Template Selection

### Choose the Right Templates

Select templates that match your project's technology stack:

```bash
# Good: Specific to your stack
gi python django postgresql

# Avoid: Too generic
gi python

# Avoid: Irrelevant templates
gi python java csharp  # Unless you're actually using all three
```

### Template Ordering

Order templates by importance and specificity:

```bash
# Good: Most specific first
gi python django postgresql redis

# Good: Framework-specific first, then general
gi react node python

# Avoid: Random ordering
gi python redis django postgresql
```

### Regular Updates

Keep your `.gitignore` files up to date:

```bash
# Check for updates weekly
gi python node --force

# Or set up automated updates in CI/CD
```

## File Organization

### Project Structure

Organize `.gitignore` files appropriately:

```
project/
├── .gitignore              # Main project .gitignore
├── frontend/
│   └── .gitignore          # Frontend-specific patterns
├── backend/
│   └── .gitignore          # Backend-specific patterns
└── docs/
    └── .gitignore          # Documentation-specific patterns
```

### Hierarchical .gitignore

Use multiple `.gitignore` files for complex projects:

```bash
# Root .gitignore
gi python node

# Frontend-specific
cd frontend && gi react webpack

# Backend-specific
cd backend && gi python django postgresql
```

## Performance Optimization

### Caching

Leverage `gi`'s caching for faster operations:

```bash
# First run: downloads templates
gi python node

# Subsequent runs: uses cache
gi python node  # Much faster
```

### Offline Usage

Use cached templates when offline:

```bash
# Force offline mode
GI_OFFLINE=true gi python node
```

### Batch Operations

Combine multiple templates in a single command:

```bash
# Good: Single command
gi python node react postgresql

# Avoid: Multiple commands
gi python
gi node
gi react
gi postgresql
```

## Security Considerations

### Sensitive Files

Always ensure sensitive files are ignored:

```bash
# Add to .gitignore manually after using gi
echo ".env" >> .gitignore
echo "config/secrets.yml" >> .gitignore
echo "*.pem" >> .gitignore
```

### Environment-Specific Patterns

Use environment-specific ignore patterns:

```bash
# Development
echo ".env.development" >> .gitignore

# Production
echo ".env.production" >> .gitignore

# Testing
echo ".env.test" >> .gitignore
```

### API Keys and Secrets

Never commit API keys or secrets:

```bash
# Add to .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore
echo "credentials.json" >> .gitignore
```

## Team Collaboration

### Consistent Templates

Use the same templates across team members:

```bash
# Create a script for team consistency
cat > setup-gitignore.sh << 'EOF'
#!/bin/bash
gi python node react postgresql redis
echo "✅ .gitignore updated for team consistency"
EOF

chmod +x setup-gitignore.sh
```

### Documentation

Document your `.gitignore` choices:

```bash
# Add comments to explain choices
cat >> .gitignore << 'EOF'

# Custom additions for our project
.env.local          # Local environment variables
docs/build/         # Generated documentation
scripts/output/     # Script output files
EOF
```

### Version Control

Track `.gitignore` changes:

```bash
# Commit .gitignore changes
git add .gitignore
git commit -m "Update .gitignore: add Python and Node.js templates"

# Use conventional commits
git commit -m "chore: update .gitignore with latest templates"
```

## Maintenance

### Regular Audits

Periodically audit your `.gitignore` files:

```bash
# Check what's being ignored
git status --ignored

# Verify patterns work
git check-ignore -v some-file

# Use gi doctor for health check
gi doctor
```

### Clean Up

Remove unused patterns:

```bash
# Review current .gitignore
cat .gitignore

# Remove patterns for technologies you no longer use
# Edit .gitignore manually or regenerate
gi python node  # Only current technologies
```

### Template Updates

Stay updated with template changes:

```bash
# Check for template updates
gi list | head -10

# Update to latest templates
gi python node --force
```

## Error Handling

### Graceful Degradation

Handle network failures gracefully:

```bash
#!/bin/bash
# update-gitignore-robust.sh

set -e

# Try online first
if gi python node; then
    echo "✅ Updated .gitignore online"
else
    echo "⚠️  Network failed, trying offline"
    if GI_OFFLINE=true gi python node; then
        echo "✅ Updated .gitignore offline"
    else
        echo "❌ Failed to update .gitignore"
        exit 1
    fi
fi
```

### Validation

Validate `.gitignore` files:

```bash
# Check syntax
git check-ignore -v .gitignore

# Test with sample files
touch test-file.py
git check-ignore test-file.py
rm test-file.py
```

## Automation

### Pre-commit Hooks

Use pre-commit hooks to maintain `.gitignore`:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: update-gitignore
        name: Update .gitignore
        entry: gi python node --force
        language: system
        pass_filenames: false
```

### CI/CD Integration

Automate `.gitignore` updates in CI/CD:

```yaml
# .github/workflows/update-gitignore.yml
name: Update .gitignore
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install gi
      - run: gi python node --force
      - name: Commit changes
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Action"
          git add .gitignore
          git diff --staged --quiet || git commit -m "chore: update .gitignore"
          git push
```

## Troubleshooting

### Common Issues

#### Template Not Found

```bash
# Check available templates
gi list | grep -i python

# Use exact name
gi Python  # Not python
```

#### Network Issues

```bash
# Check network connectivity
gi doctor

# Use offline mode
GI_OFFLINE=true gi python node
```

#### Permission Issues

```bash
# Check file permissions
ls -la .gitignore

# Fix permissions
chmod 644 .gitignore
```

### Debug Mode

Enable debug output for troubleshooting:

```bash
# Enable debug mode
GI_DEBUG=true gi python node

# Verbose output
gi python node --verbose
```

## Performance Tips

### Large Projects

For large projects, consider:

```bash
# Use specific templates only
gi python django  # Not all Python templates

# Exclude unnecessary patterns
gi python --exclude "*.pyc"  # If already handled
```

### CI/CD Optimization

Optimize for CI/CD environments:

```bash
# Cache templates
export GI_CACHE_DIR="/tmp/gi-cache"

# Use shorter timeouts
export GI_TIMEOUT=10

# Batch operations
gi python node react postgresql redis
```

## Examples

### Web Application

```bash
# Full-stack web application
gi python django postgresql redis node react webpack
```

### Mobile Application

```bash
# React Native mobile app
gi react-native node
```

### Data Science Project

```bash
# Data science with Jupyter
gi python jupyter-notebooks
```

### Microservices

```bash
# Each service gets its own .gitignore
# API service
gi python fastapi postgresql

# Frontend service  
gi node react

# Worker service
gi python celery redis
```

### Monorepo

```bash
# Root .gitignore
gi python node

# Package-specific .gitignore files
# packages/frontend/.gitignore
gi react webpack

# packages/backend/.gitignore
gi python django postgresql
```

## Summary

Following these best practices will help you:

- ✅ Choose appropriate templates for your project
- ✅ Maintain consistent `.gitignore` files across your team
- ✅ Optimize performance and reduce network usage
- ✅ Handle errors gracefully
- ✅ Automate maintenance tasks
- ✅ Keep your repository clean and secure

Remember to regularly review and update your `.gitignore` files as your project evolves and new technologies are added.
