import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_SKILL = (
    ROOT
    / "plugins"
    / "hermes-skills"
    / "skills"
    / "hermes-digital-human-character-card"
    / "SKILL.md"
)


class DigitalHumanCharacterCardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = CARD_SKILL.read_text(encoding="utf-8") if CARD_SKILL.exists() else ""

    def test_character_card_is_lightweight_staged_identity_skill(self):
        self.assertTrue(CARD_SKILL.exists())
        self.assertIn("name: hermes-digital-human-character-card", self.card)
        self.assertIn("version: 1.3.0", self.card)
        self.assertIn("STAGED MODE", self.card)
        self.assertIn("DIRECT MODE", self.card)

    def test_default_staged_flow_stops_after_face_for_user_review(self):
        self.assertIn("FACE_3VIEW_SHEET", self.card)
        self.assertIn("正脸 / 左45° / 右45°", self.card)
        self.assertIn("是否继续生成全身三视图", self.card)
        self.assertIn("BODY_3VIEW_SHEET", self.card)
        self.assertIn("正面 / 侧面 / 背面", self.card)
        self.assertIn("是否继续换衣服或生成内容图", self.card)

    def test_direct_mode_can_start_from_face_or_body_without_previous_steps(self):
        self.assertIn("只做面部三视图", self.card)
        self.assertIn("只做全身三视图", self.card)
        self.assertIn("不要求补跑前置步骤", self.card)

    def test_profile_is_optional_not_a_required_deliverable(self):
        self.assertIn("FACTUAL PROFILE", self.card)
        self.assertIn("可选", self.card)
        self.assertIn("不是必交付项", self.card)
        self.assertNotIn("exactly three final deliverables", self.card)

    def test_original_source_remains_primary_identity_evidence(self):
        self.assertIn("原始上传图是第一身份依据", self.card)
        self.assertIn("generated output", self.card)
        self.assertIn("不得静默替代 SOURCE", self.card)

    def test_normal_three_view_is_simple_and_atomic_is_recovery_only(self):
        self.assertIn("NORMAL THREE-VIEW", self.card)
        self.assertIn("一次生成一张三视图 sheet", self.card)
        self.assertIn("ATOMIC FALLBACK", self.card)
        self.assertIn("仅在三视图生成失败时启用", self.card)
        self.assertIn("不是默认流程", self.card)

    def test_handoff_points_to_xhs_content_production(self):
        self.assertIn("hermes-creative-digital-human", self.card)
        self.assertIn("换装", self.card)
        self.assertIn("姿势", self.card)
        self.assertIn("环境合成", self.card)


if __name__ == "__main__":
    unittest.main()
