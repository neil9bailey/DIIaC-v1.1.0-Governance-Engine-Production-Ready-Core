# DIIaC Architecture Fit — Security & Enterprise Architecture

## Audience
- Enterprise Architecture
- Security & Risk
- Platform & Integration Teams

---

## Architectural Positioning

DIIaC is a **governance overlay**, not a Copilot replacement.

### Logical separation
- Copilot: UI, drafting, retrieval, Microsoft Graph context
- DIIaC: deterministic validation, policy enforcement, evidence capture

There is a hard execution boundary between:
- probabilistic systems (Copilot, LLMs),
- deterministic enforcement (DIIaC).

---

## Deterministic Execution Boundary

Inside DIIaC:
- No model calls
- No probabilistic behaviour
- Same input → same output
- Versioned policies
- Immutable ledger writes

This boundary is enforced by design and test.

---

## Auth & RBAC Model

- Authentication and authorisation exist **only at the API boundary**
- Execution logic is identity-agnostic
- Auth context does not influence deterministic outcomes

This prevents:
- privilege-based behaviour drift
- non-reproducible results
- audit ambiguity

---

## Data Handling & Trust Model

- All inbound content is treated as **untrusted input**
- DIIaC does not assert truthfulness
- DIIaC asserts:
  - structural sufficiency,
  - presence of required declarations,
  - explicit risks and assumptions

Evidence pointers are recorded, not validated for truth.

---

## Zero Trust Alignment

DIIaC aligns naturally with Zero Trust principles:
- Explicit intent required to execute governance
- No implicit trust in upstream systems
- All outputs are inspectable and exportable
- Ledger provides tamper-evident traceability

---

## Deployment Reality

A typical deployment:
- Internal service (containerised)
- Behind enterprise perimeter
- Integrated via controlled API calls
- No outbound dependencies during execution

This fits regulated and high-assurance environments.

---

## Security Summary Statement

DIIaC does not introduce AI risk.
It **contains AI risk** by making it visible, bounded, and auditable.
