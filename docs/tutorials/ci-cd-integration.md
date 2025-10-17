# CI/CD Integration

Learn how to integrate `gi` into your continuous integration and deployment pipelines.

## GitHub Actions

### Basic Integration

Create a workflow that automatically updates `.gitignore` files:

```yaml
# .github/workflows/update-gitignore.yml
name: Update .gitignore

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  update-gitignore:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install gi
      run: |
        pip install gi
    
    - name: Update .gitignore
      run: |
        gi python node --force
    
    - name: Check for changes
      id: verify-changed-files
      run: |
        if [ -n "$(git status --porcelain)" ]; then
          echo "changed=true" >> $GITHUB_OUTPUT
        else
          echo "changed=false" >> $GITHUB_OUTPUT
        fi
    
    - name: Commit changes
      if: steps.verify-changed-files.outputs.changed == 'true'
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .gitignore
        git commit -m "Update .gitignore with latest templates"
        git push
```

### Multi-Project Workflow

For repositories with multiple projects:

```yaml
# .github/workflows/update-gitignores.yml
name: Update .gitignore files

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  update-gitignores:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        project:
          - { name: "frontend", templates: "node react" }
          - { name: "backend", templates: "python django" }
          - { name: "mobile", templates: "react-native" }
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install gi
      run: pip install gi
    
    - name: Update ${{ matrix.project.name }} .gitignore
      run: |
        cd ${{ matrix.project.name }}
        gi ${{ matrix.project.templates }} --force
    
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --staged --quiet || git commit -m "Update ${{ matrix.project.name }} .gitignore"
        git push
```

### Template Validation

Validate `.gitignore` files in CI:

```yaml
# .github/workflows/validate-gitignore.yml
name: Validate .gitignore

on:
  pull_request:
    paths:
      - '.gitignore'
      - '**/.gitignore'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install gi
      run: pip install gi
    
    - name: Validate .gitignore syntax
      run: |
        # Check if .gitignore files are valid
        find . -name ".gitignore" -exec git check-ignore -v {} \; || true
        
        # Test with gi doctor
        gi doctor
    
    - name: Check for outdated templates
      run: |
        # List available templates
        gi list > available_templates.txt
        
        # Check if current .gitignore uses outdated patterns
        if [ -f .gitignore ]; then
          echo "Current .gitignore patterns:"
          grep -v "^#" .gitignore | grep -v "^$" || true
        fi
```

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - update-gitignore
  - test

update-gitignore:
  stage: update-gitignore
  image: python:3.11
  script:
    - pip install gi
    - gi python node --force
    - |
      if [ -n "$(git status --porcelain)" ]; then
        git config user.email "ci@gitlab.com"
        git config user.name "GitLab CI"
        git add .gitignore
        git commit -m "Update .gitignore"
        git push origin $CI_COMMIT_REF_NAME
      fi
  only:
    - main
    - develop
```

### Multi-Stage Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - setup
  - update-gitignore
  - validate
  - test

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - ~/.cache/gi/

setup:
  stage: setup
  image: python:3.11
  script:
    - pip install gi
  artifacts:
    paths:
      - ~/.cache/gi/

update-gitignore:
  stage: update-gitignore
  image: python:3.11
  dependencies:
    - setup
  script:
    - gi python node --force
  artifacts:
    paths:
      - .gitignore
    expire_in: 1 hour

validate-gitignore:
  stage: validate
  image: python:3.11
  dependencies:
    - update-gitignore
  script:
    - gi doctor
    - git check-ignore -v .gitignore || true

test:
  stage: test
  image: python:3.11
  dependencies:
    - validate-gitignore
  script:
    - python -m pytest tests/
```

## Jenkins

### Pipeline Script

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m pip install gi'
            }
        }
        
        stage('Update .gitignore') {
            steps {
                sh 'gi python node --force'
            }
        }
        
        stage('Validate') {
            steps {
                sh 'gi doctor'
                sh 'git check-ignore -v .gitignore || true'
            }
        }
        
        stage('Commit Changes') {
            when {
                changeset "**/.gitignore"
            }
            steps {
                sh '''
                    if [ -n "$(git status --porcelain)" ]; then
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        git add .gitignore
                        git commit -m "Update .gitignore"
                        git push origin ${GIT_BRANCH#origin/}
                    fi
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

### Multi-Configuration Build

```groovy
// Jenkinsfile
pipeline {
    agent none
    
    stages {
        stage('Update .gitignore for all projects') {
            parallel {
                stage('Frontend') {
                    agent any
                    steps {
                        dir('frontend') {
                            sh 'python3 -m pip install gi'
                            sh 'gi node react --force'
                        }
                    }
                }
                
                stage('Backend') {
                    agent any
                    steps {
                        dir('backend') {
                            sh 'python3 -m pip install gi'
                            sh 'gi python django --force'
                        }
                    }
                }
                
                stage('Mobile') {
                    agent any
                    steps {
                        dir('mobile') {
                            sh 'python3 -m pip install gi'
                            sh 'gi react-native --force'
                        }
                    }
                }
            }
        }
    }
}
```

## Azure DevOps

### YAML Pipeline

```yaml
# azure-pipelines.yml
trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: UpdateGitignore
  displayName: 'Update .gitignore'
  jobs:
  - job: UpdateGitignore
    displayName: 'Update .gitignore files'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
      displayName: 'Use Python 3.11'
    
    - script: |
        pip install gi
      displayName: 'Install gi'
    
    - script: |
        gi python node --force
      displayName: 'Update .gitignore'
    
    - script: |
        if [ -n "$(git status --porcelain)" ]; then
          git config user.email "azure-pipelines@example.com"
          git config user.name "Azure Pipelines"
          git add .gitignore
          git commit -m "Update .gitignore"
          git push origin $(Build.SourceBranchName)
        fi
      displayName: 'Commit changes'
```

## CircleCI

### Configuration

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  update-gitignore:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install gi
          command: pip install gi
      - run:
          name: Update .gitignore
          command: gi python node --force
      - run:
          name: Commit changes
          command: |
            if [ -n "$(git status --porcelain)" ]; then
              git config user.email "circleci@example.com"
              git config user.name "CircleCI"
              git add .gitignore
              git commit -m "Update .gitignore"
              git push origin $CIRCLE_BRANCH
            fi

workflows:
  version: 2
  update-gitignore:
    jobs:
      - update-gitignore:
          filters:
            branches:
              only:
                - main
                - develop
```

## Best Practices

### 1. Cache Management

Cache the `gi` installation and templates:

```yaml
# GitHub Actions example
- name: Cache gi templates
  uses: actions/cache@v3
  with:
    path: ~/.cache/gi
    key: gi-templates-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      gi-templates-
```

### 2. Error Handling

Handle network failures gracefully:

```bash
#!/bin/bash
# update-gitignore.sh

set -e

# Try to update .gitignore with retries
for i in {1..3}; do
    if gi python node --force; then
        echo "Successfully updated .gitignore"
        break
    else
        echo "Attempt $i failed, retrying..."
        sleep 5
    fi
done

# Fallback to cached templates if network fails
if [ $? -ne 0 ]; then
    echo "Network failed, using cached templates"
    GI_OFFLINE=true gi python node --force
fi
```

### 3. Conditional Updates

Only update when necessary:

```yaml
# Only run on specific file changes
on:
  push:
    paths:
      - 'pyproject.toml'
      - 'package.json'
      - 'requirements.txt'
```

### 4. Security

Use secure methods for authentication:

```yaml
# Use GitHub token for authentication
- name: Commit changes
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    git config user.email "action@github.com"
    git config user.name "GitHub Action"
    git add .gitignore
    git commit -m "Update .gitignore"
    git push https://$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git
```

### 5. Notifications

Notify team members of updates:

```yaml
- name: Notify on Slack
  if: steps.verify-changed-files.outputs.changed == 'true'
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: '.gitignore has been updated with latest templates'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Monitoring and Alerting

### Health Checks

Monitor the health of your `.gitignore` files:

```bash
#!/bin/bash
# health-check.sh

# Check if .gitignore exists
if [ ! -f .gitignore ]; then
    echo "ERROR: .gitignore file missing"
    exit 1
fi

# Check if .gitignore is not empty
if [ ! -s .gitignore ]; then
    echo "ERROR: .gitignore file is empty"
    exit 1
fi

# Check for common issues
if grep -q "node_modules" .gitignore && [ -d node_modules ]; then
    echo "WARNING: node_modules directory exists but should be ignored"
fi

# Validate with gi doctor
gi doctor
```

### Metrics Collection

Collect metrics about `.gitignore` usage:

```python
#!/usr/bin/env python3
# metrics.py

import json
import subprocess
from datetime import datetime

def collect_gitignore_metrics():
    """Collect metrics about .gitignore files."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "templates_used": [],
        "file_size": 0,
        "line_count": 0
    }
    
    try:
        # Get template information
        result = subprocess.run(['gi', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            metrics["available_templates"] = len(result.stdout.strip().split('\n'))
        
        # Analyze current .gitignore
        with open('.gitignore', 'r') as f:
            content = f.read()
            metrics["file_size"] = len(content)
            metrics["line_count"] = len(content.splitlines())
            
            # Try to identify templates used
            if 'python' in content.lower():
                metrics["templates_used"].append("python")
            if 'node' in content.lower():
                metrics["templates_used"].append("node")
                
    except Exception as e:
        metrics["error"] = str(e)
    
    return metrics

if __name__ == "__main__":
    metrics = collect_gitignore_metrics()
    print(json.dumps(metrics, indent=2))
```

This comprehensive guide covers integrating `gi` into various CI/CD platforms and best practices for automated `.gitignore` management.
