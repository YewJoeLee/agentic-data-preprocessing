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
| Cross-type generalisation | Does the profiler surface meaningful differences across OC data variants? | Scenario matrix across OC20 plus feasible contrasting variants. |
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
| Task-aware plan | Profile plus a user goal. | Produce evidence-cited plan, assumptions, risk class, preview, and validation steps. | Explanation quality, reproducibility. |
| Approved operation | Small safe/allow-listed transformation. | Produce derived output, configuration, provenance, and validation report. | Reproducibility, validation. |
| Orchestration safety | Multi-agent graph with allowed parallel read-only branches and sequential mutation path. | Merge evidence deterministically; block unapproved/unsafe concurrent actions. | Reliability, correctness, reproducibility. |

Only add a full dataset family when a small documented subset and a clear scenario justify the cost. Record omitted scenarios and their reason.

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
profile, and fixed sample consistency without pickle loading. The acceptance
oracle is that it reports the discovered README and numeric-pair inventory;
either completes selected-pair inspection and fixed samples or returns explicit
issue codes; emits byte-identical JSON across two identical runs; and leaves
every unit-evidence status unresolved. Record elapsed time only as descriptive
local evidence with input configuration, revision, and machine context.

The command's concise summary must contain aggregate counts, issue codes,
mapping-load policy, and unit-evidence status. It must not use raw coordinates,
energies, system IDs, or mapping values as human-facing acceptance evidence.

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
