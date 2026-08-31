"""LangGraph workflow wiring coordinator, agents, and critics."""

try:
    from langgraph.graph import END, START, StateGraph
except ImportError:  # pragma: no cover - fallback for environments without LangGraph
    from ai_compliance_agent.langgraph_stub import END, START, StateGraph

from ai_compliance_agent.agents import (
    compliance_agent,
    compliance_critic,
    coordinator,
    document_reviewer,
    documentation_agent,
    implementer,
    implementer_critic,
    planner_critic,
    task_planner,
)
from ai_compliance_agent.state import WorkflowState


def route_after_implementation_review(state: WorkflowState) -> str:
    """Retry a rejected implementation draft, with a hard loop limit."""

    rejected = any(
        artifact.get("owner") == "Implementer"
        and artifact.get("status") == "needs_revision"
        for artifact in state.get("artifacts", [])
    )
    if rejected and state.get("implementation_retries", 0) < 2:
        return "revise"
    return "continue"


def build_workflow_app():
    graph = StateGraph(WorkflowState)
    graph.add_node("coordinator", coordinator)
    graph.add_node("document_reviewer", document_reviewer)
    graph.add_node("task_planner", task_planner)
    graph.add_node("planner_critic", planner_critic)
    graph.add_node("implementer", implementer)
    graph.add_node("implementer_critic", implementer_critic)
    graph.add_node("compliance_agent", compliance_agent)
    graph.add_node("compliance_critic", compliance_critic)
    graph.add_node("documentation_agent", documentation_agent)

    graph.add_edge(START, "coordinator")
    graph.add_edge("coordinator", "document_reviewer")
    graph.add_edge("document_reviewer", "task_planner")
    graph.add_edge("task_planner", "planner_critic")
    graph.add_edge("planner_critic", "implementer")
    graph.add_edge("implementer", "implementer_critic")
    graph.add_conditional_edges(
        "implementer_critic",
        route_after_implementation_review,
        {"revise": "implementer", "continue": "compliance_agent"},
    )
    graph.add_edge("compliance_agent", "compliance_critic")
    graph.add_edge("compliance_critic", "documentation_agent")
    graph.add_edge("documentation_agent", END)

    return graph.compile()
