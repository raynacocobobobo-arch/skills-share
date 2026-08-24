import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class CanonicalAIRoutingTests(unittest.TestCase):
    def test_old_image_prompt_skill_path_is_gone(self):
        old_skill = ROOT / "plugins/hermes-skills/skills/hermes-film-AI绘画提示词/SKILL.md"
        self.assertFalse(old_skill.exists())

    def test_web_router_uses_split_image_and_film_skills(self):
        router = (ROOT / "manifests/web-chatgpt-router.md").read_text(encoding="utf-8")
        self.assertIn("plugins/hermes-skills/skills/hermes-image-prompt-design/SKILL.md", router)
        self.assertIn("plugins/hermes-skills/skills/hermes-film-ai-production/SKILL.md", router)
        self.assertIn("hermes-image-prompt-design", router)
        self.assertIn("hermes-film-ai-production", router)
        self.assertNotIn("plugins/hermes-skills/skills/hermes-film-AI绘画提示词/SKILL.md", router)

    def test_ai_short_film_workflow_dispatches_video_to_film_skill(self):
        workflow = (
            ROOT / "plugins/hermes-workflows/workflows/ai-short-film-production/WORKFLOW.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Primary skill: `hermes-film-ai-production`", workflow)
        self.assertIn("Supporting skill: `hermes-image-prompt-design`", workflow)
        self.assertNotIn("Primary skill: `AI绘画提示词`", workflow)

    def test_ai_short_film_phases_use_canonical_split(self):
        phases = (
            ROOT / "plugins/hermes-workflows/workflows/ai-short-film-production/phases.md"
        ).read_text(encoding="utf-8")
        self.assertIn("hermes-film-ai-production", phases)
        self.assertIn("hermes-image-prompt-design", phases)
        self.assertNotIn("AI绘画提示词", phases)

    def test_watchlist_skill_targets_use_canonical_split(self):
        watchlist = (
            ROOT / "plugins/hermes-skills/skills/hermes-knowledge-scout/config/watchlist.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("ai_image:\n    - hermes-image-prompt-design", watchlist)
        self.assertIn("ai_video:\n    - hermes-film-ai-production", watchlist)
        self.assertNotIn("    - AI绘画提示词", watchlist)


if __name__ == "__main__":
    unittest.main()
