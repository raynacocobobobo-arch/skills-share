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
        cls.revision_text = (SKILL_DIR / "references/revision-control.md").read_text(encoding="utf-8")
        cls.short_text = (SKILL_DIR / "references/short-form-visual-story.md").read_text(encoding="utf-8")

    def test_recovered_version(self):
        self.assertGreaterEqual(parse_version(self.text), (13, 2, 0))

    def test_no_machine_specific_project_path(self):
        self.assertNotIn("~/Desktop/", self.text)
        self.assertNotIn("/Users/", self.text)

    def test_supporting_references_declared_and_exist(self):
        required = [
            "references/revision-control.md",
            "references/dialogue-vo-naturalness.md",
            "references/commissioned-realism.md",
            "references/short-form-visual-story.md",
        ]
        for rel in required:
            self.assertIn(rel, self.text)
            self.assertTrue((SKILL_DIR / rel).exists(), rel)

    def test_revision_modes_and_minimum_change(self):
        for token in ["新写", "大改", "局部改", "诊断", "格式化", "最小改动"]:
            self.assertIn(token, self.text)
        self.assertRegex(self.text, r"用户.*修改.*默认.*不是.*重写")

    def test_soft_approval_and_delta_only_revision_are_locked(self):
        for token in ["好很多了", "大概意思对了", "delta-only"]:
            self.assertIn(token, self.revision_text)
        self.assertIn("working baseline", self.revision_text)
        self.assertIn("reopen only the named problem", self.revision_text)

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

    def test_general_causality_and_hard_flaw_rules(self):
        self.assertIn("But / Therefore", self.text)
        self.assertIn("硬伤先删后解释", self.text)
        self.assertIn("不可逆困境六问", self.text)
        for token in ["为什么偏偏是这个人", "为什么别人不能解决", "第三方案"]:
            self.assertIn(token, self.text)

    def test_reference_work_is_abstracted_not_reskinned(self):
        self.assertIn("参考作品只抽元模型", self.text)
        self.assertIn("角色换皮", self.text)
        self.assertIn("欲望与阻力", self.text)
        self.assertIn("信息差", self.text)

    def test_action_water_filter_and_meaning_shift(self):
        self.assertIn("动作删水器", self.text)
        self.assertIn("意义变化", self.text)
        self.assertIn("setup/payoff", self.text)

    def test_short_form_visual_story_contract(self):
        for token in [
            "1–5 minute",
            "charged situation",
            "Information budget",
            "Montage must create a third meaning",
            "Repetition and meaning shift",
            "Visual action filter",
            "Large background must participate in the story",
        ]:
            self.assertIn(token, self.short_text)
        self.assertIn("references/short-form-visual-story.md", self.text)


if __name__ == "__main__":
    unittest.main()
