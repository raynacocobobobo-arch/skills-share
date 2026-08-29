import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-digital-human-character-card"
CARD_SKILL = CARD_DIR / "SKILL.md"


class DigitalHumanCharacterCardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = CARD_SKILL.read_text(encoding="utf-8") if CARD_SKILL.exists() else ""

    def test_character_card_is_atomic_render_v12(self):
        self.assertTrue(CARD_SKILL.exists(), "character-card skill must exist")
        self.assertIn("name: hermes-digital-human-character-card", self.card)
        self.assertIn("version: 1.2.0", self.card)
        self.assertIn("ATOMIC RENDER", self.card)

    def test_shorthand_invocation_still_runs_full_auto(self):
        self.assertIn("Shorthand Invocation", self.card)
        self.assertIn("路由到 Hermes 人物卡技能", self.card)
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("do not ask the user to repeat this contract", self.card)

    def test_partial_profile_and_confidence_labels_are_preserved(self):
        self.assertIn("SOURCE FULL-BODY", self.card)
        self.assertIn("SOURCE FACE CLOSE-UP", self.card)
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("All profile fields are optional", self.card)
        for label in ["USER_CONFIRMED", "OBSERVED", "ESTIMATED", "UNKNOWN"]:
            self.assertIn(label, self.card)
        self.assertIn("do not invent exact weight", self.card)

    def test_final_deliverables_remain_profile_face_sheet_body_sheet(self):
        self.assertIn("exactly three final deliverables", self.card)
        self.assertIn("DH001_PROFILE_CARD", self.card)
        self.assertIn("DH001_FACE_3VIEW_SHEET", self.card)
        self.assertIn("DH001_BODY_3VIEW_SHEET", self.card)

    def test_visual_generation_is_six_separate_atomic_jobs(self):
        self.assertIn("six separate ATOMIC IMAGE JOBS", self.card)
        for job in [
            "FACE_FRONT",
            "FACE_LEFT45",
            "FACE_RIGHT45",
            "BODY_FRONT",
            "BODY_SIDE",
            "BODY_BACK",
        ]:
            self.assertIn(job, self.card)
        self.assertIn("one view per image-generation call", self.card)

    def test_image_model_never_generates_the_final_sheets(self):
        self.assertIn("The image model must never be asked to generate a character card", self.card)
        self.assertIn("must never be asked to generate a face three-view sheet", self.card)
        self.assertIn("must never be asked to generate a body three-view sheet", self.card)
        self.assertIn("must never be asked to generate an infographic", self.card)

    def test_profile_is_not_exposed_to_visual_render_jobs(self):
        self.assertIn("PROFILE_CARD is text-only", self.card)
        self.assertIn("Do not pass PROFILE_CARD into any image-generation job", self.card)
        self.assertIn("Do not present the full PROFILE_CARD before the six atomic renders are complete", self.card)

    def test_sheet_assembly_is_deterministic_and_non_generative(self):
        self.assertIn("DETERMINISTIC SHEET ASSEMBLY", self.card)
        self.assertIn("Python/PIL or an equivalent non-generative compositor", self.card)
        self.assertIn("FACE_FRONT + FACE_LEFT45 + FACE_RIGHT45", self.card)
        self.assertIn("BODY_FRONT + BODY_SIDE + BODY_BACK", self.card)
        self.assertIn("Do not call image generation during sheet assembly", self.card)

    def test_atomic_views_are_source_anchored_and_do_not_chain(self):
        self.assertIn("STAR TOPOLOGY", self.card)
        self.assertIn("SOURCE → FACE_FRONT", self.card)
        self.assertIn("SOURCE → FACE_LEFT45", self.card)
        self.assertIn("SOURCE → FACE_RIGHT45", self.card)
        self.assertIn("SOURCE → BODY_FRONT", self.card)
        self.assertIn("SOURCE → BODY_SIDE", self.card)
        self.assertIn("SOURCE → BODY_BACK", self.card)
        self.assertIn("A generated atomic view must never become SOURCE", self.card)

    def test_full_auto_means_atomic_sequence_plus_assembly(self):
        self.assertIn("FULL AUTO means automatic orchestration, not visual aggregation", self.card)
        self.assertIn("PROFILE BUILD (internal)", self.card)
        self.assertIn("6 ATOMIC RENDERS", self.card)
        self.assertIn("2 DETERMINISTIC ASSEMBLIES", self.card)
        self.assertIn("FINAL DELIVERY", self.card)

    def test_qc_regenerates_only_the_failed_atomic_view(self):
        self.assertIn("ATOMIC VIEW QC", self.card)
        self.assertIn("regenerate only that failed view from SOURCE", self.card)
        self.assertIn("Do not regenerate or redesign the whole sheet", self.card)

    def test_manual_regression_case_covers_chatgpt_aggregation_bug(self):
        self.assertIn("MANUAL REGRESSION CASE", self.card)
        self.assertIn("180cm", self.card)
        self.assertIn("男", self.card)
        self.assertIn("40岁", self.card)
        self.assertIn("PROFILE + FACE + BODY", self.card)
        self.assertIn("ARCHITECTURE FAIL", self.card)

    def test_final_approval_can_promote_validated_sheets_to_masters(self):
        self.assertIn("IDENTITY_MASTER V1", self.card)
        self.assertIn("BODY_MASTER V1", self.card)
        self.assertIn("final human approval", self.card)
        self.assertIn("no automatic promotion", self.card)
        self.assertIn("next_skill: hermes-creative-digital-human", self.card)


if __name__ == "__main__":
    unittest.main()
