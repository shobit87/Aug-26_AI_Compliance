"""Small, explicit SOC 2 control catalog used by the portfolio demo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Control:
    control_id: str
    name: str
    keywords: tuple[str, ...]
    severity: str
    recommendation: str


SOC2_CHANGE_MANAGEMENT_CONTROLS: tuple[Control, ...] = (
    Control(
        "CC8.1",
        "Change authorization and testing",
        ("change approval", "authorized change", "testing", "rollback"),
        "high",
        "Define approval authority, pre-production testing, rollback criteria, and retained evidence.",
    ),
    Control(
        "CC6.1",
        "Logical access supporting change management",
        ("least privilege", "access review", "segregation of duties", "production access"),
        "high",
        "Document production-access restrictions, segregation of duties, and periodic access reviews.",
    ),
    Control(
        "CC7.2",
        "Monitoring of system changes",
        ("monitoring", "audit log", "change log", "alerting"),
        "medium",
        "Specify how changes are logged, monitored, reconciled, and escalated.",
    ),
    Control(
        "CC7.4",
        "Incident response integration",
        ("incident response", "major incident", "emergency change"),
        "medium",
        "Connect failed and emergency changes to incident-response and post-incident-review procedures.",
    ),
    Control(
        "CC3.2",
        "Risk identification",
        ("risk assessment", "risk rating", "impact assessment"),
        "medium",
        "Require documented risk and impact assessment before approving material changes.",
    ),
)
