# Generation Feedback Loop

## Purpose

Convert generation failures into reusable improvement knowledge.

## Feedback Record

Each failed or revised generation should record:

```yaml
generation_id:
problem_category:
problem_description:
root_cause:
solution:
future_rule:
```

## Problem Categories

### Identity

Examples:

- face drift
- age drift
- inconsistent features

### Geometry

Examples:

- wrong perspective
- incorrect body ratio
- unnatural pose

### Lighting

Examples:

- wrong shadow direction
- inconsistent exposure
- color mismatch

### Realism

Examples:

- artificial skin
- pasted appearance
- incorrect depth

## Learning Rule

Repeated corrections should become updated Skill rules or reference examples.

The objective is continuous improvement of the digital human production pipeline.
