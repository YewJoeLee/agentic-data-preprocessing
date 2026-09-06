"""Bounded metadata-record profiling for explicitly trusted OC20 pickles."""

from __future__ import annotations

import hashlib
import pickle
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MetadataFieldProfile:
    name: str
    value_type: str
    container_length: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value_type": self.value_type,
            "container_length": self.container_length,
        }


@dataclass(frozen=True)
class MetadataRecordProfile:
    system_id: str
    mapping_path: str
    sha256: str
    file_size_bytes: int
    key_present: bool
    raw_anomaly_code: int | None
    fields: tuple[MetadataFieldProfile, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "system_id": self.system_id,
            "mapping_path": self.mapping_path,
            "sha256": self.sha256,
            "file_size_bytes": self.file_size_bytes,
            "key_present": self.key_present,
            "raw_anomaly_code": self.raw_anomaly_code,
            "fields": [field.to_dict() for field in self.fields],
        }


def profile_trusted_metadata_record(
    system_id: str,
    mapping_path: str | Path,
    *,
    metadata_mapping: Mapping[str, Any] | None = None,
) -> MetadataRecordProfile:
    """Profile one metadata record after the caller has verified pickle trust."""
    path = Path(mapping_path)
    hasher = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    mapping = metadata_mapping
    if mapping is None:
        with path.open("rb") as file:
            mapping = pickle.load(file)
    if not isinstance(mapping, Mapping):
        raise ValueError("OC20 metadata pickle did not contain a mapping")
    record = mapping.get(system_id)
    if record is None:
        return MetadataRecordProfile(
            system_id, str(path), digest, path.stat().st_size, False, None, ()
        )
    if not isinstance(record, Mapping):
        raise ValueError("OC20 metadata record was not a mapping")
    fields = tuple(
        MetadataFieldProfile(
            name,
            type(value).__name__,
            len(value) if isinstance(value, (list, tuple, dict)) else None,
        )
        for name, value in sorted(record.items())
    )
    return MetadataRecordProfile(
        system_id,
        str(path),
        digest,
        path.stat().st_size,
        True,
        record.get("anomaly") if isinstance(record.get("anomaly"), int) else None,
        fields,
    )
