import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "manifests" / "web-chatgpt-router.md"
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"


class DigitalHumanSessionStateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.generate = (SKILL_DIR / "workflows/generate-realistic-content.md").read_text(encoding="utf-8")

    def test_router_keeps_digital_human_skill_sticky_for_same_task_object(self):
        self.assertIn("Sticky Skill Binding", self.router)
        self.assertIn("active skill binding", self.router.lower())
        self.assertIn("same digital-human task object", self.router)
        self.assertIn("explicitly ends", self.router)

    def test_skill_maintains_a_lightweight_session_state_card(self):
        self.assertIn("Digital Human Session State", self.skill)
        self.assertIn("current_step", self.skill)
        self.assertIn("active_identity", self.skill)
        self.assertIn("identity_anchor", self.skill)
        self.assertIn("next_allowed_action", self.skill)
        self.assertIn("Do not create a global session-state registry", self.skill)

    def test_tangential_requests_do_not_silently_skip_workflow_gates(self):
        self.assertIn("must not advance `current_step`", self.skill)
        self.assertIn("deferred requirement", self.skill.lower())
        self.assertIn("upstream gate", self.skill.lower())

    def test_generation_preflight_blocks_mutation_when_required_state_is_missing(self):
        combined = "\n".join([self.skill, self.generate])
        self.assertIn("Generation Preflight", combined)
        self.assertIn("PREFLIGHT PASS", combined)
        self.assertIn("PREFLIGHT BLOCKED", combined)
        self.assertIn("Do not execute an identity-bearing generation", combined)
        self.assertIn("Reference Map", combined)

    def test_state_is_checkpointed_after_state_changing_actions(self):
        self.assertIn("State Checkpoint", self.skill)
        self.assertIn("after every state-changing action", self.skill)
        self.assertIn("new chat", self.skill.lower())
        self.assertIn("re-bootstrap", self.skill.lower())


if __name__ == "__main__":
    unittest.main()
