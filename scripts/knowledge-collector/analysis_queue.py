"""Hermes knowledge analysis queue.

Collected assets enter analysis only after signal filtering.
"""


def should_analyze(asset):
    knowledge_types = asset.get("knowledge_type", [])
    targets = {
        "workflow",
        "methodology",
        "prompt_method",
    }
    return bool(targets.intersection(set(knowledge_types)))


def create_analysis_task(asset):
    return {
        "source_id": asset.get("source_id"),
        "task": "knowledge_extraction",
        "status": "pending",
    }
