import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "shared" / "source-library" / "专业书"


REQUIRED_INDEXES = {
    "导演创作手册.index.md": "导演创作手册.md",
    "市场营销.index.md": "市场营销.md",
    "影视综合技巧-分镜完整整理.index.md": "影视综合技巧-分镜完整整理.md",
    "影视综合技巧.index.md": "影视综合技巧.md",
    "故事片创作.index.md": "故事片创作.md",
    "电影编剧创作指南.index.md": "电影编剧创作指南.md",
    "电视解说词写作.index.md": "电视解说词写作.md",
}

REQUIRED_SECTIONS = [
    "Reference Index",
    "原文：",
    "什么时候读",
    "任务路由",
    "深读",
    "使用边界",
]


class ProfessionalReferenceIndexTests(unittest.TestCase):
    def test_required_professional_indexes_exist(self):
        for index_name in REQUIRED_INDEXES:
            with self.subTest(index=index_name):
                self.assertTrue((SOURCE_DIR / index_name).is_file())

    def test_each_index_points_to_an_existing_original_source(self):
        for index_name, source_name in REQUIRED_INDEXES.items():
            with self.subTest(index=index_name):
                index_path = SOURCE_DIR / index_name
                source_path = SOURCE_DIR / source_name
                content = index_path.read_text(encoding="utf-8")

                self.assertTrue(source_path.is_file())
                self.assertIn(f"`shared/source-library/专业书/{source_name}`", content)

    def test_each_index_has_task_driven_routing_sections(self):
        for index_name in REQUIRED_INDEXES:
            with self.subTest(index=index_name):
                content = (SOURCE_DIR / index_name).read_text(encoding="utf-8")
                for section in REQUIRED_SECTIONS:
                    self.assertIn(section, content)

    def test_indexes_do_not_depend_on_removed_central_router(self):
        for index_name in REQUIRED_INDEXES:
            with self.subTest(index=index_name):
                content = (SOURCE_DIR / index_name).read_text(encoding="utf-8")
                self.assertNotIn("manifests/reference-router.md", content)

    def test_specialized_indexes_are_preferred_over_full_library_loading(self):
        film_index = (SOURCE_DIR / "影视综合技巧.index.md").read_text(encoding="utf-8")
        storyboard_index = (
            SOURCE_DIR / "影视综合技巧-分镜完整整理.index.md"
        ).read_text(encoding="utf-8")
        marketing_index = (SOURCE_DIR / "市场营销.index.md").read_text(encoding="utf-8")

        self.assertIn("分镜任务还应优先使用更轻量的", film_index)
        self.assertIn("不要先加载体量更大的《影视综合技巧》全文", storyboard_index)
        self.assertIn("不要把整本教材默认加载进 marketing skill", marketing_index)


if __name__ == "__main__":
    unittest.main()
