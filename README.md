# AI Compliance Agent

An interview-focused LangGraph workflow for reviewing change-management documents against a small, explicit SOC 2 control catalog. The project supports a reproducible deterministic analyzer and an optional OpenAI-backed analyzer that returns the same validated Pydantic schema.

> This project assists document review. It is not legal advice, an audit opinion, or proof of compliance.

## What it demonstrates

- Typed LangGraph state and modular coordinator, reviewer, planner, implementer, critic, compliance, and documentation nodes.
- A real bounded critic repair loop: rejected implementation drafts return to the implementer and are reviewed again.
- Evidence-backed findings with control ID, severity, recommendation, and confidence.
- SOC 2 change-management catalog covering CC8.1, CC6.1, CC7.2, CC7.4, and CC3.2.
- Deterministic analysis for tests and offline demos.
- Optional OpenAI structured-output analysis using the Responses API.
- PDF, DOCX, TXT, and Markdown ingestion with type checks and a 10 MB upload limit.
- DOCX paragraph, table, header, and footer extraction.
- FastAPI, Streamlit, and CLI entry points.
- Corrected DOCX export and automatic temporary-file cleanup.

## Limitations

- The included catalog is deliberately narrow and is not a complete SOC 2 framework.
- Scanned PDFs require OCR, which is not included.
- The deterministic analyzer uses transparent keyword evidence and is not an AI model.
- Model-backed findings require human review and can be incorrect.
- Authentication, persistent audit storage, rate limiting, and enterprise retention controls are not included.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

The default mode is deterministic and makes no external model calls:

```env
COMPLIANCE_ANALYZER=deterministic
```

To enable OpenAI-backed structured analysis:

```env
COMPLIANCE_ANALYZER=openai
OPENAI_API_KEY=your-project-key
OPENAI_MODEL=gpt-4o-mini
```

Create API keys through the OpenAI platform and never commit `.env`.

## Run

FastAPI:

```powershell
uvicorn ai_compliance_agent.server:app --reload
```

Streamlit:

```powershell
streamlit run src/ai_compliance_agent/streamlit_app.py
```

CLI:

```powershell
python -m ai_compliance_agent.runner "Review SOC2 change policy" -d .\policy.docx
```

## Test

```powershell
pytest
```

The tests cover workflow execution, bounded critic repair, upload validation, structured deterministic findings, FastAPI integration, Streamlit imports, and valid nonblank DOCX export.

## Architecture

```text
Coordinator -> Document Reviewer -> Task Planner -> Planner Critic
                                           |
                                           v
                                    Implementer <----+
                                           |         |
                                           v         |
                                  Implementer Critic-+
                                           |
                                           v
                              Compliance Agent -> Compliance Critic
                                           |
                                           v
                                  Documentation Agent
```

The revision edge is bounded by `implementation_retries` to prevent infinite loops.