# OC20 Deterministic Profiler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a reproducible, read-only, serialisable profiler for the local OC20 S2EF 200K subset.

**Architecture:** Compose discovery, bounded shard inspection, lexical schema evidence, optional trusted mapping evidence, and explicit provenance/unit status into one JSON-safe profile. Keep raw observations, documented statements, and unresolved uncertainty separate; leave unit conventions unresolved until a field-specific source is verified.

**Tech Stack:** Python 3.11+, standard library, NumPy for trusted OC20 pickle compatibility, pytest, Ruff, uv.

**Spec:** `AGENTS.md`, `docs/design/oc20-data-understanding.md`, `docs/design/evaluation-plan.md`

## Global Constraints

- Keep `data/raw/` immutable and never commit OC20 data, credentials, or generated large artefacts.
- Do not add transformations, a UI, LangGraph, or agents in this milestone.
- Load mapping pickles only after explicit trust authorisation; preserve raw anomaly codes.
- Use synthetic compressed fixtures and golden JSON for automated tests.
- Run `uv run ruff format`, `uv run ruff check`, and `uv run pytest` before completion.

## Completed work

- [x] Discovery, numeric pairing, bounded inspection, row-count validation, lexical schema profiling, sample consistency, mapping-key checks, trusted metadata inspection, composed JSON, golden regression, reproducibility, and local timing evidence.

### Task 1: Integrate provenance and trusted metadata into the composed profile

**Files:**
- Modify: `src/agentic_preprocessing/oc20_profile.py`
- Modify: `src/agentic_preprocessing/oc20_metadata.py`
- Test: `tests/test_oc20_profile.py`

**Interfaces:**
- Consume: `profile_trusted_metadata_record(system_id, mapping_path)`.
- Produce: `Oc20Profile.metadata_record_profile` and explicit absence/warning evidence.

- [x] Write a failing synthetic test asserting trusted metadata schema, checksum, and raw anomaly code are present in `Oc20Profile.to_dict()`.
- [x] Run the focused test and confirm it fails because the composed field is absent.
- [x] Add the smallest optional metadata field to `Oc20Profile`, gated by `allow_pickle_load=True`.
- [x] Run the focused test and full profiler tests.

### Task 2: Add documented unit-evidence status

**Files:**
- Modify: `src/agentic_preprocessing/oc20_profile.py`
- Modify: `docs/design/oc20-data-understanding.md`
- Test: `tests/test_oc20_profile.py`

**Interfaces:**
- Produce: a JSON-safe `unit_evidence` list with field, source URL, status, and no raw-value coercion.

- [x] Write a failing test for explicit source-attributed `energy`, `free_energy`, and `forces` unit evidence plus unresolved `reference_energy` status.
- [x] Run the focused test and confirm it fails because `unit_evidence` is absent.
- [x] Add explicit unresolved unit evidence; do not infer units from raw values.
- [x] Run focused and full tests.

### Task 3: Extend golden evaluation and document the gate

**Files:**
- Modify: `tests/fixtures/oc20_profile_golden.json`
- Modify: `tests/test_oc20_profile.py`
- Modify: `docs/design/evaluation-plan.md`
- Modify: `docs/development-log.md`

- [x] Add failing golden assertions for metadata present/missing, relationship absence, anomaly preservation, and unit-evidence status.
- [x] Implement only the fixture/test updates needed for the accepted profile contract.
- [x] Record the exact profiler limitations and evaluation coverage.
- [x] Run Ruff and the full test suite.

## Acceptance review

- [x] A profile distinguishes observations, documented evidence, and unresolved uncertainty.
- [x] Trusted pickles never load unless explicitly authorised.
- [x] Synthetic golden tests cover valid and adversarial profiler scenarios.
- [x] Ruff and pytest pass; no raw data or unrelated user files are staged or committed.
