"""Validate portable skill metadata and local Markdown references."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


def validate(root: Path) -> None:
    skill = root / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if match is None:
        raise ValueError("SKILL.md needs YAML frontmatter at the start")
    header = yaml.safe_load(match.group(1))
    if not isinstance(header, dict):
        raise ValueError("Skill frontmatter must be a mapping")
    name = header.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("Skill name must be lowercase kebab case, at most 64 characters")
    description = header.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError("Description must contain 1–1024 characters")
    if not text[match.end():].strip():
        raise ValueError("Skill instructions must be non-empty")

    pages = [skill, root / "README.md", *sorted((root / "references").rglob("*.md"))]
    for page in pages:
        content = page.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            file, _, anchor = unquote(link).partition("#")
            target = (page.parent / file).resolve() if file else page
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError(f"{page.relative_to(root)} has an invalid local link: {link}")
            if anchor:
                headings = re.findall(r"^#+\s+(.+)$", target.read_text(encoding="utf-8"), re.MULTILINE)
                anchors = [re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-") for heading in headings]
                if anchor not in anchors:
                    raise ValueError(f"{page.relative_to(root)} has a missing section anchor: {link}")
    print(f"Validated {name}: metadata, instructions and {len(pages)} Markdown files")


if __name__ == "__main__":
    repository = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    try:
        validate(repository)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
