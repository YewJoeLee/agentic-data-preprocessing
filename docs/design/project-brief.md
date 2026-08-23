# Project brief

## Project goal

Develop and evaluate a prototype that helps users understand and safely preprocess heterogeneous scientific datasets for downstream machine learning. The initial domain is the Open Catalyst dataset family, beginning with a small representative OC20 subset.

The system should discover files and records, infer useful structure and semantics, identify risks, propose task-aware deterministic operations, and explain what it found and why a proposed action is safe or uncertain.

## Main objectives

1. Study general and type-specific preprocessing methods, data-quality principles, leakage risks, dataset documentation, and human-in-the-loop agent design.
2. Develop an agent that discovers dataset files, schemas, metadata, units, record relationships, and downstream-task requirements; it should generate a task-aware preprocessing plan and select appropriate deterministic tools or code operations.
3. Provide human-readable explanations, evidence, uncertainty, warnings, approval points, and rollback for important preprocessing decisions.
4. Generate reproducible preprocessing code, configuration files, and quality reports.
5. Evaluate the agent across dataset families, preprocessing tasks, data-quality problems, and user goals.

## Expected deliverables

1. A working prototype of the agentic data-understanding and preprocessing system.
2. Dataset discovery, profiling, and adapter support for representative subsets of the five Open Catalyst dataset families.
3. A workflow with previews, approval controls, and rollback for important steps.
4. An evaluation of correctness, leakage prevention, reproducibility, cross-type generalisation, runtime, and explanation quality.
5. Source code, documentation, and a final project report.

## Expected learning outcomes

1. Agentic AI workflow design, planning, tool use, validation, and human-in-the-loop interaction.
2. Data modelling for tabular, time-series, and atomistic scientific records.
3. LLM-based code generation and safe execution.

## Supervisor guidance and operating context

- **Required implementation direction:** Python is required throughout. The
  agent-workflow stage will use LangGraph for state management, approval
  checkpoints, retries, and validation. Its introduction remains gated on a
  working deterministic-profiler baseline.
- **Final architecture target:** a multi-agent system combining sequential and
  parallel orchestration. The initial profiler may remain a single-process
  implementation; multi-agent decomposition is introduced incrementally and
  evaluated rather than assumed to be beneficial.
- **Domain tooling:** FAIR-Chem is an important integration for reading and
  interpreting Open Catalyst records and dataset-specific metadata.
- **Deployment:** develop locally by default. Use NSCC only when a documented
  experiment needs larger datasets or additional compute resources.
- **LLM access:** team-provided API access is available. Keys must be managed
  outside the repository; use must remain cost-conscious and reproducible.
- **Priority order:** accuracy, reliability, scalability, cost, speed, then
  security. This order governs design trade-offs and evaluation interpretation.
- **Interface/storage:** FastAPI with React/TypeScript is the modular UI option;
  Streamlit or Gradio is the simpler prototype option. PostgreSQL and DuckDB
  are optional and require a demonstrated persistence/querying need.

## Research contribution framing

The contribution is not an autonomous data cleaner or a claim of universal scientific-data support. It is an evidence-led workflow that connects heterogeneous scientific data to reproducible preprocessing decisions while preserving human control over consequential assumptions.

## Candidate research questions

| ID | Question | Indicative evidence |
| --- | --- | --- |
| RQ1 | How accurately can deterministic inspection characterise representative Open Catalyst subsets? | Golden fixtures, manual spot checks, and categorised errors. |
| RQ2 | Can LLM-guided planning remain grounded in deterministic evidence while proposing task-aware preprocessing? | Plans that cite observations, declare uncertainty, and map to explicit tools. |
| RQ3 | Do previews, approval points, and validation reduce unsafe or irreproducible outcomes? | Scenarios where risky actions are warned about, blocked, or require approval. |
| RQ4 | How useful are explanations for understanding data and defending preprocessing choices? | A rubric for evidence traceability, clarity, uncertainty, and actionability. |
