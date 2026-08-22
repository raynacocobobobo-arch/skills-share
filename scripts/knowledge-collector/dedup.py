"""Hermes knowledge collector deduplication interface.

MVP implementation keeps the rules explicit:
1. source_id check
2. content hash check
3. semantic similarity extension point
"""


def check_source(index, source_id):
    return source_id in index


def check_hash(index, content_hash):
    return any(item.get("content_hash") == content_hash for item in index.values())


def should_collect(index, source_id, content_hash=None):
    if check_source(index, source_id):
        return False
    if content_hash and check_hash(index, content_hash):
        return False
    return True
