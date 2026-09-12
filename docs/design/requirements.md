# Requirements and scope

## Background and motivation

Scientific datasets may contain nested records, atomistic structures, trajectory order, mapping files, domain-specific labels, and heterogeneous split semantics. Treating them as ordinary clean tables risks incorrect joins, label misuse, leakage, and scientifically invalid transformations.

The system must make the structure, constraints, and uncertainty of a dataset visible before it changes anything consequential.

## Functional requirements

| ID | Requirement | Initial acceptance evidence |
| --- | --- | --- |
| FR-1 | Discover local files/directories and identify supported formats. | Tests for supported, unsupported, empty, and unreadable inputs. |
| FR-2 | Safely inspect representative records and infer fields, types, shapes, missingness, candidate identifiers, labels, and splits. | Stable structured profiles and golden fixture outputs. |
| FR-3 | Surface metadata, units, groups, mappings, sequence/trajectory semantics, and relationships where supported. | Explicit profile evidence and warnings for ambiguity. |
| FR-4 | Diagnose quality, alignment, ordering, and leakage risks. | Adversarial fixture/scenario tests. |
| FR-5 | Accept an optional downstream task goal and produce an evidence-grounded preprocessing plan. | Plan examples that cite profiler observations. |
| FR-6 | Preview risky operations and request approval for ambiguous, destructive, or scientifically consequential actions. | Preview and approval scenarios. |
| FR-7 | Execute a small allow-listed set of operations through deterministic tools. | Tool-level tests and reproducible configuration/code. |
| FR-8 | Validate output against input and stated task; produce quality/provenance reports. | Before/after diagnostics and validation reports. |
| FR-9 | Support replay or rollback for important workflow steps. | Non-destructive output policy and replay/rollback example. |
| FR-10 | Implement the post-profiler agent workflow in LangGraph, including explicit state, checkpoints, retries, and validation transitions. | A tested graph run from profile to validated report. |
| FR-11 | Support a final multi-agent orchestration design with explicit sequential and parallel execution rules. | Role contracts, merge rules, and scenarios that verify safe coordination. |
| FR-12 | Support documented representative subsets of OC20, OC22, OC20-mAds, OC20Dense, and OC20NEB through source-specific adapter contracts. | For each source: a reviewed source-derived subset, declared supported input, preserved semantic invariant, and reproducible acceptance result; synthetic fixtures complement but do not establish source support. |

## Non-functional requirements

| Area | Requirement |
| --- | --- |
| Reproducibility | Record inputs, sample policy, configuration, tool versions, operations, and validation results. |
| Scientific safety | Never silently invent values, change labels, reorder trajectories/sequences, or impute consequential values. |
| Transparency | Connect every finding and recommendation to observed evidence; distinguish fact, inference, and uncertainty. |
| Human control | Require confirmation for ambiguous, destructive, or consequential changes. |
| Testability | Keep inspection and transformation logic small, deterministic, and covered by fixtures/golden outputs. |
| Data stewardship | Treat `data/raw/` as immutable; do not commit datasets, secrets, or large generated artefacts. |
| Feasibility | Begin with documented metadata and small representative subsets; seek approval before large downloads or model/API costs. |

## Priority order

When requirements conflict, optimise in this supervisor-specified order:

1. Accuracy
2. Reliability
3. Scalability
4. Cost
5. Speed
6. Security

For example, a slower deterministic validation step is preferred over a faster
workflow that cannot establish a scientifically correct result. Security remains
mandatory; its lower ordering means it does not displace accuracy/reliability as
the differentiating research objective.

## Dataset-specific constraints

| Dataset | Important semantics to preserve |
| --- | --- |
| OC20 | Adsorption structures and relaxation trajectories; energy/force labels; split semantics. |
| OC22 | DFT total-energy labels are not directly equivalent to OC20 adsorption-energy conventions. |
| OC20-mAds | Variable adsorbate composition and coverage-dependent metadata. |
| OC20Dense | Group/mapping files must stay aligned with structures and targets. |
| OC20NEB | Reaction grouping and ordered images are essential to transition-state analysis. |

## Explicit non-goals for the baseline

- A complete multi-agent implementation before the deterministic-profiler
  baseline is demonstrated.
- A user interface, database, or web service before the workflow demonstrates
  a concrete need.
- Support for all dataset formats or all preprocessing operations.
- Full Open Catalyst downloads as a prerequisite for progress.
- Hidden LLM-based transformations or unverified scientific inference.
