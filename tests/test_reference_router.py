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


ROUTE_CASES = {
    "企业宣传片解说词": ["电视解说词写作", "导演创作手册"],
    "三分钟故事短片结构": ["故事片创作", "电影编剧创作指南"],
    "电影分镜设计": ["影视综合技巧-分镜完整整理"],
    "品牌营销策略": ["市场营销"],
    "纪录片叙事优化": ["导演创作手册", "电视解说词写作"],
}


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


def test_route_contract_cases_have_registered_targets():
    index_names = [p.stem for p in SOURCE_DIR.glob("*.index.md")]
    registered_text = "\n".join(index_names) + "\n" + ROUTER.read_text(encoding="utf-8")

    for _, targets in ROUTE_CASES.items():
        for target in targets:
            assert target in registered_text, target
