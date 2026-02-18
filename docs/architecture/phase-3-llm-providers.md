📄 FILE — Phase 3.1 Canonical Documentation
✅ Full path (recommended and consistent)
F:\App Development\vendorlogic-diiac\docs\architecture\phase-3-llm-providers.md


Create the directories if they do not already exist:

F:\App Development\vendorlogic-diiac\docs\architecture\

✅ FULL MARKDOWN CONTENTS (PASTE VERBATIM)
# Phase 3.1 – LLM Provider Interface (Canonical Reference)

This document is the **authoritative reference** for the Phase 3.1 LLM provider abstraction in VendorLogic DIIaC.

It captures the **exact filesystem layout, import paths, environment configuration, and demo artefacts** that are known to work.

This file should be treated as **frozen reference documentation** for architecture review, buyer due diligence, and future development.

---

## 1. Python Package Root (Critical)

The Python package root **must** be:



F:\App Development\vendorlogic-diiac\Backend


This directory **must be present on `PYTHONPATH`** when invoking any Python code that imports `app.*`.

### Canonical environment setting

```powershell
$env:PYTHONPATH = 'F:\App Development\vendorlogic-diiac\Backend'


This is not optional.

2. Application Package Layout (Canonical)
F:\App Development\vendorlogic-diiac\Backend\
└── app\
    ├── __init__.py
    │
    ├── llm_providers\
    │   ├── __init__.py
    │   ├── base.py
    │   ├── mock_provider.py
    │   ├── registry.py
    │   └── llm_service.py
    │
    ├── services\
    │   ├── __init__.py
    │   └── (non-LLM application services)
    │
    └── (rest of application)

Key invariants

app is the top-level Python package

All LLM-related code lives under:

app/llm_providers/


Execution logic does not import LLM providers directly

3. Canonical Import Paths

The only correct import for the LLM service is:

from app.llm_providers.llm_service import generate_from_llm


Any of the following are incorrect and will fail:

from services.llm_service ...

from app.services.llm_service ...

from llm_providers.llm_service ...

4. Phase 3.1 Demo Artefacts
4.1 PowerShell demo script
F:\App Development\vendorlogic-diiac\demos\demo-phase3-llm-provider.ps1


Purpose:

Validate LLM provider abstraction in isolation

Invoke the mock provider only

No execution

No ledger writes

No live AI dependency

4.2 Temporary Python script (runtime-generated)
F:\App Development\vendorlogic-diiac\demos\_phase3_llm_test.py


Notes:

This file is created dynamically by the PowerShell script

It is not intended to be committed

Safe to delete between runs

5. Proven Phase 3.1 Output

Successful execution produces output structurally equivalent to:

{
  'content': {'text': 'CTO cloud strategy placeholder'},
  'source': {
    'type': 'llm',
    'provider': 'mock',
    'model': 'mock-model',
    'parameters': {'temperature': 0},
    'trusted': False
  }
}


This output proves:

Provider registry resolution works

Mock provider is deterministic

Trust is explicit metadata

LLM invocation is isolated from execution

No ledger side effects occur

6. Architectural Guarantees (Locked)

Phase 3.1 establishes the following non-negotiable guarantees:

DIIaC does not depend on any LLM by default

LLM providers are optional and pluggable

Trust is declared, not assumed

Determinism is preserved

Vendor lock-in is avoided

Execution logic remains AI-agnostic

7. Phase Boundary

With Phase 3.1 complete:

Phase 1: execution mechanics validated

Phase 2: deterministic LLM replay validated

Phase 3.1: LLM provider abstraction validated

The next step is Phase 3.2, which will:

Extend execution request schemas

Carry LLM source + trust metadata into governance

Persist metadata without allowing execution to call AI
---

## Phase 3.2 — LLM Source & Trust Metadata (Canonical)

Phase 3.2 extends the execution request contract to carry **declarative provenance metadata**
about the origin of execution content.

### Key Properties

- LLMs remain strictly upstream
- Execution never invokes a model
- Metadata is optional and declarative
- Trust is explicit, never inferred
- Metadata is persisted immutably in the ledger

### Execution Contract Extension

The execution request MAY include:

```json
"llm_source": {
  "type": "llm | human | unknown",
  "provider": "string",
  "model": "string",
  "parameters": { "temperature": 0 },
  "trusted": false
}

---

## Phase 4 — Execution Boundary Hardening (Auth & RBAC)

Phase 4 introduces **authentication and role-based access control (RBAC)** at the
**API boundary only**, without modifying any deterministic execution logic.

This phase is intentionally orthogonal to Phases 1–3.

---

### Architectural Intent

Auth and RBAC exist to control **who may invoke deterministic behaviour** —
not to influence what that behaviour does.

All deterministic guarantees established in earlier phases remain intact.

---

### Placement (Critical Boundary)

Auth & RBAC are enforced **only** in the API ingress layer.

They MUST NOT appear in:

- execution contracts
- validation engine
- risk engine
- ledger logic
- policy evaluation
- LLM provider abstraction

This preserves the claim:

> “Given the same execution input, the system produces the same output,
> regardless of who submitted it.”

---

### Authentication Model

- JWT bearer tokens
- OIDC-compatible (Azure AD, Okta, Auth0, etc.)
- Signature verification only
- No user database inside DIIaC
- No session state

Authentication failures occur **before execution**.

---

### Authorization Model (RBAC)

Authorization is based on **roles carried as JWT claims**.

Example token payload:

```json
{
  "sub": "opaque-subject-id",
  "roles": ["EXECUTOR", "AUDITOR"]
}
