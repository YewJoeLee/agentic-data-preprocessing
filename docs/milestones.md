# FYP milestones

The dates below are transcribed from the supplied academic-year schedule.
Confirm any changes with the supervisor or programme office.

| Date | Milestone | Repository implication |
| --- | --- | --- |
| 10 Aug 2026 | FYP starts | Begin project work and maintain research notes. |
| 31 Aug 2026 | Project Plan/Strategy submitted to supervisor | Current near-term priority: finalize scope, architecture, risks, and initial plan. |
| 25 Jan 2027 | Interim Report submitted | Have a documented prototype, experiments, and progress evaluation. |
| 22 Mar 2027 | Final Report submitted | Submit the report for grading before any later amendments. |
| 16 Apr 2027 | Amended Final Report submitted | Final report submission after supervisor/examiner feedback. |
| 7, 10–12 May 2027 | Oral presentation | Prepare the presentation and question-and-answer material. |

## Immediate planning focus

The first technical milestone should be:

```text
Repository
  → Python environment
  → OC20 metadata or small subset
  → Manual dataset understanding
  → Deterministic dataset profiler
  → LLM reasoning layer
  → Agent workflow
```

Do not treat the full agent, UI, or all five dataset adapters as prerequisites
for the project plan.

## Detailed delivery plan

This plan expands the official dates above into a working sequence. It is a
planning baseline rather than a replacement for supervisor direction. Update
the dates, scope, and acceptance criteria when the project plan is reviewed.

### Phase 0 — project plan and experiment setup

**10–31 August 2026** — complete the project plan while keeping the first
technical experiment deliberately small.

| Week | Focus | Deliverables and evidence |
| --- | --- | --- |
| 10–16 Aug | Establish the repository and problem framing. | Repository scaffold; initial scope; reading register; confirmation of the final-year-project schedule. |
| 17–23 Aug | Translate the proposal into a testable first vertical slice. | Project scope; milestone plan; master notes; draft profile contract; risks and non-goals. |
| 24–30 Aug | Finalise the plan and define the baseline experiment. | Supervisor-ready project plan; initial OC20 subset/fixture decision; acceptance criteria; report outline. |
| 31 Aug | Submit project plan/strategy. | Submitted document and a dated record of any supervisor feedback. |

**Gate:** the project-plan submission must make a narrow, falsifiable claim:
the initial implementation is a deterministic dataset profiler, not a complete
autonomous preprocessing platform.

### Phase 1 — deterministic dataset-profiler baseline

**September–October 2026** — build a small, testable profiler for a local OC20
subset or reviewed synthetic atomistic fixtures.

| Workstream | Target capability | Acceptance evidence |
| --- | --- | --- |
| Discovery | Find files/directories, identify supported formats, and choose a safe representative sample. | Tests covering supported files, unsupported files, empty inputs, and sample-selection behaviour. |
| Record inspection | Inspect supported records and expose shapes, field names, types, missingness, candidate identifiers, labels, and split information. | Stable structured profile plus golden output for reviewed fixtures. |
| Scientific metadata | Surface units, atomistic structure metadata, groupings, mappings, and sequence/trajectory semantics where supported. | Explicit evidence fields and warnings for missing or ambiguous metadata. |
| Relationships and risks | Identify alignment, grouping, leakage, ordering, and schema-consistency risks. | Adversarial fixtures or scenarios that demonstrate detected warnings. |
| Reporting | Produce a machine-readable profile and concise human-facing summary. | Reproducible example input/output and documented limitations. |

**Gate:** do not introduce an agent framework, UI, or broad transformation
engine until the profiler can be run reproducibly and evaluated against known
facts.

### Phase 2 — safe planning and controlled preprocessing

**November–December 2026** — extend the working profiler only with a bounded,
transparent preprocessing workflow.

| Capability | Minimum behaviour | Evidence to keep |
| --- | --- | --- |
| LangGraph workflow | Implement explicit graph state, approval checkpoints, retry handling, and validation transitions after the profiler gate. | Tested graph run from profile to validated report. |
| Preprocessing plan | Convert a user goal and profiler evidence into proposed operations, assumptions, risks, and validation checks. | Example plans that cite observations rather than unsupported assumptions. |
| Preview and approval | Show source scope and predicted impact before consequential actions; require confirmation where ambiguity or loss exists. | Before/after previews and documented approval scenarios. |
| Deterministic execution | Run a small allow-listed set of explicit operations; preserve source data. | Tool tests, generated configuration/code, and provenance records. |
| Validation | Compare outputs with input and stated task; check labels, group/split constraints, units, and ordering where applicable. | Validation reports and leakage-prevention scenarios. |
| Replay/rollback | Make important steps reconstructable and recoverable. | A replay example and documented rollback or non-destructive output policy. |

**Gate:** make no claim that the prototype autonomously cleans scientific data.
The contribution is evidence-led planning and deterministic, inspectable
operations.

### Phase 3 — evaluation and interim report

**January 2027** — turn implementation artefacts into defensible evaluation
evidence before the interim-report deadline.

| Evaluation dimension | Question | Minimum artefact |
| --- | --- | --- |
| Correctness | Are profile facts and warnings right for the inspected data? | Golden tests, manual spot checks, and error categories. |
| Leakage prevention | Are related records, groups, windows, or trajectories kept in valid splits? | Scenario tests that catch invalid split/group handling. |
| Reproducibility | Can the same input and configuration reproduce a result? | Versioned configuration, sampling policy, repeated-run comparison. |
| Runtime | Is inspection practical for a representative local subset? | Timings with machine context and input size. |
| Explanation quality | Can a user trace claims and recommended actions to observed evidence? | Simple rubric with annotated examples. |

**By 25 January:** submit an interim report containing the problem framing,
implemented baseline, preliminary evaluation, failures/limitations, and the
revised plan for the final phase.

### Phase 4 — broaden evaluation and complete the report

**February–22 March 2027** — stabilise the prototype, deepen evaluation, and
write the final report.

| Period | Focus | Deliverables and evidence |
| --- | --- | --- |
| February | Improve the profiler and safe workflow only where evaluation exposes a concrete gap; introduce scoped multi-agent sequential/parallel orchestration if role contracts are stable; test one contrasting Open Catalyst semantic case if feasible. | Change log tied to evaluation findings; orchestration/merge scenarios; expanded scenario matrix; limitations register. |
| Early March | Freeze the demonstration path and assemble final results. | Stable small local demo input; final figures/tables; reproducibility checklist; draft presentation narrative. |
| By 22 March | Submit the final report. | Report, source-code snapshot, evaluation evidence, and complete references. |

**Gate:** distinguish clearly between implemented/tested functionality and
future work. Do not add risky late-stage features unless they directly resolve a
documented evaluation gap.

### Phase 5 — amendments and oral presentation

**23 March–May 2027** — address feedback, polish the evidence trail, and
prepare the defence.

| Period | Focus | Deliverables and evidence |
| --- | --- | --- |
| 23 Mar–16 Apr | Incorporate approved supervisor/examiner feedback. | Amendment log that connects feedback to report changes. |
| By 16 Apr | Submit amended final report. | Final amended report. |
| Mid-April–early May | Build and rehearse the presentation using the same claims and evidence as the report. | Slide deck, demo script, backup screenshots, timed rehearsal notes, Q&A bank. |
| 7, 10–12 May | Oral presentation. | Stable local demonstration; backup material; concise answers on scope, evidence, safety, and limitations. |

## Recurring evidence routine

- At the end of each implementation week, run relevant tests and retain one
  representative input/output example.
- Record experiments, decisions, and limitations in
  [master-notes.md](master-notes.md), including the commit or configuration
  that produced the result.
- Keep `data/raw/` immutable. Commit only reviewed fixtures and small golden
  outputs required for reproducible evaluation.
- Request approval before downloading large datasets or using paid model/API
  services.
- Every two weeks, review the milestone plan against actual evidence and adjust
  the next work item rather than silently expanding the scope.
