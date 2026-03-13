#!/usr/bin/env python3
"""Bulk edit SKILL.md files to remove boilerplate sections and transform routing references."""

import re
from pathlib import Path

SKILLS_DIR = Path("/home/kevin/claude/red-run/skills")

EXCLUDE_FILES = {
    SKILLS_DIR / "_template" / "SKILL.md",
    SKILLS_DIR / "orchestrator" / "SKILL.md",
    SKILLS_DIR / "web" / "web-discovery" / "SKILL.md",
    SKILLS_DIR / "ad" / "ad-discovery" / "SKILL.md",
    SKILLS_DIR / "privesc" / "linux-discovery" / "SKILL.md",
    SKILLS_DIR / "privesc" / "windows-discovery" / "SKILL.md",
}


def find_skill_files() -> list[Path]:
    """Find all SKILL.md files except excluded ones."""
    files = sorted(SKILLS_DIR.rglob("SKILL.md"))
    return [f for f in files if f not in EXCLUDE_FILES]


def remove_section(lines: list[str], heading_text: str, heading_prefix: str = "## ") -> tuple[list[str], int]:
    """Remove a section from heading to next same-or-higher-level heading.

    heading_prefix determines heading level: '## ' matches ## headings,
    '### ' matches ### headings. Removal stops at next heading of same or higher level.
    Correctly skips '#' lines inside fenced code blocks.
    """
    result = []
    removed = 0
    in_section = False
    in_code_block = False
    heading_level = len(heading_prefix.rstrip())

    for line in lines:
        stripped = line.rstrip()

        # Track fenced code blocks (``` or ~~~)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block

        if not in_section:
            if not in_code_block and stripped.startswith(heading_prefix.rstrip()) and heading_text in stripped:
                match = re.match(r'^(#{1,6})\s', stripped)
                if match and len(match.group(1)) == heading_level:
                    in_section = True
                    in_code_block = False  # Reset - we're removing, not tracking
                    removed += 1
                    continue
            result.append(line)
        else:
            # Inside the section being removed - check for end
            if not in_code_block:
                match = re.match(r'^(#{1,6})\s', stripped)
                if match and len(match.group(1)) <= heading_level:
                    in_section = False
                    result.append(line)
                    continue
            removed += 1

    # Clean up trailing blank lines before next section
    while len(result) >= 2 and result[-1].strip() == "" and result[-2].strip() == "":
        result.pop()

    return result, removed


def remove_reverse_shell_section(lines: list[str]) -> tuple[list[str], int]:
    """Remove 'Reverse Shell via MCP' at any heading level, or '## Shell Access (when RCE'."""
    # Try ### Reverse Shell via MCP first (most common)
    result, removed = remove_section(lines, "Reverse Shell via MCP", "### ")
    if removed > 0:
        return result, removed
    # Try #### Reverse Shell via MCP (container-escapes uses level 4)
    result, removed = remove_section(lines, "Reverse Shell via MCP", "#### ")
    if removed > 0:
        return result, removed
    # Try ## Shell Access (when RCE
    return remove_section(lines, "Shell Access (when RCE", "## ")


def transform_scope_boundary(text: str) -> tuple[str, bool]:
    """Clean up Scope Boundary section references to 'Route to **skill-name**'."""
    changed = False

    # Pattern: 'through a routing instruction ("Route to **skill-name**") or by discovering findings outside your domain'
    # The text may wrap across lines, so use \s+ to match whitespace including newlines
    old_pattern = r'through\s+a\s+routing\s+instruction\s+\("Route\s+to\s+\*\*skill-name\*\*"\)\s+or\s+by\s+discovering\s+findings\s+outside\s+your\s+domain'
    new_text = "through completing your methodology or discovering findings outside your domain"
    if re.search(old_pattern, text):
        text = re.sub(old_pattern, new_text, text)
        changed = True

    # Pattern: '- Recommended next skill (the bold **skill-name** from routing instructions)'
    old_line = r'\n\s*- Recommended next skill \(the bold \*\*skill-name\*\* from routing instructions\)\n'
    if re.search(old_line, text):
        text = re.sub(old_line, "\n", text)
        changed = True

    return text, changed


def transform_escalation_routing(text: str) -> tuple[str, int]:
    """Transform routing references in escalation sections and throughout.

    - Replace 'Route to **skill-name**' patterns (remove the skill name ref)
    - Replace 'STOP. Return to orchestrator recommending **skill**' patterns
    - Replace full escalation bullet lists with generic return instructions
    """
    changes = 0

    # Replace full escalation sections that are lists of routing rules.
    # Pattern: a ## Step N heading with "Escalat" or "Pivot" followed by bullet list
    # of routing rules ending before next ## heading.
    #
    # We handle this by finding escalation sections and checking if they're
    # predominantly routing rules.
    lines = text.split("\n")
    result_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect escalation/pivot section headings
        escalation_match = re.match(
            r'^(## Step \d+:?\s*(?:Escalat|Post-Exploit|Pivot).*)', line
        )
        if escalation_match:
            # Collect the entire section
            section_heading = line
            section_body = []
            i += 1
            while i < len(lines):
                # Next ## heading means section end
                if re.match(r'^##\s', lines[i]) and not re.match(r'^###', lines[i]):
                    break
                section_body.append(lines[i])
                i += 1

            body_text = "\n".join(section_body)

            # Count routing references in this section
            routing_refs = len(re.findall(
                r'Route to \*\*|STOP\.\s*Return to orchestrator recommending \*\*',
                body_text
            ))

            # If the section is predominantly routing rules (3+ refs), replace body
            if routing_refs >= 3:
                result_lines.append(section_heading)
                result_lines.append("")
                result_lines.append("STOP and return to the orchestrator with:")
                result_lines.append("- What was achieved (RCE, creds, file read, etc.)")
                result_lines.append("- New credentials, access, or pivot paths discovered")
                result_lines.append("- Context for next steps (platform, access method, working payloads)")
                result_lines.append("")
                changes += routing_refs
            else:
                # Keep section but transform individual routing lines
                result_lines.append(section_heading)
                for bline in section_body:
                    result_lines.append(bline)
            continue

        result_lines.append(line)
        i += 1

    text = "\n".join(result_lines)

    # Now handle individual routing references that weren't in replaced sections:

    # 'STOP. Return to orchestrator recommending **skill-name**. Pass: context.'
    # -> 'STOP and return with: what was achieved, new findings, context for next steps.'
    pattern = r'STOP\.\s*Return to orchestrator recommending \*\*[^*]+\*\*\.?\s*(?:Pass:?\s*[^\n]*)?'
    matches = re.findall(pattern, text)
    if matches:
        text = re.sub(
            pattern,
            "STOP and return with: what was achieved, new findings, context for next steps.",
            text
        )
        changes += len(matches)

    # 'Route to **skill-name**' in inline text (not in replaced sections)
    # Remove the specific skill name but keep surrounding context
    # e.g., "Route to **credential-dumping** (DCSync)" -> "escalate via DCSync"
    # More generic: just remove "Route to **name**" references
    route_pattern = r'Route to \*\*[^*]+\*\*'
    route_matches = re.findall(route_pattern, text)
    if route_matches:
        # For lines like "Route to **skill-name** for X" -> "Escalate for X"
        # For lines like "Route to **skill-name**" at end -> remove or simplify
        text = re.sub(r'Route to \*\*[^*]+\*\*', 'Escalate', text)
        changes += len(route_matches)

    # Clean up "→ ROUTE ON HIT: ... → **skill-name**" patterns
    # Keep the detection info, remove skill name
    route_on_hit = re.findall(r'→\s*\*\*[a-z0-9-]+\*\*', text)
    if route_on_hit:
        text = re.sub(r'\s*→\s*\*\*[a-z0-9-]+\*\*', '', text)
        changes += len(route_on_hit)

    return text, changes


def process_file(filepath: Path) -> dict:
    """Process a single SKILL.md file."""
    report = {
        "file": str(filepath.relative_to(SKILLS_DIR)),
        "stall_detection": 0,
        "reverse_shell": 0,
        "av_edr": 0,
        "dns_resolution": 0,
        "scope_boundary": False,
        "escalation_routing": 0,
        "total_lines_removed": 0,
    }

    text = filepath.read_text()
    original_lines = text.count("\n")
    lines = text.split("\n")

    # 4a: Remove Stall Detection
    lines, removed = remove_section(lines, "Stall Detection", "## ")
    report["stall_detection"] = removed

    # 4b: Remove Reverse Shell via MCP / Shell Access
    lines, removed = remove_reverse_shell_section(lines)
    report["reverse_shell"] = removed

    # 4d: Remove AV/EDR Detection
    lines, removed = remove_section(lines, "AV/EDR Detection", "## ")
    report["av_edr"] = removed

    # 4e: Remove DNS Resolution Failure
    lines, removed = remove_section(lines, "DNS Resolution Failure", "## ")
    report["dns_resolution"] = removed

    # Rejoin for text-level transformations
    text = "\n".join(lines)

    # 4c: Transform scope boundary
    text, scope_changed = transform_scope_boundary(text)
    report["scope_boundary"] = scope_changed

    # 4c: Transform escalation routing
    text, routing_changes = transform_escalation_routing(text)
    report["escalation_routing"] = routing_changes

    # Calculate total lines removed
    new_lines = text.count("\n")
    report["total_lines_removed"] = original_lines - new_lines

    # Write back
    filepath.write_text(text)

    return report


def main():
    files = find_skill_files()
    print(f"Found {len(files)} skill files to process\n")

    total_files = 0
    total_lines_removed = 0
    section_counts = {
        "stall_detection": 0,
        "reverse_shell": 0,
        "av_edr": 0,
        "dns_resolution": 0,
        "scope_boundary": 0,
        "escalation_routing": 0,
    }

    for filepath in files:
        report = process_file(filepath)
        total_files += 1
        total_lines_removed += report["total_lines_removed"]

        changes = []
        if report["stall_detection"]:
            changes.append(f"stall_detection ({report['stall_detection']} lines)")
            section_counts["stall_detection"] += 1
        if report["reverse_shell"]:
            changes.append(f"reverse_shell ({report['reverse_shell']} lines)")
            section_counts["reverse_shell"] += 1
        if report["av_edr"]:
            changes.append(f"av_edr ({report['av_edr']} lines)")
            section_counts["av_edr"] += 1
        if report["dns_resolution"]:
            changes.append(f"dns_resolution ({report['dns_resolution']} lines)")
            section_counts["dns_resolution"] += 1
        if report["scope_boundary"]:
            changes.append("scope_boundary")
            section_counts["scope_boundary"] += 1
        if report["escalation_routing"]:
            changes.append(f"routing ({report['escalation_routing']} refs)")
            section_counts["escalation_routing"] += 1

        if changes:
            print(f"  {report['file']}: {', '.join(changes)} [-{report['total_lines_removed']} lines]")
        else:
            print(f"  {report['file']}: no changes")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Files processed: {total_files}")
    print(f"  Total lines removed: {total_lines_removed}")
    print(f"  Stall Detection removed: {section_counts['stall_detection']}")
    print(f"  Reverse Shell via MCP removed: {section_counts['reverse_shell']}")
    print(f"  AV/EDR Detection removed: {section_counts['av_edr']}")
    print(f"  DNS Resolution Failure removed: {section_counts['dns_resolution']}")
    print(f"  Scope Boundary cleaned: {section_counts['scope_boundary']}")
    print(f"  Files with routing transforms: {section_counts['escalation_routing']}")


if __name__ == "__main__":
    main()
