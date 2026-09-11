"""Composition of the deterministic OC20 profiler's implemented slices."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .oc20_discovery import Oc20Discovery, ShardPair, discover_oc20
from .oc20_inspection import (
    InspectionIssue,
    ShardPairInspection,
    inspect_oc20_shard_pair,
)
from .oc20_mappings import (
    MappingKeyValidation,
    TrustedOc20Mappings,
    load_trusted_oc20_mappings,
    validate_oc20_mapping_keys,
)
from .oc20_metadata import MetadataRecordProfile, profile_trusted_metadata_record
from .oc20_schema import Oc20SampleSchema, profile_oc20_sample

_UNIT_EVIDENCE_FIELDS = ("energy", "free_energy", "forces", "reference_energy")


@dataclass(frozen=True)
class Oc20Profile:
    """JSON-serialisable evidence from the currently implemented OC20 slices."""

    discovery: Oc20Discovery
    selected_numeric_stem: int | None
    inspection: ShardPairInspection | None
    sample_schema: Oc20SampleSchema | None
    mapping_validation: MappingKeyValidation | None
    metadata_record_profile: MetadataRecordProfile | None
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "discovery": self.discovery.to_dict(),
            "selected_numeric_stem": self.selected_numeric_stem,
            "inspection": None
            if self.inspection is None
            else self.inspection.to_dict(),
            "sample_schema": (
                None if self.sample_schema is None else self.sample_schema.to_dict()
            ),
            "mapping_validation": (
                None
                if self.mapping_validation is None
                else self.mapping_validation.to_dict()
            ),
            "metadata_record_profile": (
                None
                if self.metadata_record_profile is None
                else self.metadata_record_profile.to_dict()
            ),
            "unit_evidence": [
                {
                    "field": field,
                    "unit": None,
                    "status": "unresolved",
                    "reason": "No verified OC20 unit convention is recorded by this profiler.",
                }
                for field in _UNIT_EVIDENCE_FIELDS
            ],
            "issues": [issue.to_dict() for issue in self.issues],
        }


def profile_oc20_dataset(
    dataset_root: str | Path,
    *,
    shard_stem: int | None = None,
    sample_index: int = 0,
    allow_pickle_load: bool = False,
) -> Oc20Profile:
    """Run the implemented deterministic profile over one valid OC20 shard pair.

    With no ``shard_stem``, the lowest valid numeric stem is selected. Pickle
    loading remains disabled unless the caller explicitly authorises trusted
    mapping files through ``allow_pickle_load=True``.
    """

    root = Path(dataset_root)
    discovery = discover_oc20(root)
    issues: list[InspectionIssue] = []
    selected_pair = _select_pair(discovery, shard_stem, issues)
    if selected_pair is None:
        return Oc20Profile(discovery, None, None, None, None, None, tuple(issues))

    inspection = inspect_oc20_shard_pair(
        root / selected_pair.structure_files[0],
        root / selected_pair.sidecar_files[0],
        sample_index=sample_index,
    )
    sample_schema = profile_oc20_sample(inspection)
    mapping_validation, trusted_mappings = _validate_mappings(
        discovery, root, inspection, allow_pickle_load, issues
    )
    metadata_record_profile = None
    if (
        allow_pickle_load
        and mapping_validation is not None
        and mapping_validation.system_id is not None
        and len(discovery.metadata_mapping_files) == 1
        and trusted_mappings is not None
        and trusted_mappings.metadata_mapping is not None
    ):
        metadata_record_profile = profile_trusted_metadata_record(
            mapping_validation.system_id,
            root / discovery.metadata_mapping_files[0],
            metadata_mapping=trusted_mappings.metadata_mapping,
        )
    issues.extend(inspection.issues)
    issues.extend(sample_schema.issues)
    if mapping_validation is not None:
        issues.extend(mapping_validation.issues)
    return Oc20Profile(
        discovery=discovery,
        selected_numeric_stem=selected_pair.numeric_stem,
        inspection=inspection,
        sample_schema=sample_schema,
        mapping_validation=mapping_validation,
        metadata_record_profile=metadata_record_profile,
        issues=_deduplicate_issues(issues),
    )


def _select_pair(
    discovery: Oc20Discovery,
    shard_stem: int | None,
    issues: list[InspectionIssue],
) -> ShardPair | None:
    valid_pairs = [pair for pair in discovery.shard_pairs if pair.is_valid_pair]
    if shard_stem is None:
        if valid_pairs:
            return valid_pairs[0]
        issues.append(
            InspectionIssue(
                "no_valid_shard_pair", "No valid numeric shard pair was found."
            )
        )
        return None

    selected_pair = next(
        (pair for pair in discovery.shard_pairs if pair.numeric_stem == shard_stem),
        None,
    )
    if selected_pair is None:
        issues.append(
            InspectionIssue(
                "requested_shard_not_found", f"Shard stem {shard_stem} was not found."
            )
        )
        return None
    if not selected_pair.is_valid_pair:
        issues.append(
            InspectionIssue(
                "requested_shard_is_invalid",
                f"Shard stem {shard_stem} has missing or duplicate counterparts.",
            )
        )
        return None
    return selected_pair


def _validate_mappings(
    discovery: Oc20Discovery,
    root: Path,
    inspection: ShardPairInspection,
    allow_pickle_load: bool,
    issues: list[InspectionIssue],
) -> tuple[MappingKeyValidation | None, TrustedOc20Mappings | None]:
    if (
        len(discovery.metadata_mapping_files) != 1
        or len(discovery.clean_slab_mapping_files) != 1
    ):
        issues.append(
            InspectionIssue(
                "ambiguous_mapping_files",
                "Mapping-key validation requires exactly one metadata and clean-slab mapping file.",
            )
        )
        return None, None
    trusted_mappings = (
        load_trusted_oc20_mappings(
            root / discovery.metadata_mapping_files[0],
            root / discovery.clean_slab_mapping_files[0],
        )
        if allow_pickle_load
        else None
    )
    return validate_oc20_mapping_keys(
        inspection,
        root / discovery.metadata_mapping_files[0],
        root / discovery.clean_slab_mapping_files[0],
        allow_pickle_load=allow_pickle_load,
        trusted_mappings=trusted_mappings,
    ), trusted_mappings


def _deduplicate_issues(
    issues: list[InspectionIssue],
) -> tuple[InspectionIssue, ...]:
    """Return deterministic profile-wide issue evidence without duplicates."""

    return tuple(sorted(set(issues), key=lambda issue: (issue.code, issue.message)))
