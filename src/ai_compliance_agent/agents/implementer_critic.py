"""Critic for the implementer agent."""

from ai_compliance_agent.state import (
    Artifact,
    WorkflowState,
    append_history,
    approve_artifact,
    ensure_defaults,
    request_revision,
)


def implementer_critic(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    artifacts = updated.get("artifacts", [])
    reviewed: list[Artifact] = []
    for artifact in artifacts:
        if artifact.get("owner") != "Implementer":
            reviewed.append(artifact)
            continue

        normalized = artifact.get("content", "").lower()
        if "evidence" not in normalized or "remediation" not in normalized:
            note = (
                "Implementation plan must mention evidence collection and remediation tracking."
            )
            reviewed.append(request_revision(artifact, note))
            append_history(updated, "ImplementerCritic requested revisions.")
        else:
            reviewed.append(approve_artifact(artifact))
            append_history(updated, "ImplementerCritic approved plan.")
    updated["artifacts"] = reviewed
    return updated
