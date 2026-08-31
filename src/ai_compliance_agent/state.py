"""Typed state helpers shared across LangGraph nodes."""

from __future__ import annotations

from typing import Any, List, Literal, Sequence, TypedDict


ArtifactStatus = Literal["draft", "needs_revision", "approved"]


class Artifact(TypedDict, total=False):
    owner: str
    content: str
    status: ArtifactStatus
    critic_notes: List[str]


class WorkflowState(TypedDict, total=False):
    request: str
    document_path: str | None
    document_text: str | None
    original_document_name: str | None
    original_document_bytes: bytes | None
    document_tone: str | None
    grammar_score: float | None
    document_recommendations: List[str]
    corrected_document: str | None
    analysis_summary: str | None
    analysis_mode: str | None
    compliance_findings: List[dict[str, Any]]
    implementation_retries: int
    tasks: List[str]
    artifacts: List[Artifact]
    compliance_gaps: List[str]
    documentation: str | None
    history: List[str]


def ensure_defaults(state: WorkflowState) -> WorkflowState:
    state.setdefault("tasks", [])
    state.setdefault("artifacts", [])
    state.setdefault("compliance_gaps", [])
    state.setdefault("documentation", None)
    state.setdefault("history", [])
    state.setdefault("document_path", None)
    state.setdefault("document_text", None)
    state.setdefault("original_document_name", None)
    state.setdefault("original_document_bytes", None)
    state.setdefault("document_tone", None)
    state.setdefault("grammar_score", None)
    state.setdefault("document_recommendations", [])
    state.setdefault("corrected_document", None)
    state.setdefault("analysis_summary", None)
    state.setdefault("analysis_mode", None)
    state.setdefault("compliance_findings", [])
    state.setdefault("implementation_retries", 0)
    return state


def append_history(state: WorkflowState, entry: str) -> WorkflowState:
    ensure_defaults(state)
    state["history"].append(entry)
    return state


def update_tasks(state: WorkflowState, tasks: Sequence[str]) -> WorkflowState:
    ensure_defaults(state)
    state["tasks"] = list(tasks)
    append_history(state, "TaskPlanner updated tasks.")
    return state


def new_artifact(owner: str, content: str) -> Artifact:
    return {
        "owner": owner,
        "content": content,
        "status": "draft",
        "critic_notes": [],
    }


def add_artifact(state: WorkflowState, artifact: Artifact) -> WorkflowState:
    ensure_defaults(state)
    state["artifacts"].append(artifact)
    append_history(state, f"{artifact['owner']} produced artifact.")
    return state


def request_revision(artifact: Artifact, note: str) -> Artifact:
    updated = dict(artifact)
    updated["status"] = "needs_revision"
    updated.setdefault("critic_notes", [])
    updated["critic_notes"] = [*updated["critic_notes"], note]
    return updated


def approve_artifact(artifact: Artifact) -> Artifact:
    updated = dict(artifact)
    updated["status"] = "approved"
    return updated


def flag_gap(state: WorkflowState, gap: str) -> WorkflowState:
    ensure_defaults(state)
    if gap not in state["compliance_gaps"]:
        state["compliance_gaps"].append(gap)
        append_history(state, f"ComplianceAgent recorded gap: {gap}")
    return state


def set_documentation(state: WorkflowState, doc: str) -> WorkflowState:
    ensure_defaults(state)
    state["documentation"] = doc
    append_history(state, "DocumentationAgent synthesized final report.")
    return state
