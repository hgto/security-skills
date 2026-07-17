import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_opencode_config_loads_repo_skills():
    config = json.loads((ROOT / "opencode.json").read_text())

    assert config["$schema"] == "https://opencode.ai/config.json"
    assert config["skills"]["paths"] == ["skills"]


def test_settle_skills_use_opencode_workflow_and_pr_description():
    security_review = (ROOT / "skills/security-review/SKILL.md").read_text()
    settle_security = (ROOT / "skills/settle-security/SKILL.md").read_text()
    settle_draft_pr = (ROOT / "skills/settle-draft-pr/SKILL.md").read_text()

    assert "name: security-review" in security_review
    assert "validator confidence below 8/10" in security_review
    assert "Never publish it as a GitHub comment or review" in security_review
    assert "load and execute `security-review`" in settle_security
    assert "load and execute `security-review`" in settle_draft_pr
    assert "Do not post a PR comment" in settle_security
    assert "## Security review" in settle_draft_pr
    assert "Never post the security result as a PR comment or review" in settle_draft_pr
    assert "/security-review" not in settle_security
    assert "/security-review" not in settle_draft_pr
