"""Structured domain models for compliance analysis."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]


class ComplianceFinding(BaseModel):
    """A traceable gap mapped to a known compliance control."""

    control_id: str
    control_name: str
    severity: Severity
    finding: str
    evidence: str = "No supporting evidence found in the document."
    recommendation: str
    confidence: float = Field(ge=0.0, le=1.0)


class DocumentAnalysis(BaseModel):
    """Validated output shared by deterministic and model-backed analyzers."""

    framework: str = "SOC 2"
    summary: str
    tone: str
    grammar_score: float = Field(ge=0.0, le=100.0)
    findings: list[ComplianceFinding] = Field(default_factory=list)
    corrected_document: str
    analyzer: Literal["deterministic", "openai"]
