"""Focused tests for multi-record OC20 sample consistency evidence."""

from __future__ import annotations

import json
import lzma
from pathlib import Path

import agentic_preprocessing.oc20_inspection as oc20_inspection
from agentic_preprocessing.oc20_consistency import profile_oc20_sample_consistency


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_profile_oc20_sample_consistency_reports_schema_and_empty_fields_in_one_scan(
    tmp_path: Path, monkeypatch
) -> None:
    structure = tmp_path / "0.extxyz.xz"
    sidecar = tmp_path / "0.txt.xz"
    write_xz(
        structure,
        "0\nProperties=species:S:1:pos:R:3 energy=-1\n"
        "0\nProperties=species:S:1:pos:R:3 energy=-2\n"
        "0\nProperties=species:S:1:pos:R:3 energy=-3\n",
    )
    write_xz(sidecar, "random1,frame1,-1\nrandom2,frame2,\nrandom3,frame3,-3\n")

    original_lzma_open = lzma.open
    opened_paths: list[str] = []

    def count_lzma_open(path, *args, **kwargs):
        opened_paths.append(Path(path).name)
        return original_lzma_open(path, *args, **kwargs)

    monkeypatch.setattr(oc20_inspection.lzma, "open", count_lzma_open)

    result = profile_oc20_sample_consistency(structure, sidecar, (0, 1, 2))

    assert result.structure_samples_found == 3
    assert result.sidecar_samples_found == 3
    assert result.atom_property_schema_consistent is True
    assert result.header_field_names_consistent is True
    assert result.sidecar_field_count_consistent is True
    assert result.sidecar_empty_field_counts == (0, 0, 1)
    assert result.issues == ()
    assert opened_paths == ["0.extxyz.xz", "0.txt.xz"]
    json.dumps(result.to_dict())


def test_consistency_is_unknown_when_any_requested_sample_is_missing(
    tmp_path: Path,
) -> None:
    structure = tmp_path / "0.extxyz.xz"
    sidecar = tmp_path / "0.txt.xz"
    write_xz(structure, "0\nProperties=species:S:1\n")
    write_xz(sidecar, "random1,frame1,-1\n")

    result = profile_oc20_sample_consistency(structure, sidecar, (0, 1))

    assert result.structure_samples_found == 1
    assert result.sidecar_samples_found == 1
    assert result.atom_property_schema_consistent is None
    assert result.header_field_names_consistent is None
    assert result.sidecar_field_count_consistent is None
    assert [issue.code for issue in result.issues].count(
        "missing_structure_sample"
    ) == 1
    assert [issue.code for issue in result.issues].count("missing_sidecar_sample") == 1
