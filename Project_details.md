# AI Compliance Agent — Project Details

## 1. Project purpose

This project is a LangGraph-based document-review workflow for change-management compliance. It accepts a compliance request and an optional PDF, DOCX, TXT, or Markdown policy document. The workflow extracts the document, evaluates it against a focused SOC 2 control catalog, produces traceable findings, sends an implementation plan through a bounded critic/revision loop, and generates reviewer-friendly documentation and a corrected DOCX draft.

The application supports two analysis modes:

- **Deterministic:** transparent keyword-based checks used for repeatable tests and offline demonstrations.
- **OpenAI:** optional model-backed analysis that returns the same validated Pydantic output structure.

The tool assists human review. It is not an audit opinion, legal advice, or proof that an organization is compliant.

## 2. High-level workflow

```text
User / uploaded document
          |
          v
Coordinator
          |
          v
Document Reviewer ----> Analyzer ----> SOC 2 control catalog
          |
          v
Task Planner -> Planner Critic
          |
          v
Implementer <------------------+
          |                     |
          v                     |
Implementer Critic -- revision-+
          |
          v
Compliance Agent -> Compliance Critic
          |
          v
Documentation Agent
          |
          v
CLI / FastAPI / Streamlit output and DOCX download
```

The implementer loop is limited by `implementation_retries`, preventing an accidental infinite graph cycle.

## 3. Root files

### `README.md`

**Purpose:** The public introduction and operating guide for developers, reviewers, and interviewers.

**Why it is needed:** A repository should explain what it does, what it does not do, how to install it, how to select an analyzer, how to run each interface, and how to execute tests. Its limitations section prevents the prototype from overstating its audit or legal capabilities.

### `Project_details.md`

**Purpose:** This detailed architectural and file-by-file reference.

**Why it is needed:** The README is intentionally concise. This document explains internal responsibilities, boundaries, agents, data flow, and maintenance considerations in enough detail for onboarding and interviews.

### `pyproject.toml`

**Purpose:** Python package and dependency configuration.

**Contains:**

- Package name, version, description, and supported Python version.
- Runtime dependencies such as LangGraph, FastAPI, Streamlit, Pydantic, OpenAI, python-docx, and pypdf.
- Development dependencies such as pytest and pytest-asyncio.
- Setuptools build configuration.

**Why it is needed:** It makes installation reproducible through `pip install -e ".[dev]"` and allows the `src/` package to be imported from the CLI, API, tests, and Streamlit.

### `.env.example`

**Purpose:** A safe template for runtime configuration.

**Contains:** Analyzer mode, OpenAI model name, and an empty API-key field.

**Why it is needed:** It documents required environment variables without exposing a real secret. A developer copies it to `.env` and supplies local values.

### `.env`

**Purpose:** Local, private runtime configuration.

**Why it is needed:** It stores machine-specific settings and secrets outside source code. It must remain ignored by Git and must never be printed, committed, or included in screenshots.

### `.gitignore`

**Purpose:** Prevent generated or sensitive files from entering source control.

**Excludes:** Virtual environments, Python caches, editable-install metadata, `.env`, Streamlit secrets, runtime logs, generated PDFs, backups, and archives.

**Why it is needed:** It keeps commits reviewable and reduces the risk of leaking credentials or committing hundreds of generated dependency files.

## 4. Core package files

All maintained application code lives under `src/ai_compliance_agent/`.

### `src/ai_compliance_agent/__init__.py`

**Purpose:** Marks the directory as a Python package and exposes `build_workflow_app` as its small public API.

**Why it is needed:** Consumers can import the workflow builder directly from `ai_compliance_agent` without depending on internal module paths.

### `src/ai_compliance_agent/state.py`

**Purpose:** Defines the shared `WorkflowState`, artifact structure, defaults, and state mutation helpers.

**Important state fields:**

- `request`: The user’s compliance objective.
- `document_path`, `document_text`, `original_document_name`, `original_document_bytes`: Uploaded-document context.
- `document_tone`, `grammar_score`: Document-quality results.
- `analysis_summary`, `analysis_mode`: Analyzer explanation and provenance.
- `compliance_findings`: Structured, evidence-backed control findings.
- `document_recommendations`, `corrected_document`: Remediation outputs.
- `tasks`, `artifacts`, `compliance_gaps`, `documentation`: Workflow products.
- `implementation_retries`: Safety counter for the critic repair loop.
- `history`: Human-readable audit trail of node execution.

**Why it is needed:** Every LangGraph node must agree on the shape and meaning of shared data. Central helpers also prevent each node from implementing defaults, artifact statuses, or history behavior differently.

### `src/ai_compliance_agent/models.py`

**Purpose:** Defines validated domain models using Pydantic.

**Models:**

- `ComplianceFinding`: Control ID/name, severity, finding, evidence, recommendation, and confidence.
- `DocumentAnalysis`: Framework, summary, tone, 0–100 grammar score, findings, corrected text, and analyzer provenance.

**Why it is needed:** Deterministic and OpenAI analyzers must produce the same reliable contract. Validation prevents malformed severities, out-of-range confidence scores, or incomplete results from silently entering the graph.

### `src/ai_compliance_agent/controls.py`

**Purpose:** Stores the focused SOC 2 change-management control catalog.

**Current controls:** CC8.1, CC6.1, CC7.2, CC7.4, and CC3.2.

**Why it is needed:** Findings should map to explicit controls rather than vague compliance language. Keeping the catalog separate makes it reviewable, testable, and replaceable with a versioned external catalog later.

**Important limitation:** This is a portfolio-sized subset, not the complete SOC 2 Trust Services Criteria.

### `src/ai_compliance_agent/analyzers.py`

**Purpose:** Implements the interchangeable document-analysis layer.

**Components:**

- `ComplianceAnalyzer`: Protocol defining the analyzer contract.
- `DeterministicComplianceAnalyzer`: Reproducible offline baseline that compares document concepts against the catalog.
- `OpenAIComplianceAnalyzer`: Uses the OpenAI Responses API structured parsing interface and returns `DocumentAnalysis`.
- `get_analyzer`: Explicitly selects `deterministic` or `openai` from `COMPLIANCE_ANALYZER`.
- `_grammar_score`: Transparent 0–100 baseline scoring function.

**Why it is needed:** Workflow nodes should depend on a stable business interface rather than a specific model vendor. This separation also prevents tests from making paid network calls.

**Design decision:** A failed OpenAI analysis is not silently replaced with deterministic output. Silent fallback could make users believe a model reviewed the document when it did not.

### `src/ai_compliance_agent/workflow.py`

**Purpose:** Registers every node and connects them into the LangGraph execution graph.

**Important function:** `build_workflow_app()` compiles the graph used by all three entry points.

**Conditional route:** `route_after_implementation_review()` returns the draft to the implementer when the critic requests revision and the retry limit has not been reached.

**Why it is needed:** Orchestration belongs in one file so agent logic remains focused and the CLI, FastAPI, and Streamlit applications execute exactly the same workflow.

### `src/ai_compliance_agent/langgraph_stub.py`

**Purpose:** Minimal compatibility runner for environments where LangGraph is unavailable.

**Supports:** Nodes, normal edges, conditional edges, cycles, and a 100-step safety limit.

**Why it is needed:** It allows basic offline execution and keeps tests understandable in restricted environments. Production and normal development should use the official LangGraph dependency.

### `src/ai_compliance_agent/uploads.py`

**Purpose:** Central upload validation shared by FastAPI and Streamlit.

**Checks:** Supported extension, nonempty content, 10 MB limit, PDF signature, and DOCX ZIP signature.

**Why it is needed:** A filename extension is not proof of file type. Central validation keeps both interfaces consistent and reduces malformed-file and resource-exhaustion risks.

### `src/ai_compliance_agent/exports.py`

**Purpose:** Converts corrected text into an in-memory DOCX file.

**Why it is needed:** Users need a real Word artifact rather than text bytes saved with a misleading `.docx` extension. In-memory generation avoids permanent storage of document content.

### `src/ai_compliance_agent/runner.py`

**Purpose:** Typer/Rich command-line interface.

**Inputs:** A compliance request and optional `--document-path`/`-d`.

**Outputs:** Documentation, quality metrics, recommendations, corrected draft, gaps, and workflow history.

**Why it is needed:** The CLI is useful for automation, demonstrations, debugging, and environments where a web UI is unnecessary.

### `src/ai_compliance_agent/server.py`

**Purpose:** FastAPI entry point with an HTML upload form.

**Routes:**

- `GET /`: Displays the request/upload page.
- `POST /analyze`: Validates and temporarily stores an upload, runs the workflow in a thread pool, renders escaped results, and deletes the temporary file.
- `/docs`: Automatically provided FastAPI documentation.

**Why it is needed:** It demonstrates backend integration and provides a lightweight browser interface without requiring a separate JavaScript application.

**Security responsibilities:** Upload validation, HTML escaping, temporary-file deletion, and avoiding secret exposure.

### `src/ai_compliance_agent/streamlit_app.py`

**Purpose:** Primary interactive dashboard.

**Features:** Request form, document upload, progress indicator, quality metrics, original/corrected comparison, control-finding table, recommendations, workflow history, analyzer provenance, and corrected DOCX download.

**Why it is needed:** It gives interviewers and nontechnical reviewers a clear way to explore the workflow and understand why each finding was produced.

## 5. Agent files

All workflow nodes live under `src/ai_compliance_agent/agents/`. Each function accepts `WorkflowState` and returns an updated state.

### `agents/__init__.py`

**Purpose:** Re-exports every agent function used by `workflow.py`.

**Why it is needed:** It gives the workflow one stable import location and documents the supported node set.

### `agents/coordinator.py`

**Agent:** Coordinator.

**Responsibility:** Initializes defaults, reads the request, and records the beginning of the workflow in history.

**Why it is needed:** It is the controlled entry point for orchestration. In a larger system it would also classify requests, choose frameworks, and route work to specialized graphs.

### `agents/document_reviewer.py`

**Agent:** Document reviewer.

**Responsibility:** Locates the temporary document, saves original metadata, extracts PDF/DOCX/text content, detects empty or scanned documents, invokes the selected analyzer, maps validated results into workflow state, records findings, and creates a corrected-document artifact.

**Why it is needed:** File parsing and compliance reasoning are different concerns. The reviewer coordinates them while the analyzer remains replaceable.

### `agents/planner.py`

**Agent:** Task planner.

**Responsibility:** Converts the user request into an ordered task list and adds framework-oriented tasks when it recognizes SOC 2, GDPR, or HIPAA terms.

**Why it is needed:** Downstream implementation should operate on explicit work items instead of an unstructured request.

**Limitation:** Only the included SOC 2 catalog currently supports evidence-backed document findings; GDPR/HIPAA planner tasks do not imply full framework support.

### `agents/planner_critic.py`

**Agent:** Planner critic.

**Responsibility:** Verifies that the task list has enough actionable steps and injects a safe baseline if planning is insufficient.

**Why it is needed:** It prevents downstream nodes from operating on an empty or unusably small plan.

### `agents/implementer.py`

**Agent:** Implementer.

**Responsibility:** Converts planned tasks into an implementation-plan artifact. On a retry, it incorporates evidence-retention and remediation-tracking requirements requested by the critic.

**Why it is needed:** Findings alone are not actionable. The implementer demonstrates how workflow tasks become a remediation artifact.

### `agents/implementer_critic.py`

**Agent:** Implementer critic.

**Responsibility:** Checks whether the implementation plan covers evidence and remediation. It either approves the artifact or marks it `needs_revision`, adds critic notes, and increments the bounded retry counter.

**Why it is needed:** This node provides an actual quality gate and drives the graph’s conditional repair loop.

### `agents/compliance.py`

**Agent:** Compliance agent.

**Responsibility:** Retains structured findings produced by the document analyzer. When no document findings exist, it applies a small fallback heuristic to the implementation artifacts.

**Why it is needed:** It consolidates compliance gaps before final critical review and supports request-only workflows where no document is uploaded.

### `agents/compliance_critic.py`

**Agent:** Compliance critic.

**Responsibility:** Verifies and records the complete set of compliance gaps without silently truncating findings.

**Why it is needed:** Compliance findings must not disappear merely to make output shorter. This critic preserves completeness and creates an audit-history entry.

### `agents/documentation.py`

**Agent:** Documentation agent.

**Responsibility:** Synthesizes the request, tasks, artifacts, quality metrics, recommendations, evidence-backed control findings, corrected draft, and outstanding gaps into the final report.

**Why it is needed:** Workflow state is optimized for machines. Stakeholders require one coherent, readable output.

## 6. Test files

### `tests/conftest.py`

**Purpose:** Adds the `src/` directory to the Python import path for tests.

**Why it is needed:** Tests can import the local package reliably even before an editable installation is created.

### `tests/test_workflow.py`

**Purpose:** End-to-end workflow regression tests.

**Covers:** Documentation generation, coordinator history, bounded implementer repair, final artifact approval, document extraction, recommendations, corrected text, tone, and grammar score.

### `tests/test_analyzers.py`

**Purpose:** Verifies the deterministic analyzer’s structured contract.

**Covers:** Control IDs, evidence presence, grammar scoring, and analyzer provenance without network calls.

### `tests/test_uploads.py`

**Purpose:** Verifies file-ingestion security rules.

**Covers:** Rejecting a fake PDF and accepting valid text input.

### `tests/test_exports.py`

**Purpose:** Prevents blank or mislabeled DOCX regressions.

**Covers:** ZIP/DOCX signature, successful reopening with python-docx, and presence of corrected text.

### `tests/test_server.py`

**Purpose:** FastAPI integration tests.

**Covers:** Landing-page rendering and multipart document analysis through the HTTP interface.

### `tests/test_streamlit_app.py`

**Purpose:** Streamlit import smoke test.

**Covers:** Ensures the dashboard module imports successfully and exposes its `main` entry point.

## 7. Generated and local-only directories

### `venv3/`

**Purpose:** Local Python virtual environment containing dependencies.

**Why it is not source:** It is machine-specific, large, reproducible from `pyproject.toml`, and ignored by Git.

### `.run/`

**Purpose:** Standard-output and error logs for locally running FastAPI and Streamlit processes.

**Why it is not source:** Logs are runtime artifacts and may contain machine-specific diagnostic information.

### `__pycache__/`, `.pytest_cache/`, and `*.egg-info/`

**Purpose:** Python bytecode, pytest metadata, and editable-install metadata.

**Why they are not source:** Tools regenerate them automatically. They should remain ignored and can be deleted safely when the related process is not using them.

## 8. Runtime configuration

| Variable | Default | Purpose |
|---|---|---|
| `COMPLIANCE_ANALYZER` | `deterministic` | Selects `deterministic` or `openai`. |
| `OPENAI_API_KEY` | None | Authenticates model-backed analysis. Required only in OpenAI mode. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Selects the OpenAI model used by the structured analyzer. |

## 9. Typical data flow

1. The CLI, FastAPI page, or Streamlit dashboard creates an initial state with a request and optional temporary document path.
2. The coordinator initializes and logs the request.
3. The document reviewer extracts content and calls the selected analyzer.
4. The analyzer returns a validated `DocumentAnalysis` with `ComplianceFinding` records.
5. The planner creates work items and the planner critic validates them.
6. The implementer creates a first remediation plan.
7. The implementer critic requests missing evidence/remediation language.
8. LangGraph routes the workflow back to the implementer.
9. The revised plan is approved and processing continues.
10. The compliance agent and critic retain the complete gap set.
11. The documentation agent produces the final stakeholder report.
12. The interface renders results and Streamlit can generate a corrected DOCX in memory.
13. Temporary uploaded files are deleted.

## 10. Safe extension points

- Add a versioned full-framework catalog behind the control-catalog interface.
- Add GDPR or HIPAA analyzers only when authoritative controls and evaluation data are available.
- Add OCR as a separate extraction service for scanned PDFs.
- Add JSON API endpoints without changing workflow nodes.
- Replace in-memory execution with persistent LangGraph checkpoints for authenticated enterprise workflows.
- Add authentication, rate limiting, structured logging, request IDs, retention policies, and encrypted storage before public deployment.
- Add model evaluation datasets measuring finding precision, recall, evidence quality, and correction usefulness.
