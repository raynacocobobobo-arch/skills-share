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


def parse_version(value: object) -> tuple[int, ...]:
    """Parse a simple numeric skill version such as 13.0.0 or v13.0.0."""
    text = str(value or "").strip()
    if text.startswith(("v", "V")):
        text = text[1:]
    if not re.fullmatch(r"\d+(?:\.\d+)*", text):
        raise ValueError(f"invalid skill version: {value!r}")
    return tuple(int(part) for part in text.split("."))


def compare_registry_versions(
    baseline: dict[str, object],
    candidate: dict[str, object],
    allow_downgrade: bool = False,
) -> list[str]:
    """Reject a candidate registry that removes or lowers an existing version."""
    errors: list[str] = []
    baseline_skills = baseline.get("skills")
    candidate_skills = candidate.get("skills")
    if not isinstance(baseline_skills, list) or not isinstance(candidate_skills, list):
        return ["baseline/candidate registry must contain a skills list"]

    baseline_by_path: dict[str, dict[str, object]] = {}
    for item in baseline_skills:
        if isinstance(item, dict) and item.get("skill_path"):
            baseline_by_path[str(item["skill_path"])] = item

    for item in candidate_skills:
        if not isinstance(item, dict) or not item.get("skill_path"):
            continue
        path = str(item["skill_path"])
        previous = baseline_by_path.get(path)
        if not previous:
            continue

        old_version = str(previous.get("version") or "").strip()
        new_version = str(item.get("version") or "").strip()

        # Legacy skills may not yet declare a version. Once a canonical version
        # exists, however, a later change may not silently remove it.
        if not old_version:
            continue
        if not new_version:
            errors.append(f"{path}: version removed; baseline is {old_version}")
            continue

        try:
            old_parts = parse_version(old_version)
            new_parts = parse_version(new_version)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue

        width = max(len(old_parts), len(new_parts))
        old_key = old_parts + (0,) * (width - len(old_parts))
        new_key = new_parts + (0,) * (width - len(new_parts))
        if new_key < old_key and not allow_downgrade:
            errors.append(f"{path}: version downgrade {old_version} -> {new_version}")

    return errors


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
    version = str(meta.get("version") or "").strip()
    triggers = meta.get("triggers")
    if not isinstance(triggers, list):
        triggers = []

    if not meta.get("name"):
        errors.append(f"{skill_md}: missing frontmatter name")
    if not description:
        errors.append(f"{skill_md}: missing frontmatter description")
    if version:
        try:
            parse_version(version)
        except ValueError as exc:
            errors.append(f"{skill_md}: {exc}")

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
        "version": version,
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


def load_registry(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"baseline registry not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid baseline registry JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"baseline registry must be a JSON object: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Run publish validation: compare against the current registry and rewrite it.",
    )
    parser.add_argument("--write-registry", action="store_true")
    parser.add_argument(
        "--baseline-registry",
        type=Path,
        help="Compare skill versions against this previously accepted registry.",
    )
    parser.add_argument(
        "--allow-version-downgrade",
        action="store_true",
        help="Explicit emergency override for a documented version rollback.",
    )
    args = parser.parse_args()

    if args.publish:
        args.write_registry = True
        if not args.baseline_registry:
            args.baseline_registry = REGISTRY_PATH

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

    if args.baseline_registry:
        try:
            baseline = load_registry(args.baseline_registry)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if args.allow_version_downgrade:
                print("WARNING: version downgrade override enabled", file=sys.stderr)
            errors.extend(
                compare_registry_versions(
                    baseline,
                    registry,
                    allow_downgrade=args.allow_version_downgrade,
                )
            )

    if args.write_registry and not errors:
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
