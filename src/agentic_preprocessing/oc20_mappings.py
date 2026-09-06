"""Opt-in validation of inspected OC20 system IDs against trusted pickles."""

from __future__ import annotations

import pickle
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .oc20_inspection import InspectionIssue, ShardPairInspection


@dataclass(frozen=True)
class MappingKeyValidation:
    """Serializable mapping-membership evidence for one inspected system ID."""

    system_id: str | None
    metadata_mapping_path: str
    clean_slab_mapping_path: str
    pickle_load_attempted: bool
    metadata_key_present: bool | None
    clean_slab_mapping_key_present: bool | None
    clean_slab_system_id: str | None
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "system_id": self.system_id,
            "metadata_mapping_path": self.metadata_mapping_path,
            "clean_slab_mapping_path": self.clean_slab_mapping_path,
            "pickle_load_attempted": self.pickle_load_attempted,
            "metadata_key_present": self.metadata_key_present,
            "clean_slab_mapping_key_present": self.clean_slab_mapping_key_present,
            "clean_slab_system_id": self.clean_slab_system_id,
            "issues": [issue.to_dict() for issue in self.issues],
        }


@dataclass(frozen=True)
class TrustedOc20Mappings:
    """Trusted in-memory mappings retained only for one profiling operation."""

    metadata_mapping: Mapping[str, Any] | None
    clean_slab_mapping: Mapping[str, Any] | None
    issues: tuple[InspectionIssue, ...]


def load_trusted_oc20_mappings(
    metadata_mapping_path: str | Path, clean_slab_mapping_path: str | Path
) -> TrustedOc20Mappings:
    """Load both trusted mappings once for validation and bounded metadata use."""

    issues: list[InspectionIssue] = []
    return TrustedOc20Mappings(
        metadata_mapping=_load_mapping(Path(metadata_mapping_path), "metadata", issues),
        clean_slab_mapping=_load_mapping(
            Path(clean_slab_mapping_path), "clean-slab", issues
        ),
        issues=tuple(issues),
    )


def validate_oc20_mapping_keys(
    inspection: ShardPairInspection,
    metadata_mapping_path: str | Path,
    clean_slab_mapping_path: str | Path,
    *,
    allow_pickle_load: bool = False,
    trusted_mappings: TrustedOc20Mappings | None = None,
) -> MappingKeyValidation:
    """Check an inspected sidecar system ID in explicitly trusted mappings.

    Pickle deserialisation can execute code. Callers must set
    ``allow_pickle_load=True`` only after independently verifying the source
    and checksum of both local files. This function reads mappings but never
    modifies them or writes derived data.
    """

    metadata_path = Path(metadata_mapping_path)
    clean_slab_path = Path(clean_slab_mapping_path)
    issues: list[InspectionIssue] = []
    system_id = _sample_system_id(inspection, issues)

    if not allow_pickle_load:
        issues.append(
            InspectionIssue(
                "pickle_load_not_authorized",
                "Mapping files were not loaded; explicit trust is required for pickle.",
            )
        )
        return MappingKeyValidation(
            system_id=system_id,
            metadata_mapping_path=str(metadata_path),
            clean_slab_mapping_path=str(clean_slab_path),
            pickle_load_attempted=False,
            metadata_key_present=None,
            clean_slab_mapping_key_present=None,
            clean_slab_system_id=None,
            issues=tuple(issues),
        )

    loaded_mappings = trusted_mappings or load_trusted_oc20_mappings(
        metadata_path, clean_slab_path
    )
    issues.extend(loaded_mappings.issues)
    metadata_mapping = loaded_mappings.metadata_mapping
    clean_slab_mapping = loaded_mappings.clean_slab_mapping

    metadata_key_present = (
        None
        if metadata_mapping is None or system_id is None
        else system_id in metadata_mapping
    )
    clean_slab_mapping_key_present = (
        None
        if clean_slab_mapping is None or system_id is None
        else system_id in clean_slab_mapping
    )
    clean_slab_system_id: str | None = None
    if (
        clean_slab_mapping_key_present
        and clean_slab_mapping is not None
        and system_id is not None
    ):
        clean_slab_value = clean_slab_mapping[system_id]
        if isinstance(clean_slab_value, str):
            clean_slab_system_id = clean_slab_value
        else:
            issues.append(
                InspectionIssue(
                    "invalid_clean_slab_mapping_value",
                    "The clean-slab mapping value is not a string system ID.",
                )
            )

    return MappingKeyValidation(
        system_id=system_id,
        metadata_mapping_path=str(metadata_path),
        clean_slab_mapping_path=str(clean_slab_path),
        pickle_load_attempted=True,
        metadata_key_present=metadata_key_present,
        clean_slab_mapping_key_present=clean_slab_mapping_key_present,
        clean_slab_system_id=clean_slab_system_id,
        issues=tuple(issues),
    )


def _sample_system_id(
    inspection: ShardPairInspection, issues: list[InspectionIssue]
) -> str | None:
    if inspection.sidecar_sample is None or not inspection.sidecar_sample.fields:
        issues.append(
            InspectionIssue(
                "missing_system_id",
                "The inspection contains no sidecar system ID to validate.",
            )
        )
        return None
    return inspection.sidecar_sample.fields[0]


def _load_mapping(
    path: Path, label: str, issues: list[InspectionIssue]
) -> Mapping[str, Any] | None:
    try:
        with path.open("rb") as file:
            loaded = pickle.load(file)
    except (
        AttributeError,
        EOFError,
        ImportError,
        OSError,
        pickle.UnpicklingError,
    ) as error:
        issues.append(
            InspectionIssue(
                "mapping_load_error",
                f"Could not load the {label} mapping at {path}: {error}",
            )
        )
        return None

    if not isinstance(loaded, Mapping):
        issues.append(
            InspectionIssue(
                "invalid_mapping_type",
                f"The {label} mapping at {path} is not a key-value mapping.",
            )
        )
        return None
    return loaded
