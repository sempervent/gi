# Templates

Complete guide to available `.gitignore` templates and how to use them effectively.

## 📋 Template Categories

`gi` supports 200+ official templates organized into categories:

### 🌐 Languages & Frameworks

#### Web Development
- **JavaScript**: `Node`, `React`, `Vue`, `Angular`, `Express`
- **Python**: `Python`, `Django`, `Flask`, `Jupyter`
- **PHP**: `PHP`, `Laravel`, `Symfony`, `WordPress`
- **Ruby**: `Ruby`, `Rails`, `Jekyll`
- **Go**: `Go`, `Beego`, `Revel`

#### Mobile Development
- **iOS**: `Swift`, `Objective-C`, `Xcode`
- **Android**: `Kotlin`, `Java`, `Android`
- **Cross-platform**: `React Native`, `Flutter`, `Xamarin`

#### Desktop Development
- **C++**: `C++`, `CMake`, `Qt`
- **C#**: `VisualStudio`, `Unity`, `Xamarin`
- **Rust**: `Rust`, `Cargo`
- **Java**: `Java`, `Spring`, `Maven`, `Gradle`

#### Data Science
- **Python**: `Python`, `Jupyter`, `Pandas`, `NumPy`
- **R**: `R`, `RStudio`
- **Julia**: `Julia`
- **MATLAB**: `MATLAB`

### 🛠️ Tools & IDEs

#### Code Editors
- **VS Code**: `Global/VisualStudioCode`
- **JetBrains**: `Global/JetBrains` (IntelliJ, PyCharm, WebStorm, etc.)
- **Vim**: `Global/Vim`
- **Emacs**: `Global/Emacs`
- **Sublime Text**: `Global/SublimeText`

#### Development Tools
- **Docker**: `Docker`, `Kubernetes`
- **Git**: `Global/Git`
- **CI/CD**: `GitHub Actions`, `Jenkins`
- **Testing**: `Jest`, `Pytest`, `Mocha`

### 🖥️ Operating Systems

#### Desktop
- **macOS**: `Global/macOS`
- **Windows**: `Global/Windows`
- **Linux**: `Global/Linux`

#### Mobile
- **iOS**: `iOS`, `Xcode`
- **Android**: `Android`

## 🎯 Popular Template Combinations

### Full-Stack Web Development

```bash
# React + Node.js + TypeScript + VS Code
gi main node react typescript vscode

# Django + Python + VS Code
gi main python django vscode

# Laravel + PHP + VS Code
gi main php laravel vscode
```

### Mobile Development

```bash
# React Native + Node.js
gi main node react-native

# Flutter + Dart
gi main flutter

# Native iOS + Swift
gi main swift xcode
```

### Data Science

```bash
# Python data science stack
gi main python jupyter pandas

# R development
gi main r rstudio

# Jupyter notebooks
gi main python jupyter
```

### Desktop Development

```bash
# C++ development
gi main cpp cmake vscode

# C# development
gi main csharp visualstudio

# Rust development
gi main rust cargo
```

## 🔍 Finding Templates

### Search by Category

```bash
# Web frameworks
gi search react
gi search django
gi search laravel

# Mobile frameworks
gi search flutter
gi search react-native

# IDEs
gi search studio
gi search code
```

### Browse by Category

```bash
# List all templates
gi list

# Filter by category
gi list --category "Language/Framework"
gi list --category "Global"
```

## 📝 Template Content Examples

### Python Template

```gitignore
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
```

### Node.js Template

```gitignore
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
```

### VS Code Template

```gitignore
# Visual Studio Code
.vscode/
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
```

## 🎨 Using Aliases Effectively

### Common Aliases

```bash
# Languages
gi main python node rust go java

# Frameworks
gi main django flask react vue angular

# Tools
gi main vscode jetbrains docker

# Platforms
gi main macos windows linux
```

### Alias Combinations

```bash
# Web development
gi main python django vscode
gi main node react vscode
gi main php laravel vscode

# Mobile development
gi main flutter android
gi main react-native node

# Data science
gi main python jupyter pandas
```

## 🔧 Customizing Templates

### Preview Before Using

```bash
# Check what's in a template
gi show Python
gi show Global/JetBrains
gi show Docker
```

### Combine Strategically

```bash
# Start with base language
gi main python

# Add framework
gi main python django

# Add development tools
gi main python django vscode

# Add deployment tools
gi main python django vscode docker
```

## 📊 Template Statistics

### Most Popular Templates

1. **Python** - Most versatile language
2. **Node** - Web development
3. **Global/VisualStudioCode** - Popular IDE
4. **Global/JetBrains** - Professional IDEs
5. **Docker** - Containerization

### Category Distribution

- **Languages**: 40+ templates
- **Frameworks**: 30+ templates
- **Tools**: 25+ templates
- **Platforms**: 15+ templates
- **Global**: 20+ templates

## 🚀 Advanced Usage

### Template Inheritance

Some templates build on others:

```bash
# Django builds on Python
gi main python django  # Includes Python rules + Django-specific

# React builds on Node
gi main node react     # Includes Node rules + React-specific
```

### Custom Combinations

```bash
# Full-stack with everything
gi main python django node react typescript vscode docker

# Data science with visualization
gi main python jupyter pandas matplotlib seaborn

# Mobile development
gi main flutter android ios
```

## 💡 Best Practices

### 1. Start Simple
```bash
# Start with basic language
gi main python

# Add complexity gradually
gi main python django
gi main python django vscode
```

### 2. Use Aliases
```bash
# Good
gi main python django vscode

# Avoid
gi main Python Django "Global/VisualStudioCode"
```

### 3. Preview First
```bash
# Always check what you're adding
gi show Django
gi show Global/VisualStudioCode
```

### 4. Keep It Relevant
```bash
# Only include what you actually use
gi main python django  # If you use Django
gi main python flask   # If you use Flask
```

## 🔍 Troubleshooting

### Template Not Found

```bash
# Search for similar templates
gi search python
gi search django

# List all templates
gi list
```

### Too Many Rules

```bash
# Start with fewer templates
gi main python  # Instead of python django flask

# Use specific templates
gi main python django  # Instead of python django flask
```

### Missing Rules

```bash
# Check if template exists
gi show Python
gi show Django

# Combine related templates
gi main python django vscode
```

---

**Next:** [Configuration Guide](configuration.md) to customize your `gi` setup!
