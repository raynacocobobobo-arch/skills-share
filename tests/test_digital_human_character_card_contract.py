import unittest
from pathlib import Path


# V1.2 regression contract: routing, original-source locking, and identity-failure recovery.
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
        self.assertIn("version: 1.2.0", self.card)

    def test_shorthand_invocation_defaults_to_full_auto_three_outputs(self):
        self.assertIn("Shorthand Invocation", self.card)
        self.assertIn("路由到 Hermes 人物卡技能", self.card)
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("do not ask the user to repeat this contract", self.card)
        self.assertIn("at least one usable full-body or near-full-body image", self.card)
        self.assertIn("at least one usable face or close-up image", self.card)
        self.assertIn("Missing age, weight, hairstyle, or similar profile fields must not block normal execution", self.card)

    def test_route_must_load_skill_before_identity_bearing_image_operation(self):
        self.assertIn("Hard Execution Contract", self.card)
        self.assertIn("ROUTE → LOAD SKILL", self.card)
        self.assertIn("Never jump directly from a Hermes character-card request to image generation", self.card)
        self.assertIn("Do not claim that the character-card skill was executed if this SKILL.md was not loaded", self.card)

    def test_inputs_allow_partial_factual_profile(self):
        self.assertIn("SOURCE FULL-BODY", self.card)
        self.assertIn("SOURCE FACE CLOSE-UP", self.card)
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("All fields are optional", self.card)
        self.assertIn("人物资料:", self.card)
        self.assertIn("age", self.card)
        self.assertIn("height", self.card)
        self.assertIn("weight", self.card)

    def test_profile_card_separates_information_confidence(self):
        for label in ["USER_CONFIRMED", "OBSERVED", "ESTIMATED", "UNKNOWN"]:
            self.assertIn(label, self.card)
        self.assertIn("do not infer sensitive traits such as ethnicity", self.card)
        self.assertIn("do not invent exact weight", self.card)

    def test_output_is_exactly_three_deliverables(self):
        self.assertIn("exactly three core deliverables", self.card)
        self.assertIn("DH001_PROFILE_CARD", self.card)
        self.assertIn("DH001_FACE_3VIEW_SHEET", self.card)
        self.assertIn("DH001_BODY_3VIEW_SHEET", self.card)
        self.assertNotIn("exactly six standard image assets", self.card)

    def test_face_sheet_contains_three_identity_useful_views_and_is_isolated(self):
        self.assertIn("FACE_FRONT", self.card)
        self.assertIn("FACE_LEFT45", self.card)
        self.assertIn("FACE_RIGHT45", self.card)
        self.assertIn("one face three-view sheet", self.card)
        self.assertIn("FACE sheet must contain face views only", self.card)
        self.assertIn("no BODY_3VIEW", self.card)
        self.assertIn("no combined character-design poster", self.card)

    def test_face_views_are_all_anchored_to_original_face_source(self):
        self.assertIn("Face Source Lock", self.card)
        self.assertIn("Each of FACE_FRONT, FACE_LEFT45, and FACE_RIGHT45 must be solved from original SOURCE FACE CLOSE-UP evidence", self.card)
        self.assertIn("Do not generate a side/45-degree identity by treating a generated front view as the new identity source", self.card)
        self.assertIn("Generated FACE panels are siblings, not parents", self.card)

    def test_body_sheet_contains_front_side_back_and_is_isolated(self):
        self.assertIn("BODY_FRONT", self.card)
        self.assertIn("BODY_SIDE", self.card)
        self.assertIn("BODY_BACK", self.card)
        self.assertIn("one full-body three-view sheet", self.card)
        self.assertIn("BODY sheet must contain body views only", self.card)
        self.assertIn("no FACE_3VIEW", self.card)

    def test_body_sheet_re_reads_original_face_and_body_source(self):
        self.assertIn("Body Source Lock", self.card)
        self.assertIn("original SOURCE FULL-BODY controls body geometry", self.card)
        self.assertIn("original SOURCE FACE CLOSE-UP controls facial identity", self.card)
        self.assertIn("Do not use the generated FACE_3VIEW_SHEET as upstream identity authority for BODY_3VIEW_SHEET", self.card)

    def test_full_auto_runs_continuously_but_does_not_merge_outputs(self):
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("PROFILE_CARD → FACE_3VIEW_SHEET → BODY_3VIEW_SHEET", self.card)
        self.assertIn("Do not ask the user to say “next” between stages", self.card)
        self.assertIn("FULL AUTO means continuous execution, not a single combined image", self.card)
        self.assertIn("All three deliverables must remain separate", self.card)

    def test_internal_qc_retries_and_rejects_combined_layout(self):
        self.assertIn("INTERNAL FACE QC", self.card)
        self.assertIn("INTERNAL BODY QC", self.card)
        self.assertIn("up to 2 automatic retries", self.card)
        self.assertIn("LAYOUT_FAIL", self.card)
        self.assertIn("Retry with stricter output isolation", self.card)

    def test_user_likeness_rejection_hard_stops_and_restarts_from_source(self):
        self.assertIn("Likeness Rejection Hard Stop", self.card)
        self.assertIn("不像本人", self.card)
        self.assertIn("IDENTITY_FAIL", self.card)
        self.assertIn("exclude the rejected candidate from all subsequent identity/reference inputs", self.card)
        self.assertIn("restart from original SOURCE", self.card)
        self.assertIn("The latest generated image is never preferred merely because it is recent in the chat", self.card)

    def test_two_sheets_are_generated_from_source_not_from_each_other(self):
        self.assertIn("STAR TOPOLOGY", self.card)
        self.assertIn("SOURCE → FACE_3VIEW_SHEET", self.card)
        self.assertIn("SOURCE → BODY_3VIEW_SHEET", self.card)
        self.assertIn("Do not use a generated FACE sheet as upstream identity authority", self.card)
        self.assertIn("generated candidate cannot become SOURCE", self.card)

    def test_final_delivery_must_include_profile_card(self):
        self.assertIn("FINAL DELIVERY", self.card)
        self.assertIn("Do not finish with image links alone", self.card)
        self.assertIn("must also include the PROFILE_CARD content", self.card)

    def test_final_approval_can_promote_validated_sheets_to_masters(self):
        self.assertIn("IDENTITY_MASTER V1", self.card)
        self.assertIn("BODY_MASTER V1", self.card)
        self.assertIn("final human approval", self.card)
        self.assertIn("no automatic promotion", self.card)
        self.assertIn("next_skill: hermes-creative-digital-human", self.card)


if __name__ == "__main__":
    unittest.main()
