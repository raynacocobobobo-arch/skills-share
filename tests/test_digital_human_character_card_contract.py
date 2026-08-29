import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-digital-human-character-card"
CARD_SKILL = CARD_DIR / "SKILL.md"


class DigitalHumanCharacterCardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = CARD_SKILL.read_text(encoding="utf-8") if CARD_SKILL.exists() else ""

    def test_character_card_is_a_separate_upstream_skill(self):
        self.assertTrue(CARD_SKILL.exists(), "character-card skill must exist")
        self.assertIn("name: hermes-digital-human-character-card", self.card)
        self.assertIn("version: 1.0.0", self.card)

    def test_inputs_are_source_full_body_close_face_and_factual_profile(self):
        self.assertIn("SOURCE FULL-BODY", self.card)
        self.assertIn("SOURCE FACE CLOSE-UP", self.card)
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("age", self.card)
        self.assertIn("height", self.card)
        self.assertIn("weight", self.card)

    def test_output_is_exactly_three_deliverables(self):
        self.assertIn("exactly three deliverables", self.card)
        self.assertIn("DH001_PROFILE_CARD", self.card)
        self.assertIn("DH001_FACE_3VIEW_SHEET", self.card)
        self.assertIn("DH001_BODY_3VIEW_SHEET", self.card)
        self.assertNotIn("exactly six standard image assets", self.card)

    def test_face_sheet_contains_three_identity_useful_views(self):
        self.assertIn("FACE_FRONT", self.card)
        self.assertIn("FACE_LEFT45", self.card)
        self.assertIn("FACE_RIGHT45", self.card)
        self.assertIn("one face three-view sheet", self.card)
        self.assertIn("Do not substitute a face-back view", self.card)

    def test_body_sheet_contains_front_side_back(self):
        self.assertIn("BODY_FRONT", self.card)
        self.assertIn("BODY_SIDE", self.card)
        self.assertIn("BODY_BACK", self.card)
        self.assertIn("one full-body three-view sheet", self.card)

    def test_full_auto_mode_requires_no_intermediate_reply(self):
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("No intermediate user reply is required", self.card)
        self.assertIn("PROFILE_CARD → FACE_3VIEW_SHEET → BODY_3VIEW_SHEET", self.card)

    def test_internal_identity_qc_retries_without_user_prompt(self):
        self.assertIn("INTERNAL IDENTITY QC", self.card)
        self.assertIn("bounded automatic retry", self.card)
        self.assertIn("do not ask the user to say next", self.card)
        self.assertIn("stop only when SOURCE is insufficient", self.card)

    def test_two_sheets_are_generated_from_source_not_from_each_other(self):
        self.assertIn("STAR TOPOLOGY", self.card)
        self.assertIn("SOURCE → FACE_3VIEW_SHEET", self.card)
        self.assertIn("SOURCE → BODY_3VIEW_SHEET", self.card)
        self.assertIn("Never use FACE_3VIEW_SHEET to generate BODY_3VIEW_SHEET", self.card)
        self.assertIn("generated candidate cannot become SOURCE", self.card)

    def test_final_approval_can_promote_validated_sheets_to_masters(self):
        self.assertIn("IDENTITY_MASTER V1", self.card)
        self.assertIn("BODY_MASTER V1", self.card)
        self.assertIn("final human approval", self.card)
        self.assertIn("no automatic promotion", self.card)

    def test_scope_stops_before_wardrobe_scene_action_and_batch_content(self):
        for phrase in [
            "wardrobe production",
            "scene compositing",
            "action production",
            "batch content production",
        ]:
            self.assertIn(phrase, self.card)
        self.assertIn("hand off to hermes-creative-digital-human", self.card)


if __name__ == "__main__":
    unittest.main()
