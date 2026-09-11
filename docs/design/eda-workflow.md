# Exploratory data analysis workflow guideline

This guideline is the project-wide reference for exploratory data analysis
(EDA). It adapts the six-practice framing from the supplied Google Career
Certificate reference guide: EDA is iterative and non-sequential. It does not
replace the project safety rules, dataset-specific documentation, or a
scientific transformation specification.

The practices may recur in any useful order. Validation is required after any
consequential operation, and presenting evidence may reveal a need to return to
discovery, structuring, joining, or validation.

## Six practices in this project

| Practice | Purpose here | Safety boundary | Current OC20 evidence |
| --- | --- | --- | --- |
| Discovering | Inventory local files, formats, and candidate relationships. | Read-only; do not decompress, load pickles, or select ambiguous inputs without recording it. | README, compressed shards, and mapping pickles are discovered and numeric shard pairs are checked. |
| Structuring | Describe records, schemas, fields, shapes, lexical types, identifiers, and missingness evidence. | Retain raw values and distinguish observations from scientific interpretation. | Bounded extended-XYZ and sidecar samples are profiled into JSON-safe schema evidence. |
| Cleaning | Identify potential data-quality concerns and propose explicit corrective operations. | Never silently alter scientific values, labels, units, mappings, or trajectory order. Actual cleaning is deferred until an approved controlled-workflow stage. | Not implemented; malformed, missing, and unresolved information are reported as evidence. |
| Joining | Relate records using documented identifiers and mappings. | Validate keys, preserve absent relationships, and never fabricate a match. | Sampled `system_id` values are checked against trusted metadata and clean-slab mappings only after explicit authorisation. |
| Validating | Check integrity, provenance, schemas, joins, assumptions, and effects of an operation. | Repeat after discovery choices, joins, structuring, cleaning, and any future transformation. | Numeric pairing, row-count, malformed-record, schema-consistency, mapping-key, checksum, explicit group/split, explicit sequence-order, and golden-output checks are implemented. |
| Presenting | Communicate evidence, uncertainty, limitations, previews, and required approvals. | Do not present inferred scientific meaning or a transformed result as a source fact. | The profiler produces serialisable evidence and the reconnaissance notebook presents one read-only structure view. |

## How to use this guideline

1. Scope each experiment or implementation task by naming the EDA practices it
   exercises; do not assume the six practices form a one-way sequence.
2. Record the evidence, assumptions, limitations, and validation performed for
   those practices in the development log.
3. Treat Cleaning as a proposed operation until a future approved workflow
   specifies its deterministic tool, source scope, expected impact, and
   validation checks.
4. Use Presenting to expose uncertainty and request review. Feedback may start
   another EDA iteration; it is not proof that data are clean or ready for a
   model.

## Current milestone position

As of 11 September 2026, the project has completed **Phase 1: deterministic
dataset-profiler baseline** (September--October 2026) of the
[milestone plan](../milestones.md) for its bounded scope. The core OC20
evidence path is implemented and tested: discovery, bounded structuring, safe
joining, validation, and minimal presentation. Cleaning, LLM-based planning,
deterministic transformations, approval checkpoints, LangGraph, and multi-agent
orchestration are not implemented.

The deterministic-profiler acceptance scope is closed for its bounded evidence
claims; its workstream-by-workstream evidence and limitations are recorded in
the [Phase 1 acceptance matrix](oc20-profiler-phase-1-acceptance.md). A
non-executing readiness planner exists as early preparatory evidence, but Phase
2 has not started formally. LLM-based planning, deterministic transformations,
approval checkpoints, LangGraph, and multi-agent orchestration remain
unimplemented.

## Source note

The iterative, non-sequential six-practice framing is adapted from the supplied
*Reference guide: The EDA process* (Google Career Certificate). This guideline
uses original project-specific wording and applies stricter controls for
scientific data.
