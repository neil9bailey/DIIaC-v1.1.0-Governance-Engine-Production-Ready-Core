\# VendorLogic — DIIaC

\## Runtime Architecture (v0.5.0-B5 Hardening)



Authoritative as of tag:

v0.5.0-B5-hardening-stable



---



\## 1. Deployment Model



Docker Topology:



Docker

&nbsp;├── diiac-frontend   → Port 5173 (Vite)

&nbsp;└── diiac-backend    → Port 3001 (Node / Express)

&nbsp;       |

&nbsp;       ├── RBAC enforcement

&nbsp;       ├── Governed PowerShell execution

&nbsp;       ├── Ledger JSONL append-only chain

&nbsp;       ├── Freeze + notarisation

&nbsp;       ├── Derived generation (EU AI Act)

&nbsp;       ├── Decision Pack layer (additive)

&nbsp;       └── Reporting endpoints



There is no Python runtime component.

There is no FastAPI.

There is no uvicorn.



Port 3001 is exclusively owned by Node.



---



\## 2. Backend Authority



All backend logic resides in:



backend-ui-bridge/server.js



If functionality is not referenced from this file,

it does not exist in runtime.



---



\## 3. Ledger Model



Ledger file:

workspace/ledger/ledger.jsonl



Characteristics:



• Append-only  

• Hash-chained via `record\_hash`  

• Each record contains:

&nbsp; - previous\_hash

&nbsp; - record\_hash

• GENESIS root when empty

• Freeze enforced via ledger.anchor.json



No in-memory ledger state is authoritative.



---



\## 4. Freeze Model



Freeze state stored in:



workspace/ledger/ledger.anchor.json



When frozen:



• appendLedger() becomes no-op

• verify continues functioning

• No retroactive mutation allowed



---



\## 5. Derived Generation



EU AI Act derived generation:



Endpoint:

POST /derived/eu-ai-act



Executed via:

PowerShell script under artefacts/derived/run/



Derived outputs are artefact-layer files.

Ledger records contain DERIVED\_GENERATION entries.



---



\## 6. Decision Pack Layer (Additive — B5 Extension)



Decision packs stored under:



workspace/artefacts/decision-packs/{execution\_id}/



Files:



• decision.json

• ledger\_snapshot.json

• artefacts\_index.json



Properties:



• Created after successful ledger append

• Non-blocking

• Does not mutate ledger

• Does not alter hash structure

• Uses existing record\_hash root



---



\## 7. Security Model



RBAC enforced via requireRole()



Allowed headers:

x-role



No implicit execution.



All governed endpoints require admin role.



---



\## 8. Architectural Constraints



For v0.5.0-B5:



• Node is the sole backend runtime.

• No dual backend.

• No Python execution layer.

• No change to record\_hash model.

• No change to freeze model.

• Additive extensions only.



---



\## 9. Invariants



The following must always remain true:



✔ Ledger verify returns deterministic root  

✔ record\_hash model unchanged  

✔ Freeze state persistent  

✔ Decision packs never alter ledger  

✔ PowerShell execution isolated  

✔ Node owns port 3001  



Deviation from these rules constitutes architecture drift.



---



Authoritative.

