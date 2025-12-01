"""Agent that produces stakeholder-friendly documentation."""

from ai_compliance_agent.state import WorkflowState, ensure_defaults, set_documentation


def documentation_agent(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    summary = [
        f"Request: {updated.get('request', '')}",
        "Tasks:",
    ]
    summary.extend(f"- {task}" for task in updated.get("tasks", []))
    summary.append("\nApproved Artifacts:")
    for artifact in updated.get("artifacts", []):
        summary.append(f"- {artifact.get('owner')}: {artifact.get('status')}")
    tone = updated.get("document_tone")
    grammar = updated.get("grammar_score")
    if tone or grammar is not None:
        summary.append("\nDocument Quality:")
        if tone:
            summary.append(f"- Tone: {tone}")
        if grammar is not None:
            summary.append(f"- Grammar Score: {grammar:.2f}")
    recommendations = updated.get("document_recommendations", [])
    if recommendations:
        summary.append("\nDocument Recommendations:")
        summary.extend(f"- {rec}" for rec in recommendations)
    corrected = updated.get("corrected_document")
    if corrected:
        summary.append("\nAI Corrected Document Draft:")
        summary.append(corrected)
    gaps = updated.get("compliance_gaps", [])
    if gaps:
        summary.append("\nOutstanding Gaps:")
        summary.extend(f"- {gap}" for gap in gaps)
    else:
        summary.append("\nOutstanding Gaps: None")
    doc = "\n".join(summary)
    return set_documentation(updated, doc)
