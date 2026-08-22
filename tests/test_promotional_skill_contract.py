import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-film-宣传片创作" / "SKILL.md"


def parse_version(text: str) -> tuple[int, int, int]:
    match = re.search(r"^version:\s*([0-9]+)\.([0-9]+)\.([0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise AssertionError("Promotional film Skill must declare semantic version X.Y.Z")
    return tuple(int(part) for part in match.groups())


class PromotionalFilmSkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_PATH.read_text(encoding="utf-8")

    def test_current_version(self):
        self.assertGreaterEqual(parse_version(self.text), (3, 2, 0))

    def test_revision_modes_and_minimum_change(self):
        for token in ["A 从零创作", "B 结构重构", "C 基于现稿改稿", "D 局部润色", "E 既有 Word 修改"]:
            self.assertIn(token, self.text)
        self.assertIn("最小必要改动", self.text)

    def test_locked_content_is_preserved(self):
        for token in ["LOCKED", "CONFIRMED", "TENTATIVE", "CONFLICT"]:
            self.assertIn(token, self.text)
        self.assertRegex(self.text, r"LOCKED.*不.*自动重写")

    def test_core_numbers_may_be_spoken(self):
        self.assertIn("禁止机械执行“旁白不能出现数字”", self.text)
        self.assertIn("A级：必须听见", self.text)
        self.assertIn("是否值得占用听觉带宽", self.text)

    def test_time_and_information_budget_is_required(self):
        self.assertIn("时长与信息预算（强制）", self.text)
        for token in ["总时长", "目标旁白字数区间", "A级口播事实/数据", "B级字幕信息", "C级删减信息"]:
            self.assertIn(token, self.text)

    def test_existing_word_requires_doc_reviewer(self):
        self.assertIn("doc-reviewer", self.text)
        self.assertIn("原 Word 副本", self.text)
        self.assertIn("不能从空白文档重建", self.text)


if __name__ == "__main__":
    unittest.main()
