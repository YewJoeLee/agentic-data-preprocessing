# Architecture and workflow design

## Design principle

Separate reasoning from data operations:

```text
User goal + local dataset
        |
Deterministic discovery and profiling
        |
Evidence bundle
        |
LLM-guided interpretation and plan
        |
Preview + risk classification + approval, when required
        |
Deterministic execution and validation
        |
Profile / quality report / provenance / explanation
```

## Staged architecture

### Stage 1: deterministic profiler (current implementation baseline)

- Dataset discovery and format inspection.
- Safe representative sampling.
- Record/schema/metadata/relationship profiling.
- Structured profile and human-readable summary.
- Tests using reviewed synthetic fixtures and small local subsets.

### Stage 2: controlled agent workflow

- Implement the workflow as a LangGraph state machine after the profiler gate.
- Interpret a user goal using profiler evidence.
- Produce a typed preprocessing plan with assumptions, risks, proposed tools, expected impact, and validation steps.
- Preview the plan and require approval where policy demands it.
- Execute only allow-listed deterministic operations.
- Store provenance and validate the result.

### Stage 3: final multi-agent orchestration target

The intended final implementation is a multi-agent system with a sequential
control flow and limited parallel branches. LangGraph provides the shared-state,
checkpoint, retry, and routing mechanism. A UI and database-backed state remain
conditional extensions.

#### Sequential backbone

```text
discover -> profile -> interpret goal -> plan -> policy/approval
         -> execute approved operations -> validate -> explain/report
```

#### Parallel branches

Parallelism is permitted only for independent work that has no side effects,
such as format-specific inspection, separate metadata/relationship checks,
candidate plan analysis, or independent validation checks. A coordinator merges
their evidence into shared state before the next sequential decision.

Transformations must not run in parallel unless they are proven independent,
operate on isolated derived outputs, and the plan explicitly permits it.

## Proposed roles

The baseline may implement these as ordinary modules. In the final target,
separate LangGraph nodes/agents implement the roles under a shared-state and
coordination contract.

| Role | Responsibility | Must not do |
| --- | --- | --- |
| Discovery/profiler | Collect deterministic facts about files, records, schema, metadata, and relationships. | Infer unsupported scientific meaning without evidence. |
| Planner | Turn a user goal and evidence into a plan, assumptions, risks, and validation checks. | Perform transformations or present guesses as facts. |
| Policy/approval layer | Classify risk and determine when confirmation is required. | Approve its own risky actions silently. |
| Executor | Run explicit deterministic operations. | Invent values or mutate raw source data. |
| Validator | Compare output with input, task, and constraints. | Declare success without checks. |
| Explainer | Present evidence, decisions, uncertainty, warnings, and provenance. | Hide limitations or overstate confidence. |
| Coordinator | Route sequential stages, launch allowed read-only parallel branches, merge their evidence, and apply retry policy. | Bypass approval, merge contradictory evidence silently, or run unsafe concurrent mutations. |

## Shared state design

Use a typed, serialisable workflow state. Keep raw scientific records outside the state where possible; state should contain references and summaries.

```text
WorkflowState
  run_id, created_at, source_refs, user_goal
  discovery: files, formats, sampling_policy
  profile: schema, metadata, units, relationships, warnings, evidence_refs
  plan: proposed_operations, assumptions, risks, expected_impact
  approvals: requested, granted/declined, rationale
  execution: operations_run, generated_config, output_refs
  validation: checks, results, before_after_summary
  provenance: code_version, tool_versions, timestamps
  explanation: user-facing summary and limitations
```

### State invariants

- Each claim in `profile` or `plan` has an evidence reference or an explicit uncertainty label.
- `execution` cannot begin for an operation that requires approval until that approval is recorded.
- Output references never overwrite raw inputs.
- Validation results are recorded before a run is described as complete.
- Replaying a run uses the stored configuration and the same declared sample policy.

## Tool registry

Tools should be explicit, deterministic, versioned, and narrow in purpose.

| Tool family | Example operations | Inputs/outputs |
| --- | --- | --- |
| Discovery | List files, identify formats, select safe samples. | Dataset reference -> file inventory/sample manifest. |
| Inspection | Parse supported records, calculate shapes/types/missingness. | Sample -> structured observations. |
| Domain adapters | Extract atomistic metadata, units, trajectory/group semantics. | Supported record -> domain evidence/warnings. |
| Transformation | Select fields, cast types, join validated mappings, encode/scale when unambiguous. | Approved plan + input -> derived output/configuration. |
| Validation | Check split/group isolation, alignment, label/shape preservation, report diffs. | Input + output + task -> validation report. |

## Approval and rollback policy

Require approval when an action may delete/overwrite values, change labels or units, alter trajectory order, break group alignment, select an ambiguous join, or otherwise make a scientifically consequential assumption.

Prefer non-destructive derived outputs. Rollback is implemented by preserving the source, retaining run provenance, and allowing a prior configuration/output to be selected or regenerated.

## Future design decisions

| Option | Trigger to consider it | Evidence required before adoption |
| --- | --- | --- |
| LangGraph/workflow orchestration | Required post-profiler agent-workflow implementation. | Profiler gate is met; graph has explicit state/checkpoint/retry/validation tests. |
| Multiple specialised agents | Final intended architecture; introduce incrementally when a role contract is stable. | A defined protocol, shared-state contract, safe merge rules, and evaluation benefit. |
| FAIR-Chem integration | Needed to inspect/validate an OC format that simpler tools cannot support safely. | Adapter contract, small fixture, and reproducible integration test. |
| Database | File-based provenance becomes insufficient for required queries or concurrent runs. | Concrete access pattern and migration/data-retention plan. |
| UI | Evidence shows a CLI/report is inadequate for the approval or explanation workflow. | User need, wireframe, and scoped acceptance criteria. |
