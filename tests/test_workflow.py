"""Regression tests for the LangGraph workflow."""

from ai_compliance_agent.state import ensure_defaults
from ai_compliance_agent.workflow import build_workflow_app


def test_workflow_generates_documentation():
    app = build_workflow_app()
    result = app.invoke({"request": "Create SOC2 change management checklist"})
    ensure_defaults(result)

    assert result.get("tasks"), "Planner should populate tasks."
    assert result.get("documentation"), "Documentation agent should write output."
    assert "Coordinator received request" in " ".join(result["history"])


def test_compliance_critic_limits_gap_volume():
    app = build_workflow_app()
    result = app.invoke({"request": "GDPR + HIPAA gap review"})
    ensure_defaults(result)

    assert len(result["compliance_gaps"]) <= 5


def test_document_reviewer_enriches_state(tmp_path):
    sample = tmp_path / "policy.txt"
    sample.write_text("Change policy outline without enough detail.")
    app = build_workflow_app()
    result = app.invoke(
        {"request": "Review SOC2 change policy", "document_path": str(sample)}
    )
    ensure_defaults(result)

    assert result["document_text"]
    assert result["document_recommendations"]
    assert result["corrected_document"]
    assert result["document_tone"]
    assert result["grammar_score"] is not None
