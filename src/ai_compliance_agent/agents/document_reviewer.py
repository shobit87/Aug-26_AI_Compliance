"""Agent that extracts uploaded documents and delegates structured analysis."""

from __future__ import annotations

from pathlib import Path

from ai_compliance_agent.analyzers import get_analyzer
from ai_compliance_agent.state import (
    WorkflowState,
    add_artifact,
    append_history,
    ensure_defaults,
    flag_gap,
    new_artifact,
)

try:
    from docx import Document as DocxDocument
except ImportError:  # pragma: no cover
    DocxDocument = None  # type: ignore[assignment]

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None  # type: ignore[assignment]


def document_reviewer(state: WorkflowState) -> WorkflowState:
    updated: WorkflowState = dict(state)
    ensure_defaults(updated)
    path_value = updated.get("document_path")
    if not path_value:
        append_history(updated, "DocumentReviewer skipped (no document supplied).")
        return updated

    candidate = Path(path_value)
    if not candidate.exists():
        flag_gap(updated, f"Provided document not found: {candidate}")
        append_history(updated, f"DocumentReviewer could not locate document: {candidate}")
        return updated

    updated["original_document_bytes"] = candidate.read_bytes()
    updated["original_document_name"] = candidate.name
    text = _read_document_text(candidate)
    updated["document_text"] = text
    if not text.strip():
        flag_gap(updated, "The uploaded document contains no extractable text; OCR may be required.")
        append_history(updated, f"DocumentReviewer found no text in {candidate.name}.")
        return updated

    analysis = get_analyzer().analyze(text, updated.get("request", ""))
    updated["analysis_summary"] = analysis.summary
    updated["analysis_mode"] = analysis.analyzer
    updated["document_tone"] = analysis.tone
    updated["grammar_score"] = analysis.grammar_score
    updated["compliance_findings"] = [item.model_dump() for item in analysis.findings]
    updated["document_recommendations"] = [
        item.recommendation for item in analysis.findings
    ]
    updated["corrected_document"] = analysis.corrected_document
    append_history(
        updated,
        f"DocumentReviewer analyzed {candidate.name} with {analysis.analyzer} mode.",
    )

    for finding in analysis.findings:
        flag_gap(updated, f"{finding.control_id}: {finding.finding}")

    if analysis.findings:
        artifact = new_artifact("DocumentReviewer", analysis.corrected_document)
        artifact["status"] = "approved"
        updated = add_artifact(updated, artifact)
    return updated


def _read_document_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx" and DocxDocument:
        document = DocxDocument(path)
        blocks = [p.text for p in document.paragraphs if p.text.strip()]
        for table in document.tables:
            for row in table.rows:
                blocks.append(" | ".join(cell.text.strip() for cell in row.cells))
        for section in document.sections:
            blocks.extend(p.text for p in section.header.paragraphs if p.text.strip())
            blocks.extend(p.text for p in section.footer.paragraphs if p.text.strip())
        return "\n".join(blocks)
    if suffix == ".pdf" and PdfReader:
        reader = PdfReader(str(path))
        return "\n".join(filter(None, (page.extract_text() for page in reader.pages)))
    return path.read_text(encoding="utf-8", errors="ignore")