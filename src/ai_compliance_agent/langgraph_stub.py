"""Minimal LangGraph stub used when the real dependency is unavailable."""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

START = "__start__"
END = "__end__"


class _CompiledGraph:
    def __init__(self, sequence: List[Callable[[dict], Optional[dict]]]):
        self._sequence = sequence

    def invoke(self, state: dict) -> dict:
        current = dict(state)
        for fn in self._sequence:
            updates = fn(current)
            if isinstance(updates, dict):
                current.update(updates)
        return current


class StateGraph:
    """Simple directed graph runner compatible with LangGraph's API surface we need."""

    def __init__(self, state_type: object):
        self.state_type = state_type
        self._nodes: Dict[str, Callable[[dict], Optional[dict]]] = {}
        self._edges: Dict[str, List[str]] = {}
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

    def compile(self) -> _CompiledGraph:
        if not self._start:
            raise ValueError("Graph start node not defined.")

        order: List[str] = []
        visited = set()

        def dfs(node: str):
            if node in visited or node == END:
                return
            visited.add(node)
            order.append(node)
            for nxt in self._edges.get(node, []):
                if nxt == END:
                    continue
                dfs(nxt)

        dfs(self._start)
        call_sequence = [self._nodes[name] for name in order]
        return _CompiledGraph(call_sequence)
