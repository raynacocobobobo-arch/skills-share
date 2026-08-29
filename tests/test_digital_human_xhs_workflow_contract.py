import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-creative-digital-human"
SKILL = SKILL_DIR / "SKILL.md"
POSE_LIBRARY = SKILL_DIR / "references" / "xhs-pose-shot-library.md"


class DigitalHumanXhsWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""

    def test_skill_is_xhs_content_production_v3(self):
        self.assertTrue(SKILL.exists())
        self.assertIn("version: 3.0.1", self.skill)
        self.assertIn("小红书", self.skill)
        self.assertIn("真人感内容生产", self.skill)

    def test_workflow_supports_staged_and_direct_entry(self):
        self.assertIn("STAGED MODE", self.skill)
        self.assertIn("DIRECT MODE", self.skill)
        self.assertIn("可以从任意模块直接开始", self.skill)
        self.assertIn("不要求补跑前置步骤", self.skill)

    def test_core_modules_are_identity_outfit_pose_shot_scene(self):
        for module in ["IDENTITY", "OUTFIT", "POSE", "SHOT", "SCENE"]:
            self.assertIn(module, self.skill)
        self.assertIn("按当前请求组合需要的模块", self.skill)

    def test_ambiguous_next_step_does_not_invent_outfit_or_content(self):
        self.assertIn("AMBIGUOUS NEXT-STEP GATE", self.skill)
        self.assertIn("下一步", self.skill)
        self.assertIn("不得自行选择 OUTFIT", self.skill)
        self.assertIn("不得直接生成内容图", self.skill)
        self.assertIn("服装参考图或穿搭描述", self.skill)
        self.assertIn("环境 / 姿势 / 镜头", self.skill)

    def test_direct_scene_composite_accepts_face_body_and_environment(self):
        self.assertIn("人物面部图 + 人物全身图 + 环境照片", self.skill)
        self.assertIn("直接进入 SCENE", self.skill)
        for item in ["透视", "人物尺度", "接地", "光向", "色温", "景深", "遮挡"]:
            self.assertIn(item, self.skill)

    def test_outfit_and_pose_can_be_changed_without_rebuilding_identity(self):
        self.assertIn("换装", self.skill)
        self.assertIn("改姿势", self.skill)
        self.assertIn("保持人物身份和体型", self.skill)
        self.assertIn("无需重新建立人物卡", self.skill)

    def test_original_user_photos_are_primary_identity_anchor(self):
        self.assertIn("原始人物照片优先", self.skill)
        self.assertIn("生成图只作为辅助参考", self.skill)
        self.assertIn("人物跑偏时重新挂回原始人物图", self.skill)

    def test_pose_and_shot_library_is_optional_and_natural_language_friendly(self):
        self.assertIn("xhs-pose-shot-library.md", self.skill)
        self.assertIn("不要求用户记编号", self.skill)
        self.assertIn("自然语言", self.skill)
        self.assertTrue(POSE_LIBRARY.exists(), "pose/shot reference library must exist")

    def test_skill_can_plan_coherent_multi_image_xhs_sets(self):
        self.assertIn("4–6 张", self.skill)
        self.assertIn("同一套穿搭", self.skill)
        self.assertIn("同一环境", self.skill)
        self.assertIn("镜头变化", self.skill)
        self.assertIn("姿势变化", self.skill)

    def test_recovery_is_lightweight_not_default_state_machine(self):
        self.assertIn("LIGHT RECOVERY", self.skill)
        self.assertIn("先回到原始人物图", self.skill)
        self.assertIn("复杂 recovery 不是默认流程", self.skill)
        self.assertNotIn("Digital Human Session State", self.skill)
        self.assertNotIn("Generation Preflight", self.skill)
        self.assertNotIn("Identity Anchor Card", self.skill)


if __name__ == "__main__":
    unittest.main()
