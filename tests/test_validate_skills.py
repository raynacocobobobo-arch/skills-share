import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate-skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
validate_skills = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_skills)


class ValidateSkillsVersionTests(unittest.TestCase):
    def make_skill(self, root: Path, dirname: str, version: str) -> Path:
        skill = root / "plugins" / "hermes-skills" / "skills" / dirname / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text(
            "---\n"
            "name: demo\n"
            "description: demo skill\n"
            f"version: {version}\n"
            "---\n"
            "# Demo\n",
            encoding="utf-8",
        )
        return skill

    def test_registry_record_includes_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = self.make_skill(root, "demo", "13.0.0")
            old_root = validate_skills.ROOT
            old_skills_root = validate_skills.SKILLS_ROOT
            try:
                validate_skills.ROOT = root
                validate_skills.SKILLS_ROOT = root / "plugins" / "hermes-skills" / "skills"
                record, errors = validate_skills.validate_skill(skill)
            finally:
                validate_skills.ROOT = old_root
                validate_skills.SKILLS_ROOT = old_skills_root
            self.assertEqual(errors, [])
            self.assertEqual(record["version"], "13.0.0")

    def test_version_downgrade_is_rejected(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "11.1.0"}]},
        )
        self.assertTrue(any("version downgrade" in error for error in errors))

    def test_version_upgrade_is_allowed(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "11.1.0"}]},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
        )
        self.assertEqual(errors, [])

    def test_equal_version_is_allowed(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
        )
        self.assertEqual(errors, [])

    def test_new_skill_without_baseline_is_allowed(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": []},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "1.0.0"}]},
        )
        self.assertEqual(errors, [])

    def test_malformed_version_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_skills.parse_version("banana")

    def test_removing_existing_version_is_rejected(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": ""}]},
        )
        self.assertTrue(any("version removed" in error for error in errors))

    def test_explicit_downgrade_override_is_allowed(self):
        errors = validate_skills.compare_registry_versions(
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "13.0.0"}]},
            {"skills": [{"skill_path": "skills/demo/SKILL.md", "version": "11.1.0"}]},
            allow_downgrade=True,
        )
        self.assertEqual(errors, [])

    def test_registry_semantic_match_ignores_json_formatting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            compact = root / "compact.json"
            pretty = root / "pretty.json"
            compact.write_text('{"schema_version":1,"skills":[{"name":"demo"}]}', encoding="utf-8")
            pretty.write_text(
                '{\n  "schema_version": 1,\n  "skills": [\n    {\n      "name": "demo"\n    }\n  ]\n}\n',
                encoding="utf-8",
            )
            committed = validate_skills.load_registry(compact)
            generated = validate_skills.load_registry(pretty)
            self.assertEqual(validate_skills.compare_registry_content(committed, generated), [])

    def test_registry_semantic_mismatch_is_rejected(self):
        errors = validate_skills.compare_registry_content(
            {"skill_count": 1, "skills": [{"name": "demo"}]},
            {"skill_count": 2, "skills": [{"name": "demo"}, {"name": "other"}]},
        )
        self.assertTrue(any("registry content mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
