#!/bin/bash
# Install script for gi

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install with pipx
install_with_pipx() {
    print_status "Installing gi with pipx..."
    
    if command_exists pipx; then
        pipx install .
        print_success "gi installed successfully with pipx!"
        print_status "You can now use 'gi' from anywhere in your terminal."
    else
        print_error "pipx is not installed. Please install pipx first:"
        echo "  python -m pip install --user pipx"
        echo "  python -m pipx ensurepath"
        return 1
    fi
}

# Function to install with pip
install_with_pip() {
    print_status "Installing gi with pip..."
    
    if command_exists pip; then
        pip install --user .
        print_success "gi installed successfully with pip!"
        print_warning "Make sure ~/.local/bin is in your PATH"
        print_status "You may need to restart your terminal or run:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    else
        print_error "pip is not available. Please install Python and pip first."
        return 1
    fi
}

# Function to install in virtual environment
install_in_venv() {
    print_status "Installing gi in virtual environment..."
    
    if command_exists python3; then
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -e .
        print_success "gi installed in virtual environment!"
        print_status "Activate the environment with:"
        echo "  source .venv/bin/activate"
    else
        print_error "python3 is not available. Please install Python 3.9+ first."
        return 1
    fi
}

# Main installation logic
main() {
    print_status "Installing gi - .gitignore Combiner"
    echo
    
    # Check if we're in the right directory
    if [ ! -f "pyproject.toml" ]; then
        print_error "pyproject.toml not found. Please run this script from the gi project root."
        exit 1
    fi
    
    # Check Python version
    if command_exists python3; then
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [ "$(echo "$python_version < 3.9" | bc -l 2>/dev/null || echo "0")" -eq 1 ]; then
            print_error "Python 3.9+ is required. Found Python $python_version"
            exit 1
        fi
        print_status "Python version: $python_version ✓"
    else
        print_error "Python 3.9+ is required but not found."
        exit 1
    fi
    
    # Try different installation methods
    if command_exists pipx; then
        install_with_pipx
    elif command_exists pip; then
        install_with_pip
    else
        print_warning "Neither pipx nor pip found. Installing in virtual environment..."
        install_in_venv
    fi
    
    echo
    print_success "Installation complete!"
    print_status "Try running: gi --help"
}

# Run main function
main "$@"
