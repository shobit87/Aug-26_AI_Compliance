# AI Compliance Agent (LangGraph)

This project demonstrates how to frame an "agentic" compliance workflow as a LangGraph-based micro-architecture. It wires a coordinator, multiple specialized agents, and critic nodes to enforce deterministic validations before any result gets surfaced.

## Features

- Coordinator node that decomposes a request into actionable compliance tasks.
- Specialized agents for planning, implementation, compliance review, and documentation.
- Critic nodes that validate each agent's work and trigger repair loops when needed.
- Shared typed state that persists decisions, artifacts, and validation status through the graph.
- CLI runner (`python -m ai_compliance_agent.runner`) that executes the workflow end-to-end on sample input.
- FastAPI and Streamlit UIs with document reviewer metrics (tone, grammar score, recommendations, and AI-corrected drafts).
- Pytest-based regression tests for the critic logic and state transitions.

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Populate the `OPENAI_API_KEY` or compatible LLM credentials in a `.env` file if you want to swap the stubbed models with live ones.

> **Note:** The project includes a minimal LangGraph compatibility stub so tests can run in environments where the real dependency is unavailable. Once you `pip install langgraph`, the workflow automatically switches to the official implementation.

## Running the Workflow

```bash
python -m ai_compliance_agent.runner "Create a SOC2 change-management checklist"
```

Pass the optional `--document-path` (`-d`) flag to analyze an existing policy document (PDF, DOCX, or plain text). The document reviewer will extract the text, highlight missing sections, map each gap to compliance findings, and emit an AI-corrected draft within the CLI output.

```bash
python -m ai_compliance_agent.runner \
  "Validate SOC2 change policy" \
  --document-path docs/change_policy.docx
```

## Web UI (FastAPI)

Run the bundled FastAPI server to upload documents through a browser:

```bash
uvicorn ai_compliance_agent.server:app --reload
```

Then open http://127.0.0.1:8000 to submit a compliance request plus an optional PDF/DOCX/text file. The page renders the generated documentation, recommendations, corrected draft, and workflow history.

## Streamlit UI

Alternatively, launch the Streamlit dashboard:

```bash
streamlit run ai_compliance_agent/streamlit_app.py
```

This provides an interactive sidebar to enter the compliance request, upload files, preview the corrected draft, and download AI-generated recommendations directly from the browser.

## Running the Tests

```bash
pytest
```

## Extending the Graph

1. Add a new state field in `ai_compliance_agent/state.py`.
2. Implement the agent logic under `ai_compliance_agent/agents/`.
3. Register the node and any critic in `ai_compliance_agent/workflow.py`.
4. Add unit tests or sample transcripts under `tests/`.

Because each node focuses on a narrow responsibility, you can iterate on models or tools independently without touching the rest of the workflow—exactly what interviewers expect when they call "agentic AI" a micro-architecture.
