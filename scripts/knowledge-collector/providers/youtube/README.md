# YouTube Provider

## Purpose

Collect YouTube knowledge sources into Hermes Knowledge Library.

## Pipeline

```
Video URL
 ↓
Metadata
 ↓
Transcript
 ↓
Normalization
 ↓
Knowledge Filter
 ↓
Analysis Queue
```

## Output

```
metadata.json
transcript.md
source-info.md
```

## Rules

- Keep source traceability.
- Do not analyze during collection.
- Do not store duplicate assets.
