import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNC_WORKFLOW = ROOT / ".github" / "workflows" / "sync-skill-registry.yml"
VALIDATE_WORKFLOW = ROOT / ".github" / "workflows" / "validate-skills.yml"


class RegistryAutoSyncContractTests(unittest.TestCase):
    def test_sync_workflow_exists_and_writes_only_feature_branches(self):
        text = SYNC_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("contents: write", text)
        self.assertIn("branches-ignore:", text)
        self.assertIn("- main", text)
        self.assertIn("plugins/hermes-skills/skills/**", text)

    def test_sync_workflow_regenerates_registry_and_commits_only_when_changed(self):
        text = SYNC_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("python3 scripts/validate-skills.py", text)
        self.assertIn("--write-registry", text)
        self.assertIn("git diff --quiet -- manifests/skill-registry.json", text)
        self.assertIn("git add manifests/skill-registry.json", text)
        self.assertIn("chore: auto-sync skill registry", text)
        self.assertIn("git push", text)

    def test_validation_does_not_require_manual_registry_match(self):
        text = VALIDATE_WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("Require semantic registry match", text)
        self.assertNotIn("--check-registry", text)
        self.assertNotIn("Capture committed registry", text)

    def test_validation_still_checks_versions_and_generates_registry(self):
        text = VALIDATE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("--baseline-registry", text)
        self.assertIn("--write-registry", text)
        self.assertIn("Upload generated registry", text)


if __name__ == "__main__":
    unittest.main()
