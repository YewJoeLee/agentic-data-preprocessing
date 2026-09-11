# Weekly development log

Use this log to retain the evidence needed for the interim report, final report, and oral presentation. The calendar plan is in [milestones.md](milestones.md); the evaluation framework is in [design/evaluation-plan.md](design/evaluation-plan.md).

## Update routine

- Add one entry per active development week and one entry for every meaningful experiment or design decision.
- Include the commit, command/configuration, fixture/subset, and observed outcome wherever applicable.
- Name the [EDA practices](design/eda-workflow.md) exercised and the evidence
  recorded for each; treat the practices as iterative rather than sequential.
- Record failed experiments and limitations immediately.
- Link to saved figures, reports, or golden outputs rather than pasting large generated artefacts into this file.

## Weekly entry template

```md
## YYYY-MM-DD to YYYY-MM-DD — Week [N]

### Goal

- [What project question or milestone was this week intended to advance?]

### Work completed

- [Implementation, reading, design, or evaluation work]
- EDA practices: [Discovering, Structuring, Cleaning, Joining, Validating, and/or Presenting]

### Evidence

- Commit/configuration: `[fill in]`
- Input/fixture: `[fill in]`
- Test/command/result: `[fill in]`
- Output/figure/report: `[fill in]`

### Decisions and rationale

- [Decision, evidence, and consequence]

### Limitations or failures

- [What did not work, remain uncertain, or require deferral?]

### Next actions

- [Concrete next step linked to a milestone or evaluation scenario]
```

## Experiment entry template

```md
### E-[NN] — [short title]

- Date:
- Research question / claim:
- Input and user goal:
- Code revision and configuration:
- Expected oracle:
- Observed result:
- Outcome: pass / fail / partial
- Interpretation and limitation:
- Report or presentation use:
```

## Reading historical acceptance results

Acceptance entries preserve the behaviour observed at their recorded revision.
The entries dated 11 September before `5d988d2` predate the safety correction
that surfaces `pickle_load_not_authorized` in the concise summary. Do not treat
their “no issue codes” wording as the current command behaviour; use the
[Phase 1 acceptance record](design/oc20-profiler-phase-1-acceptance.md) and
the later “Profiler review safety corrections” entry for the current contract.

## 2026-09-04 — OC20 200K reconnaissance and viewing

### Goal

- Establish a factual understanding of the selected OC20 input before
  implementing the deterministic profiler.

### Work completed

- Downloaded and extracted the OC20 S2EF 200K training subset with the OC20
  metadata and clean-slab relationship mappings kept under `data/raw/`.
- Inspected the supplied README, one extended-XYZ structure, its paired
  sidecar row, and the matching mapping entries.
- Configured a local Python 3.12.14 environment with Tk support for ASE GUI
  viewing; added NumPy after the metadata pickle demonstrated that it was
  required.
- Added `notebooks/01_oc20_reconnaissance.ipynb`, a read-only visual companion
  that streams one compressed structure before plotting it and joins its
  matching metadata.

### Evidence

- Commit/configuration: working tree; Python 3.12.14, Tk 9.0.4, NumPy 2.5.2.
- Input/fixture: OC20 S2EF 200K `0.extxyz.xz`, `0.txt.xz`,
  `oc20_data_mapping.pkl`, and `mapping_adslab_slab.pkl`.
- Test/command/result: `uv run pytest` — 1 passed after environment and NumPy
  updates; `uv run jupyter nbconvert --to notebook --execute --stdout
  notebooks/01_oc20_reconnaissance.ipynb` completed without saving outputs.
- Output/figure/report: visual inspection in ASE GUI; detailed observations in
  `docs/design/oc20-data-understanding.md`; reproducible notebook in
  `notebooks/01_oc20_reconnaissance.ipynb`.

### Decisions and rationale

- Treat extended-XYZ energy and sidecar reference energy as separate fields.
- Treat shard ordering and sidecar correspondence as explicit data integrity
  invariants.
- Adopt NumPy for the supported OC20 mapping format; defer ASE and FAIR-Chem as
  runtime dependencies until an adapter is required; retain ASE as a
  development-only visualisation tool.

### Limitations or failures

- The first metadata load failed until NumPy was installed, demonstrating that
  its presence is a format requirement.
- The current evidence covers only one training subset and one manually
  inspected record; no golden fixture or automated profiler output exists.

### Next actions

- Implement deterministic discovery and numeric shard-pair validation with
  tests based on small reviewed synthetic fixtures.

## 2026-09-05 — Deterministic OC20 profiler baseline evaluation

### Goal

- Establish reproducible correctness and local runtime evidence for the
  discovery-to-profile baseline before transformations or agent workflow work.

### Work completed

- Added deterministic discovery, paired-shard inspection, lexical schema,
  sampled consistency, opt-in mapping checks, bounded trusted metadata
  profiling, and serialisable composed-profile evidence.
- Kept every unit convention unresolved until it has a field-specific
  authoritative source; no unit is inferred from raw values.
- Changed multi-sample consistency to stream each shard once and reuse trusted
  mapping loads within a single profile operation.

### Evidence

- Fixture coverage: valid and invalid numeric pairs, malformed structures,
  row-count mismatches, schema consistency, mapping-key outcomes, and a
  path-independent golden profile summary.
- Reproducibility: the same synthetic fixture yields identical normalised JSON
  on repeated profile runs.
- Command/result: `uv run ruff check && uv run pytest` — 23 passed on Python
  3.12.14.
- Local timing, S2EF 200K shard `0` (single run; descriptive only): discovery
  0.0049 s; one-pair inspection 0.8678 s; three-sample consistency 0.8618 s.

### Limitations

- Timings are not a cross-machine benchmark and do not include trusted pickle
  deserialisation, full-shard schema profiling, or transformations.

## 2026-09-11 — OC20 profiler acceptance evaluation

### Goal

- Demonstrate that the deterministic profiler can produce repeatable,
  human-readable, read-only evidence on the local OC20 S2EF 200K subset.

### Work completed

- Added a standard-output-only acceptance command that composes a bounded
  profile and fixed-sample consistency evidence without loading mapping
  pickles by default.
- Ran the command twice against shard `0`, record `0`, and consistency records
  `0 1 2`, retaining generated JSON only under `/private/tmp/`.
- EDA practices: Discovering, Structuring, Validating, and Presenting.

### Evidence

- Commit/configuration: working tree based on `26c5d4d`; Python 3.12.14;
  `uv sync --locked`; pickle loading disabled.
- Input/fixture: local OC20 S2EF 200K subset under `data/raw/`; shard `0`;
  fixed records `0`, `1`, and `2`.
- Test/command/result: two JSON acceptance runs compared with `cmp` were
  byte-identical. The aggregate summary reported 40 valid shard pairs, all
  three structure and sidecar samples found, no issue codes, and unresolved
  unit evidence.
- Output/figure/report: one summary run completed in 1.888 seconds elapsed.
  This is descriptive local timing, not a cross-machine benchmark; the JSON
  reports were not retained in the repository.

### Decisions and rationale

- The Phase 1 reporting gap is closed for the bounded OC20 profile: the same
  configuration now produces serialisable evidence and a concise summary
  without exposing source-record values.
- Select split/group leakage-risk evidence as the next Phase 1 gap. This run
  confirmed file, sample, and schema evidence, but it did not exercise a
  relationship-group or split-risk scenario, which remains an explicit
  evaluation requirement.

### Limitations or failures

- The run covers one training-subset shard and three fixed records only; it
  does not establish full-subset schema uniformity or cross-type support.
- Mapping pickles were deliberately not deserialised, so no trusted metadata
  or clean-slab relationship claim is made from this acceptance run.

### Next actions

- Add a reviewed synthetic group/split-risk scenario and deterministic warning
  evidence before considering controlled preprocessing or agent workflow work.

## 2026-09-11 — Explicit group/split risk oracle

### Goal

- Add deterministic leakage-risk evidence without inventing an OC20 group
  semantic.

### Work completed

- Added a pure analyser for caller-supplied group/split assignments and
  synthetic cross-split, same-split, missing-evidence, and repeatability tests.
- EDA practices: Structuring and Validating.

### Evidence

- Commit/configuration: `c86127c`; Python 3.12.14.
- Input/fixture: in-memory synthetic assignments only; no raw OC20 files or
  mapping pickles.
- Test/command/result: `uv run pytest tests/test_oc20_risks.py -v` — 4 passed;
  full suite — 43 passed.

### Decisions and rationale

- A leakage risk is reported only for explicitly supplied group IDs that span
  multiple split labels. Missing values are warning evidence and do not create
  a safe group result.

### Limitations

- Clean-slab IDs and metadata fields are not treated as leakage groups. No
  claim about their grouping semantics is made until an authoritative OC20
  source defines that relationship.

## 2026-09-11 — Explicit sequence-order risk oracle

### Goal

- Add deterministic ordering-risk evidence without inventing OC20 trajectory
  semantics.

### Work completed

- Added a pure analyser for caller-supplied ordered-group assignments and
  synthetic duplicate, non-monotonic, safe-control, invalid-evidence, and
  repeatability tests.
- EDA practices: Structuring and Validating.

### Evidence

- Commit/configuration: current sequence-risk feature slice; Python 3.12.14.
- Input/fixture: in-memory synthetic ordered-group assignments only; no raw
  OC20 files or mapping pickles.
- Test/command/result: `uv run pytest tests/test_oc20_sequence_risks.py -v` —
  4 passed.

### Decisions and rationale

- The caller supplies both group IDs and observed order. Duplicate positions
  and decreasing positions are evidence of risk; missing or negative positions
  are uncertainty, not a safe result.

### Limitations

- No OC20 S2EF record is claimed to be a trajectory/image sequence. The
  analyser is not connected to OC20NEB until an authoritative grouping and
  ordering source is documented.

## 2026-09-11 — OC20 evidence-grounded readiness planner

### Goal

- Demonstrate a user-goal-aware planning contract without a transformation or
  LLM.

### Work completed

- Added a pure readiness planner that combines a caller-supplied goal with
  aggregate OC20 profile evidence and returns review-only checks, risks,
  assumptions, and validation requirements.
- EDA practices: Structuring, Validating, and Presenting.

### Evidence

- Input/fixture: in-memory synthetic OC20 profile fixtures only; no raw OC20
  files or mapping pickles.
- Test/command/result: `uv run pytest tests/test_oc20_planning.py -v` — 4
  passed.

### Decisions and rationale

- The plan blocks when profile selection is invalid and requests review for
  unresolved units. It performs no mutation and retains the user goal verbatim.

### Limitations

- The planner does not interpret goal text beyond retaining it, call an LLM,
  execute an operation, or provide approval workflow state.

## 2026-09-11 — Phase 1 deterministic-profiler closeout

### Goal

- Consolidate the deterministic-profiler evaluation evidence before starting
  any formal Phase 2 implementation.

### Work completed

- Re-ran the bounded, read-only local acceptance oracle twice and compared its
  JSON reports byte-for-byte.
- Mapped every Phase 1 workstream to its focused synthetic tests, local
  acceptance evidence, and explicit boundary in the
  [Phase 1 acceptance matrix](design/oc20-profiler-phase-1-acceptance.md).
- EDA practices: Discovering, Structuring, Joining, Validating, and Presenting.

### Evidence

- Commit/configuration: documentation closeout working tree; Python 3.12.14;
  `uv sync --locked`; mapping pickle loading disabled.
- Input/fixture: local S2EF-200K training subset under `data/raw/`; shard `0`;
  sample `0`; fixed consistency samples `0`, `1`, and `2`; reviewed synthetic
  fixtures in the automated suite.
- Test/command/result: two JSON acceptance runs compared with `cmp` were
  byte-identical. The summary reported 40 valid pairs, no issue codes,
  unresolved unit evidence, and structures and sidecars present for all three
  fixed samples. One summary run took 0.892 seconds elapsed.
- Output/figure/report: JSON comparison outputs remain only in `/private/tmp`;
  the committed record contains aggregate evidence only.

### Decisions and rationale

- Close Phase 1 for the bounded S2EF-200K/synthetic-fixture scope. Evidence
  supports deterministic profiling and reporting, not a claim of general OC20
  support or autonomous preprocessing.
- Keep Phase 2 not formally started. The early readiness planner is
  non-executing preparatory evidence and does not authorize transformations,
  approval workflow, LangGraph, or agents.

### Limitations

- The local check examines one shard and three fixed records; it does not prove
  full-subset schema uniformity, mapping correctness, or cross-type support.
- Units, relationship semantics, and sequence semantics remain unresolved
  without authoritative source evidence.

### Next actions

- Select and approve the next phase only when it addresses a documented
  evaluation gap; do not infer an execution workflow from this closeout.

## 2026-09-11 — Profiler review safety corrections

### Goal

- Correct the deterministic-profiler safety and reporting defects identified
  before any formal Phase 2 work.

### Work completed

- Aggregated and deduplicated selected-pair inspection, schema, and
  mapping-validation issues into profile evidence used by the readiness planner
  and concise acceptance summary.
- Blocked readiness planning for structural-integrity failures; made incomplete
  fixed-sample consistency unknown rather than consistent; rejected symlinked
  discovery paths; and added blank-ID, malformed-mapping, and atom-row schema
  validation evidence.
- Clarified that acceptance makes two complete scans of the selected shard.
- EDA practices: Discovering, Structuring, Joining, Validating, and Presenting.

### Evidence

- Commit/configuration: the profiler-review fix commit containing this entry;
  Python 3.12.14; `uv sync --locked`; mapping pickle loading disabled.
- Input/fixture: reviewed synthetic fixtures plus the local S2EF-200K training
  subset under `data/raw/`; shard `0`; sample `0`; fixed consistency samples
  `0`, `1`, and `2`.
- Test/command/result: focused regression tests were written first and failed
  against the prior behaviour. The full suite passed with 60 tests. Two JSON
  acceptance runs compared with `cmp` were byte-identical. The summary reported
  40 valid pairs, `pickle_load_not_authorized`, unresolved unit evidence, and
  structures and sidecars present for all three fixed samples in 0.960 seconds.
- Output/figure/report: JSON comparison outputs remain only in `/private/tmp`;
  the committed record contains aggregate evidence only.

### Decisions and rationale

- Disabled pickle loading is visible policy evidence, not a data-integrity
  failure; it does not by itself block a review-only plan.
- Data-integrity and schema failures block readiness planning. Unknown
  consistency remains distinct from a positive consistency result.

### Limitations

- Acceptance still performs two complete selected-shard scans. The cost is
  documented rather than presented as a constant-byte sample operation.
- The local result remains a bounded spot check and does not establish
  full-subset uniformity or support for other OC20 tasks.
