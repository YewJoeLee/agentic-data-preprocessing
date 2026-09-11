# OC20 deterministic-profiler Phase 1 acceptance

## Scope and decision

This record closes the bounded **Phase 1 deterministic OC20 profiler** scope on
11 September 2026. It evaluates the local OC20 S2EF-200K training subset and
reviewed synthetic fixtures; it does not establish support for every OC20 task
or data family. The underlying data remain read-only under `data/raw/`.

The phase is accepted for its stated scope: deterministic discovery, bounded
record and schema evidence, explicit uncertainty, relationship-risk checks
with caller-supplied semantics, and serialisable reporting. The evidence does
not authorize transformations, autonomous cleaning, an approval workflow,
LangGraph, or agent orchestration.

## Acceptance matrix

| Phase 1 workstream | Evidence and oracle | Observed outcome | Boundary retained |
| --- | --- | --- | --- |
| Discovery and numeric pairing | `tests/test_oc20_discovery.py`; local acceptance command | Synthetic fixtures cover valid, missing, and duplicate counterparts. The local summary found 40 valid numeric pairs and no issue codes. | The result inventories the local subset only; it does not assert coverage of validation/OOD splits or other OC20 releases. |
| Bounded record inspection and schema evidence | `tests/test_oc20_inspection.py`, `tests/test_oc20_schema.py`, and `tests/test_oc20_profile.py`; fixed local samples `0`, `1`, and `2` | Fixtures cover matched counts, mismatches, malformed sidecars, truncated structures, lexical schema evidence, and a stable composed profile. The local run found all three structure and sidecar samples. | Fixed samples do not prove schema uniformity across every record or shard. |
| Scientific metadata and units | `tests/test_oc20_mappings.py` and unit-evidence profile tests | Mapping access requires explicit pickle trust; serialised unit evidence remains unresolved without field-specific authoritative documentation. | The acceptance command disables pickle loading and makes no trusted-metadata, mapping-value, or inferred-unit claim. |
| Relationships and risk evidence | `tests/test_oc20_risks.py` and `tests/test_oc20_sequence_risks.py` | Synthetic scenarios deterministically identify cross-split group risks and duplicate/non-monotonic positions only when callers supply explicit group and order semantics. | No clean-slab ID is inferred to be a leakage group, and no S2EF record is treated as an OC20NEB sequence. OC20Dense alignment remains out of scope. |
| Reporting and reproducibility | `tests/test_oc20_acceptance.py`; repeated local JSON acceptance run compared with `cmp` | Two identical runs produced byte-identical JSON. The concise summary contained aggregate counts, mapping policy, unit status, issue codes, and fixed-sample counts without raw source values. | The 0.892-second run is descriptive local evidence, not a cross-machine performance benchmark. |

## Read-only local acceptance configuration

The closeout used Python 3.12.14 and the lockfile-resolved environment. Mapping
pickle loading was disabled. It selected shard `0`, inspected sample `0`, and
checked fixed consistency samples `0`, `1`, and `2`.

```bash
uv run python -m agentic_preprocessing.oc20_acceptance \
  --dataset-root data/raw \
  --shard-stem 0 \
  --sample-index 0 \
  --consistency-indices 0 1 2 \
  --format summary
```

The command reported 40 valid shard pairs, no issue codes, disabled mapping
pickle loading, unresolved unit evidence, and structures and sidecars present
for all three fixed consistency samples. Two JSON runs with the same arguments
were byte-identical. Generated reports were retained only in `/private/tmp`.

## Remaining limitations and follow-up gate

- The acceptance run is a bounded spot check, not a full-subset scan or a
  cross-type generalisation result.
- Unit conventions, mapping semantics, and sequence/group relationships remain
  unresolved unless a field-specific or dataset-authoritative source supports
  them.
- The mapping-alignment and OC20NEB scenarios in the evaluation plan remain
  future, separately justified work; they are not silently generalized from
  S2EF evidence.
- Any Phase 2 work must begin with a separate, approved preview-and-approval
  design. The committed readiness planner is non-executing preparatory
  evidence, not a Phase 2 implementation start.

## Evidence links

- [Evaluation plan](evaluation-plan.md)
- [OC20 data-understanding note](oc20-data-understanding.md)
- [EDA workflow guideline](eda-workflow.md)
- [Development log](../development-log.md)
- [Milestones](../milestones.md)
