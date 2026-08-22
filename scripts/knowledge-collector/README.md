# Hermes Knowledge Collector

## Purpose

MVP execution layer for Hermes external knowledge acquisition.

This layer collects and normalizes external sources. It does not decide skill upgrades.

## Pipeline

```
watchlist.yaml
    ↓
discovery
    ↓
dedup/index check
    ↓
transcript collection
    ↓
metadata generation
    ↓
knowledge-library/raw
```

## Planned Modules

```
knowledge-collector/

cli.py
scheduler.py
discovery.py
dedup.py
transcript.py
storage.py
```

## Rules

- Never duplicate collected assets.
- Keep raw sources immutable.
- Analysis is a separate stage.
