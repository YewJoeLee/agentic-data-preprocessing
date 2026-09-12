# Agentic AI for Automated Data Understanding and Preprocessing

Final Year Project, AY2026/27.

## Goal

Investigate whether an LLM-based agent can understand scientific datasets and
generate safe, task-aware, reproducible preprocessing workflows using
deterministic tools.

## Current scope

The initial prototype focuses on the Open Catalyst dataset family, beginning
with a small OC20 subset. The first implementation milestone is a deterministic
dataset profiler that can:

- discover files and identify formats;
- inspect records and infer schemas;
- surface metadata, units, and relationships; and
- produce a structured dataset profile.

LLM-based reasoning and workflow generation will be added after this profiling
baseline is working.

## Repository layout

```text
src/agentic_preprocessing/  Python package
tests/                      Automated tests
docs/                       Project and research notes
data/                       Local data instructions and placeholders
```

The datasets themselves are not stored in Git. See [`data/README.md`](data/README.md)
for local-data guidance.

## Development

The reference development environment uses Python 3.12.14. The package
supports Python 3.11 and newer, but new environment differences should be
recorded before experiments are compared.

Install the project and its development dependencies with `uv`:

```bash
uv sync
```

Run the test suite with:

```bash
uv run pytest
```

### OC20 profiler acceptance evaluation

Run a bounded, read-only acceptance report for the local OC20 subset with:

```bash
uv run python -m agentic_preprocessing.oc20_acceptance \
  --dataset-root data/raw \
  --shard-stem 0 \
  --sample-index 0 \
  --consistency-indices 0 1 2 \
  --format summary
```

The command writes only to standard output and does not load mapping pickles
unless `--allow-pickle-load` is explicitly supplied. It performs one full
selected-pair integrity scan and one full fixed-sample consistency scan; this
is bounded to the selected shard, but is not a constant-byte read. Do not
redirect its JSON output into the repository; use a temporary location for
repeatability checks.

### Output formats

`--format summary` is the default human-readable report. It contains aggregate
evidence only:

| Summary line | Meaning |
| --- | --- |
| `Valid shard pairs` | Number of numeric stems with exactly one structure and one sidecar shard. |
| `Selected numeric stem` | The valid shard selected for bounded inspection. |
| `Mapping pickle loading` | Whether pickle loading was disabled or explicitly authorised. |
| `Unit evidence` | Field-unit status. `unresolved` means no authoritative field-specific convention is recorded. |
| `Issue codes` | Aggregate warnings from profile and consistency checks. `pickle_load_not_authorized` is expected policy evidence when pickle loading is disabled. |
| `Fixed consistency samples` | Structure and sidecar samples found out of the requested fixed indices. |

Use JSON when another program, an experiment record, or a detailed review
needs the complete structured evidence:

```bash
uv run python -m agentic_preprocessing.oc20_acceptance \
  --dataset-root data/raw \
  --shard-stem 0 \
  --sample-index 0 \
  --consistency-indices 0 1 2 \
  --format json > /private/tmp/oc20-acceptance.json
```

The JSON top level contains `profile`, `sample_consistency`,
`consistency_indices`, and `pickle_loading_authorised`.

| JSON section | Meaning |
| --- | --- |
| `profile.discovery` | README/shard/pickle inventory, numeric pair status, and ignored symlinks. |
| `profile.inspection` | Record and row counts, scan completion, selected bounded samples, and parsing issues. |
| `profile.sample_schema` | Header fields, atom-property declarations, lexical types, and schema issues. |
| `profile.mapping_validation` | Mapping-key evidence and pickle-loading policy. |
| `profile.metadata_record_profile` | Trusted metadata schema, checksum, size, and anomaly evidence; normally `null` when pickle loading is disabled. |
| `profile.unit_evidence` | Per-field unit status; this remains unresolved until an authoritative source is recorded. |
| `profile.issues` | Deduplicated profile-level issues. |
| `sample_consistency` | Schema/field-count consistency and empty-field evidence across only the requested sample indices. |

JSON can include bounded raw sample fields for evidence. Do not commit it or
write it under `data/`; use a temporary location such as `/private/tmp`.

### Trusted mapping-pickle inspection

Python pickle deserialisation can execute code. Enable mapping inspection only
after independently verifying the mapping files' source and checksum:

```bash
uv run python -m agentic_preprocessing.oc20_acceptance \
  --dataset-root data/raw \
  --shard-stem 0 \
  --sample-index 0 \
  --consistency-indices 0 1 2 \
  --allow-pickle-load \
  --format summary
```

This option remains read-only. It permits mapping-key validation and bounded
metadata evidence; it does not transform source data or establish a verified
scientific unit convention.

## Commit messages

Use Conventional Commits with an optional lowercase scope:

```text
type(optional-scope): short imperative summary
```

Allowed types are `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`,
`ci`, `style`, `revert`, and `setup`. `setup` is used for repository or
project initialization work; routine maintenance should use the more specific
standard type.

Enable the versioned local hook once per clone:

```bash
git config --local core.hooksPath .githooks
```

The `commit-msg` hook validates the subject. The `pre-commit` hook runs Ruff's
formatting and lint checks without modifying files. If formatting fails, run:

```bash
uv run ruff format .
```

The hooks are local safeguards, so each clone must run the activation command
above before making commits.
