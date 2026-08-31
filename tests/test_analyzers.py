from ai_compliance_agent.analyzers import DeterministicComplianceAnalyzer


def test_deterministic_analysis_returns_control_mapped_findings():
    result = DeterministicComplianceAnalyzer().analyze(
        "All changes require change approval and testing with a rollback plan.",
        "Review this SOC 2 policy",
    )
    assert result.grammar_score > 0
    assert all(finding.control_id.startswith("CC") for finding in result.findings)
    assert all(finding.evidence for finding in result.findings)
    assert result.analyzer == "deterministic"