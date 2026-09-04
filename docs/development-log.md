# Weekly development log

Use this log to retain the evidence needed for the interim report, final report, and oral presentation. The calendar plan is in [milestones.md](milestones.md); the evaluation framework is in [design/evaluation-plan.md](design/evaluation-plan.md).

## Update routine

- Add one entry per active development week and one entry for every meaningful experiment or design decision.
- Include the commit, command/configuration, fixture/subset, and observed outcome wherever applicable.
- Record failed experiments and limitations immediately.
- Link to saved figures, reports, or golden outputs rather than pasting large generated artefacts into this file.

## Weekly entry template

```md
## YYYY-MM-DD to YYYY-MM-DD — Week [N]

### Goal

- [What project question or milestone was this week intended to advance?]

### Work completed

- [Implementation, reading, design, or evaluation work]

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
