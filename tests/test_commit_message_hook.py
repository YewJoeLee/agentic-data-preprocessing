from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).parents[1] / ".githooks" / "commit-msg"
PRE_COMMIT_HOOK = Path(__file__).parents[1] / ".githooks" / "pre-commit"


def run_hook(tmp_path: Path, subject: str) -> subprocess.CompletedProcess[str]:
    message_file = tmp_path / "commit-message"
    message_file.write_text(f"{subject}\n\nBody text.\n", encoding="utf-8")
    return subprocess.run(
        [str(HOOK), str(message_file)],
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "subject",
    [
        "feat(oc20): add deterministic profiler baseline",
        "fix: reject ambiguous numeric shard pairs",
        "docs(eda): describe the six-step workflow",
        "setup(repo): add initial repository files",
    ],
)
def test_commit_message_hook_accepts_project_convention(
    tmp_path: Path, subject: str
) -> None:
    assert HOOK.is_file(), "The versioned commit-msg hook must exist."
    assert run_hook(tmp_path, subject).returncode == 0


@pytest.mark.parametrize(
    "subject",
    [
        "add deterministic profiler baseline",
        "chore: update dependencies",
        "feat oc20: add profiler",
        "feat(OC20): add profiler",
    ],
)
def test_commit_message_hook_rejects_invalid_subjects(
    tmp_path: Path, subject: str
) -> None:
    assert HOOK.is_file(), "The versioned commit-msg hook must exist."
    assert run_hook(tmp_path, subject).returncode != 0


def test_pre_commit_hook_runs_ruff_checks() -> None:
    assert PRE_COMMIT_HOOK.is_file(), "The versioned pre-commit hook must exist."

    completed = subprocess.run(
        [str(PRE_COMMIT_HOOK)],
        check=False,
        capture_output=True,
        text=True,
        cwd=PRE_COMMIT_HOOK.parents[1],
    )

    assert completed.returncode == 0, completed.stderr
