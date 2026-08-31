"""Agent that assesses the plan against basic compliance heuristics."""

from ai_compliance_agent.state import WorkflowState, append_history, ensure_defaults, flag_gap


def compliance_agent(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    if updated.get("compliance_findings"):
        append_history(
            updated,
            "ComplianceAgent retained evidence-backed control findings from DocumentReviewer.",
        )
        return updated
    heuristics = [
        ("change", "Change management approvals missing."),
        ("asset", "Asset inventory linkage unclear."),
        ("incident", "Incident response alignment required."),
    ]
    artifacts = updated.get("artifacts", [])
    plan_text = "\n".join(artifact.get("content", "") for artifact in artifacts)
    lower = plan_text.lower()
    for keyword, gap in heuristics:
        if keyword not in lower:
            flag_gap(updated, gap)
    if not updated.get("compliance_gaps"):
        append_history(updated, "ComplianceAgent found no obvious gaps.")
    return updated
