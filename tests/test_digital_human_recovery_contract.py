import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"


class DigitalHumanRecoveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.create = (SKILL_DIR / "workflows/create-character.md").read_text(encoding="utf-8")
        cls.generate = (SKILL_DIR / "workflows/generate-realistic-content.md").read_text(encoding="utf-8")
        cls.improve = (SKILL_DIR / "workflows/improve-output.md").read_text(encoding="utf-8")

    def test_identity_failure_enters_recovery_loop_not_hard_stop(self):
        combined = "\n".join([self.skill, self.create, self.generate, self.improve])
        self.assertIn("Identity Recovery Loop", combined)
        self.assertNotIn("Identity Drift = Hard Stop", combined)
        self.assertNotIn("identity fails, STOP", combined)

    def test_recovery_prefers_approved_master_before_source(self):
        self.assertIn("latest approved IDENTITY MASTER", self.improve)
        self.assertIn("SOURCE only if the approved master itself is invalid", self.improve)

    def test_failed_candidate_is_rejected_without_stopping_workflow(self):
        self.assertIn("REJECTED", self.improve)
        self.assertIn("continue the workflow in recovery mode", self.improve)

    def test_retry_budget_and_escalation_are_explicit(self):
        self.assertIn("Retry Budget", self.improve)
        self.assertIn("Tool Escalation", self.improve)
        self.assertIn("change strategy", self.improve)


if __name__ == "__main__":
    unittest.main()
