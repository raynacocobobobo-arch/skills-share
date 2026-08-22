"""Hermes source discovery interface.

Provider-specific discovery is injected later.
"""


def discover_sources(watchlist):
    """Return enabled sources from watchlist."""
    results = []
    for source in watchlist.get("sources", {}).get("youtube", []):
        if source.get("enabled", True):
            results.append(source)
    return results


def create_collection_target(source, item):
    return {
        "platform": source.get("collector"),
        "creator": source.get("name"),
        "item": item,
        "status": "pending",
    }
