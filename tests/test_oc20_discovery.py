"""Focused tests for the read-only OC20 discovery slice."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_preprocessing.oc20_discovery import discover_oc20


def touch(root: Path, relative_path: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def test_discover_oc20_inventories_supported_files_and_valid_pairs(
    tmp_path: Path,
) -> None:
    touch(tmp_path, "s2ef_train_200K/README_s2ef_train_200K.md")
    touch(tmp_path, "s2ef_train_200K/s2ef_train_200K/0.extxyz.xz")
    touch(tmp_path, "s2ef_train_200K/s2ef_train_200K/0.txt.xz")
    touch(tmp_path, "s2ef_train_200K/s2ef_train_200K/12.extxyz.xz")
    touch(tmp_path, "s2ef_train_200K/s2ef_train_200K/12.txt.xz")
    touch(tmp_path, "oc20_data_mapping.pkl")
    touch(tmp_path, "mapping_adslab_slab.pkl")
    touch(tmp_path, ".DS_Store")
    touch(tmp_path, "notes/not_a_shard.extxyz.xz")

    result = discover_oc20(tmp_path)

    assert result.readme_files == ("s2ef_train_200K/README_s2ef_train_200K.md",)
    assert result.metadata_mapping_files == ("oc20_data_mapping.pkl",)
    assert result.clean_slab_mapping_files == ("mapping_adslab_slab.pkl",)
    assert result.valid_shard_pair_count == 2
    assert [pair.numeric_stem for pair in result.shard_pairs] == [0, 12]
    assert all(pair.is_valid_pair for pair in result.shard_pairs)

    profile = result.to_dict()
    assert profile["mapping_pickles"]["oc20_data_mapping"] == ["oc20_data_mapping.pkl"]
    json.dumps(profile)


def test_discover_oc20_reports_missing_and_duplicate_counterparts(
    tmp_path: Path,
) -> None:
    touch(tmp_path, "shards/3.extxyz.xz")
    touch(tmp_path, "shards/4.txt.xz")
    touch(tmp_path, "shards/7.extxyz.xz")
    touch(tmp_path, "alternate/007.extxyz.xz")
    touch(tmp_path, "shards/7.txt.xz")
    touch(tmp_path, "alternate/007.txt.xz")

    result = discover_oc20(tmp_path)
    pairs = {pair.numeric_stem: pair for pair in result.shard_pairs}

    assert pairs[3].missing_counterparts == ("sidecar",)
    assert pairs[3].duplicate_counterparts == ()
    assert pairs[4].missing_counterparts == ("structure",)
    assert pairs[4].duplicate_counterparts == ()
    assert pairs[7].missing_counterparts == ()
    assert pairs[7].duplicate_counterparts == ("structure", "sidecar")
    assert pairs[7].structure_files == ("alternate/007.extxyz.xz", "shards/7.extxyz.xz")
    assert pairs[7].sidecar_files == ("alternate/007.txt.xz", "shards/7.txt.xz")
    assert result.valid_shard_pair_count == 0


def test_discover_oc20_requires_an_existing_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not a directory"):
        discover_oc20(tmp_path / "missing")


def test_discover_oc20_ignores_symlinked_files_outside_dataset_root(
    tmp_path: Path,
) -> None:
    outside_structure = tmp_path.parent / f"{tmp_path.name}-outside.extxyz.xz"
    outside_structure.touch()
    (tmp_path / "0.extxyz.xz").symlink_to(outside_structure)
    touch(tmp_path, "0.txt.xz")

    result = discover_oc20(tmp_path)

    assert result.ignored_symlink_files == ("0.extxyz.xz",)
    assert result.structure_shards == ()
    assert result.valid_shard_pair_count == 0
    assert result.to_dict()["ignored_symlink_files"] == ["0.extxyz.xz"]
