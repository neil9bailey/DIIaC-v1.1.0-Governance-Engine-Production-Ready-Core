# Phase 4 — Microsoft 365 Copilot Integration (Governance Overlay)

This document defines the **authoritative architecture** for integrating DIIaC™
as a governance overlay for Microsoft 365 Copilot.

This design is **model-external**, **Microsoft-aligned**, and **deterministic
where governance decisions are concerned**.

---

## Architectural Premise

Microsoft 365 Copilot is a shared service that:
- grounds prompts using Microsoft Graph
- respects user permissions
- operates inside the Microsoft 365 boundary

DIIaC™ does not replace or bypass this architecture.

Instead, DIIaC provides a **decision-integrity layer around Copilot usage**.

---

## Integration Points

DIIaC integrates at two supported extension points:

1. **Pre-grounding Request Governance**
   - Raw prompt capture
   - Risk classification (R1–R5)
   - Policy enforcement
   - Prompt hardening (safe meta-prompt)

2. **Post-generation Response Governance**
   - Evidence and citation binding
   - Confidence bounds
   - Unsupported claim detection
   - Human approval gating (if required)

Microsoft Graph grounding remains mandatory and untouched.

---

## Governance Capabilities

DIIaC provides:

- Policy-as-Code enforcement
- Deterministic risk scoring
- Provenance binding
- Immutable audit logging
- Human approval workflows

These capabilities are **external to the LLM** and **do not influence model generation**.

---

## Determinism Boundary

DIIaC guarantees determinism for:
- policy evaluation
- risk classification
- approval decisions
- audit record generation

DIIaC does not guarantee:
- answer correctness
- semantic truth
- business outcomes

---

## Security & Compliance Alignment

- Data remains within Microsoft 365 boundary
- Microsoft Graph permissions are enforced
- No credential handling inside DIIaC
- No model training or fine-tuning by default

DIIaC produces artefacts that **support compliance audits**.
It does not certify compliance.

---

## Explicit Non-Goals

This integration does not:
- replace Copilot
- bypass Microsoft security
- generate content
- claim regulatory compliance
- remove human accountability

---

## Phase Boundary

With Phase 4 defined:
- Copilot remains the execution plane
- DIIaC becomes the governance plane
- Determinism and auditability are preserved

## Runtime Support & Compatibility

DIIaC is designed and validated for use on **supported, enterprise-grade Python runtimes only**.

### Supported Python Versions

- **Python 3.10**
- **Python 3.11**
- **Python 3.12** (CI baseline)

### CI Enforcement

All continuous integration pipelines execute against **Python 3.12** to ensure:

- deterministic behaviour
- reproducible builds
- compatibility with supported dependency versions

### Explicit Exclusions

- Pre-release or experimental Python versions (e.g. 3.13+, 3.14+) are **not supported**
- End-of-life Python versions are **not supported**

This policy ensures DIIaC remains suitable for regulated enterprise environments and long-term operational support.


