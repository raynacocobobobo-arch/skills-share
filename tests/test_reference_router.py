import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]


ROUTER = ROOT / "manifests" / "reference-router.md"
SOURCE_DIR = ROOT / "shared" / "source-library" / "专业书"


REQUIRED_ROUTER_TERMS = [
    "宣传片",
    "故事片",
    "分镜",
    "解说词",
    "纪录片",
    "营销",
]


REQUIRED_INDEX_SECTIONS = [
    "适用技能",
    "什么时候读",
    "任务",
]


REQUIRED_SKILLS = [
    "hermes-film-宣传片创作",
    "hermes-film-故事片创作",
    "hermes-film-影视分镜",
    "hermes-film-石化简易分镜",
    "hermes-business-marketing-copilot",
    "hermes-business-marketing-plan",
]


def test_reference_router_exists_and_covers_domains():
    assert ROUTER.exists()
    content = ROUTER.read_text(encoding="utf-8")
    for term in REQUIRED_ROUTER_TERMS:
        assert term in content


def test_professional_source_indexes_have_routing_metadata():
    indexes = list(SOURCE_DIR.glob("*.index.md"))
    assert indexes

    for index in indexes:
        content = index.read_text(encoding="utf-8")
        for section in REQUIRED_INDEX_SECTIONS:
            assert section in content, index


def test_target_skills_keep_reference_routing_entry():
    skill_root = ROOT / "plugins" / "hermes-skills" / "skills"

    for skill in REQUIRED_SKILLS:
        skill_file = skill_root / skill / "SKILL.md"
        assert skill_file.exists(), skill_file
        content = skill_file.read_text(encoding="utf-8")
        assert "Reference Routing" in content, skill_file


def test_router_does_not_encourage_full_library_loading():
    content = ROUTER.read_text(encoding="utf-8").lower()
    forbidden = [
        "load all professional books",
        "load entire professional source library",
        "读取全部专业书",
    ]

    for phrase in forbidden:
        assert phrase not in content
