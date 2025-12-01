"""Agent that inspects uploaded documents and suggests compliance fixes."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from ai_compliance_agent.state import (
    WorkflowState,
    add_artifact,
    append_history,
    ensure_defaults,
    flag_gap,
    new_artifact,
)

try:  # pragma: no cover - exercised indirectly in tests
    from docx import Document as DocxDocument
except ImportError:  # pragma: no cover - dependency optional at runtime
    DocxDocument = None  # type: ignore[assignment]

try:  # pragma: no cover - exercised indirectly in tests
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - dependency optional at runtime
    PdfReader = None  # type: ignore[assignment]


_SECTION_HEURISTICS = {
    "Change Approval Workflow": [
        "change advisory board",
        "change approval",
        "cab",
    ],
    "Asset Inventory Link": [
        "asset inventory",
        "cmdb",
        "configuration management",
    ],
    "Incident Response Tie-in": [
        "incident response",
        "major incident",
        "ir plan",
    ],
    "Testing & Validation": [
        "testing",
        "validation",
        "rollback",
    ],
}


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
    updated["document_tone"] = _analyze_tone(text)
    updated["grammar_score"] = _estimate_grammar_score(text)

    recommendations = _derive_recommendations(text)
    updated["document_recommendations"] = recommendations

    corrected = _apply_corrections(text, recommendations)
    updated["corrected_document"] = corrected

    append_history(updated, f"DocumentReviewer analyzed {candidate.name}.")

    for rec in recommendations:
        flag_gap(updated, rec)

    artifact_needed = bool(recommendations)
    if artifact_needed:
        artifact = new_artifact("DocumentReviewer", corrected)
        artifact["status"] = "approved"
        updated = add_artifact(updated, artifact)

    return updated


def _read_document_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx" and DocxDocument:
        document = DocxDocument(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    if suffix == ".pdf" and PdfReader:
        reader = PdfReader(str(path))
        return "\n".join(filter(None, (page.extract_text() for page in reader.pages)))

    return path.read_text(encoding="utf-8", errors="ignore")


def _derive_recommendations(text: str) -> List[str]:
    lower = text.lower()
    recommendations: List[str] = []
    for section, keywords in _SECTION_HEURISTICS.items():
        if not _contains_any(lower, keywords):
            recommendations.append(f"{section} is missing or lacks enough detail.")
    if len(text.strip().split()) < 100:
        recommendations.append("Document is short; add fuller procedural details.")
    return recommendations


def _apply_corrections(text: str, recommendations: Iterable[str]) -> str:
    recs = list(recommendations)
    if not recs:
        return text

    remediation = "\n".join(f"- {rec}" for rec in recs)
    corrected_sections = "\n\n".join(
        f"{title}\n{'-' * len(title)}\nDescribe {title.lower()} responsibilities, approvals, "
        "evidence capture, and tooling references."
        for title in _SECTION_HEURISTICS.keys()
    )
    return (
        f"{text}\n\n---\nAI Remediation Draft\n---\n"
        f"Recommendations:\n{remediation}\n\n"
        f"Suggested Sections:\n{corrected_sections}"
    )


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _analyze_tone(text: str) -> str:
    positive_markers = [
        "approved",
        "aligned",
        "validated",
        "documented",
        "evidence",
        "reviewed",
    ]
    risk_markers = [
        "gap",
        "issue",
        "missing",
        "risk",
        "escalate",
        "exception",
    ]
    lower = text.lower()
    pos_hits = sum(lower.count(marker) for marker in positive_markers)
    neg_hits = sum(lower.count(marker) for marker in risk_markers)
    if neg_hits > pos_hits * 1.2:
        return "Risk-alert"
    if pos_hits >= neg_hits:
        return "Professional-positive"
    return "Neutral"


def _estimate_grammar_score(text: str) -> float:
    import re

    words = text.split()
    if not words:
        return 0.0
    sentence_splits = [segment.strip() for segment in re.split(r"[.!?]", text) if segment.strip()]
    sentence_count = max(1, len(sentence_splits))
    avg_sentence_length = len(words) / sentence_count
    long_sentence_penalty = max(0.0, (avg_sentence_length - 25) / 50)
    punctuation_marks = len(re.findall(r"[,:;]", text))
    punctuation_bonus = min(punctuation_marks / max(len(words), 1) * 2.0, 0.15)
    base_score = 0.85 - long_sentence_penalty + punctuation_bonus
    base_score = max(0.1, min(1.0, base_score))
    return round(base_score, 2)
