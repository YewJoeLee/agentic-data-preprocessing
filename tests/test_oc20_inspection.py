"""Focused tests for read-only OC20 compressed-shard inspection."""

from __future__ import annotations

import json
import lzma
from pathlib import Path

import pytest

from agentic_preprocessing.oc20_inspection import inspect_oc20_shard_pair


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_inspect_oc20_shard_pair_streams_sample_and_validates_counts(
    tmp_path: Path,
) -> None:
    structure_path = tmp_path / "0.extxyz.xz"
    sidecar_path = tmp_path / "0.txt.xz"
    write_xz(
        structure_path,
        "2\n"
        "Properties=species:S:1:pos:R:3 energy=-1.0\n"
        "H 0.0 0.0 0.0\n"
        "O 0.0 0.0 1.0\n"
        "1\n"
        "Properties=species:S:1:pos:R:3 energy=-2.0\n"
        "He 1.0 0.0 0.0\n",
    )
    write_xz(sidecar_path, "random1,frame0,-1.0\nrandom2,frame1,-2.0\n")

    result = inspect_oc20_shard_pair(structure_path, sidecar_path, sample_index=1)

    assert result.structure_record_count == 2
    assert result.sidecar_row_count == 2
    assert result.row_counts_match is True
    assert result.structure_sample is not None
    assert result.structure_sample.atom_count == 1
    assert result.structure_sample.property_names == ("species", "pos")
    assert result.sidecar_sample is not None
    assert result.sidecar_sample.fields == ("random2", "frame1", "-2.0")
    assert result.issues == ()
    json.dumps(result.to_dict())


def test_inspect_oc20_shard_pair_reports_row_count_mismatch(tmp_path: Path) -> None:
    structure_path = tmp_path / "1.extxyz.xz"
    sidecar_path = tmp_path / "1.txt.xz"
    write_xz(structure_path, "0\nProperties=species:S:1\n0\nProperties=species:S:1\n")
    write_xz(sidecar_path, "random1,frame0,-1.0\n")

    result = inspect_oc20_shard_pair(structure_path, sidecar_path)

    assert result.structure_scan_complete is True
    assert result.sidecar_scan_complete is True
    assert result.structure_record_count == 2
    assert result.sidecar_row_count == 1
    assert result.row_counts_match is False
    assert [issue.code for issue in result.issues] == ["row_count_mismatch"]


def test_inspect_oc20_shard_pair_reports_invalid_sidecar_fields(tmp_path: Path) -> None:
    structure_path = tmp_path / "invalid-sidecar.extxyz.xz"
    sidecar_path = tmp_path / "invalid-sidecar.txt.xz"
    write_xz(structure_path, "0\nProperties=species:S:1\n")
    write_xz(sidecar_path, "random1,frame0\n")

    result = inspect_oc20_shard_pair(structure_path, sidecar_path)

    assert result.row_counts_match is True
    assert [issue.code for issue in result.issues] == ["invalid_sidecar_field_count"]


def test_inspect_oc20_shard_pair_reports_atom_row_property_count_mismatch(
    tmp_path: Path,
) -> None:
    structure_path = tmp_path / "invalid-atoms.extxyz.xz"
    sidecar_path = tmp_path / "invalid-atoms.txt.xz"
    write_xz(
        structure_path,
        "1\nProperties=species:S:1:pos:R:3\nH 0.0 0.0\n",
    )
    write_xz(sidecar_path, "random1,frame0,-1.0\n")

    result = inspect_oc20_shard_pair(structure_path, sidecar_path)

    assert result.structure_scan_complete is True
    assert result.row_counts_match is True
    assert [issue.code for issue in result.issues] == [
        "atom_row_property_count_mismatch"
    ]


def test_inspect_oc20_shard_pair_reports_truncated_structure(tmp_path: Path) -> None:
    structure_path = tmp_path / "2.extxyz.xz"
    sidecar_path = tmp_path / "2.txt.xz"
    write_xz(
        structure_path,
        "2\nProperties=species:S:1:pos:R:3\nH 0.0 0.0 0.0\n",
    )
    write_xz(sidecar_path, "random1,frame0,-1.0\n")

    result = inspect_oc20_shard_pair(structure_path, sidecar_path)

    assert result.structure_scan_complete is False
    assert result.structure_record_count == 0
    assert result.row_counts_match is None
    assert [issue.code for issue in result.issues] == ["truncated_structure_record"]


def test_inspect_oc20_shard_pair_rejects_negative_sample_index(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        inspect_oc20_shard_pair(
            tmp_path / "0.extxyz.xz", tmp_path / "0.txt.xz", sample_index=-1
        )
