"""Tests for the read-only OC20 profiler acceptance evidence."""

from __future__ import annotations

import json
import lzma
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_preprocessing.oc20_acceptance import (
    evaluate_oc20_acceptance,
    format_oc20_acceptance_summary,
    main,
)


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_acceptance_evaluation_composes_profile_and_consistency(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,0,-1.0\n")

    result = evaluate_oc20_acceptance(
        tmp_path,
        shard_stem=0,
        sample_index=0,
        consistency_indices=(0,),
    )

    assert result.profile.selected_numeric_stem == 0
    assert result.sample_consistency is not None
    assert result.sample_consistency.sample_indices == (0,)
    assert result.pickle_loading_authorised is False
    json.dumps(result.to_dict())


def test_summary_reports_evidence_without_raw_values_or_invented_units(
    tmp_path: Path,
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,0,-1.0\n")

    summary = format_oc20_acceptance_summary(
        evaluate_oc20_acceptance(tmp_path, consistency_indices=(0,))
    )

    assert "Valid shard pairs: 1" in summary
    assert "Unit evidence: unresolved" in summary
    assert "system-1" not in summary
    assert "-1.0" not in summary


def test_summary_includes_selected_pair_integrity_issues(tmp_path: Path) -> None:
    write_xz(
        tmp_path / "0.extxyz.xz",
        "0\nProperties=species:S:1\n0\nProperties=species:S:1\n",
    )
    write_xz(tmp_path / "0.txt.xz", "system-1,0,-1.0\n")

    summary = format_oc20_acceptance_summary(
        evaluate_oc20_acceptance(tmp_path, consistency_indices=(0,))
    )

    assert "row_count_mismatch" in summary


def test_acceptance_preserves_no_valid_pair_evidence(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")

    result = evaluate_oc20_acceptance(tmp_path, shard_stem=None)

    assert result.sample_consistency is None
    assert [issue.code for issue in result.profile.issues] == ["no_valid_shard_pair"]


def test_acceptance_rejects_invalid_consistency_indices_without_a_valid_pair(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="unique, non-negative, and non-empty"):
        evaluate_oc20_acceptance(tmp_path, consistency_indices=(0, -1))


def test_cli_emits_json_to_standard_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,0,-1.0\n")

    exit_code = main(
        [
            "--dataset-root",
            str(tmp_path),
            "--consistency-indices",
            "0",
            "--format",
            "json",
        ]
    )

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out)["profile"]["selected_numeric_stem"] == 0


def test_cli_emits_deterministic_summary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,0,-1.0\n")

    exit_code = main(["--dataset-root", str(tmp_path), "--consistency-indices", "0"])

    assert exit_code == 0
    assert "Mapping pickle loading: disabled" in capsys.readouterr().out


def test_cli_rejects_missing_dataset_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as error:
        main(["--dataset-root", str(tmp_path / "missing")])

    assert error.value.code == 2
    assert "not a directory" in capsys.readouterr().err


def test_module_help_has_no_runpy_warning() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "agentic_preprocessing.oc20_acceptance", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "RuntimeWarning" not in completed.stderr
