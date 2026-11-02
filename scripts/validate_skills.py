#!/usr/bin/env python3
"""Validate metadata and local resources for independently installable skills."""

import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml


def local_link_errors(document, skill_dir):
    errors = []
    root = skill_dir.resolve()
    for token in MarkdownIt().parse(document.read_text(encoding="utf-8")):
        for child in token.children or []:
            if child.type == "link_open":
                href = child.attrGet("href")
            elif child.type == "image":
                href = child.attrGet("src")
            else:
                continue
            parts = urlsplit(href or "")
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = Path(unquote(parts.path))
            label = f"{document.relative_to(skill_dir)}: {href}"
            target = (document.parent / path).resolve()
            if path.is_absolute() or not target.is_relative_to(root):
                errors.append(f"{label}: local resources must stay inside the skill")
            elif not target.exists():
                errors.append(f"{label}: local resource not found")
    return errors


def validate_skill(skill_dir):
    skill_dir = Path(skill_dir)
    entry = skill_dir / "SKILL.md"
    if not entry.is_file():
        return ["SKILL.md is required"]

    errors = []
    try:
        lines = entry.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            return ["SKILL.md must start with YAML frontmatter"]
        end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
        if end is None:
            return ["SKILL.md YAML frontmatter is not closed"]
        metadata = yaml.safe_load("\n".join(lines[1:end]))
        if not isinstance(metadata, dict):
            return ["SKILL.md frontmatter must be a mapping"]

        name = metadata.get("name")
        if not isinstance(name, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", name
        ) or len(name) > 64:
            errors.append("name must use lowercase letters, digits and hyphens (max 64)")
        elif name != skill_dir.name:
            errors.append(f"name '{name}' must match directory '{skill_dir.name}'")

        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append("description must be a nonempty string")
        elif len(description) > 1024:
            errors.append("description must be at most 1024 characters")

        for document in sorted(skill_dir.rglob("*.md")):
            errors.extend(local_link_errors(document, skill_dir))

        agent_file = skill_dir / "agents" / "openai.yaml"
        if agent_file.is_file():
            agent_metadata = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
            if not isinstance(agent_metadata, dict):
                errors.append("agents/openai.yaml must be a YAML mapping")
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "skills",
    )
    args = parser.parse_args()
    if not args.skills_root.is_dir():
        parser.error(f"skills directory not found: {args.skills_root}")
    skills = sorted(
        path for path in args.skills_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    if not skills:
        parser.error("no skill directories found")
    failed = False
    for skill in skills:
        errors = validate_skill(skill)
        if errors:
            failed = True
            for error in errors:
                print(f"ERROR {skill.name}: {error}")
        else:
            print(f"OK {skill.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
