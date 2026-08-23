# Agent instructions

## Project

This repository contains a Final Year Project research prototype for **agentic
AI for automated scientific data understanding and preprocessing**.

The current focus is the Open Catalyst dataset family, starting with a small
OC20 subset. The immediate implementation milestone is a deterministic dataset
profiler. It should discover files, identify formats, inspect records, infer
schemas, surface metadata and units, identify relationships, and produce a
structured profile.

Do not begin by building a multi-agent framework. Add abstractions only when a
working experiment demonstrates that they are needed.

## Repository map

- `src/agentic_preprocessing/` — installable Python package
- `tests/` — automated tests
- `data/` — local-data instructions and ignored dataset directories
- `docs/` — project notes, literature notes, and design decisions

## Working rules

1. Keep research code reproducible and prefer small, testable vertical slices.
2. Keep LLM reasoning separate from deterministic inspection and transformation
   code. Scientific transformations must be implemented by explicit tools or
   libraries, not hidden in prompts.
3. Treat `data/raw/` as immutable. Never commit OC20, other datasets,
   credentials, `.env` files, model outputs, or large generated artifacts.
4. Do not silently invent, overwrite, or impute scientific values. Preserve
   source data and make consequential assumptions explicit.
5. Ask for approval before downloading full datasets or incurring model/API
   costs. Prefer small, documented subsets for local experiments.
6. Reviewed synthetic fixtures and small golden test outputs may be committed
   under `tests/` when they are necessary for reproducible evaluation.
7. Do not add LangGraph, orchestration frameworks, or a UI until the profiling
   baseline and its evaluation needs justify them.
8. Preserve existing user work. Inspect relevant files before editing and keep
   unrelated changes untouched.

## Development commands

The reference environment uses Python 3.12.13. Use `uv` to create and sync the
project environment from the lockfile:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

The package uses a `src/` layout. New functionality should normally have a
corresponding test under `tests/`.

## Definition of done

Before considering a change complete:

- run the relevant tests, or explain why they could not be run;
- check that no dataset, secret, or generated artifact was added;
- update documentation when behavior or project decisions change; and
- report important assumptions and any remaining limitations.
