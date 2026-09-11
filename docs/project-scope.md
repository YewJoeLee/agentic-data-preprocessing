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
