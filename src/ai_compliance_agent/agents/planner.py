"""Planning agent that decomposes the request into actionable tasks."""

from __future__ import annotations

from typing import List

from ai_compliance_agent.state import WorkflowState, update_tasks


def task_planner(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    request = updated.get("request", "").lower()
    tasks: List[str] = [
        "Clarify compliance objective and success metrics",
        "Gather regulatory controls and organizational policies",
        "Map controls to product architecture",
        "Propose remediation or mitigation steps",
        "Produce reviewer-ready documentation",
    ]
    if "soc" in request:
        tasks.insert(1, "Align tasks to SOC2 trust service criteria")
    if "gdpr" in request:
        tasks.insert(1, "Validate lawful bases for data processing")
    if "hipaa" in request:
        tasks.insert(1, "Assess PHI data flows and safeguards")

    deduped = list(dict.fromkeys(tasks))  # keeps order
    return update_tasks(updated, deduped)
