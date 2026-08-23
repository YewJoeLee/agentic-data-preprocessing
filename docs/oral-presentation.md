# Oral presentation preparation

Use this document to turn the report's evidence into a concise, defensible oral presentation. The project schedule is in [milestones.md](milestones.md), and the evidence source is [the development log](development-log.md).

## Core message

Scientific datasets cannot safely be treated as generic clean tables. This project develops an evidence-led workflow in which deterministic tools inspect, transform, and validate data, while an LLM plans, selects tools, reasons over evidence, and explains decisions. Human approval protects ambiguous or scientifically consequential changes.

## Suggested 10-12 minute narrative

| Time | Beat | Purpose |
| --- | --- | --- |
| 0:00-0:45 | Problem and stakes | Explain why scientific data may include units, structures, groupings, mappings, sequences, and label conventions that must be understood before preprocessing. |
| 0:45-1:45 | Aim and contribution | State the evidence-led human-in-the-loop contribution and deterministic/LLM separation. |
| 1:45-3:00 | Dataset challenge | Use OC20 plus one contrasting example such as OC20NEB ordering or OC20Dense group alignment. |
| 3:00-4:30 | Architecture | Walk through discover -> profile -> plan -> preview/approve -> execute -> validate -> explain. |
| 4:30-6:30 | Demonstration | Show a stable small subset, profile evidence, a warning/assumption, and the structured output. |
| 6:30-8:30 | Evaluation | Present scenarios, tests, metrics, and one honest limitation. |
| 8:30-9:45 | Findings | Connect results to research questions and scope decisions. |
| 9:45-10:30 | Limits/future work | State boundaries and evidence-driven next steps without overclaiming. |
| 10:30-12:00 | Backup/Q&A | Keep architecture, results, examples, and literature comparison ready. |

## Likely examiner questions

| Question | Answer prompt |
| --- | --- |
| Why use an LLM? | It interprets user goals, selects exposed deterministic tools, and turns evidence into a comprehensible plan. It is not trusted to perform hidden scientific transformations. |
| What is agentic if tools are deterministic? | Agency is evidence-grounded planning, tool selection, iteration, and explanation; determinism remains for operations needing reproducibility and auditability. |
| How do you prevent hallucination? | Do not ask the model to invent data facts. Ground claims in profiler evidence, represent uncertainty, validate outputs, and require approval for consequential decisions. |
| Why OC20 first? | It supplies atomistic structures, energy/force labels, trajectories, and split semantics while small subsets keep the experiment feasible and reproducible. |
| How is this evaluated beyond a demo? | Reviewed fixtures, scenario tests, correctness/leakage checks, repeatability, timings, and an explanation-quality rubric. |
| What are the limits? | The prototype supports a bounded set of formats and operations, uses representative subsets, and does not establish broad production or scientific-generalisation claims. |
| Why defer UI/orchestration? | The core research risk is whether deterministic profiling and evidence-led safety controls work. Extra framework complexity does not prove that baseline. |

## Demo checklist

- Use a small local input that can be reset quickly; do not rely on a live network download.
- Show one profile fact, one domain-relevant relationship/warning, and one safety or approval decision.
- Keep screenshots or a recorded fallback for the complete workflow.
- Be ready to show where source code, tests, configuration, and results live.
- Time a full rehearsal and record questions or weak transitions below.

## Rehearsal log

| Date | Duration | Feedback / questions | Change before next rehearsal |
| --- | ---: | --- | --- |
| `[YYYY-MM-DD]` | `[minutes]` | `[fill in]` | `[fill in]` |
