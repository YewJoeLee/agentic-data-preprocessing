# Literature review and research gap

## Purpose

This document records the project's interpretation of relevant work: the
research gap, transferable design lessons, limitations, and report-ready
claims. The complete paper, code, dataset, and tooling links are maintained in
the [project reference registry](../references.md).

## Reading analysis map

| Source | Design/evaluation lesson | Questions to answer while reading |
| --- | --- | --- |
| [AutoDCWorkflow](../references.md#autodcworkflow) | Purpose-driven cleaning plans and answer/data/workflow evaluation can inform task-aware planning scenarios. | How are purpose, workflow correctness, and data quality operationalised? Which parts transfer beyond tables? |
| [Data Interpreter](../references.md#data-interpreter) | Planning, execution, observation, refinement, and validation are distinct workflow stages. | What graph/state pattern is used? How are code failures and validation results handled? |
| [Jellyfish](../references.md#jellyfish) | General preprocessing capabilities include error detection, imputation, schema matching, and entity matching. | Which tasks are relevant to scientific data, and which would be unsafe without domain-specific evidence? |
| [CleanAgent](../references.md#cleanagent) | Controlled tools are safer and more auditable than unrestricted code generation. | What tool constraints and approval/validation patterns are reusable? |
| [DataFlow-Harness](../references.md#dataflow-harness) | Explicit, editable pipelines support traceability and review. | How are pipeline steps represented, inspected, and revised? |
| [ASE and FAIR-Chem](../references.md#dataset-and-tooling-references) | Atomistic data needs explicit structure, trajectory, label, unit, and dataset-semantics handling. | Which APIs and data conventions are necessary for the first OC20 adapter? |

## Research gap to investigate

General-purpose data-preprocessing agents and data-cleaning systems do not by
themselves establish safe handling of scientific semantics such as units,
atomistic structure metadata, group alignment, ordered reaction-path images, or
label conventions. This project tests a narrower hypothesis: an evidence-led
LLM planning layer plus deterministic profiling and validation can make those
constraints visible and support more reproducible preprocessing decisions.

## Reading note template

```text
Citation key:
Reference-registry entry:
Date read:
Research problem:
Method / system:
Dataset and evaluation:
Useful finding:
Limitation or threat to validity:
Direct relevance to this FYP:
Report section / claim supported:
Quotation or precise page/section reference (if needed):
Follow-up question:
```

## Citation hygiene

- Add or update links and bibliographic metadata only in
  [references.md](../references.md).
- Prefer primary papers and official dataset/tool documentation for technical
  claims.
- Keep URLs, access dates, page numbers, and exact quotations in the reference
  manager or reading notes.
- Distinguish a paper's demonstrated result from a design inspiration.
- Link each literature claim in the final report to a source you have read.
