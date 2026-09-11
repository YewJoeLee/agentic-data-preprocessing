# Technology decisions

## Decision policy

Introduce a dependency only when a working experiment justifies it. Prefer small, testable vertical slices over a broad platform. Record the reason, alternatives, and evidence for each adopted technology below.

## Current baseline

| Area | Choice | Rationale |
| --- | --- | --- |
| Language/package layout | Python package with `src/` layout. | Fits deterministic data inspection and existing repository structure. |
| Environment | Python 3.12.14 with `uv` is the reference environment. | The package retains Python 3.11 compatibility; record any future environment difference before comparing experiments. |
| Tests | `pytest`. | Supports small fixtures and deterministic golden-output testing. |
| Numerical data support | NumPy. | OC20's official metadata mapping uses NumPy values and cannot be loaded without it. |
| Exploration notebook | JupyterLab, ASE, and Matplotlib as development-only tools. | Provide a reproducible, read-only OC20 visual inspection without coupling visualisation to the runtime profiler. |
| Data handling | Local metadata and small representative subsets; raw data remains immutable. | Feasible and reproducible without large downloads. |
| Compute/deployment | Local development by default; NSCC only for a documented larger-data or compute need. | Keeps the baseline runnable while retaining a scale-up path. |
| Documentation | Markdown under `docs/`. | Version-controlled, reviewable living design and evidence. |

## Conditional integrations

| Technology | Potential role | Adoption criterion | Current status |
| --- | --- | --- | --- |
| NumPy/pandas | Deterministic tabular inspection/transformation. | NumPy is required to load the selected OC20 metadata mapping; pandas remains conditional. | NumPy adopted; pandas candidate. |
| ASE | Atomistic `Atoms` and trajectory handling. | Development-only use is justified for the OC20 reconnaissance notebook; a runtime adapter remains conditional on a tested parser contract. | Development tool adopted; runtime adapter candidate. |
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

## Decision records

### ADR-001 / 2026-09-04 — Adopt NumPy for OC20 metadata inspection

- **Decision:** Add NumPy as a runtime dependency.
- **Context:** `oc20_data_mapping.pkl` contains NumPy scalar values, and the
  standard-library unpickler fails without the `numpy` module.
- **Options considered:** Keep mappings unsupported; use an ephemeral
  inspection environment; add NumPy to the reproducible project environment.
- **Decision and rationale:** Add NumPy because mapping inspection is an
  explicit capability of the initial OC20 profiler, not a one-off analysis.
- **Evidence:** The successful local inspection of `random1331004` loaded after
  adding NumPy and exposed the expected scientific metadata fields.
- **Consequences:** Pin resolved versions in `uv.lock`; add parser and profile
  tests before claiming full mapping support. Keep pandas and ASE conditional.
- **Revisit trigger:** Replace or supplement pickle loading if a safer official
  serialisation format becomes available or a security review requires it.

### ADR-002 / 2026-09-04 — Add a read-only OC20 reconnaissance notebook

- **Decision:** Add JupyterLab, ASE, and Matplotlib to the development group
  and create one small OC20 visualisation notebook.
- **Context:** Manual inspection is needed to establish ground truth for the
  profiler and produce a reviewable visual evidence trail.
- **Decision and rationale:** Keep the notebook narrowly scoped to one
  streamed record, its sidecar row, and its mappings. It must not contain
  reusable profiler logic or write derived data.
- **Consequences:** The development environment is larger, but runtime profiler
  dependencies remain limited to NumPy. The notebook's read path serves as a
  manually verified reference for later parser tests.
- **Revisit trigger:** Promote ASE to a runtime dependency only when the
  deterministic parser/adaptor contract requires it and is covered by tests.

## Integration safeguards

- Do not place scientific transformation logic inside a prompt.
- Pin and record versions for libraries used in evaluation.
- Add an integration test and a reviewed small fixture before claiming adapter support.
- Seek approval before data downloads that are large or before paid model/API usage.
- Do not add a UI or database merely because it was listed in the original proposal.
- Implement LangGraph only after the profiler baseline is demonstrably working;
  then keep graph nodes, transitions, retries, and state contracts testable.
