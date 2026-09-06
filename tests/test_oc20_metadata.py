from __future__ import annotations

import pickle
from pathlib import Path

from agentic_preprocessing.oc20_metadata import profile_trusted_metadata_record


def test_profile_trusted_metadata_record_reports_bounded_schema(tmp_path: Path) -> None:
    path = tmp_path / "oc20_data_mapping.pkl"
    with path.open("wb") as file:
        pickle.dump(
            {"random1": {"ads_id": 1, "miller_index": (1, 1, 1), "split": "train"}},
            file,
        )
    result = profile_trusted_metadata_record("random1", path)
    assert result.key_present is True
    assert [
        (field.name, field.value_type, field.container_length)
        for field in result.fields
    ] == [("ads_id", "int", None), ("miller_index", "tuple", 3), ("split", "str", None)]
    assert len(result.sha256) == 64
