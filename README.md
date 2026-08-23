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
