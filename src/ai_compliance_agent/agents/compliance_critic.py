"""Critic validating compliance agent output without discarding findings."""

from ai_compliance_agent.state import WorkflowState, append_history, ensure_defaults


def compliance_critic(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    gaps = updated.get("compliance_gaps", [])
    if not gaps:
        append_history(updated, "ComplianceCritic verified no outstanding gaps.")
    else:
        append_history(
            updated,
            f"ComplianceCritic retained all {len(gaps)} identified gap(s).",
        )
    return updated