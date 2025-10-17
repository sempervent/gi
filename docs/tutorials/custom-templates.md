# Custom Templates

Learn how to create and use custom `.gitignore` templates with `gi`.

## Creating Custom Templates

### Local Template Files

You can create local template files that `gi` can use alongside the official templates.

#### Template File Structure

Create a template file with the following structure:

```bash
# CustomTemplate.gitignore
# Description: My custom template for XYZ projects

# Custom ignore patterns
*.custom
build/
dist/
.env.local
```

#### Template Directory

Store custom templates in a dedicated directory:

```bash
mkdir -p ~/.config/gi/templates
cp MyTemplate.gitignore ~/.config/gi/templates/
```

### Template Metadata

Add metadata to your custom templates:

```bash
# MyTemplate.gitignore
# Name: MyTemplate
# Description: Custom template for my specific project type
# Author: Your Name
# Version: 1.0.0

# Template content
*.log
temp/
```

## Using Custom Templates

### Local Template Usage

Reference custom templates by their filename (without `.gitignore`):

```bash
# Use a custom template
gi MyTemplate

# Combine with official templates
gi python MyTemplate
```

### Template Aliases

Create aliases for your custom templates in the configuration:

```toml
# ~/.config/gi/config.toml

[aliases]
mytemplate = "MyTemplate"
custom = "MyTemplate"
```

Then use the aliases:

```bash
gi mytemplate
gi python custom
```

## Template Best Practices

### Naming Conventions

- Use descriptive names: `Django-WebApp`, `React-Native-Mobile`
- Avoid generic names: `Custom`, `MyTemplate`
- Use consistent casing: `PascalCase` or `kebab-case`

### Content Guidelines

#### Header Comments

Always include header comments:

```bash
# TemplateName.gitignore
# Description: Brief description of what this template is for
# Use cases: When to use this template
# Author: Your name or organization
```

#### Organized Sections

Organize patterns into logical sections:

```bash
# Build artifacts
build/
dist/
*.o
*.so

# Dependencies
node_modules/
venv/
__pycache__/

# IDE files
.vscode/
.idea/
*.swp

# OS files
.DS_Store
Thumbs.db
```

#### Comments

Add comments for complex patterns:

```bash
# Ignore all files in subdirectories named 'temp'
**/temp/*

# Ignore backup files but keep the original
*~
*.bak
*.backup

# Ignore log files but keep error logs
*.log
!error.log
```

### Testing Templates

Test your templates before sharing:

```bash
# Test the template
gi MyTemplate --dry-run

# Test with existing project
gi MyTemplate -o test.gitignore
git check-ignore -v some-file  # Test if patterns work
```

## Sharing Templates

### GitHub Repository

Create a GitHub repository for your templates:

```bash
# Create repository structure
mkdir my-gitignore-templates
cd my-gitignore-templates

# Add templates
cp ~/.config/gi/templates/*.gitignore .

# Create README
cat > README.md << EOF
# My Custom .gitignore Templates

Collection of custom .gitignore templates for specific use cases.

## Templates

- **MyTemplate**: Description of what this template is for
- **AnotherTemplate**: Another description

## Usage

Download the template file and use it with gi:

\`\`\`bash
gi MyTemplate
\`\`\`
EOF

# Initialize git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/my-gitignore-templates.git
git push -u origin main
```

### Template Registry

Consider submitting popular templates to the official registry:

1. Fork the [github/gitignore](https://github.com/github/gitignore) repository
2. Add your template to the appropriate directory
3. Submit a pull request with:
   - Template file
   - Description
   - Use cases
   - Examples

## Advanced Customization

### Template Inheritance

Create base templates that can be extended:

```bash
# BaseWeb.gitignore
# Base template for web projects

# Common web patterns
*.log
.env
node_modules/
```

```bash
# ReactApp.gitignore
# Extends BaseWeb for React applications

# Include base patterns
# (manually copy or reference)

# React-specific patterns
build/
dist/
.eslintcache
```

### Dynamic Templates

Create templates that adapt based on context:

```bash
#!/bin/bash
# generate-template.sh

# Generate template based on project type
if [ "$1" = "react" ]; then
    cat > .gitignore << EOF
# React Application
node_modules/
build/
dist/
.env.local
EOF
elif [ "$1" = "python" ]; then
    cat > .gitignore << EOF
# Python Application
__pycache__/
*.pyc
venv/
.env
EOF
fi
```

### Template Validation

Create validation scripts for your templates:

```bash
#!/bin/bash
# validate-template.sh

template_file="$1"

if [ ! -f "$template_file" ]; then
    echo "Error: Template file not found"
    exit 1
fi

# Check for required header
if ! grep -q "^# .*\.gitignore$" "$template_file"; then
    echo "Warning: Missing template header"
fi

# Check for description
if ! grep -q "^# Description:" "$template_file"; then
    echo "Warning: Missing description"
fi

# Test with git
if command -v git >/dev/null 2>&1; then
    echo "Testing with git..."
    git check-ignore -v "$template_file" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Template validation passed"
    else
        echo "Template validation failed"
    fi
fi
```

## Integration with gi

### Custom Template Directory

Configure `gi` to use your custom template directory:

```toml
# ~/.config/gi/config.toml

[templates]
custom_dir = "~/.config/gi/templates"
```

### Template Discovery

`gi` will automatically discover templates in the custom directory:

```bash
# List all templates (including custom ones)
gi list

# Search custom templates
gi search mytemplate
```

### Template Priority

Custom templates take precedence over official templates with the same name:

```bash
# If you have a custom "Python.gitignore", it will be used instead of the official one
gi python
```

## Examples

### Web Development Template

```bash
# WebDev.gitignore
# Description: Comprehensive template for web development projects
# Use cases: Full-stack web applications, SPAs, static sites

# Dependencies
node_modules/
bower_components/
vendor/

# Build outputs
build/
dist/
out/
.next/
.nuxt/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output/

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/
```

### Data Science Template

```bash
# DataScience.gitignore
# Description: Template for data science and machine learning projects
# Use cases: Jupyter notebooks, Python data analysis, ML experiments

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# Data files
*.csv
*.tsv
*.json
*.parquet
*.h5
*.hdf5
*.pkl
*.pickle

# Model files
*.model
*.pkl
*.joblib
*.h5
*.pb

# Large datasets (uncomment as needed)
# data/
# datasets/
# raw_data/

# Experiment tracking
mlruns/
.mlflow/

# Weights & Biases
wandb/

# TensorBoard
runs/
logs/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

This comprehensive guide covers creating, using, and sharing custom `.gitignore` templates with `gi`.
