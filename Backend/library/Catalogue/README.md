# VendorLogic DIIaC™ Catalogue

This catalogue contains governed, machine-readable decision inputs.
It is intentionally minimal and expandable.

## What This Is
- A reference library of vendors and decision frameworks
- Data-only, schema-validated
- Explicitly invoked by execution contracts

## What This Is Not
- A recommendation engine
- A scoring system
- A vendor selection mechanism

## How Entries Are Used
Catalogue entries are applied **only if explicitly referenced** by a decision contract.
Unreferenced entries are inert.

## How to Add a Vendor
1. Create a new file under `/library/vendors`
2. Conform strictly to `vendor.schema.json`
3. Avoid opinion, ranking, or scoring language
4. Commit as data-only (no code changes required)

## How to Add an Overlay
1. Create a new file under `/library/overlays`
2. Conform strictly to `overlay.schema.json`
3. Define constraints, not recommendations
4. Failure conditions must be explicit

## Governance Guarantee
Adding entries never changes execution behaviour.
Governance, validation, and assurance logic remain deterministic.
