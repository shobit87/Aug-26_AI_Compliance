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
    retry_count = updated.get("implementation_retries", 0)
    quality_clause = (
        "Owners must retain approval evidence and track remediation through closure."
        if retry_count
        else "Owners should document assigned owners and target dates."
    )
    content = (
        "Compliance Implementation Plan\n"
        "==============================\n"
        f"Request: {updated.get('request', '')}\n\n"
        "Task Breakdown:\n"
        f"{bullet_plan}\n"
        f"\n{quality_clause}"
    )
    artifact = new_artifact(owner="Implementer", content=content)
    updated["artifacts"] = [
        item for item in updated.get("artifacts", []) if item.get("owner") != "Implementer"
    ]
    return add_artifact(updated, artifact)
