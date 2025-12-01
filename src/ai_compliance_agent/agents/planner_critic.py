"""Critic that validates planner output before downstream execution."""

from ai_compliance_agent.state import WorkflowState, append_history, ensure_defaults


def planner_critic(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    tasks = updated.get("tasks", [])
    if len(tasks) < 3:
        fallback = [
            "Baseline compliance gap assessment",
            "Control mapping",
            "Documentation prep",
        ]
        updated["tasks"] = fallback
        append_history(
            updated,
            "PlannerCritic injected fallback tasks because planner output was insufficient.",
        )
    else:
        append_history(updated, "PlannerCritic approved planner output.")
    return updated
