import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"


class DigitalHumanFaceRepairContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.generate = (SKILL_DIR / "workflows/generate-realistic-content.md").read_text(encoding="utf-8")
        cls.improve = (SKILL_DIR / "workflows/improve-output.md").read_text(encoding="utf-8")
        cls.combined = "\n".join([cls.skill, cls.generate, cls.improve])

    def test_v24_adds_face_crop_pack_as_identity_support_asset(self):
        self.assertIn("version: 2.4.0", self.skill)
        self.assertIn("FACE CROP PACK", self.skill)
        self.assertIn("@DH001_FACE_FRONT_CLOSE", self.skill)
        self.assertIn("@DH001_FACE_L45_CLOSE", self.skill)
        self.assertIn("@DH001_FACE_R45_CLOSE", self.skill)

    def test_final_image_triage_has_three_explicit_outcomes(self):
        self.assertIn("Final Image Triage", self.combined)
        self.assertIn("APPROVED", self.combined)
        self.assertIn("FACE_REPAIR", self.combined)
        self.assertIn("REGENERATE", self.combined)

    def test_face_repair_is_allowed_only_for_face_only_failure(self):
        self.assertIn("Face Repair Eligibility", self.combined)
        self.assertIn("head angle", self.combined.lower())
        self.assertIn("pose", self.combined.lower())
        self.assertIn("prop", self.combined.lower())
        self.assertIn("REGENERATE", self.improve)

    def test_face_repair_uses_approved_identity_inputs_and_preserves_other_layers(self):
        self.assertIn("IDENTITY_MASTER", self.combined)
        self.assertIn("FACE_CROP_PACK", self.combined)
        self.assertIn("preserve", self.combined.lower())
        self.assertIn("composition", self.combined.lower())
        self.assertIn("pose", self.combined.lower())
        self.assertIn("scene", self.combined.lower())

    def test_face_repair_output_cannot_become_identity_authority_automatically(self):
        self.assertIn("must not automatically become", self.combined.lower())
        self.assertIn("Identity Master", self.combined)
        self.assertIn("APPROVED", self.combined)


if __name__ == "__main__":
    unittest.main()
