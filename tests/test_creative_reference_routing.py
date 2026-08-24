import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


FRAMEWORKS = [
    "shared/creative-framework/film/visual-language-directing.md",
    "shared/creative-framework/film/documentary.md",
    "shared/creative-framework/promo/corporate-film.md",
    "shared/creative-framework/marketing/strategy.md",
]

SKILL_ROUTES = {
    "plugins/hermes-skills/skills/hermes-film-宣传片创作/SKILL.md": [
        "shared/creative-framework/promo/corporate-film.md",
        "shared/source-library/专业书/电视解说词写作.index.md",
    ],
    "plugins/hermes-skills/skills/hermes-film-故事片创作/SKILL.md": [
        "references/creative-framework-routing.md",
        "shared/source-library/专业书/故事片创作.index.md",
    ],
    "plugins/hermes-skills/skills/hermes-film-影视分镜/SKILL.md": [
        "shared/creative-framework/film/storyboard-directing.md",
        "shared/source-library/专业书/影视综合技巧-分镜完整整理.index.md",
    ],
    "plugins/hermes-skills/skills/hermes-film-石化简易分镜/SKILL.md": [
        "shared/creative-framework/film/storyboard-directing.md",
        "shared/source-library/专业书/影视综合技巧-分镜完整整理.index.md",
    ],
    "plugins/hermes-skills/skills/hermes-business-marketing-copilot/SKILL.md": [
        "shared/creative-framework/marketing/strategy.md",
        "shared/source-library/专业书/市场营销.index.md",
    ],
    "plugins/hermes-skills/skills/hermes-business-marketing-plan/SKILL.md": [
        "shared/creative-framework/marketing/strategy.md",
        "shared/source-library/专业书/市场营销.index.md",
    ],
}


class CreativeReferenceRoutingTests(unittest.TestCase):
    def test_required_creative_frameworks_exist(self):
        for relative_path in FRAMEWORKS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_film_decision_map_does_not_point_to_missing_framework(self):
        decision_map = ROOT / "shared/creative-framework/film/creative-decision-map.md"
        content = decision_map.read_text(encoding="utf-8")
        self.assertIn("visual-language-directing.md", content)
        self.assertTrue(
            (decision_map.parent / "visual-language-directing.md").is_file(),
            "creative-decision-map.md references a missing framework",
        )

    def test_target_skills_own_their_reference_routing(self):
        for skill_path, required_routes in SKILL_ROUTES.items():
            with self.subTest(skill=skill_path):
                content = (ROOT / skill_path).read_text(encoding="utf-8")
                for route in required_routes:
                    self.assertIn(route, content)

    def test_routing_does_not_restore_central_reference_router(self):
        for skill_path in SKILL_ROUTES:
            with self.subTest(skill=skill_path):
                content = (ROOT / skill_path).read_text(encoding="utf-8")
                self.assertNotIn("manifests/reference-router.md", content)


if __name__ == "__main__":
    unittest.main()
