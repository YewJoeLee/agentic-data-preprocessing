# Project scope

## Project

**Agentic AI for Automated Data Understanding and Preprocessing**

This Final Year Project investigates an LLM-based agent that can inspect,
understand, and preprocess scientific datasets, especially catalyst datasets,
for downstream machine learning.

## Problem and intended workflow

The system should not assume that a dataset is a clean table with a known
schema. It should be able to:

1. discover files, formats, records, and existing splits;
2. infer fields, keys, labels, groups, sequences, units, and relationships;
3. diagnose data-quality and scientific-consistency issues;
4. understand the user's downstream task;
5. propose a task-aware preprocessing plan;
6. preview important or risky operations and request approval;
7. execute transformations with deterministic tools;
8. validate the result against the input and the stated task; and
9. explain decisions, evidence, uncertainty, warnings, and provenance.

Users should be able to compare before-and-after diagnostics and replay or
roll back important workflow steps.

## Core design constraint

The LLM plans, selects tools, reasons over evidence, and explains decisions.
Deterministic libraries perform inspection, transformations, and validation.

The system must not silently:

- invent values;
- change labels;
- reorder sequences or trajectories; or
- make scientifically consequential imputations.

Ambiguous or destructive actions require human confirmation. Transformations
should be reproducible through generated code, configuration, and quality
reports.

## Initial implementation scope

Start with a deterministic dataset profiler before building the agent workflow.
The first vertical slice should discover a local dataset directory, inspect a
small representative sample, and produce a structured profile.

The initial evaluation domain is the Open Catalyst family, beginning with
OC20. FLASH weather sequences are optional and should only be considered if
time and data access allow.

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

Because the public datasets are large, development should use metadata and
small representative subsets.

## Expected deliverables

- a working prototype of the agentic data-understanding and preprocessing
  system;
- discovery, profiling, and adapter support for representative subsets of the
  Open Catalyst families;
- previews, approval controls, and rollback for important workflow steps;
- evaluation of correctness, leakage prevention, reproducibility,
  cross-type generalisation, runtime, and explanation quality; and
- source code, documentation, and the final project report.

## Suggested implementation technologies

The original project specification mentions LangGraph, FAIR-Chem, NumPy,
pandas, pymatgen, FastAPI, and React with TypeScript. These are implementation
options, not requirements for the initial scaffold. Introduce them only when a
working experiment justifies the dependency.
