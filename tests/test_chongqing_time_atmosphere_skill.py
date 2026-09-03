import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/hermes-skills/skills/hermes-creative-chongqing-time-atmosphere/SKILL.md"
SOURCE_MAP = ROOT / "plugins/hermes-skills/skills/hermes-creative-chongqing-time-atmosphere/references/chongqing-time-source-map.md"


class ChongqingTimeAtmosphereSkillTests(unittest.TestCase):
    def test_skill_exists_and_routes_project_phrases(self):
        self.assertTrue(SKILL.is_file())
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("重庆时间，按设定出图", content)
        self.assertIn("核心空间", content)
        self.assertIn("场景气氛图", content)
        self.assertIn("环境母图", content)

    def test_skill_uses_live_project_repository_as_authority(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("raynacocobobobo-arch/lora", content)
        self.assertIn("重庆时间/ACTIVE-DOCS-INDEX.md", content)
        self.assertIn("SCENE-PROMPT-TEMPLATE-V3.md", content)
        self.assertIn("do not rely on an embedded stale canon summary", content)

    def test_core_space_means_dominant_action_geography(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("dominant action geography", content)
        self.assertIn("runtime coverage", content)
        self.assertIn("state-change coverage", content)
        self.assertIn("not a local device room by default", content)

    def test_seedance_rule_is_structural_compression(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("structural compression", content)
        self.assertIn("删噪声，不删身份", content)
        self.assertIn("合并结构，不削平空间", content)

    def test_source_map_declares_live_read_order(self):
        self.assertTrue(SOURCE_MAP.is_file())
        content = SOURCE_MAP.read_text(encoding="utf-8")
        self.assertIn("CURRENT.md", content)
        self.assertIn("CANON-PRECEDENCE-V4.md", content)
        self.assertIn("ACTIVE-DOCS-INDEX.md", content)
        self.assertIn("relevant episode", content)

    def test_chatgpt_router_exposes_skill(self):
        router = (ROOT / "manifests/web-chatgpt-router.md").read_text(encoding="utf-8")
        self.assertIn("hermes-creative-chongqing-time-atmosphere", router)
        self.assertIn("重庆时间，按设定出图", router)


if __name__ == "__main__":
    unittest.main()
