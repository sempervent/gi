"""Template name normalization and aliases."""

from __future__ import annotations

# Mapping of common aliases to official template names
ALIASES: dict[str, str] = {
    "cpp": "C++",
    "csharp": "VisualStudio",
    "c#": "VisualStudio",
    "vscode": "Global/VisualStudioCode",
    "macos": "Global/macOS",
    "mac": "Global/macOS",
    "jetbrains": "Global/JetBrains",
    "intellij": "Global/JetBrains",
    "idea": "Global/JetBrains",
    "vim": "Global/Vim",
    "emacs": "Global/Emacs",
    "sublime": "Global/SublimeText",
    "atom": "Global/Atom",
    "eclipse": "Global/Eclipse",
    "netbeans": "Global/NetBeans",
    "xcode": "Global/Xcode",
    "android": "Global/Android",
    "ios": "Global/iOS",
    "windows": "Global/Windows",
    "linux": "Global/Linux",
    "node": "Node",
    "npm": "Node",
    "yarn": "Node",
    "js": "Node",
    "javascript": "Node",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "react": "React",
    "vue": "Vue",
    "angular": "Angular",
    "svelte": "Svelte",
    "next": "Next.js",
    "nuxt": "Nuxt.js",
    "gatsby": "Gatsby",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "rails": "Rails",
    "spring": "Spring",
    "gradle": "Gradle",
    "maven": "Maven",
    "sbt": "Scala",
    "scala": "Scala",
    "kotlin": "Kotlin",
    "java": "Java",
    "go": "Go",
    "golang": "Go",
    "rust": "Rust",
    "c": "C",
    "c++": "C++",
    "cxx": "C++",
    "fsharp": "FSharp",
    "vb": "VisualBasic",
    "vbnet": "VisualBasic",
    "php": "PHP",
    "ruby": "Ruby",
    "perl": "Perl",
    "python": "Python",
    "py": "Python",
    "r": "R",
    "matlab": "MATLAB",
    "octave": "Octave",
    "julia": "Julia",
    "haskell": "Haskell",
    "ocaml": "OCaml",
    "erlang": "Erlang",
    "elixir": "Elixir",
    "clojure": "Clojure",
    "lisp": "CommonLisp",
    "scheme": "Scheme",
    "racket": "Racket",
    "lua": "Lua",
    "tcl": "Tcl",
    "awk": "Awk",
    "bash": "Bash",
    "zsh": "Zsh",
    "fish": "Fish",
    "powershell": "PowerShell",
    "ps1": "PowerShell",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "vagrant": "Vagrant",
    "packer": "Packer",
    "helm": "Helm",
    "git": "Git",
    "svn": "Subversion",
    "hg": "Mercurial",
    "bzr": "Bazaar",
    "cvs": "CVS",
    "darcs": "Darcs",
    "fossil": "Fossil",
    "monotone": "Monotone",
    "arch": "Arch",
    "bitkeeper": "BitKeeper",
    "perforce": "Perforce",
    "clearcase": "ClearCase",
    "tfs": "TFS",
    "vss": "VSS",
    "rcs": "RCS",
    "sccs": "SCCS",
    "p4": "Perforce",
    "p4v": "Perforce",
    "p4admin": "Perforce",
    "p4d": "Perforce",
    "p4p": "Perforce",
    "p4s": "Perforce",
    "p4web": "Perforce",
    "p4ws": "Perforce",
    "p4x": "Perforce",
    "p4y": "Perforce",
    "p4z": "Perforce",
}


def normalize_template_name(name: str) -> str:
    """Normalize a template name to its canonical form."""
    # Remove .gitignore suffix if present
    name = name.removesuffix(".gitignore")

    # Convert to lowercase for case-insensitive matching
    name_lower = name.lower()

    # Check aliases first
    if name_lower in ALIASES:
        return ALIASES[name_lower]

    # Convert underscores and dashes to spaces, then title case
    normalized = name.replace("_", " ").replace("-", " ").strip()

    # Handle special cases for Global/ templates
    if normalized.startswith("global/"):
        parts = normalized.split("/")
        return "/".join(part.title() for part in parts)

    # Convert to title case, but preserve existing capitalization for known patterns
    if "/" in normalized:
        # Handle paths like "Global/VisualStudioCode"
        parts = normalized.split("/")
        return "/".join(part.title() for part in parts)
    # Handle simple names like "Python", "C++", etc.
    return normalized.title()


def parse_template_names(input_str: str) -> list[str]:
    """Parse a string of template names, handling both spaces and commas."""
    # Split by both commas and spaces, then clean up
    names = []
    for part in input_str.replace(",", " ").split():
        cleaned_part = part.strip()
        if cleaned_part:
            names.append(cleaned_part)

    return names


def resolve_template_names(names: list[str]) -> list[str]:
    """Resolve a list of template names to their canonical forms."""
    resolved = []
    for name in names:
        canonical = normalize_template_name(name)
        if canonical not in resolved:  # Avoid duplicates
            resolved.append(canonical)

    return resolved
