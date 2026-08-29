import unittest
from pathlib import Path


# V1.3 regression contract: fixed output format, view-orientation gates,
# source locking, limited-source mode, and rejection recovery.
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
        self.assertIn("version: 1.3.0", self.card)

    def test_shorthand_invocation_uses_evidence_bounded_full_auto(self):
        self.assertIn("Shorthand Invocation", self.card)
        self.assertIn("路由到 Hermes 人物卡技能", self.card)
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("do not ask the user to repeat this contract", self.card)
        self.assertIn("STANDARD MODE", self.card)
        self.assertIn("FACE-FIRST LIMITED MODE", self.card)
        self.assertIn("do not force BODY generation", self.card)

    def test_route_must_load_skill_before_identity_bearing_image_operation(self):
        self.assertIn("Hard Execution Contract", self.card)
        self.assertIn("LOAD SKILL", self.card)
        self.assertIn("Never jump directly from a Hermes character-card request to image generation", self.card)
        self.assertIn("Do not claim that the character-card skill was executed if this SKILL.md was not loaded", self.card)

    def test_inputs_allow_partial_factual_profile(self):
        self.assertIn("SOURCE FULL-BODY", self.card)
        self.assertIn("SOURCE FACE CLOSE-UP", self.card)
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("All fields are optional", self.card)
        self.assertIn("A single clear face or upper-body image is sufficient for FACE-FIRST LIMITED MODE", self.card)
        self.assertIn("人物资料:", self.card)

    def test_profile_card_separates_information_confidence(self):
        for label in ["USER_CONFIRMED", "OBSERVED", "ESTIMATED", "UNKNOWN"]:
            self.assertIn(label, self.card)
        self.assertIn("do not infer sensitive traits such as ethnicity", self.card)
        self.assertIn("do not invent exact weight", self.card)

    def test_output_contract_keeps_three_named_asset_types(self):
        self.assertIn("three possible core deliverables", self.card)
        self.assertIn("DH001_PROFILE_CARD", self.card)
        self.assertIn("DH001_FACE_3VIEW_SHEET", self.card)
        self.assertIn("DH001_BODY_3VIEW_SHEET", self.card)
        self.assertIn("Not every run must produce all three", self.card)

    def test_face_sheet_has_fixed_three_panel_format(self):
        for view in ["FACE_LEFT45", "FACE_FRONT", "FACE_RIGHT45"]:
            self.assertIn(view, self.card)
        self.assertIn("Fixed FACE Sheet Layout", self.card)
        self.assertIn("aspect_ratio: 3:2", self.card)
        self.assertIn("layout: horizontal_3_panel", self.card)
        self.assertIn("background: neutral_light_gray", self.card)
        self.assertIn("labels_only: true", self.card)
        self.assertIn("FACE sheet must contain face views only", self.card)
        self.assertIn("no combined character-design poster", self.card)

    def test_universal_image_output_rejects_decorative_infographics(self):
        self.assertIn("Universal Output Format Contract", self.card)
        self.assertIn("no decorative UI", self.card)
        self.assertIn("no biography block", self.card)
        self.assertIn("no statistics table", self.card)
        self.assertIn("FORMAT_FAIL", self.card)

    def test_face_views_are_all_anchored_to_original_face_source(self):
        self.assertIn("Face Source Lock", self.card)
        self.assertIn("Each of FACE_FRONT, FACE_LEFT45, and FACE_RIGHT45 must be solved from original SOURCE FACE CLOSE-UP evidence", self.card)
        self.assertIn("Do not generate a side/45-degree identity by treating a generated front view as the new identity source", self.card)
        self.assertIn("Generated FACE panels are siblings, not parents", self.card)

    def test_left_and_right_45_must_have_opposite_yaw(self):
        self.assertIn("FACE Orientation Geometry", self.card)
        self.assertIn("yaw ≈ -45°", self.card)
        self.assertIn("yaw ≈ +45°", self.card)
        self.assertIn("must have opposite yaw directions", self.card)
        self.assertIn("if both 45° panels turn toward the same side, mark `VIEW_ORIENTATION_FAIL`", self.card)

    def test_duplicate_45_direction_regression_is_rejected_before_identity(self):
        self.assertIn("Regression Case — Duplicate 45° Direction", self.card)
        self.assertIn("FACE_LEFT45  = face turns toward direction A", self.card)
        self.assertIn("FACE_RIGHT45 = face also turns toward direction A", self.card)
        self.assertIn("ORIENTATION: FAIL", self.card)
        self.assertIn("FINAL: REJECT", self.card)
        self.assertIn("do not continue to identity QC after a P0 orientation failure", self.card)

    def test_body_sheet_has_fixed_front_side_back_format(self):
        for view in ["BODY_FRONT", "BODY_SIDE", "BODY_BACK"]:
            self.assertIn(view, self.card)
        self.assertIn("Fixed BODY Sheet Layout", self.card)
        self.assertIn("crop: full_body_head_to_toe", self.card)
        self.assertIn("BODY sheet must contain body views only", self.card)
        self.assertIn("Only generate this deliverable in STANDARD MODE", self.card)

    def test_body_sheet_re_reads_original_face_and_body_source(self):
        self.assertIn("Body Source Lock", self.card)
        self.assertIn("original SOURCE FULL-BODY controls body geometry", self.card)
        self.assertIn("original SOURCE FACE CLOSE-UP controls facial identity", self.card)
        self.assertIn("Do not use the generated FACE_3VIEW_SHEET as upstream identity authority for BODY_3VIEW_SHEET", self.card)

    def test_qc_gate_order_is_format_orientation_identity_geometry(self):
        self.assertIn("QC Gate Priority", self.card)
        self.assertIn("FORMAT → ORIENTATION → IDENTITY → GEOMETRY", self.card)
        self.assertIn("VIEW ORIENTATION GATE", self.card)
        self.assertIn("This gate runs before likeness analysis", self.card)
        self.assertIn("up to 2 automatic retries", self.card)

    def test_candidate_status_requires_all_gates_before_accept(self):
        self.assertIn("Candidate Status Contract", self.card)
        for field in ["FORMAT:", "ORIENTATION:", "IDENTITY:", "GEOMETRY:", "FINAL: ACCEPT | REJECT"]:
            self.assertIn(field, self.card)
        self.assertIn("generated` never means `passed", self.card)
        self.assertIn("do not claim `ACCEPT` unless all required gates pass", self.card)

    def test_full_auto_respects_standard_and_limited_modes(self):
        self.assertIn("FULL AUTO MODE", self.card)
        self.assertIn("PROFILE_CARD → FACE_3VIEW_SHEET → FACE QC → BODY_3VIEW_SHEET → BODY QC", self.card)
        self.assertIn("PROFILE_CARD → FACE_3VIEW_SHEET → FACE QC → STOP", self.card)
        self.assertIn("Do not ask the user to say “next” between stages", self.card)
        self.assertIn("not permission to invent unsupported assets", self.card)

    def test_user_likeness_rejection_hard_stops_and_restarts_from_source(self):
        self.assertIn("Likeness Rejection Hard Stop", self.card)
        self.assertIn("不像本人", self.card)
        self.assertIn("IDENTITY_FAIL", self.card)
        self.assertIn("exclude the rejected candidate from all subsequent identity/reference inputs", self.card)
        self.assertIn("restart from original SOURCE", self.card)
        self.assertIn("The latest generated image is never preferred merely because it is recent in the chat", self.card)

    def test_structural_rejection_hard_stops_and_restarts_from_source(self):
        self.assertIn("Structural Rejection Hard Stop", self.card)
        self.assertIn("两张都是左视图", self.card)
        self.assertIn("VIEW_ORIENTATION_FAIL", self.card)
        self.assertIn("do not debate identity first", self.card)
        self.assertIn("restart from original SOURCE", self.card)

    def test_two_sheets_are_generated_from_source_not_from_each_other(self):
        self.assertIn("STAR TOPOLOGY", self.card)
        self.assertIn("SOURCE → FACE_3VIEW_SHEET", self.card)
        self.assertIn("SOURCE → BODY_3VIEW_SHEET", self.card)
        self.assertIn("Do not use a generated FACE sheet as upstream identity authority", self.card)
        self.assertIn("generated candidate cannot become SOURCE", self.card)

    def test_limited_mode_never_promotes_body_master(self):
        self.assertIn("FACE_ASSET_READY_BODY_PENDING", self.card)
        self.assertIn("body_master: null", self.card)
        self.assertIn("No BODY_MASTER exists until sufficient SOURCE body evidence is supplied", self.card)

    def test_final_delivery_includes_profile_and_acceptance_state(self):
        self.assertIn("FINAL DELIVERY", self.card)
        self.assertIn("Do not finish with image links alone", self.card)
        self.assertIn("must also include the PROFILE_CARD content", self.card)
        self.assertIn("acceptance state of each generated sheet", self.card)

    def test_final_approval_can_promote_validated_sheets_to_masters(self):
        self.assertIn("IDENTITY_MASTER V1", self.card)
        self.assertIn("BODY_MASTER V1", self.card)
        self.assertIn("final human approval", self.card)
        self.assertIn("There is no automatic promotion", self.card)
        self.assertIn("next_skill: hermes-creative-digital-human", self.card)


if __name__ == "__main__":
    unittest.main()
