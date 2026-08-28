# Registry Auto-Sync V2 Design

## Goal

Make `SKILL.md` the single source of truth. Keep `manifests/skill-registry.json` as a generated catalog for routing/tooling, but remove the need for humans or agents to remember to edit it manually.

## Design

1. `scripts/validate-skills.py` remains the canonical registry generator and validator.
2. A dedicated GitHub Actions workflow runs on pushes to non-main branches when skill metadata or the validator changes. It regenerates the registry and commits the generated file back to the same branch only when content changed.
3. The normal validation workflow validates skill structure/version rules and regenerates the registry for inspection, but no longer fails solely because the committed registry was stale at workflow start. Registry drift is repaired by the auto-sync workflow rather than treated as a human-maintained invariant.
4. The auto-sync commit is guarded against loops: a second workflow run sees no diff and exits without committing.
5. `main` remains protected by PR flow. The sync workflow never writes directly to `main`.
6. Router semantics remain independent: routing logic decides which skill to use; registry remains a machine-readable catalog/path index.

## Safety constraints

- Do not introduce a database or second manifest format.
- Do not change existing skill routing semantics.
- Preserve version downgrade protection and repository validation.
- Auto-sync may write only `manifests/skill-registry.json` on the triggering non-main branch.
- If generation/validation fails, do not commit anything.

## Verification

The final PR head must receive the repository's required `validate` check before merge.
