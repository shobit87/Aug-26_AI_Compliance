"""Minimal LangGraph stub used when the real dependency is unavailable."""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

START = "__start__"
END = "__end__"


class _CompiledGraph:
    def __init__(self, nodes, edges, conditional, start):
        self._nodes = nodes
        self._edges = edges
        self._conditional = conditional
        self._start = start

    def invoke(self, state: dict) -> dict:
        current = dict(state)
        node = self._start
        steps = 0
        while node and node != END:
            steps += 1
            if steps > 100:
                raise RuntimeError("Workflow exceeded the 100-step safety limit.")
            updates = self._nodes[node](current)
            if isinstance(updates, dict):
                current.update(updates)
            if node in self._conditional:
                router, mapping = self._conditional[node]
                node = mapping[router(current)]
            else:
                destinations = self._edges.get(node, [])
                node = destinations[0] if destinations else END
        return current


class StateGraph:
    """Small compatibility runner for the graph features used by this project."""

    def __init__(self, state_type: object):
        self.state_type = state_type
        self._nodes: Dict[str, Callable[[dict], Optional[dict]]] = {}
        self._edges: Dict[str, List[str]] = {}
        self._conditional = {}
        self._start: Optional[str] = None

    def add_node(self, name: str, fn: Callable[[dict], Optional[dict]]):
        self._nodes[name] = fn
        self._edges.setdefault(name, [])

    def add_edge(self, source: str, target: str):
        if source == START:
            self._start = target
            return
        self._edges.setdefault(source, [])
        self._edges[source].append(target)

    def add_conditional_edges(self, source: str, router, mapping):
        self._conditional[source] = (router, mapping)

    def compile(self) -> _CompiledGraph:
        if not self._start:
            raise ValueError("Graph start node not defined.")
        return _CompiledGraph(
            self._nodes,
            self._edges,
            self._conditional,
            self._start,
        )