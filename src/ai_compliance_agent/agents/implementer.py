"""Implementation agent that drafts a compliance action plan."""

from ai_compliance_agent.state import (
    WorkflowState,
    add_artifact,
    ensure_defaults,
    new_artifact,
)


def implementer(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    tasks = updated.get("tasks", [])
    if not tasks:
        return updated

    bullet_plan = "\n".join(f"- {task}" for task in tasks)
    content = (
        "Compliance Implementation Plan\n"
        "==============================\n"
        f"Request: {updated.get('request', '')}\n\n"
        "Task Breakdown:\n"
        f"{bullet_plan}\n"
        "\nOwners should provide evidence for each control and document remediation windows."
    )
    artifact = new_artifact(owner="Implementer", content=content)
    return add_artifact(updated, artifact)
