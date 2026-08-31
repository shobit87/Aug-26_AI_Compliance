"""Paraphrased SOC 2 Security/Common Criteria catalog.

This is implementation guidance for the portfolio application, not licensed AICPA
criteria text, legal advice, or an audit opinion.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Control:
    control_id: str
    category: str
    name: str
    objective: str
    keywords: tuple[str, ...]
    evidence_examples: tuple[str, ...]
    severity: str
    recommendation: str


def _control(
    control_id: str,
    category: str,
    name: str,
    objective: str,
    keywords: tuple[str, ...],
    evidence: tuple[str, ...],
    recommendation: str,
    severity: str = "medium",
) -> Control:
    return Control(control_id, category, name, objective, keywords, evidence, severity, recommendation)


SOC2_COMMON_CRITERIA_CONTROLS: tuple[Control, ...] = (
    # CC1 — Control Environment
    _control("CC1.1", "Control Environment", "Integrity and ethical values", "Leadership defines, communicates, and demonstrates expected ethical behavior.", ("code of conduct", "ethics", "integrity", "disciplinary"), ("Code of conduct", "Annual attestations", "Ethics training records"), "Document ethical expectations, acknowledgement, escalation, and enforcement."),
    _control("CC1.2", "Control Environment", "Independent oversight", "An appropriately independent governing body oversees internal control.", ("board oversight", "audit committee", "independent director", "governance"), ("Board charter", "Committee minutes", "Oversight reports"), "Define board or committee responsibilities and retain evidence of oversight."),
    _control("CC1.3", "Control Environment", "Structure, authority, and responsibility", "Reporting lines and decision rights support control ownership and accountability.", ("organization chart", "roles and responsibilities", "delegation", "authority"), ("Organization chart", "RACI matrix", "Delegation policy"), "Assign control owners and document authority, escalation, and reporting lines."),
    _control("CC1.4", "Control Environment", "Commitment to competence", "Personnel and contractors have the skills needed to perform control responsibilities.", ("competency", "training", "job description", "performance review"), ("Job descriptions", "Training completion", "Performance evaluations"), "Define role competencies and retain hiring, training, and evaluation evidence."),
    _control("CC1.5", "Control Environment", "Accountability for controls", "Individuals are held accountable for assigned internal-control responsibilities.", ("accountability", "control owner", "performance objective", "consequence"), ("Control-owner register", "Performance objectives", "Exception follow-up"), "Link control ownership to performance review and documented consequences."),

    # CC2 — Communication and Information
    _control("CC2.1", "Communication and Information", "Relevant quality information", "The organization identifies and uses reliable information needed to operate controls.", ("data quality", "information owner", "source system", "report validation"), ("Data dictionary", "Report validation", "Information-owner register"), "Define information sources, owners, quality checks, and retention."),
    _control("CC2.2", "Communication and Information", "Internal communication", "Control responsibilities and material issues are communicated internally.", ("internal communication", "policy distribution", "escalation", "awareness"), ("Policy acknowledgements", "Internal notices", "Escalation records"), "Establish channels for policies, control changes, incidents, and escalation."),
    _control("CC2.3", "Communication and Information", "External communication", "Relevant control and security matters are communicated to external parties.", ("customer notification", "regulator", "external communication", "security contact"), ("Customer notices", "Regulatory correspondence", "Security contact process"), "Define authorized external communications, triggers, owners, and evidence."),

    # CC3 — Risk Assessment
    _control("CC3.1", "Risk Assessment", "Suitable objectives", "Business and control objectives are specific enough to support risk identification.", ("control objective", "business objective", "risk appetite", "success criteria"), ("Approved objectives", "Risk appetite statement", "Control mapping"), "Document measurable objectives and connect them to controls and risk appetite."),
    _control("CC3.2", "Risk Assessment", "Risk identification and analysis", "Risks to objectives are identified, assessed, prioritized, and assigned.", ("risk assessment", "risk rating", "impact assessment", "risk owner"), ("Risk register", "Impact assessment", "Risk-treatment plan"), "Require documented likelihood, impact, ownership, treatment, and review dates."),
    _control("CC3.3", "Risk Assessment", "Fraud risk", "Risk assessment considers internal and external fraud scenarios.", ("fraud risk", "misconduct", "conflict of interest", "whistleblower"), ("Fraud-risk assessment", "Conflict declarations", "Hotline reports"), "Include fraud scenarios, incentives, opportunities, and mitigating controls."),
    _control("CC3.4", "Risk Assessment", "Significant change", "Material business, technology, regulatory, and personnel changes trigger risk reassessment.", ("significant change", "regulatory change", "reorganization", "technology change"), ("Change-risk assessments", "Acquisition review", "Regulatory-impact analysis"), "Define change triggers and require timely reassessment of affected controls."),

    # CC4 — Monitoring Activities
    _control("CC4.1", "Monitoring Activities", "Ongoing and separate evaluations", "Controls are evaluated through operational monitoring and independent review.", ("control testing", "continuous monitoring", "internal audit", "self assessment"), ("Control test results", "Internal-audit reports", "Monitoring dashboards"), "Define testing frequency, independence, sampling, evidence, and follow-up."),
    _control("CC4.2", "Monitoring Activities", "Deficiency evaluation and communication", "Control deficiencies are evaluated, prioritized, reported, and remediated.", ("control deficiency", "remediation plan", "issue tracking", "root cause"), ("Issue register", "Root-cause analysis", "Remediation closure evidence"), "Track deficiencies by severity, owner, due date, root cause, and validation."),

    # CC5 — Control Activities
    _control("CC5.1", "Control Activities", "Control selection and development", "Control activities are selected and designed to reduce identified risks.", ("control design", "preventive control", "detective control", "risk treatment"), ("Risk-control matrix", "Control design review", "Procedure documents"), "Map risks to preventive and detective controls with clear owners and frequency."),
    _control("CC5.2", "Control Activities", "Technology general controls", "Technology controls support reliable operation of business and security controls.", ("general IT controls", "infrastructure control", "application control", "technology dependency"), ("IT control matrix", "Configuration standards", "System ownership records"), "Document technology dependencies and the access, change, and operation controls supporting them."),
    _control("CC5.3", "Control Activities", "Policies and procedures", "Policies define expectations and procedures translate them into repeatable actions.", ("policy", "procedure", "control owner", "review frequency"), ("Approved policies", "Operating procedures", "Review and acknowledgement records"), "Maintain approved, versioned policies and procedures with owners and review cycles."),

    # CC6 — Logical and Physical Access Controls
    _control("CC6.1", "Logical and Physical Access", "Logical access security", "Logical access is restricted according to authorized business need.", ("least privilege", "access review", "segregation of duties", "production access"), ("Access-control policy", "Role matrix", "Periodic access reviews"), "Document least privilege, role design, privileged access, and review requirements.", "high"),
    _control("CC6.2", "Logical and Physical Access", "User registration and authorization", "New access is approved, provisioned, and authenticated through controlled processes.", ("access request", "manager approval", "provisioning", "multi-factor authentication"), ("Access tickets", "Approval records", "Identity-provider configuration"), "Require approved requests, unique identities, strong authentication, and provisioning evidence.", "high"),
    _control("CC6.3", "Logical and Physical Access", "Access modification and removal", "Access changes and terminations are processed promptly and reviewed.", ("termination", "deprovision", "access removal", "role change"), ("Termination tickets", "HR-IAM reconciliation", "Deprovisioning reports"), "Define time-bound removal for terminations and changes, with periodic reconciliation.", "high"),
    _control("CC6.4", "Logical and Physical Access", "Physical access restriction", "Physical entry to facilities and sensitive assets is authorized and monitored.", ("badge access", "visitor log", "data center access", "physical security"), ("Badge reports", "Visitor logs", "Facility access reviews"), "Restrict and periodically review physical access; retain visitor and entry evidence.", "high"),
    _control("CC6.5", "Logical and Physical Access", "Asset disposal", "Confidential information and media are protected during disposal or reuse.", ("secure disposal", "media sanitization", "certificate of destruction", "asset disposal"), ("Destruction certificates", "Sanitization logs", "Asset-disposal tickets"), "Define approved sanitization and destruction methods with chain-of-custody evidence.", "high"),
    _control("CC6.6", "Logical and Physical Access", "Protection from external threats", "Boundaries protect systems and data from unauthorized external access.", ("firewall", "network segmentation", "intrusion prevention", "remote access"), ("Firewall rules", "Network diagrams", "Remote-access configuration"), "Document boundary controls, secure remote access, rule reviews, and segmentation.", "high"),
    _control("CC6.7", "Logical and Physical Access", "Secure transmission and movement", "Data is protected when transmitted, moved, or removed from controlled environments.", ("encryption in transit", "data transfer", "removable media", "key management"), ("TLS configuration", "Transfer approvals", "Key-management records"), "Require approved encrypted transfer methods and control removable media and cryptographic keys.", "high"),
    _control("CC6.8", "Logical and Physical Access", "Malicious software prevention", "Controls prevent, detect, and respond to malicious or unauthorized software.", ("anti-malware", "endpoint protection", "application allowlist", "malware"), ("Endpoint coverage", "Detection alerts", "Malware-response tickets"), "Deploy managed endpoint protection, monitor coverage, and investigate detections.", "high"),

    # CC7 — System Operations
    _control("CC7.1", "System Operations", "Configuration and vulnerability management", "Systems are configured securely and vulnerabilities are identified and addressed.", ("secure configuration", "vulnerability scan", "patch management", "hardening"), ("Configuration baselines", "Scan reports", "Patch dashboards"), "Maintain secure baselines, scan routinely, prioritize vulnerabilities, and validate remediation.", "high"),
    _control("CC7.2", "System Operations", "Security monitoring and anomaly detection", "Systems and changes are monitored for anomalies indicating control failure or attack.", ("monitoring", "audit log", "change log", "alerting"), ("SIEM alerts", "Audit-log configuration", "Monitoring coverage reports"), "Specify log sources, alert rules, retention, review ownership, and escalation.", "high"),
    _control("CC7.3", "System Operations", "Security event evaluation", "Detected events are analyzed to determine impact and incident status.", ("event triage", "security event", "severity classification", "correlation"), ("Triage records", "Severity matrix", "Investigation timeline"), "Define event triage, severity, evidence preservation, and incident-declaration criteria.", "high"),
    _control("CC7.4", "System Operations", "Incident response", "Confirmed incidents are contained, investigated, communicated, and resolved.", ("incident response", "containment", "major incident", "emergency change"), ("Incident plan", "Incident tickets", "Communication records"), "Maintain tested response procedures covering roles, containment, communication, evidence, and emergency changes.", "critical"),
    _control("CC7.5", "System Operations", "Incident recovery and improvement", "Recovery restores operations and lessons learned improve controls.", ("disaster recovery", "post incident review", "lessons learned", "recovery"), ("Recovery records", "Post-incident review", "Corrective-action tracking"), "Define recovery validation, post-incident review, corrective actions, owners, and deadlines.", "high"),

    # CC8 — Change Management
    _control("CC8.1", "Change Management", "Authorized system changes", "Changes are requested, risk assessed, approved, tested, deployed, and reviewed through controlled procedures.", ("change approval", "authorized change", "testing", "rollback"), ("Change tickets", "Test results", "Approval and deployment records"), "Define authorization, segregation, testing, rollback, emergency changes, and retained evidence.", "high"),

    # CC9 — Risk Mitigation
    _control("CC9.1", "Risk Mitigation", "Risk treatment", "Selected responses reduce identified risks to acceptable levels.", ("risk treatment", "risk acceptance", "mitigation plan", "residual risk"), ("Treatment plans", "Risk acceptances", "Residual-risk approvals"), "Document treatment decisions, accountable owners, due dates, and residual-risk approval.", "high"),
    _control("CC9.2", "Risk Mitigation", "Vendor and business-partner risk", "Risks from vendors and partners are assessed and monitored throughout the relationship.", ("vendor risk", "third party", "due diligence", "supplier monitoring"), ("Vendor assessments", "Security clauses", "SOC reports and monitoring records"), "Tier vendors, perform due diligence, contract for security, monitor performance, and manage termination.", "high"),
)

CONTROL_INDEX = {control.control_id: control for control in SOC2_COMMON_CRITERIA_CONTROLS}

CHANGE_MANAGEMENT_CONTROL_IDS = ("CC8.1", "CC3.2", "CC6.1", "CC7.2", "CC7.4")
SOC2_CHANGE_MANAGEMENT_CONTROLS: tuple[Control, ...] = tuple(
    CONTROL_INDEX[control_id] for control_id in CHANGE_MANAGEMENT_CONTROL_IDS
)


def get_control(control_id: str) -> Control:
    """Return a catalog control by identifier or raise a clear lookup error."""

    try:
        return CONTROL_INDEX[control_id.upper()]
    except KeyError as exc:
        raise KeyError(f"Unknown SOC 2 control identifier: {control_id}") from exc


def controls_by_category(category: str) -> tuple[Control, ...]:
    """Return all controls in a category using case-insensitive matching."""

    normalized = category.strip().casefold()
    return tuple(
        control
        for control in SOC2_COMMON_CRITERIA_CONTROLS
        if control.category.casefold() == normalized
    )