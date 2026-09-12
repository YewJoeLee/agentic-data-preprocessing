# Evaluation plan

## Evaluation aim

Assess whether the prototype makes scientific-data understanding and preprocessing decisions more correct, safe, reproducible, and explainable on representative Open Catalyst scenarios. Evaluation must be more than a successful end-to-end demonstration.

## Evaluation dimensions

Interpret evaluation results using the project priority order: **accuracy ->
reliability -> scalability -> cost -> speed -> security**. A result that gains
speed or lowers cost does not compensate for an incorrect or unreliable
scientific outcome.

| Dimension | Question | Evidence / measure |
| --- | --- | --- |
| Correctness | Are profile facts, inferred relationships, and warnings correct for inspected data? | Golden fixture assertions, manual spot checks, categorised errors. |
| Leakage prevention | Are related records, groups, windows, or trajectories kept in valid splits? | Adversarial split/group scenarios and caught validation failures. |
| Reproducibility | Can the same input/configuration reproduce the same profile or output? | Versioned configuration, sampling policy, hashes/diffs, repeated-run comparison. |
| Cross-type generalisation | Does the prototype surface and preserve meaningful differences across the five declared OC sources? | Source-specific adapter acceptance matrix across documented source-derived representative subsets; reviewed synthetic fixtures test negative or failure cases only. |
| Runtime | Is inspection practical for a representative local subset? | Timings by step with machine context and input size. |
| Explanation quality | Can a user trace claims/actions back to evidence? | Rubric: evidence, clarity, uncertainty, risk, next action. |

## Dataset and scenario matrix

| Scenario | Dataset/fixture | Expected behaviour | Primary dimensions |
| --- | --- | --- | --- |
| Basic discovery/profile | Small OC20 subset or synthetic atomistic fixture. | Identify files, records, fields, labels, and splits; emit stable profile. | Correctness, reproducibility, runtime. |
| Missing/ambiguous metadata | Reviewed fixture with missing unit/field/group information. | State uncertainty and warn rather than invent a value or meaning. | Correctness, explanation quality. |
| Group/split risk | Fixture with related records that could be split independently. | Surface leakage risk or reject invalid handling. | Leakage prevention, validation. |
| Ordering risk | OC20NEB-like ordered-image fixture. | Preserve and explain sequence/reaction-grouping constraints. | Correctness, safety, explanation quality. |
| Mapping alignment risk | OC20Dense-like structure/mapping fixture. | Detect or report broken/misaligned mappings. | Correctness, validation. |
| Task-aware plan | Profile plus a user goal. | Produce a schema-valid, evidence-cited plan, assumptions, risk class, preview, validation steps, and LLM run record when a model is used. | Explanation quality, reproducibility. |
| Approved operation | Small safe/allow-listed transformation. | Produce derived output, configuration, provenance, and validation report. | Reproducibility, validation. |
| Orchestration safety | Multi-agent graph with allowed parallel read-only branches and sequential mutation path. | Merge evidence deterministically; block unapproved/unsafe concurrent actions; retain state, retry, approval, and merge evidence. | Reliability, correctness, reproducibility. |

Only add support for a representative subset from a declared dataset family
when a documented input and clear scenario justify the cost. Record omitted
scenarios and their reason.

## Planned source coverage and adapter acceptance

Each source becomes supported only after the listed source-specific oracle
passes on a documented source-derived representative subset. A reviewed
synthetic fixture that resembles a source's risk is useful evaluation evidence,
but it is not source-adapter support.

| Source | Current status | Semantic oracle for planned adapter support |
| --- | --- | --- |
| OC20 | Bounded S2EF-200K profiler accepted. | Maintain the Phase 1 acceptance oracle and use it as the controlled-workflow baseline. |
| OC22 | Not supported. | Identify and retain total-energy label evidence; block comparisons or aggregation that present those values as OC20 adsorption energies. |
| OC20-mAds | Not supported. | Surface variable adsorbate composition and coverage metadata; report absent or inconsistent composition evidence without inventing a match. |
| OC20Dense | Not supported. | Validate explicit structure, target, group, and mapping alignment; report missing or ambiguous counterparts. |
| OC20NEB | Not supported. | Validate authoritative reaction IDs and strictly ordered image positions before any reaction-level or transition-state summary. |

Every planned adapter acceptance record must name the source reference, input
format, sample policy, parser/tool version, preserved invariant, known
unsupported features, and repeated-run result. The Phase 3 evidence cards and
Phase 4 timing are maintained in [milestones](../milestones.md).

## User-goal coverage

The goal suite makes the proposal's example requests testable without treating
unsupported source semantics as known facts.

| User goal | Required evidence and safe outcome |
| --- | --- |
| Explain a dataset's files, fields, units, record structure, and possible tasks. | Return discovered evidence and clearly label unknown units or semantics; make no transformation. |
| Prepare an OC20 subset for model training. | Produce an evidence-cited, previewed plan; execute only approved initial allow-listed operations and preserve source data. |
| Prepare a sequence dataset for forecasting. | Require explicit group and time/order fields; warn or refuse when they are absent, ambiguous, or unsuitable for leakage checks. |
| Convert an OC20NEB trajectory to reaction-level records. | Refuse until the OC20NEB adapter validates authoritative reaction groups, image order, and field-specific units; then require preview, approval, and validation. |

## Baseline evidence status

The OC20 deterministic-profiler baseline now has reviewed synthetic fixtures
covering valid discovery, missing or duplicate counterparts, row-count
mismatches, malformed structures, unauthorised pickles, mapping-key outcomes,
and a stable golden-profile summary. A repeat-run test compares normalised JSON
for the same fixture. Runtime is measured separately on the local 200K subset;
it is descriptive local evidence, not a cross-machine benchmark.

The composed-profile golden summary also asserts that unit conventions are
explicitly unresolved until a field-specific authoritative source is recorded.
Trusted metadata-present/absent and clean-slab-relationship-absent scenarios
preserve raw anomaly codes or explicit absence without fabricating values.

## Phase 1 local acceptance oracle

The bounded local OC20 acceptance command runs discovery, one selected shard
profile, and fixed sample consistency without pickle loading. Its JSON report
contains the discovered README and numeric-pair inventory; its concise summary
contains aggregate counts and issue codes only. The oracle is that it either
completes selected-pair inspection and fixed samples or returns explicit issue
codes, emits byte-identical JSON across two identical runs, and leaves every
unit-evidence status unresolved. Record elapsed time only as descriptive local
evidence with input configuration, revision, and machine context.

The command's concise summary must contain aggregate counts, issue codes,
mapping-load policy, and unit-evidence status. It must not use raw coordinates,
energies, system IDs, or mapping values as human-facing acceptance evidence.
It uses one full selected-pair integrity scan and one full fixed-sample
consistency scan, so its bounded scope is the selected shard and samples, not
constant-byte runtime.

The resulting bounded-scope closeout is recorded in the
[Phase 1 acceptance matrix](oc20-profiler-phase-1-acceptance.md). It maps each
Phase 1 workstream to the applicable oracle, observed evidence, and retained
limitation; it is not a substitute for the cross-type and operation scenarios
listed in this plan.

## Explicit group/split risk oracle

`analyse_group_split_risks()` reports a cross-split group only when its caller
supplies the same explicit group ID with two or more distinct split labels.
Missing group IDs and missing split labels are warning evidence, not a safe
result, and the affected assignment is excluded from group aggregation. This
oracle does not derive group IDs from OC20 clean-slab mappings, metadata fields,
filenames, shard order, or record order.

## Explicit sequence-order risk oracle

`analyse_sequence_risks()` reports duplicate positions and decreasing positions
only within caller-supplied explicit group IDs. Iterable order is treated as
observed source order because the caller supplies it; a missing group, missing
position, or negative position is warning evidence and is excluded from
aggregation. The oracle does not derive trajectory, reaction, image-order, or
other sequence semantics from OC20 S2EF data, mappings, filenames, or record
order. An authoritative OC20NEB source is required before applying this check
to an OC20NEB dataset.

## Evidence-grounded readiness-plan oracle

`build_oc20_readiness_plan()` preserves a non-empty caller-supplied goal and
produces a non-executing plan from aggregate `Oc20Profile` evidence. It blocks
when no valid shard pair is selected, surfaces unresolved unit fields and
profile issue codes as review/risk evidence, and requires deterministic-profile
plus explicit group/split and sequence-order validation before any future
operation. Its output contains no raw source-record values or mutation step;
passing this oracle is not evidence of autonomous preprocessing.

## Explanation-quality rubric

| Criterion | Pass condition |
| --- | --- |
| Evidence | Important claims point to files, fields, records, or computed observations. |
| Clarity | A user can identify what was found, what is proposed, and what happens next. |
| Uncertainty | Missing, ambiguous, or unsupported information is labelled rather than guessed. |
| Safety | Risks to labels, units, ordering, group alignment, or splits are visible. |
| Actionability | The plan, approval requirement, deterministic tool, and validation check are clear. |

## Experiment record

Record each experiment in [the development log](../development-log.md) with:

- experiment ID/date and research question;
- input/fixture and sample-selection method;
- source-code revision, command/configuration, and tool/model versions;
- observed result, expected oracle, and outcome;
- metrics, figures, profile/output paths, and limitations;
- report section or oral slide where the evidence will be used.

## Reporting rules

- Report unsuccessful cases and limitations alongside successes.
- Do not aggregate non-equivalent targets such as OC20 and OC22 energies as if they were directly comparable.
- State the oracle behind each correctness claim.
- Use “demonstrates on representative subsets” rather than claims of universal scientific-data support.
