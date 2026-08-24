# Main Reconciliation — 2026-08-24

Purpose: reconcile the canonical `main` branch before recovering changes from stale feature branches.

Observed drift:

- `plugins/hermes-skills/skills/` contains skills added after the last committed registry generation.
- `manifests/skill-registry.json` is therefore expected to differ from fresh validator output.
- No stale feature branch should be merged until the current canonical branch validates cleanly.

Repair rule:

1. Run the repository validator against the current canonical tree.
2. Regenerate `manifests/skill-registry.json` from that tree.
3. Require regression tests and registry consistency checks to pass.
4. Keep this reconciliation limited to canonical-state repair; do not recover unrelated feature-branch changes in this PR.
