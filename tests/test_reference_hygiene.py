import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILM_SKILLS = ROOT / "plugins" / "hermes-skills" / "skills"
STORY_REFS = FILM_SKILLS / "hermes-film-故事片创作" / "references"
SHARED_FILM = ROOT / "shared" / "film-methodology"


class ReferenceHygieneTests(unittest.TestCase):
    def test_gdevelop_cache_not_copied_into_film_references(self):
        polluted = []
        for skill_dir in FILM_SKILLS.glob("hermes-film-*"):
            polluted.extend(skill_dir.rglob("GDEVELOP_OFFICIAL_DOC_CACHE.md"))
        polluted.extend(SHARED_FILM.rglob("GDEVELOP_OFFICIAL_DOC_CACHE.md"))
        self.assertEqual(polluted, [], f"GDevelop cache leaked into film references: {polluted}")

    def test_story_references_do_not_contain_promotional_reference_bundle(self):
        polluted = [path for path in STORY_REFS.rglob("*.md") if path.name.startswith("宣传片创作-")]
        self.assertEqual(polluted, [], f"Promotional-film references leaked into Story Skill: {polluted}")


if __name__ == "__main__":
    unittest.main()
