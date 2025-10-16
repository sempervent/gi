"""Entry point for gi when run as a module."""

from .cli import app

def main() -> None:
    """Main entry point for the gi CLI."""
    app()

if __name__ == "__main__":
    main()
