import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "hermes-skills" / "skills" / "hermes-film-故事片创作"
SKILL_PATH = SKILL_DIR / "SKILL.md"


def parse_version(text: str) -> tuple[int, int, int]:
    match = re.search(r"^version:\s*([0-9]+)\.([0-9]+)\.([0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise AssertionError("Story Skill must declare semantic version X.Y.Z")
    return tuple(int(part) for part in match.groups())


class StorySkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_PATH.read_text(encoding="utf-8")

    def test_recovered_version(self):
        self.assertGreaterEqual(parse_version(self.text), (13, 1, 0))

    def test_no_machine_specific_project_path(self):
        self.assertNotIn("~/Desktop/", self.text)
        self.assertNotIn("/Users/", self.text)

    def test_supporting_references_declared_and_exist(self):
        required = [
            "references/revision-control.md",
            "references/dialogue-vo-naturalness.md",
            "references/commissioned-realism.md",
        ]
        for rel in required:
            self.assertIn(rel, self.text)
            self.assertTrue((SKILL_DIR / rel).exists(), rel)

    def test_revision_modes_and_minimum_change(self):
        for token in ["新写", "大改", "局部改", "诊断", "格式化", "最小改动"]:
            self.assertIn(token, self.text)
        self.assertRegex(self.text, r"用户.*修改.*默认.*不是.*重写")

    def test_source_priority_and_fact_states(self):
        self.assertIn("信息源优先级", self.text)
        for state in ["LOCKED", "CONFIRMED", "TENTATIVE", "CONFLICT", "INFERRED", "DO_NOT_INVENT"]:
            self.assertIn(state, self.text)

    def test_templates_are_optional_tools(self):
        self.assertIn("可选工具", self.text)
        self.assertIn("15 节拍", self.text)
        self.assertIn("英雄之旅", self.text)
        self.assertRegex(self.text, r"不.*强制.*套")

    def test_referential_integrity_is_required(self):
        self.assertIn("引用完整性", self.text)
        for token in ["重命名", "重编号", "合并", "删除"]:
            self.assertIn(token, self.text)

    def test_dialogue_and_vo_contract(self):
        self.assertIn("人话五检", self.text)
        self.assertIn("旁白只承担", self.text)
        self.assertIn("画面", self.text)
        self.assertIn("复读", self.text)

    def test_commissioned_realism_contract(self):
        self.assertIn("真实原型", self.text)
        self.assertIn("DO_NOT_INVENT", self.text)
        self.assertIn("权限", self.text)
        self.assertIn("非职业演员", self.text)


if __name__ == "__main__":
    unittest.main()
