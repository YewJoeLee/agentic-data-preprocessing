"""Focused tests for composition of deterministic OC20 profile evidence."""

from __future__ import annotations

import json
import lzma
import pickle
from pathlib import Path

import agentic_preprocessing.oc20_mappings as oc20_mappings
import agentic_preprocessing.oc20_metadata as oc20_metadata
from agentic_preprocessing.oc20_profile import profile_oc20_dataset


def write_xz(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def write_pickle(path: Path, content: object) -> None:
    with path.open("wb") as file:
        pickle.dump(content, file)


def test_profile_oc20_dataset_composes_read_only_evidence(tmp_path: Path) -> None:
    shard_directory = tmp_path / "s2ef_train_200K"
    write_xz(shard_directory / "0.extxyz.xz", "0\nProperties=species:S:1 energy=-1.0\n")
    write_xz(tmp_path / "s2ef_train_200K" / "0.txt.xz", "random1,frame2,-1.0\n")
    write_pickle(tmp_path / "oc20_data_mapping.pkl", {"random1": {}})
    write_pickle(tmp_path / "mapping_adslab_slab.pkl", {"random1": "slab1"})

    profile = profile_oc20_dataset(tmp_path)

    assert profile.selected_numeric_stem == 0
    assert profile.inspection is not None
    assert profile.inspection.row_counts_match is True
    assert profile.sample_schema is not None
    assert profile.sample_schema.atom_properties[0].name == "species"
    assert profile.mapping_validation is not None
    assert profile.mapping_validation.pickle_load_attempted is False
    assert [issue.code for issue in profile.issues] == ["pickle_load_not_authorized"]
    json.dumps(profile.to_dict())


def test_profile_oc20_dataset_reports_when_no_valid_pair_exists(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")

    profile = profile_oc20_dataset(tmp_path)

    assert profile.selected_numeric_stem is None
    assert profile.inspection is None
    assert profile.sample_schema is None
    assert profile.mapping_validation is None
    assert [issue.code for issue in profile.issues] == ["no_valid_shard_pair"]


def test_profile_promotes_selected_pair_integrity_issues(tmp_path: Path) -> None:
    write_xz(
        tmp_path / "0.extxyz.xz",
        "0\nProperties=species:S:1\n0\nProperties=species:S:1\n",
    )
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")

    profile = profile_oc20_dataset(tmp_path)

    assert profile.inspection is not None
    assert profile.inspection.row_counts_match is False
    assert "row_count_mismatch" in {issue.code for issue in profile.issues}


def test_profile_oc20_dataset_matches_synthetic_golden_summary(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")

    profile = profile_oc20_dataset(tmp_path).to_dict()
    golden_path = Path(__file__).parent / "fixtures" / "oc20_profile_golden.json"
    expected = json.loads(golden_path.read_text(encoding="utf-8"))
    actual = {
        "selected_numeric_stem": profile["selected_numeric_stem"],
        "valid_shard_pair_count": profile["discovery"]["valid_shard_pair_count"],
        "structure_record_count": profile["inspection"]["structure_record_count"],
        "sidecar_row_count": profile["inspection"]["sidecar_row_count"],
        "row_counts_match": profile["inspection"]["row_counts_match"],
        "atom_properties": [
            property_["name"]
            for property_ in profile["sample_schema"]["atom_properties"]
        ],
        "sidecar_fields": [
            field["name"] for field in profile["sample_schema"]["sidecar_fields"]
        ],
        "issues": [issue["code"] for issue in profile["issues"]],
        "unit_evidence_status": [item["status"] for item in profile["unit_evidence"]],
    }
    assert actual == expected


def test_profile_includes_trusted_metadata_provenance_and_raw_anomaly(
    tmp_path: Path, monkeypatch
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")
    write_pickle(tmp_path / "oc20_data_mapping.pkl", {"random1": {"anomaly": 3}})
    write_pickle(tmp_path / "mapping_adslab_slab.pkl", {"random1": "slab1"})

    original_pickle_load = pickle.load
    load_count = 0

    def count_pickle_load(file):
        nonlocal load_count
        load_count += 1
        return original_pickle_load(file)

    monkeypatch.setattr(oc20_mappings.pickle, "load", count_pickle_load)
    monkeypatch.setattr(oc20_metadata.pickle, "load", count_pickle_load)

    profile = profile_oc20_dataset(tmp_path, allow_pickle_load=True).to_dict()

    assert profile["metadata_record_profile"]["key_present"] is True
    assert len(profile["metadata_record_profile"]["sha256"]) == 64
    assert profile["metadata_record_profile"]["raw_anomaly_code"] == 3
    assert load_count == 2


def test_profile_reports_absent_metadata_and_clean_slab_relationship(
    tmp_path: Path,
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")
    write_pickle(tmp_path / "oc20_data_mapping.pkl", {})
    write_pickle(tmp_path / "mapping_adslab_slab.pkl", {})

    profile = profile_oc20_dataset(tmp_path, allow_pickle_load=True).to_dict()

    assert profile["mapping_validation"]["metadata_key_present"] is False
    assert profile["mapping_validation"]["clean_slab_mapping_key_present"] is False
    assert profile["mapping_validation"]["clean_slab_system_id"] is None
    assert profile["metadata_record_profile"]["key_present"] is False


def test_profile_marks_unverified_unit_conventions_as_unresolved(
    tmp_path: Path,
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1 energy=-1.0\n")
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")

    evidence = profile_oc20_dataset(tmp_path).to_dict()["unit_evidence"]

    assert {(item["field"], item["unit"], item["status"]) for item in evidence} == {
        ("energy", None, "unresolved"),
        ("free_energy", None, "unresolved"),
        ("forces", None, "unresolved"),
        ("reference_energy", None, "unresolved"),
    }


def test_profile_unit_evidence_is_not_shared_between_serialized_outputs(
    tmp_path: Path,
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1 energy=-1.0\n")
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")

    first = profile_oc20_dataset(tmp_path).to_dict()
    first["unit_evidence"][0]["status"] = "mutated"
    second = profile_oc20_dataset(tmp_path).to_dict()

    assert second["unit_evidence"][0]["status"] == "unresolved"
