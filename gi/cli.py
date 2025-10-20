"""Command-line interface for gi."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .combine import combine_templates
from .fetch import get_fetcher
from .names import parse_template_names, resolve_template_names
from .util import (
    get_auto_detect_templates,
    get_cache_dir,
    read_existing_gitignore,
    safe_write_file,
)

app = typer.Typer(
    name="gi",
    help="A CLI tool to combine .gitignore templates from github/gitignore",
    no_args_is_help=True,
)
console = Console()


@app.command()
def main(
    templates: str | None = typer.Argument(
        None,
        help="Template names to combine (space or comma separated). If not provided, auto-detect will be used.",
    ),
    output: Path | None = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file path (default: .gitignore in current directory)",
    ),
    append: bool = typer.Option(
        False,
        "-a",
        "--append",
        help="Append to existing .gitignore instead of replacing",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Overwrite existing file without prompting",
    ),
    no_cache: bool = typer.Option(
        False,
        "--no-cache",
        help="Ignore cache for this run",
    ),
    update_index: bool = typer.Option(
        False,
        "--update-index",
        help="Refresh the list of available templates",
    ),
    from_url: str | None = typer.Option(
        None,
        "--from",
        help="Override source repository URL (advanced)",
    ),
    no_auto_detect: bool = typer.Option(
        False,
        "--no-auto-detect",
        help="Disable automatic OS and development environment detection",
    ),
) -> None:
    """Combine .gitignore templates into a single file."""
    # Handle auto-detection if no templates provided
    if not templates and not no_auto_detect:
        console.print("[blue]Auto-detecting templates based on your system...[/blue]")
        auto_detected = get_auto_detect_templates()
        if auto_detected:
            console.print(f"[green]Detected:[/green] {', '.join(auto_detected)}")
            templates = " ".join(auto_detected)
        else:
            console.print(
                "[yellow]No templates could be auto-detected. Please specify templates manually.[/yellow]"
            )
            raise typer.Exit(1)
    elif not templates:
        console.print(
            "[red]Error:[/red] No templates specified and auto-detect is disabled"
        )
        raise typer.Exit(1)

    # Parse template names
    template_names = parse_template_names(templates)
    if not template_names:
        console.print("[red]Error:[/red] No valid template names found")
        raise typer.Exit(1)

    # Resolve template names to canonical forms
    resolved_names = resolve_template_names(template_names)

    # Set up fetcher
    fetcher = get_fetcher()
    if from_url:
        from .fetch import GitIgnoreFetcher

        fetcher = GitIgnoreFetcher(from_url)

    # Update index if requested
    if update_index:
        try:
            console.print("Updating template index...")
            fetcher.get_index(force=True)
            console.print("[green]✓[/green] Template index updated")
        except Exception as e:
            console.print(f"[red]Error updating index:[/red] {e}")
            raise typer.Exit(1) from e

    # Fetch templates
    templates_content = {}
    failed_templates = []

    for template_name in resolved_names:
        try:
            content = fetcher.get_template(template_name, no_cache=no_cache)
            templates_content[template_name] = content
            console.print(f"[green]✓[/green] Fetched {template_name}")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to fetch {template_name}: {e}")
            failed_templates.append(template_name)

    if failed_templates:
        console.print(
            f"\n[yellow]Warning:[/yellow] Failed to fetch {len(failed_templates)} template(s)",
        )
        console.print("Available templates: [bold]gi list[/bold]")
        if not templates_content:
            raise typer.Exit(1)

    # Determine output path
    if output is None:
        output = Path(".gitignore")

    # Read existing content if appending
    existing_content = ""
    if append and output.exists():
        existing_content = read_existing_gitignore(output) or ""

    # Combine templates
    try:
        combined_content = combine_templates(
            templates_content,
            existing_content=existing_content,
            append=append,
            include_header=True,
        )
    except Exception as e:
        console.print(f"[red]Error combining templates:[/red] {e}")
        raise typer.Exit(1) from e

    # Write output file
    if not safe_write_file(output, combined_content, force=force) and output.exists():
        console.print(f"[yellow]File {output} already exists.[/yellow]")
        if not typer.confirm("Overwrite?"):
            console.print("Aborted.")
            raise typer.Exit(1)
    else:
        safe_write_file(output, combined_content, force=True)

    console.print(f"[green]✓[/green] Created {output}")
    console.print(
        f"Combined {len(templates_content)} template(s): {', '.join(templates_content.keys())}",
    )


@app.command(name="list")
def list_templates() -> None:
    """List all available .gitignore templates."""
    fetcher = get_fetcher()

    try:
        templates = fetcher.list_templates()
        if not templates:
            console.print("[yellow]No templates found.[/yellow]")
            console.print(
                "Try running with [bold]--update-index[/bold] to refresh the list.",
            )
            return

        # Group templates by category
        global_templates = []
        regular_templates = []

        for template in sorted(templates):
            if template.startswith("Global/"):
                global_templates.append(template)
            else:
                regular_templates.append(template)

        # Create table
        table = Table(title="Available .gitignore Templates")
        table.add_column("Template Name", style="cyan")
        table.add_column("Category", style="magenta")

        # Add regular templates
        for template in regular_templates:
            table.add_row(template, "Language/Framework")

        # Add global templates
        for template in global_templates:
            table.add_row(template, "Global/Editor")

        console.print(table)
        console.print(f"\nTotal: {len(templates)} templates")

    except Exception as e:
        console.print(f"[red]Error fetching templates:[/red] {e}")
        console.print(
            "Try running with [bold]--update-index[/bold] to refresh the list.",
        )
        raise typer.Exit(1) from e


@app.command(name="search")
def search(
    query: str = typer.Argument(..., help="Search query (case-insensitive)"),
) -> None:
    """Search for .gitignore templates by name."""
    if not query.strip():
        console.print("[red]Error:[/red] Search query cannot be empty")
        raise typer.Exit(1)

    fetcher = get_fetcher()

    try:
        matches = fetcher.search_templates(query)
        if not matches:
            console.print(f"[yellow]No templates found matching '{query}'[/yellow]")
            return

        # Create table
        table = Table(title=f"Templates matching '{query}'")
        table.add_column("Template Name", style="cyan")
        table.add_column("Category", style="magenta")

        for template in sorted(matches):
            category = (
                "Global/Editor"
                if template.startswith("Global/")
                else "Language/Framework"
            )
            table.add_row(template, category)

        console.print(table)
        console.print(f"\nFound {len(matches)} template(s)")

    except Exception as e:
        console.print(f"[red]Error searching templates:[/red] {e}")
        raise typer.Exit(1) from e


@app.command(name="show")
def show(
    template: str = typer.Argument(..., help="Template name to display"),
) -> None:
    """Show the raw content of a .gitignore template."""
    fetcher = get_fetcher()

    try:
        content = fetcher.get_template(template)
        console.print(content, end="")
    except Exception as e:
        console.print(f"[red]Error fetching template '{template}':[/red] {e}")
        console.print("Use [bold]gi list[/bold] to see available templates.")
        raise typer.Exit(1) from e


@app.command(name="doctor")
def doctor() -> None:
    """Show diagnostic information about gi's cache and configuration."""
    import json
    import time

    from .fetch import get_fetcher
    from .util import get_index_cache_path

    console.print("[bold]gi Diagnostic Information[/bold]\n")

    # Cache directory
    cache_dir = get_cache_dir()
    console.print(f"Cache directory: [cyan]{cache_dir}[/cyan]")
    console.print(
        f"Cache exists: [green]{'Yes' if cache_dir.exists() else 'No'}[/green]",
    )

    # Index cache
    index_path = get_index_cache_path()
    console.print(f"Index cache: [cyan]{index_path}[/cyan]")

    if index_path.exists():
        try:
            with index_path.open(encoding="utf-8") as f:
                index_data = json.load(f)

            fetched_at = index_data.get("fetched_at", "Unknown")
            source = index_data.get("source", "Unknown")
            template_count = len(index_data.get("templates", []))

            console.print("Index exists: [green]Yes[/green]")
            console.print(f"Last fetched: [yellow]{fetched_at}[/yellow]")
            console.print(f"Source: [cyan]{source}[/cyan]")
            console.print(f"Template count: [blue]{template_count}[/blue]")

            # Check if index is stale
            from .util import is_stale_cache

            if is_stale_cache(index_path):
                console.print(
                    "Index status: [yellow]Stale (older than 24 hours)[/yellow]",
                )
            else:
                console.print("Index status: [green]Fresh[/green]")

        except (json.JSONDecodeError, OSError) as e:
            console.print(f"Index exists: [red]Yes (corrupted: {e})[/red]")
    else:
        console.print("Index exists: [red]No[/red]")

    # Template cache files
    template_files = list(cache_dir.glob("*.gitignore"))
    console.print(f"Cached templates: [blue]{len(template_files)}[/blue]")

    if template_files:
        console.print("Cached template files:")
        for template_file in sorted(template_files):
            size = template_file.stat().st_size
            mtime = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(template_file.stat().st_mtime),
            )
            console.print(
                f"  [cyan]{template_file.name}[/cyan] ({size} bytes, {mtime})",
            )

    # Test network connectivity
    console.print("\n[bold]Network Test[/bold]")
    try:
        fetcher = get_fetcher()
        # Try to fetch a simple template
        test_content = fetcher.get_template("Python", no_cache=True)
        console.print("GitHub connectivity: [green]OK[/green]")
        console.print(
            f"Test fetch (Python): [green]OK[/green] ({len(test_content)} bytes)",
        )
    except Exception as e:
        console.print("GitHub connectivity: [red]Failed[/red]")
        console.print(f"Error: {e}")


if __name__ == "__main__":
    app()
