# Capability Extraction Execution Flow

## Purpose

Creator Distillation must not directly map Creator content to existing Skills.

The required intermediate layer is Capability Extraction.

## Execution Pipeline

```
Creator Source
↓
Methods Extraction
↓
Capability Extraction
↓
Capability Map
↓
Skill Impact Assessment
↓
Implementation
```

## Capability Map Output

Each extracted capability should define:

```yaml
name:
category:
problem_solved:
reusable:
workflow:
artifacts:
candidate_skills:
decision:
  - enhance_existing
  - create_new
```

## Decision Rules

Enhance existing Skill when:

- the capability overlaps with an existing reusable workflow
- the domain implementation can extend the current Skill

Create new Skill only when:

- existing Skills cannot cover it
- the workflow is repeatedly reusable
- it creates measurable value

## Example

A Creator teaching multiple ChatGPT Work workflows should not become:

```
Creator
↓
One Skill
```

Instead:

```
Creator
↓
Capabilities
├── Strategy Workflow
├── Meeting Preparation Workflow
├── Content Creation Workflow
└── AI Building Workflow
↓
Multiple Skill decisions
```
