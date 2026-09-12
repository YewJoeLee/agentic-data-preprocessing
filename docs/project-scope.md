# Operational scope and dataset boundaries

This is the canonical record of the project's **current operational scope**:
what data families are in bounds, which safety boundaries apply, and what work
is deferred. It does not repeat the proposal objectives, deliverables, or
future architecture; those belong to the
[project brief](design/project-brief.md), [requirements](design/requirements.md),
and [architecture](design/architecture.md).

## Current operational boundary

The completed first implementation is a deterministic, read-only OC20
profiler for a local S2EF-200K subset and reviewed synthetic fixtures. It
discovers files, validates numeric shard pairs, inspects bounded samples,
produces serialisable evidence, and reports uncertainty rather than changing
scientific values.

Raw input remains immutable. LLM reasoning, transformations, approval
checkpoints, LangGraph, multi-agent orchestration, a UI, and a database are not
implemented. The non-executing readiness planner is preparatory evidence, not
a formal Phase 2 workflow. See [milestones](milestones.md) for authoritative
phase status and the [Phase 1 OC20 acceptance record](design/oc20-profiler-phase-1-acceptance.md)
for the tested boundary.

The system must never silently invent values, change labels, reorder sequences
or trajectories, or make scientifically consequential imputations. Any future
ambiguous or destructive operation requires explicit approval and a
non-destructive, reproducible validation path.

FLASH weather sequences are not in the active scope and are considered only if
a documented evaluation gap and data access justify them.

All committed implementation and evaluation coverage is atomistic. The final
report must describe the prototype as evidence-led support for representative
Open Catalyst subsets, not as verified support for every scientific-data type.
A non-atomistic comparison requires its own approved scope, documented input,
and acceptance oracle.

## Evaluation datasets

The five Open Catalyst sources belong to one atomistic-data family but exercise
different schemas, groupings, target definitions, and sequence semantics:

- **OC20** — adsorption structures and relaxation trajectories with energy and
  force labels.
- **OC22** — oxide electrocatalysts with DFT total-energy labels; these labels
  should not be combined with OC20 by simply concatenating records.
- **OC20-mAds** — up to five adsorbates on one surface, testing variable
  composition and coverage-dependent metadata.
- **OC20Dense** — grouped alternative placements for adsorbate-surface systems;
  group and mapping files must remain aligned with structures and targets.
- **OC20NEB** — ordered reaction-path calculations whose image order and
  reaction grouping are essential for transition-state analysis.

Because the public datasets are large, development uses metadata and small,
representative subsets.

## Source coverage status

The table records support claims, not an inventory of available public data.
Each support claim requires a documented source-derived representative subset;
reviewed synthetic fixtures only exercise expected or failure behaviour. Neither
requires a full dataset download.

| Source | Current status | Planned boundary |
| --- | --- | --- |
| OC20 | Implemented only for the bounded S2EF-200K profiler and reviewed synthetic fixtures. | Retain as the baseline reference for the controlled workflow and cross-source evaluation. |
| OC22 | Not supported. | Add a representative-subset adapter after source documentation confirms how total-energy labels are represented; never combine those labels directly with OC20 adsorption energies. |
| OC20-mAds | Not supported. | Add a representative-subset adapter that preserves variable adsorbate composition and coverage metadata. |
| OC20Dense | Not supported; OC20Dense-like synthetic mapping-risk fixtures are not source-adapter support. | Add a representative-subset adapter that validates structure, target, group, and mapping alignment. |
| OC20NEB | Not supported; OC20NEB-like synthetic ordering-risk fixtures are not source-adapter support. | Add a representative-subset adapter that validates authoritative reaction grouping and image order before any reaction-level summary. |

The authoritative timing and entry gates for these planned adapters are in the
[milestones](milestones.md); their source-specific acceptance oracles are in
the [evaluation plan](design/evaluation-plan.md).

## Canonical references

- [Project brief](design/project-brief.md) — proposal objectives, expected
  deliverables, supervisor guidance, and research questions.
- [Requirements](design/requirements.md) — functional, non-functional, and
  scientific-safety requirements.
- [Architecture](design/architecture.md) — staged workflow and future system
  design.
- [Technology decisions](design/technology-decisions.md) — adopted and
  deferred technologies.
- [Evaluation plan](design/evaluation-plan.md) — scenarios, oracles, and
  reporting rules.
