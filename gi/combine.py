"""Combine and deduplicate .gitignore templates."""

import re


def parse_lines(text: str) -> list[str]:
    """Parse text into lines with universal newlines."""
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def normalize_line(line: str) -> str:
    """Normalize a line for deduplication purposes."""
    # Strip trailing whitespace
    line = line.rstrip()

    # For non-comment lines, normalize internal whitespace
    if not line.startswith("#") and line.strip():
        # Collapse multiple spaces to single space, but preserve brackets
        line = re.sub(r"[ \t]+", " ", line)

    return line


def is_blank_line(line: str) -> bool:
    """Check if a line is blank (empty or only whitespace)."""
    return not line.strip()


def should_preserve_line(line: str) -> bool:
    """Check if a line should be preserved during deduplication."""
    # Always preserve comments and non-blank lines
    return line.strip() != ""


def deduplicate_lines(templates_content: dict[str, str]) -> list[str]:
    """Deduplicate lines across templates, preserving first occurrence."""
    seen_lines: set[str] = set()
    result_lines: list[str] = []

    for template_name, content in templates_content.items():
        lines = parse_lines(content)

        # Add section header
        result_lines.append(f"###> {template_name}.gitignore")

        i = 0
        while i < len(lines):
            line = lines[i]
            normalized = normalize_line(line)

            # Handle comment blocks - try to keep them with their associated rules
            if line.strip().startswith("#"):
                comment_lines = [line]
                j = i + 1

                # Collect consecutive comment lines
                while j < len(lines) and lines[j].strip().startswith("#"):
                    comment_lines.append(lines[j])
                    j += 1

                # Look for the next non-blank, non-comment line
                next_rule_line = None
                k = j
                while k < len(lines):
                    if not is_blank_line(lines[k]) and not lines[k].strip().startswith(
                        "#",
                    ):
                        next_rule_line = lines[k]
                        break
                    k += 1

                # If we found a rule line, check if the whole comment block + rule is unique
                if next_rule_line:
                    comment_block = "\n".join(comment_lines)
                    rule_normalized = normalize_line(next_rule_line)
                    combined_key = f"{comment_block}\n{rule_normalized}"

                    if combined_key not in seen_lines:
                        seen_lines.add(combined_key)
                        result_lines.extend(comment_lines)
                        result_lines.append(next_rule_line)
                        i = k + 1
                        continue
                    # Skip the comment block and rule
                    i = k + 1
                    continue
                # No associated rule, just add comments if unique
                comment_block = "\n".join(comment_lines)
                if comment_block not in seen_lines:
                    seen_lines.add(comment_block)
                    result_lines.extend(comment_lines)
                i = j
                continue

            # Handle regular lines
            if should_preserve_line(line):
                if normalized not in seen_lines:
                    seen_lines.add(normalized)
                    result_lines.append(line)
            else:
                # Blank line - add it
                result_lines.append(line)

            i += 1

        # Add section footer
        result_lines.append(f"###< {template_name}.gitignore")
        result_lines.append("")  # Add blank line between sections

    return result_lines


def collapse_blank_lines(lines: list[str]) -> list[str]:
    """Collapse runs of more than 2 blank lines to maximum 1."""
    result = []
    blank_count = 0

    for line in lines:
        if is_blank_line(line):
            blank_count += 1
            if blank_count <= 1:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)

    return result


def merge_with_existing(
    existing_text: str, new_text: str, strategy: str = "append",
) -> str:
    """Merge new content with existing .gitignore content."""
    if strategy == "replace":
        return new_text

    if not existing_text.strip():
        return new_text

    # Parse existing content
    existing_lines = parse_lines(existing_text)
    new_lines = parse_lines(new_text)

    # Find existing gi-generated sections to avoid duplicates
    existing_sections = set()
    i = 0
    while i < len(existing_lines):
        line = existing_lines[i]
        if line.startswith("###> "):
            section_name = line[5:]
            existing_sections.add(section_name)
            # Skip to end of section
            while i < len(existing_lines) and not existing_lines[i].startswith("###< "):
                i += 1
        i += 1

    # Filter out sections that already exist
    filtered_new_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        if line.startswith("###> "):
            section_name = line[5:]
            if section_name in existing_sections:
                # Skip this entire section
                while i < len(new_lines) and not new_lines[i].startswith("###< "):
                    i += 1
                if i < len(new_lines):
                    i += 1  # Skip the ###< line
                continue
        filtered_new_lines.append(line)
        i += 1

    # Combine existing and new content
    combined_lines = existing_lines + filtered_new_lines

    # Collapse excessive blank lines
    combined_lines = collapse_blank_lines(combined_lines)

    # Ensure single trailing newline
    result = "\n".join(combined_lines)
    if result and not result.endswith("\n"):
        result += "\n"

    return result


def generate_header(
    template_names: list[str], source_url: str = "github/gitignore (HEAD)",
) -> str:
    """Generate a header for the combined .gitignore file."""
    import time  # noqa: PLC0415

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    templates_str = ", ".join(template_names)

    return f"""# .gitignore generated by gi
# Source: {source_url} — fetched {timestamp}
# Templates: {templates_str}

"""


def combine_templates(
    templates_content: dict[str, str],
    existing_content: str = "",
    *,  # Force keyword-only arguments
    append: bool = False,
    include_header: bool = True,
    source_url: str = "github/gitignore (HEAD)",
) -> str:
    """Combine multiple .gitignore templates into a single file."""
    if not templates_content:
        return existing_content or ""

    # Deduplicate lines across templates
    deduplicated_lines = deduplicate_lines(templates_content)

    # Collapse excessive blank lines
    deduplicated_lines = collapse_blank_lines(deduplicated_lines)

    # Generate the combined content
    if include_header:
        header = generate_header(list(templates_content.keys()), source_url)
        combined_content = header + "\n".join(deduplicated_lines)
    else:
        combined_content = "\n".join(deduplicated_lines)

    # Ensure single trailing newline
    if combined_content and not combined_content.endswith("\n"):
        combined_content += "\n"

    # Merge with existing content if appending
    if append and existing_content:
        combined_content = merge_with_existing(
            existing_content, combined_content, "append",
        )

    return combined_content
