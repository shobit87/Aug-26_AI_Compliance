from ai_compliance_agent.analyzers import DeterministicComplianceAnalyzer
from ai_compliance_agent.controls import (
    CONTROL_INDEX,
    SOC2_CHANGE_MANAGEMENT_CONTROLS,
    SOC2_COMMON_CRITERIA_CONTROLS,
)


def test_deterministic_analysis_returns_control_mapped_findings():
    result = DeterministicComplianceAnalyzer().analyze(
        "All changes require change approval and testing with a rollback plan.",
        "Review this SOC 2 policy",
    )
    assert result.grammar_score > 0
    assert all(finding.control_id.startswith("CC") for finding in result.findings)
    assert all(finding.evidence for finding in result.findings)
    assert result.analyzer == "deterministic"

def test_soc2_common_criteria_catalog_is_complete_and_unique():
    assert len(SOC2_COMMON_CRITERIA_CONTROLS) == 33
    assert len(CONTROL_INDEX) == 33
    assert len({item.control_id for item in SOC2_COMMON_CRITERIA_CONTROLS}) == 33
    assert {item.category for item in SOC2_COMMON_CRITERIA_CONTROLS} == {
        "Control Environment",
        "Communication and Information",
        "Risk Assessment",
        "Monitoring Activities",
        "Control Activities",
        "Logical and Physical Access",
        "System Operations",
        "Change Management",
        "Risk Mitigation",
    }
    assert {item.control_id for item in SOC2_CHANGE_MANAGEMENT_CONTROLS} == {
        "CC3.2", "CC6.1", "CC7.2", "CC7.4", "CC8.1"
    }