## Meta Prompt Generator v1.0.0

This is the **first stable release** of Meta Prompt Generator.

v1.0.0 establishes a locked, deterministic contract for prompt generation using roles, modules, and schemas.

### Highlights
- Deterministic prompt assembly
- Schema-driven output enforcement
- Safe schema inheritance (single-parent, cycle-safe)
- Fail-fast validation of all library content
- Hardened API with no silent failures
- CI-enforced content validation

### Stability Guarantees
- Required modules are always present
- Output format is explicit and stable
- Invalid content fails immediately
- No silent fallbacks or mutation

### Intended Use
- Prompt engineering infrastructure
- AI system governance
- Controlled prompt generation pipelines
- Internal or external API-backed prompt services

This release locks all v1 behavior.  
Future v1.x releases will be backward-compatible.

---

**Tag:** `v1.0.0`
