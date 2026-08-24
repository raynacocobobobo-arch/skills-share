import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
FRAMEWORK_ROOT = ROOT / "shared" / "creative-framework"


REQUIRED_FRAMEWORKS = [
    "film/screenwriting-directing.md",
    "film/storyboard-directing.md",
    "film/visual-language-directing.md",
    "film/documentary.md",
    "promo/corporate-film.md",
    "marketing/strategy.md",
]


class CreativeReferenceRoutingTests(unittest.TestCase):
    def test_required_creative_frameworks_exist(self):
        for relative_path in REQUIRED_FRAMEWORKS:
            with self.subTest(path=relative_path):
                self.assertTrue((FRAMEWORK_ROOT / relative_path).is_file())

    def test_framework_index_registers_canonical_assets(self):
        index = FRAMEWORK_ROOT / "README.md"
        self.assertTrue(index.is_file())
        content = index.read_text(encoding="utf-8")

        for relative_path in REQUIRED_FRAMEWORKS:
            with self.subTest(path=relative_path):
                self.assertIn(f"`{relative_path}`", content)

        self.assertIn("shared/source-library/专业书/*.index.md", content)
        self.assertIn("Skill = entry", content)

    def test_film_decision_map_does_not_point_to_missing_framework(self):
        decision_map = FRAMEWORK_ROOT / "film" / "creative-decision-map.md"
        content = decision_map.read_text(encoding="utf-8")
        self.assertIn("visual-language-directing.md", content)
        self.assertTrue(
            (decision_map.parent / "visual-language-directing.md").is_file(),
            "creative-decision-map.md references a missing framework",
        )

    def test_story_framework_routing_targets_existing_frameworks(self):
        routing = (
            ROOT
            / "plugins/hermes-skills/skills/hermes-film-故事片创作/references/creative-framework-routing.md"
        )
        self.assertTrue(routing.is_file())
        content = routing.read_text(encoding="utf-8")

        for relative_path in [
            "shared/creative-framework/film/screenwriting-directing.md",
            "shared/creative-framework/film/storyboard-directing.md",
        ]:
            with self.subTest(path=relative_path):
                self.assertIn(relative_path, content)
                self.assertTrue((ROOT / relative_path).is_file())

    def test_framework_layer_does_not_restore_central_reference_router(self):
        for path in FRAMEWORK_ROOT.rglob("*.md"):
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("manifests/reference-router.md", content)


if __name__ == "__main__":
    unittest.main()
