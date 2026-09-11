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

The reference development environment uses Python 3.12.13. The package
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
unless `--allow-pickle-load` is explicitly supplied. Do not redirect its JSON
output into the repository; use a temporary location for repeatability checks.

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
