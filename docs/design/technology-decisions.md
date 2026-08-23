# Technology decisions

## Decision policy

Introduce a dependency only when a working experiment justifies it. Prefer small, testable vertical slices over a broad platform. Record the reason, alternatives, and evidence for each adopted technology below.

## Current baseline

| Area | Choice | Rationale |
| --- | --- | --- |
| Language/package layout | Python package with `src/` layout. | Fits deterministic data inspection and existing repository structure. |
| Environment | Python 3.12.13 managed with `uv`. | Reproducible environment from lockfile. |
| Tests | `pytest`. | Supports small fixtures and deterministic golden-output testing. |
| Data handling | Local metadata and small representative subsets; raw data remains immutable. | Feasible and reproducible without large downloads. |
| Compute/deployment | Local development by default; NSCC only for a documented larger-data or compute need. | Keeps the baseline runnable while retaining a scale-up path. |
| Documentation | Markdown under `docs/`. | Version-controlled, reviewable living design and evidence. |

## Conditional integrations

| Technology | Potential role | Adoption criterion | Current status |
| --- | --- | --- | --- |
| NumPy/pandas | Deterministic tabular inspection/transformation. | Needed by a concrete supported operation. | Candidate. |
| ASE | Atomistic `Atoms` and trajectory handling. | Needed for a supported fixture or OC adapter. | Candidate. |
| FAIR-Chem | Open Catalyst conventions/data tooling and record interpretation. | Introduce with a small adapter contract/fixture for the selected OC format. | Important planned integration. |
| FAIR-Chem capability guide | Reusable guidance for generating and validating FAIR-Chem inspection/preprocessing code. | A repeated, validated FAIR-Chem workflow shows that a reusable guide would reduce errors or duplication. | Optional future artefact. |
| pymatgen | Materials-science parsing/metadata. | Needed for a documented domain check. | Candidate. |
| LLM API/model | Evidence-grounded planning and explanation. | Deterministic profiler baseline and evaluation protocol exist; approval obtained for cost. | Deferred. |
| LangGraph | Required stateful workflow orchestration, checkpoints, retries, approvals, and validation. | Deterministic-profiler gate is met; add graph tests and a minimal end-to-end workflow. | Required after baseline. |
| FastAPI | Backend service. | A service boundary is required by a verified user/workflow need. | Deferred. |
| React/TypeScript | Approval/explanation UI. | CLI/report output is demonstrably inadequate; wireframes and acceptance criteria exist. | Deferred. |
| Database | Persistent queryable run state. | File-based provenance fails a defined retrieval/concurrency need. | Deferred. |

## Decision record template

```text
Decision ID/date: [e.g., ADR-001 / YYYY-MM-DD]
Decision: [adopt / defer / reject a technology or design]
Context: [specific problem and constraints]
Options considered: [list]
Decision and rationale: [why this option]
Evidence: [experiment, benchmark, fixture, or user need]
Consequences: [new scope, risks, tests, documentation]
Revisit trigger: [what would cause this to change]
```

## Integration safeguards

- Do not place scientific transformation logic inside a prompt.
- Pin and record versions for libraries used in evaluation.
- Add an integration test and a reviewed small fixture before claiming adapter support.
- Seek approval before data downloads that are large or before paid model/API usage.
- Do not add a UI or database merely because it was listed in the original proposal.
- Implement LangGraph only after the profiler baseline is demonstrably working;
  then keep graph nodes, transitions, retries, and state contracts testable.
