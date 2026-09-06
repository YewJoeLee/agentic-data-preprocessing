"""Focused tests for lexical OC20 sample-schema profiling."""

from __future__ import annotations

import json
import lzma
from pathlib import Path

from agentic_preprocessing.oc20_inspection import inspect_oc20_shard_pair
from agentic_preprocessing.oc20_schema import profile_oc20_sample


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_profile_oc20_sample_reports_declared_and_lexical_types(tmp_path: Path) -> None:
    structure_path = tmp_path / "0.extxyz.xz"
    sidecar_path = tmp_path / "0.txt.xz"
    write_xz(
        structure_path,
        "1\n"
        'Lattice="1.0 0.0 0.0" Properties=species:S:1:pos:R:3:tags:I:1:move_mask:L:1 '
        'energy=-1.5 pbc="T T T"\n'
        "H 0.0 0.0 0.0\n",
    )
    write_xz(sidecar_path, "random1,frame2,-1.5\n")

    inspection = inspect_oc20_shard_pair(structure_path, sidecar_path)
    profile = profile_oc20_sample(inspection)

    assert [
        (field.name, field.observed_type) for field in profile.structure_header_fields
    ] == [
        ("Lattice", "real_vector"),
        ("Properties", "string"),
        ("energy", "real"),
        ("pbc", "boolean_vector"),
    ]
    assert [property_.to_dict() for property_ in profile.atom_properties] == [
        {
            "name": "species",
            "declared_type_code": "S",
            "declared_value_type": "string",
            "components_per_atom": 1,
        },
        {
            "name": "pos",
            "declared_type_code": "R",
            "declared_value_type": "real",
            "components_per_atom": 3,
        },
        {
            "name": "tags",
            "declared_type_code": "I",
            "declared_value_type": "integer",
            "components_per_atom": 1,
        },
        {
            "name": "move_mask",
            "declared_type_code": "L",
            "declared_value_type": "boolean",
            "components_per_atom": 1,
        },
    ]
    assert [(field.name, field.observed_type) for field in profile.sidecar_fields] == [
        ("system_id", "string"),
        ("frame_number", "string"),
        ("reference_energy", "real"),
    ]
    assert profile.issues == ()
    json.dumps(profile.to_dict())


def test_profile_oc20_sample_reports_invalid_property_declaration(
    tmp_path: Path,
) -> None:
    structure_path = tmp_path / "bad.extxyz.xz"
    sidecar_path = tmp_path / "bad.txt.xz"
    write_xz(structure_path, "0\nProperties=species:S\n")
    write_xz(sidecar_path, "random1,frame2,-1.5\n")

    profile = profile_oc20_sample(inspect_oc20_shard_pair(structure_path, sidecar_path))

    assert profile.atom_properties == ()
    assert [issue.code for issue in profile.issues] == [
        "invalid_properties_declaration"
    ]
