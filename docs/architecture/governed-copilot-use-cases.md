# Governed Copilot Use Case Catalogue — DIIaC (v1.3.0)

This catalogue defines concrete enterprise scenarios where DIIaC governs Copilot-assisted content.
Each use case is mapped to:
- user role,
- governed mode,
- contract expectations (structure + sufficiency),
- deterministic risk signalling,
- evidence and audit outputs.

Key invariant:
- Copilot may generate content.
- DIIaC validates content deterministically and records evidence immutably.

---

## 1. Catalogue Overview

### 1.1 Persona set
- Bid Manager / Proposal Lead
- Procurement Lead / Commercial Manager
- CTO / Enterprise Architect
- Vendor Management / Service Owner

### 1.2 Output types governed (business-critical)
- Bid / tender responses
- Customer responses (assurance, security posture, delivery approach)
- Procurement evaluations and vendor comparisons
- Strategy baselines and roadmaps

---

## 2. Use Case: Bid Response (Governed)

### Role
Bid Manager / Proposal Lead

### Governed mode
"Bid Response (Governed)"

### Input sources (untrusted)
- Copilot draft text from RFP documents
- Human authored sections
- Internal reference material excerpts

### Contract expectations (example structure)
- Executive summary
- Scope and assumptions
- Compliance matrix (requirements → response)
- Delivery approach and milestones
- Dependencies and exclusions
- Risks and mitigations
- Evidence references / links

### Deterministic policy gate (what DIIaC checks)
- Required sections present
- Minimum content thresholds per section
- Explicit assumptions and exclusions present
- Risks and mitigations populated
- Evidence references present (as fields, not validated truth)

### Deterministic risk signals (example)
- LOW / BOARD_SAFE when structure and sufficiency thresholds met
- MODERATE when evidence references are missing or thin
- HIGH when required compliance matrix is missing

### Evidence captured
- Policy fingerprint: policy_id, policy_version, policy_hash
- Validation result: pass/fail + missing fields
- Risk assessment: risk_level + assurance + signals
- Ledger entry hash and chain integrity

---

## 3. Use Case: Customer Assurance Response (Governed)

### Role
Account Director / Delivery Lead / Security Stakeholder

### Governed mode
"Customer Response (Governed)"

### Common scenario
Responding to customer security/compliance questions, delivery capability assertions, SLA commitments.

### Contract expectations (example structure)
- Customer question
- Response statement
- Evidence pointers (policies, certifications, internal artefacts)
- Limitations / exclusions
- Approval owner(s)

### Deterministic policy gate
- No unqualified commitments (requires "limitations/exclusions" field)
- Evidence pointers required for any capability claim (pointer existence only)
- Approval owner present (human accountability captured)

### Evidence captured
- Deterministic validation output (commitment hygiene)
- Audit trail suitable for later dispute resolution

---

## 4. Use Case: Procurement Evaluation (Governed)

### Role
Procurement Lead / Commercial Manager

### Governed mode
"Procurement Evaluation (Governed)"

### Contract expectations (example structure)
- Evaluation criteria list (weighted)
- Vendor evidence per criterion
- Scoring rationale per criterion
- Risks, dependencies, exit plan
- Final recommendation + approver

### Deterministic policy gate
- Every criterion must have:
  - evidence field populated,
  - score present,
  - rationale present
- Exit plan required (prevents “sticky vendor” decisions without plan)
- Decision owner required

### Deterministic risk signals
- HIGH if evidence missing for any weighted criterion
- MODERATE if exit plan absent
- LOW when completeness and rationale thresholds met

### Evidence captured
- Ledger chain provides defensible “why this vendor” record

---

## 5. Use Case: Vendor Comparison Pack (Governed)

### Role
Vendor Management / Service Owner / Architecture Review Board

### Governed mode
"Vendor Comparison (Governed)"

### Contract expectations (example structure)
- Comparison dimensions (security, cost, delivery, support, compliance)
- Side-by-side table fields
- Explicit assumptions (pricing model, licensing, term)
- Trade-offs summary
- Recommendation + constraints

### Deterministic policy gate
- Dimensions must be complete (no empty comparison fields)
- Assumptions must be explicit
- Trade-offs required (prevents purely narrative comparisons)

### Evidence captured
- Repeatable, auditable vendor comparison artefact trace

---

## 6. Use Case: CTO Strategy Baseline (Governed)

### Role
CTO / Enterprise Architect

### Governed mode
"CTO Strategy Output (Governed)"

### Contract expectations (example structure)
- Current state baseline
- Target state (12–24 months)
- Constraints (budget, security, skills)
- Key decisions required (with owners)
- Risks / mitigations
- Dependency map
- Board summary

### Deterministic policy gate
- Baseline must exist (no “strategy without current state”)
- Constraints required
- Decision owners required (human accountability)
- Risks required

### Evidence captured
- Board-safe determinism: same baseline yields same classification
- Ledger provides “what was known when” trace

---

## 7. What the Buyer Should Notice (Cross-Use-Case)

Across all governed modes:
- Outputs become structurally consistent and reviewable
- Risk becomes explicit and deterministic (not “AI confidence”)
- Evidence trails become inspectable and exportable
- Copilot remains the UI; DIIaC governs execution and audit

This is not an AI demo.
This is decision hygiene infrastructure around AI-assisted workflows.
