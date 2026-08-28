import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"


class DigitalHumanIdentityAnchorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.create = (SKILL_DIR / "workflows/create-character.md").read_text(encoding="utf-8")
        cls.generate = (SKILL_DIR / "workflows/generate-realistic-content.md").read_text(encoding="utf-8")

    def test_anchor_card_is_per_character_not_another_global_registry(self):
        self.assertIn("Identity Anchor Card", self.skill)
        self.assertIn("one per character", self.skill)
        self.assertIn("Do not create a global digital-human registry", self.skill)

    def test_tag_is_a_stable_alias_not_a_magic_image_lookup(self):
        combined = "\n".join([self.skill, self.create, self.generate])
        self.assertIn("Tags are stable aliases, not image payloads", combined)
        self.assertIn("tag alone does not satisfy Explicit Master Re-attachment", combined)

    def test_active_identity_version_is_explicit_and_immutable(self):
        combined = "\n".join([self.skill, self.create])
        self.assertIn("ACTIVE", combined)
        self.assertIn("DEPRECATED", combined)
        self.assertIn("never overwrite an approved master in place", combined)

    def test_session_bootstrap_requires_current_task_attachment(self):
        self.assertIn("IDENTITY ANCHOR READY", self.generate)
        self.assertIn("IDENTITY ANCHOR MISSING", self.generate)
        self.assertIn("physically attached to the current task", self.generate)

    def test_reference_map_is_numbered_and_role_bound(self):
        self.assertIn("Reference Map", self.generate)
        self.assertIn("REF01", self.generate)
        self.assertIn("IDENTITY ONLY", self.generate)
        self.assertIn("BODY ONLY", self.generate)
        self.assertIn("WARDROBE ONLY", self.generate)
        self.assertIn("POSE ONLY", self.generate)
        self.assertIn("SCENE ONLY", self.generate)

    def test_priority_is_symbolic_not_fake_numeric_weight(self):
        combined = "\n".join([self.skill, self.generate])
        self.assertIn("CRITICAL / HIGH / NORMAL", combined)
        self.assertIn("Do not invent numeric reference weights", combined)


if __name__ == "__main__":
    unittest.main()
