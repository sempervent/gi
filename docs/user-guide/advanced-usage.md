# Advanced Usage

Power user features and advanced techniques for `gi`.

## 🚀 Advanced Commands

### Batch Operations

```bash
# Create multiple .gitignore files
for project in frontend backend mobile; do
  gi main python node -o $project/.gitignore
done
```

### Script Integration

```bash
#!/bin/bash
# setup-project.sh

# Create project structure
mkdir -p {frontend,backend,mobile}

# Generate .gitignore files
gi main node react typescript -o frontend/.gitignore
gi main python django -o backend/.gitignore
gi main flutter android ios -o mobile/.gitignore

echo "Project structure created with .gitignore files"
```

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
name: Update .gitignore
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  update-gitignore:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup gi
        run: pip install gi
      - name: Update .gitignore
        run: gi main python node react -o .gitignore
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .gitignore
          git commit -m "Update .gitignore" || exit 0
          git push
```

### GitLab CI

```yaml
update-gitignore:
  script:
    - pip install gi
    - gi main python node react -o .gitignore
    - git add .gitignore
    - git commit -m "Update .gitignore" || true
    - git push
  only:
    - schedules
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    triggers {
        cron('0 0 * * 0')  // Weekly
    }
    stages {
        stage('Update .gitignore') {
            steps {
                sh 'pip install gi'
                sh 'gi main python node react -o .gitignore'
                sh 'git add .gitignore'
                sh 'git commit -m "Update .gitignore" || true'
                sh 'git push'
            }
        }
    }
}
```

## 🎯 Template Management

### Custom Template Sources

```bash
# Use custom repository
export GI_SOURCE_URL="your-org/custom-gitignore"

# Use specific branch
export GI_SOURCE_BRANCH="custom-branch"
```

### Template Validation

```bash
# Check template content
gi show Python | head -20

# Validate template syntax
gi show Python | grep -E "^\s*[^#\s]" | head -10
```

### Template Comparison

```bash
# Compare templates
diff <(gi show Python) <(gi show Django)
```

## 🔍 Advanced Search

### Complex Queries

```bash
# Search with multiple terms
gi search python | grep -i django
gi search node | grep -i react

# Search by category
gi list --category "Language/Framework" | grep -i python
```

### Template Analysis

```bash
# Count rules in template
gi show Python | grep -c "^[^#]"

# Find common patterns
gi show Python | grep -E "\.(py|pyc|pyo)$"
```

## 🎨 Custom Workflows

### Project Templates

```bash
#!/bin/bash
# create-web-project.sh

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

# Create project structure
mkdir -p $PROJECT_NAME/{frontend,backend}
cd $PROJECT_NAME

# Generate .gitignore files
gi main node react typescript vscode -o frontend/.gitignore
gi main python django vscode -o backend/.gitignore
gi main docker kubernetes -o .gitignore

echo "Web project '$PROJECT_NAME' created with .gitignore files"
```

### Team Standards

```bash
#!/bin/bash
# setup-team-standards.sh

# Create team .gitignore standards
gi main python django vscode docker -o team-standards/python-django.gitignore
gi main node react typescript vscode docker -o team-standards/node-react.gitignore
gi main flutter android ios vscode -o team-standards/flutter-mobile.gitignore

echo "Team standards created in team-standards/"
```

## 🔧 Performance Optimization

### Cache Management

```bash
# Pre-populate cache
gi list > /dev/null  # Downloads all templates

# Check cache size
du -sh ~/.cache/gi  # Linux/macOS
dir %LOCALAPPDATA%\gi\cache  # Windows

# Clean old cache
find ~/.cache/gi -type f -mtime +30 -delete  # Linux/macOS
```

### Network Optimization

```bash
# Use local repository
export GI_SOURCE_URL="file:///path/to/local/gitignore-repo"

# Use custom CDN
export GI_SOURCE_URL="https://cdn.example.com/gitignore"
```

## 🎯 Advanced Aliases

### Custom Alias Script

```bash
#!/bin/bash
# gi-aliases.sh

# Define custom aliases
alias gi-web="gi main node react typescript vscode"
alias gi-python="gi main python django vscode"
alias gi-mobile="gi main flutter android ios"

# Use aliases
gi-web -o frontend/.gitignore
gi-python -o backend/.gitignore
gi-mobile -o mobile/.gitignore
```

### Team Aliases

```bash
# ~/.bashrc or ~/.zshrc
alias gi-team-python="gi main python django vscode docker"
alias gi-team-node="gi main node react typescript vscode docker"
alias gi-team-mobile="gi main flutter android ios vscode"
```

## 🔍 Debugging and Troubleshooting

### Verbose Mode

```bash
# Enable verbose output
export GI_VERBOSE="true"
gi main python

# Debug specific command
gi main python --verbose
```

### Network Debugging

```bash
# Test network connectivity
curl -I https://api.github.com/repos/github/gitignore/contents

# Check specific template
curl -s https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore | head -10
```

### Cache Debugging

```bash
# Check cache contents
ls -la ~/.cache/gi  # Linux/macOS
dir %LOCALAPPDATA%\gi\cache  # Windows

# Clear cache
rm -rf ~/.cache/gi  # Linux/macOS
rmdir /s %LOCALAPPDATA%\gi\cache  # Windows
```

## 🎨 Integration Examples

### VS Code Tasks

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Update .gitignore",
            "type": "shell",
            "command": "gi",
            "args": ["main", "python", "node", "react", "-o", ".gitignore"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

### Makefile Integration

```makefile
.PHONY: update-gitignore
update-gitignore:
	gi main python node react -o .gitignore
	git add .gitignore
	git commit -m "Update .gitignore" || true

.PHONY: setup-project
setup-project: update-gitignore
	@echo "Project setup complete"
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install gi
RUN pip install gi

# Copy setup script
COPY setup-gitignore.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/setup-gitignore.sh

# Use in container
RUN setup-gitignore.sh
```

## 🚀 Pro Tips

### 1. Use Scripts for Common Patterns

```bash
#!/bin/bash
# gi-patterns.sh

case $1 in
    "web")
        gi main node react typescript vscode
        ;;
    "python")
        gi main python django vscode
        ;;
    "mobile")
        gi main flutter android ios vscode
        ;;
    *)
        echo "Usage: $0 {web|python|mobile}"
        ;;
esac
```

### 2. Automate with Git Hooks

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Update .gitignore if templates changed
if [ -f .gitignore-templates ]; then
    gi main $(cat .gitignore-templates) -o .gitignore
    git add .gitignore
fi
```

### 3. Use Environment-Specific Configs

```bash
# Development
export GI_CACHE_TTL="3600"  # 1 hour

# Production
export GI_CACHE_TTL="86400"  # 24 hours
```

### 4. Monitor Template Changes

```bash
#!/bin/bash
# monitor-templates.sh

# Check for template updates
gi main python --update-index

# Compare with previous version
if [ -f .gitignore.backup ]; then
    diff .gitignore.backup .gitignore
fi

# Backup current version
cp .gitignore .gitignore.backup
```

## 📚 Best Practices

### 1. Version Control

```bash
# Track template sources
echo "python node react" > .gitignore-templates
git add .gitignore-templates
git commit -m "Add .gitignore template sources"
```

### 2. Team Collaboration

```bash
# Share template preferences
cat > team-gitignore-sources << EOF
python
django
vscode
docker
EOF
```

### 3. Documentation

```bash
# Document .gitignore generation
cat > README-gitignore.md << EOF
# .gitignore Generation

This .gitignore file is generated using:

\`\`\`bash
gi main python django vscode docker
\`\`\`

To regenerate:

\`\`\`bash
gi main python django vscode docker -o .gitignore
\`\`\`
EOF
```

---

**Next:** [Best Practices](tutorials/best-practices.md) for professional workflows!
