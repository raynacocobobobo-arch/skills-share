"""Hermes Knowledge Collector CLI MVP."""

from discovery import discover_sources


def collect(watchlist):
    sources = discover_sources(watchlist)
    return {
        "sources_found": len(sources),
        "status": "discovery_complete",
    }


if __name__ == "__main__":
    print("Hermes Knowledge Collector MVP")
