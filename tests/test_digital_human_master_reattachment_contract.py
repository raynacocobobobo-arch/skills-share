import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"


class DigitalHumanMasterReattachmentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.create = (SKILL_DIR / "workflows/create-character.md").read_text(encoding="utf-8")
        cls.build = (SKILL_DIR / "workflows/build-character-asset.md").read_text(encoding="utf-8")
        cls.generate = (SKILL_DIR / "workflows/generate-realistic-content.md").read_text(encoding="utf-8")
        cls.improve = (SKILL_DIR / "workflows/improve-output.md").read_text(encoding="utf-8")

    def test_master_is_explicitly_reattached_not_recalled_from_chat_history(self):
        combined = "\n".join([self.skill, self.generate])
        self.assertIn("Explicit Master Re-attachment", combined)
        self.assertIn("conversation history is not an identity source", combined)
        self.assertIn("re-attach", self.generate.lower())

    def test_reference_images_have_single_declared_roles(self):
        for role in [
            "IDENTITY ONLY",
            "BODY ONLY",
            "WARDROBE ONLY",
            "POSE ONLY",
            "SCENE ONLY",
        ]:
            self.assertIn(role, self.generate)
        self.assertIn("one declared role", self.generate)

    def test_web_production_flow_is_project_plus_short_chats(self):
        self.assertIn("one project", self.skill.lower())
        self.assertIn("multiple short chats", self.skill.lower())
        self.assertIn("permanent master assets", self.skill.lower())

    def test_edit_first_generate_second_is_explicit(self):
        combined = "\n".join([self.skill, self.generate])
        self.assertIn("Edit-first", combined)
        self.assertIn("Generate-second", combined)

    def test_candidate_hard_stop_blocks_downstream_contamination_not_recovery(self):
        combined = "\n".join([self.skill, self.improve])
        self.assertIn("Candidate Hard Stop", combined)
        self.assertIn("must not continue downstream", combined)
        self.assertIn("does not terminate the whole production workflow", self.improve)

    def test_user_facing_eight_step_flow_is_named(self):
        self.assertIn("8-Step Production Flow", self.skill)
        for step in [
            "1. SOURCE INTAKE",
            "2. IDENTITY MASTER",
            "3. STANDARD THREE-VIEW",
            "4. IDENTITY VALIDATION",
            "5. WARDROBE",
            "6. ENVIRONMENT",
            "7. ACTION",
            "8. BATCH CONTENT",
        ]:
            self.assertIn(step, self.skill)


if __name__ == "__main__":
    unittest.main()
