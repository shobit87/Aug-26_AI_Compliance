"""FastAPI entrypoint exposing a simple UI for document review."""

from __future__ import annotations
import html
import os
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse

from ai_compliance_agent.state import ensure_defaults
from ai_compliance_agent.workflow import build_workflow_app
from ai_compliance_agent.uploads import UploadValidationError, validate_upload

app = FastAPI(title="AI Compliance Agent")
workflow_app = build_workflow_app()

FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>AI Compliance Agent</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 2rem; }}
      .card {{ border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-top: 1.5rem; }}
      textarea {{ width: 100%; min-height: 6rem; }}
      pre {{ white-space: pre-wrap; word-break: break-word; }}
      ul {{ padding-left: 1.5rem; }}
      label {{ display: block; margin-top: 1rem; font-weight: bold; }}
      input[type="submit"] {{ margin-top: 1rem; padding: 0.5rem 1rem; }}
    </style>
  </head>
  <body>
    <h1>AI Compliance Agent</h1>
    <form method="post" action="/analyze" enctype="multipart/form-data">
      <label for="request_text">Compliance Request</label>
      <textarea id="request_text" name="request_text" required placeholder="e.g., Review SOC2 change policy">{{request_text}}</textarea>

      <label for="document">Upload Policy Document (PDF, DOCX, or text)</label>
      <input type="file" id="document" name="document" />

      <input type="submit" value="Analyze" />
    </form>
    {result_section}
  </body>
</html>
"""


def _render_result_section(result: Optional[dict]) -> str:
    if not result:
        return ""

    documentation = html.escape(result.get("documentation") or "No documentation produced.")
    recommendations = "".join(
        f"<li>{html.escape(rec)}</li>" for rec in result.get("document_recommendations", [])
    ) or "<li>None</li>"
    corrected = html.escape(result.get("corrected_document") or "No corrections necessary.")
    gaps = "".join(f"<li>{html.escape(gap)}</li>" for gap in result.get("compliance_gaps", [])) or "<li>None</li>"
    history = "".join(f"<li>{html.escape(entry)}</li>" for entry in result.get("history", [])) or "<li>None</li>"

    return f"""
    <section class="card">
      <h2>Results</h2>
      <h3>Documentation</h3>
      <pre>{documentation}</pre>
      <h3>Document Recommendations</h3>
      <ul>{recommendations}</ul>
      <h3>AI Corrected Document</h3>
      <pre>{corrected}</pre>
      <h3>Compliance Gaps</h3>
      <ul>{gaps}</ul>
      <h3>History</h3>
      <ul>{history}</ul>
    </section>
    """


@app.get("/", response_class=HTMLResponse)
async def landing() -> HTMLResponse:
    content = FORM_TEMPLATE.format(request_text="", result_section="")
    return HTMLResponse(content)


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request_text: str = Form(...),
    document: UploadFile | None = File(None),
) -> HTMLResponse:
    tmp_path: Optional[Path] = None
    try:
        if document:
            data = await document.read()
            try:
                suffix = validate_upload(document.filename or "", data)
            except UploadValidationError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc
            handle = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            handle.write(data)
            handle.flush()
            tmp_path = Path(handle.name)
            handle.close()

        state = {"request": request_text, "document_path": str(tmp_path) if tmp_path else None}
        result = await run_in_threadpool(workflow_app.invoke, state)
        ensure_defaults(result)
    finally:
        if tmp_path and tmp_path.exists():
            os.unlink(tmp_path)

    result_html = _render_result_section(result)
    content = FORM_TEMPLATE.format(request_text=html.escape(request_text), result_section=result_html)
    return HTMLResponse(content)
