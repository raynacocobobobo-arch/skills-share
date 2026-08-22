#!/usr/bin/env python3
"""Validate Hermes skill repository structure and optionally write a registry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "plugins" / "hermes-skills" / "skills"
REGISTRY_PATH = ROOT / "manifests" / "skill-registry.json"

LOCAL_PATH_PATTERNS = [
    "/Users/rayna/" + "Desktop",
    "/Users/rayna/Documents/" + "Obsidian Vault",
]

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+(?!<REDACTED_TOKEN>)[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(r"(?i)(api[_ -]?key\s*[:=]\s*)(?!<)[A-Za-z0-9._~+/=-]{20,}"),
    re.compile(r"(?i)(password\s*[:=]\s*)(?!<)[^\s`\"']{12,}"),
]


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].splitlines()
    body = text[end + 4 :]
    meta: dict[str, object] = {}
    current_key: str | None = None
    for line in raw:
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip().strip('"')
            meta[current_key] = value
        elif current_key and line.strip().startswith("-"):
            existing = meta.get(current_key)
            if not isinstance(existing, list):
                meta[current_key] = []
            item = line.strip()[1:].strip().strip('"')
            cast_list = meta[current_key]
            assert isinstance(cast_list, list)
            cast_list.append(item)
    return meta, body


def find_reference_mentions(text: str) -> list[str]:
    mentions = set()
    for match in re.findall(r"`([^`]+)`", text):
        if match.startswith(("references/", "assets/", "scripts/", "templates/")):
            mentions.add(match)
    return sorted(mentions)


def validate_skill(skill_md: Path) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    meta, _ = parse_frontmatter(text)
    rel_dir = skill_md.parent.relative_to(SKILLS_ROOT).as_posix()

    name = str(meta.get("name") or skill_md.parent.name)
    description = str(meta.get("description") or "")
    triggers = meta.get("triggers")
    if not isinstance(triggers, list):
        triggers = []

    if not meta.get("name"):
        errors.append(f"{skill_md}: missing frontmatter name")
    if not description:
        errors.append(f"{skill_md}: missing frontmatter description")

    for pattern in LOCAL_PATH_PATTERNS:
        if pattern in text:
            errors.append(f"{skill_md}: contains local path {pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{skill_md}: contains possible secret")

    references = find_reference_mentions(text)
    missing_refs = []
    for ref in references:
        if " " in ref and not Path(ref).suffix:
            continue
        candidate = skill_md.parent / ref
        if not candidate.exists():
            missing_refs.append(ref)

    record = {
        "name": name,
        "description": description,
        "category": rel_dir.split("/", 1)[0],
        "skill_dir": rel_dir,
        "skill_path": skill_md.relative_to(ROOT).as_posix(),
        "triggers": triggers,
        "references": references,
        "missing_references": missing_refs,
    }
    return record, errors


def collect_text_files() -> list[Path]:
    suffixes = {".md", ".json", ".yaml", ".yml", ".toml", ".txt", ".py", ".sh", ".service"}
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in suffixes or path.name in {"README.md", "SECURITY.md", "AGENTS.md"}:
            files.append(path)
    return files


def validate_repo_text() -> list[str]:
    errors: list[str] = []
    for path in collect_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern in text:
                errors.append(f"{path.relative_to(ROOT)}: contains local path {pattern}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: contains possible secret")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-registry", action="store_true")
    args = parser.parse_args()

    if not SKILLS_ROOT.exists():
        print(f"Missing skills root: {SKILLS_ROOT}", file=sys.stderr)
        return 1

    records = []
    errors = []
    for skill_md in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        record, skill_errors = validate_skill(skill_md)
        records.append(record)
        errors.extend(skill_errors)

    errors.extend(validate_repo_text())

    registry = {
        "schema_version": 1,
        "source": "plugins/hermes-skills/skills",
        "skill_count": len(records),
        "skills": records,
    }

    if args.write_registry:
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY_PATH.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"skills: {len(records)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
