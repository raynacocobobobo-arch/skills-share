#!/usr/bin/env python3
"""Incrementally register a Hermes skill in skill-registry.json.

Designed to avoid manual editing of large registry files.
"""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="manifests/skill-registry.json")
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--triggers", nargs="+", required=True)
    args = parser.parse_args()

    path = Path(args.registry)
    data = json.loads(path.read_text(encoding="utf-8"))

    if any(s.get("name") == args.name for s in data["skills"]):
        raise SystemExit(f"skill already exists: {args.name}")

    data["skills"].append({
        "name": args.name,
        "description": args.description,
        "version": "",
        "category": args.category,
        "skill_dir": args.skill_dir,
        "skill_path": args.skill_path,
        "triggers": args.triggers,
        "references": [],
        "missing_references": []
    })
    data["skill_count"] = len(data["skills"])

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
