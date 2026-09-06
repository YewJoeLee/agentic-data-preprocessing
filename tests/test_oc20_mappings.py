"""Focused tests for opt-in OC20 mapping-key validation."""

from __future__ import annotations

import json
import lzma
import pickle
from pathlib import Path

from agentic_preprocessing.oc20_inspection import inspect_oc20_shard_pair
from agentic_preprocessing.oc20_mappings import validate_oc20_mapping_keys


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def inspected_sample(tmp_path: Path):
    structure_path = tmp_path / "0.extxyz.xz"
    sidecar_path = tmp_path / "0.txt.xz"
    write_xz(structure_path, "0\nProperties=species:S:1\n")
    write_xz(sidecar_path, "random1,frame2,-1.5\n")
    return inspect_oc20_shard_pair(structure_path, sidecar_path)


def write_pickle(path: Path, content: object) -> None:
    with path.open("wb") as file:
        pickle.dump(content, file)


def test_validate_oc20_mapping_keys_requires_explicit_pickle_trust(
    tmp_path: Path,
) -> None:
    result = validate_oc20_mapping_keys(
        inspected_sample(tmp_path),
        tmp_path / "oc20_data_mapping.pkl",
        tmp_path / "mapping_adslab_slab.pkl",
    )

    assert result.system_id == "random1"
    assert result.pickle_load_attempted is False
    assert result.metadata_key_present is None
    assert result.clean_slab_mapping_key_present is None
    assert [issue.code for issue in result.issues] == ["pickle_load_not_authorized"]


def test_validate_oc20_mapping_keys_checks_trusted_synthetic_mappings(
    tmp_path: Path,
) -> None:
    metadata_path = tmp_path / "oc20_data_mapping.pkl"
    clean_slab_path = tmp_path / "mapping_adslab_slab.pkl"
    write_pickle(metadata_path, {"random1": {"split": "train"}})
    write_pickle(clean_slab_path, {"random1": "slab99"})

    result = validate_oc20_mapping_keys(
        inspected_sample(tmp_path),
        metadata_path,
        clean_slab_path,
        allow_pickle_load=True,
    )

    assert result.pickle_load_attempted is True
    assert result.metadata_key_present is True
    assert result.clean_slab_mapping_key_present is True
    assert result.clean_slab_system_id == "slab99"
    assert result.issues == ()
    json.dumps(result.to_dict())
