"""Coordinator agent that seeds the workflow history."""

from ai_compliance_agent.state import WorkflowState, append_history, ensure_defaults


def coordinator(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    request = updated.get("request", "")
    summary = f"Coordinator received request: {request[:80]}"
    append_history(updated, summary)
    return updated
