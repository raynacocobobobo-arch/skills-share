import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-digital-human-character-card"
CARD_SKILL = CARD_DIR / "SKILL.md"
PRODUCTION_SKILL = (
    ROOT
    / "plugins"
    / "hermes-skills"
    / "skills"
    / "hermes-creative-digital-human"
    / "SKILL.md"
)


class DigitalHumanCharacterCardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = CARD_SKILL.read_text(encoding="utf-8") if CARD_SKILL.exists() else ""
        cls.production = PRODUCTION_SKILL.read_text(encoding="utf-8")

    def test_character_card_is_a_separate_upstream_skill(self):
        self.assertTrue(CARD_SKILL.exists(), "character-card skill must exist")
        self.assertIn("name: hermes-digital-human-character-card", self.card)
        self.assertIn("version: 1.0.0", self.card)
        self.assertIn("CHARACTER_CARD_READY", self.card)

    def test_inputs_are_source_full_body_close_face_and_factual_profile(self):
        self.assertIn("SOURCE FULL-BODY", self.card)
        self.assertIn("SOURCE FACE CLOSE-UP", self.card)
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("age", self.card)
        self.assertIn("height", self.card)
        self.assertIn("weight", self.card)

    def test_output_is_one_quant_profile_and_exactly_six_standard_assets(self):
        self.assertIn("QUANTITATIVE PROFILE CARD", self.card)
        for asset in [
            "BODY_FRONT",
            "BODY_SIDE",
            "BODY_BACK",
            "FACE_FRONT",
            "FACE_LEFT45",
            "FACE_RIGHT45",
        ]:
            self.assertIn(asset, self.card)
        self.assertIn("exactly six standard image assets", self.card)

    def test_face_set_is_three_identity_useful_views_not_a_back_of_face(self):
        self.assertIn("FACE_FRONT", self.card)
        self.assertIn("FACE_LEFT45", self.card)
        self.assertIn("FACE_RIGHT45", self.card)
        self.assertIn("Do not substitute a face-back view", self.card)

    def test_identity_lock_happens_before_standard_asset_generation(self):
        self.assertIn("IDENTITY LOCK", self.card)
        self.assertIn("Identity Lock = APPROVED", self.card)
        self.assertIn("Do not generate the six standard assets before Identity Lock is approved", self.card)

    def test_each_standard_view_uses_star_topology_not_generation_chaining(self):
        self.assertIn("STAR TOPOLOGY", self.card)
        self.assertIn("Never use BODY_FRONT to generate BODY_SIDE", self.card)
        self.assertIn("Never use FACE_FRONT to generate FACE_LEFT45", self.card)
        self.assertIn("generated candidate cannot become SOURCE", self.card)

    def test_approved_face_and_body_sets_map_cleanly_to_downstream_masters(self):
        self.assertIn("IDENTITY_MASTER V1", self.card)
        self.assertIn("BODY_MASTER V1", self.card)
        self.assertIn("explicit human approval", self.card)
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

    def test_existing_production_skill_delegates_missing_character_card_upstream(self):
        self.assertIn("hermes-digital-human-character-card", self.production)
        self.assertIn("CHARACTER_CARD_READY", self.production)
        self.assertIn("resume production", self.production)


if __name__ == "__main__":
    unittest.main()
