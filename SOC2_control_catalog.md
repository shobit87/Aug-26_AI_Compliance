# SOC 2 Security/Common Criteria Control Catalog

This is original, paraphrased implementation guidance for the AI Compliance Agent. It covers the 33 Security/Common Criteria from `CC1.1` through `CC9.2`. It does not reproduce licensed AICPA text, replace the official standard, provide legal advice, or constitute an audit opinion.

The active change-management profile uses `CC8.1`, `CC3.2`, `CC6.1`, `CC7.2`, and `CC7.4`; the complete catalog supports future policy-specific profiles.

## Control Environment

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC1.1 | Integrity and ethical values | Leadership defines, communicates, and demonstrates expected ethical behavior. | Medium | Code of conduct; Annual attestations; Ethics training records |
| CC1.2 | Independent oversight | An appropriately independent governing body oversees internal control. | Medium | Board charter; Committee minutes; Oversight reports |
| CC1.3 | Structure, authority, and responsibility | Reporting lines and decision rights support control ownership and accountability. | Medium | Organization chart; RACI matrix; Delegation policy |
| CC1.4 | Commitment to competence | Personnel and contractors have the skills needed to perform control responsibilities. | Medium | Job descriptions; Training completion; Performance evaluations |
| CC1.5 | Accountability for controls | Individuals are held accountable for assigned internal-control responsibilities. | Medium | Control-owner register; Performance objectives; Exception follow-up |
## Communication and Information

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC2.1 | Relevant quality information | The organization identifies and uses reliable information needed to operate controls. | Medium | Data dictionary; Report validation; Information-owner register |
| CC2.2 | Internal communication | Control responsibilities and material issues are communicated internally. | Medium | Policy acknowledgements; Internal notices; Escalation records |
| CC2.3 | External communication | Relevant control and security matters are communicated to external parties. | Medium | Customer notices; Regulatory correspondence; Security contact process |
## Risk Assessment

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC3.1 | Suitable objectives | Business and control objectives are specific enough to support risk identification. | Medium | Approved objectives; Risk appetite statement; Control mapping |
| CC3.2 | Risk identification and analysis | Risks to objectives are identified, assessed, prioritized, and assigned. | Medium | Risk register; Impact assessment; Risk-treatment plan |
| CC3.3 | Fraud risk | Risk assessment considers internal and external fraud scenarios. | Medium | Fraud-risk assessment; Conflict declarations; Hotline reports |
| CC3.4 | Significant change | Material business, technology, regulatory, and personnel changes trigger risk reassessment. | Medium | Change-risk assessments; Acquisition review; Regulatory-impact analysis |
## Monitoring Activities

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC4.1 | Ongoing and separate evaluations | Controls are evaluated through operational monitoring and independent review. | Medium | Control test results; Internal-audit reports; Monitoring dashboards |
| CC4.2 | Deficiency evaluation and communication | Control deficiencies are evaluated, prioritized, reported, and remediated. | Medium | Issue register; Root-cause analysis; Remediation closure evidence |
## Control Activities

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC5.1 | Control selection and development | Control activities are selected and designed to reduce identified risks. | Medium | Risk-control matrix; Control design review; Procedure documents |
| CC5.2 | Technology general controls | Technology controls support reliable operation of business and security controls. | Medium | IT control matrix; Configuration standards; System ownership records |
| CC5.3 | Policies and procedures | Policies define expectations and procedures translate them into repeatable actions. | Medium | Approved policies; Operating procedures; Review and acknowledgement records |
## Logical and Physical Access

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC6.1 | Logical access security | Logical access is restricted according to authorized business need. | High | Access-control policy; Role matrix; Periodic access reviews |
| CC6.2 | User registration and authorization | New access is approved, provisioned, and authenticated through controlled processes. | High | Access tickets; Approval records; Identity-provider configuration |
| CC6.3 | Access modification and removal | Access changes and terminations are processed promptly and reviewed. | High | Termination tickets; HR-IAM reconciliation; Deprovisioning reports |
| CC6.4 | Physical access restriction | Physical entry to facilities and sensitive assets is authorized and monitored. | High | Badge reports; Visitor logs; Facility access reviews |
| CC6.5 | Asset disposal | Confidential information and media are protected during disposal or reuse. | High | Destruction certificates; Sanitization logs; Asset-disposal tickets |
| CC6.6 | Protection from external threats | Boundaries protect systems and data from unauthorized external access. | High | Firewall rules; Network diagrams; Remote-access configuration |
| CC6.7 | Secure transmission and movement | Data is protected when transmitted, moved, or removed from controlled environments. | High | TLS configuration; Transfer approvals; Key-management records |
| CC6.8 | Malicious software prevention | Controls prevent, detect, and respond to malicious or unauthorized software. | High | Endpoint coverage; Detection alerts; Malware-response tickets |
## System Operations

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC7.1 | Configuration and vulnerability management | Systems are configured securely and vulnerabilities are identified and addressed. | High | Configuration baselines; Scan reports; Patch dashboards |
| CC7.2 | Security monitoring and anomaly detection | Systems and changes are monitored for anomalies indicating control failure or attack. | High | SIEM alerts; Audit-log configuration; Monitoring coverage reports |
| CC7.3 | Security event evaluation | Detected events are analyzed to determine impact and incident status. | High | Triage records; Severity matrix; Investigation timeline |
| CC7.4 | Incident response | Confirmed incidents are contained, investigated, communicated, and resolved. | Critical | Incident plan; Incident tickets; Communication records |
| CC7.5 | Incident recovery and improvement | Recovery restores operations and lessons learned improve controls. | High | Recovery records; Post-incident review; Corrective-action tracking |
## Change Management

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC8.1 | Authorized system changes | Changes are requested, risk assessed, approved, tested, deployed, and reviewed through controlled procedures. | High | Change tickets; Test results; Approval and deployment records |
## Risk Mitigation

| ID | Control | Review objective | Severity | Example evidence |
|---|---|---|---|---|
| CC9.1 | Risk treatment | Selected responses reduce identified risks to acceptable levels. | High | Treatment plans; Risk acceptances; Residual-risk approvals |
| CC9.2 | Vendor and business-partner risk | Risks from vendors and partners are assessed and monitored throughout the relationship. | High | Vendor assessments; Security clauses; SOC reports and monitoring records |

## Evidence-quality guidance

Strong evidence should be attributable, time-bound, complete, and reproducible. A policy usually demonstrates design intent, not operating effectiveness. Reviewers should seek approved procedures, configurations, tickets, approvals, logs, population reports, samples, exceptions, remediation records, and independent validation.

## Severity conventions

- **Critical:** A missing capability may materially prevent containment of a major security incident.
- **High:** A missing capability creates direct access, security, change, recovery, or third-party exposure.
- **Medium:** A missing capability weakens governance, monitoring, documentation, or risk-management reliability.
- **Low:** A localized improvement with limited direct security impact.

Severity is a review default, not an organization-specific conclusion. Final severity must consider scope, data sensitivity, threat exposure, compensating controls, and business impact.

## Maintenance rules

1. Keep licensed official criteria outside this repository unless use is authorized.
2. Record the framework publication and mapping version used by the organization.
3. Treat keywords as discovery aids, never proof of operating effectiveness.
4. Require human review of model-generated findings and evidence.
5. Add or change criteria through versioned catalog updates and regression tests.
