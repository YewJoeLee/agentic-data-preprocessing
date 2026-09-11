# Master notes

This is the entry point for the project's living design and evidence records.
Use the linked documents as the canonical home for new content rather than
recreating the same material here.

## Project contract

The project investigates an agentic system for automated scientific-data
understanding and preprocessing. The LLM plans, selects tools, reasons over
collected evidence, and explains decisions; deterministic tools inspect,
transform, and validate data.

The system must not silently invent values, change labels, reorder sequences or
trajectories, or make scientifically consequential imputations. Ambiguous or
destructive actions require human confirmation.

## Living document map

| Document | Primary scope | Update when |
| --- | --- | --- |
| [Project brief](design/project-brief.md) | Goal, objectives, deliverables, learning outcomes, research questions, and contribution framing. | Scope or project commitments change. |
| [Requirements](design/requirements.md) | Background, functional/non-functional requirements, safety constraints, and baseline non-goals. | A requirement is accepted, deferred, or clarified. |
| [Architecture](design/architecture.md) | Staged workflow, proposed roles, shared state, tool registry, approvals, provenance, and future architecture options. | A design decision or interface changes. |
| [EDA workflow guideline](design/eda-workflow.md) | Six iterative EDA practices, their scientific-safety boundaries, and current milestone position. | An EDA practice, safety boundary, or project-stage assessment changes. |
| [OC20 data understanding](design/oc20-data-understanding.md) | Observed OC20 200K structure, mappings, viewing workflow, profiler evidence contract, and limitations. | A dataset inspection finding or supported OC20 input changes. |
| [Technology decisions](design/technology-decisions.md) | Adopted technologies, conditional integrations, and decision records. | A dependency is introduced, deferred, or rejected. |
| [Literature review](design/literature-review.md) | Reading summary, research gap, and claim-verification notes. | A source is read or cited. |
| [Evaluation plan](design/evaluation-plan.md) | Evaluation questions, datasets, scenarios, measures, rubric, and reporting rules. | An experiment is planned or revised. |
| [Development log](development-log.md) | Weekly work, experiments, decisions, evidence, failures, and next actions. | At least once per active development week. |
| [Oral presentation preparation](oral-presentation.md) | Presentation narrative, Q&A bank, demo checklist, and rehearsal log. | After every rehearsal or useful question. |
| [FYP milestones](milestones.md) | Authoritative academic schedule and detailed delivery plan. | The supervisor or programme office confirms a date/scope change. |

## Design maturity and scope guardrails

1. **Baseline:** deterministic local dataset profiler for a small OC20 subset
   or reviewed synthetic atomistic fixtures.
2. **Controlled workflow:** evidence-grounded plan, preview, approval,
   deterministic execution, validation, and provenance for a small allow-list
   of operations.
3. **Evaluation:** correctness, leakage prevention, reproducibility, runtime,
   cross-type generalisation, and explanation quality.
4. **Final workflow target:** LangGraph-based multi-agent orchestration with a
   sequential backbone and safe, read-only parallel branches. It is introduced
   only after the profiler baseline; FAIR-Chem adapters expand as supported
   fixtures demonstrate need. A UI or database remains conditional.

This target does not authorise building the workflow before the profiler
baseline is tested.

## Update order

1. Record work and evidence in the development log.
2. Update the relevant focused design document when the finding changes a
   requirement, decision, architecture, evaluation scenario, or literature
   claim.
3. Update milestones only for confirmed schedule or delivery-plan changes.
4. Update the oral-preparation note after a rehearsal, supervisor discussion,
   or examiner-style question.
