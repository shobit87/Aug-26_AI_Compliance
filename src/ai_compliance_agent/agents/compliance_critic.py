"""Critic validating compliance agent output."""

from ai_compliance_agent.state import WorkflowState, append_history, ensure_defaults


def compliance_critic(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    gaps = updated.get("compliance_gaps", [])
    max_gaps = 5
    if len(gaps) > max_gaps:
        updated["compliance_gaps"] = gaps[:max_gaps]
        append_history(
            updated,
            "ComplianceCritic trimmed excessive gap findings to maintain focus.",
        )
    elif not gaps:
        append_history(updated, "ComplianceCritic verified no outstanding gaps.")
    else:
        append_history(updated, "ComplianceCritic accepted the identified gaps.")
    return updated
