"""Multi-record consistency evidence for a read-only OC20 shard sample."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .oc20_inspection import InspectionIssue, inspect_oc20_shard_pair_samples
from .oc20_schema import profile_oc20_sample


@dataclass(frozen=True)
class Oc20SampleConsistency:
    """Serializable schema consistency and empty-field evidence for samples."""

    sample_indices: tuple[int, ...]
    structure_samples_found: int
    sidecar_samples_found: int
    atom_property_schema_consistent: bool | None
    header_field_names_consistent: bool | None
    sidecar_field_count_consistent: bool | None
    sidecar_empty_field_counts: tuple[int, ...]
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "sample_indices": list(self.sample_indices),
            "structure_samples_found": self.structure_samples_found,
            "sidecar_samples_found": self.sidecar_samples_found,
            "atom_property_schema_consistent": self.atom_property_schema_consistent,
            "header_field_names_consistent": self.header_field_names_consistent,
            "sidecar_field_count_consistent": self.sidecar_field_count_consistent,
            "sidecar_empty_field_counts": list(self.sidecar_empty_field_counts),
            "issues": [issue.to_dict() for issue in self.issues],
        }


def profile_oc20_sample_consistency(
    structure_path: str | Path,
    sidecar_path: str | Path,
    sample_indices: Iterable[int] = (0, 1, 2),
) -> Oc20SampleConsistency:
    """Compare fixed record samples without writing or transforming source data.

    Each index is inspected independently so the existing strict row-count
    validation is retained. Empty-field counts apply only to selected sidecar
    rows; they are not a whole-shard missingness claim.
    """

    indices = tuple(sample_indices)
    if (
        not indices
        or any(index < 0 for index in indices)
        or len(set(indices)) != len(indices)
    ):
        raise ValueError("sample_indices must be unique, non-negative, and non-empty")

    inspections = inspect_oc20_shard_pair_samples(
        structure_path, sidecar_path, sample_indices=indices
    )
    schemas = [profile_oc20_sample(inspection) for inspection in inspections]
    structure_found = sum(
        inspection.structure_sample is not None for inspection in inspections
    )
    sidecar_found = sum(
        inspection.sidecar_sample is not None for inspection in inspections
    )
    issues = [issue for inspection in inspections for issue in inspection.issues]
    issues.extend(issue for schema in schemas for issue in schema.issues)

    atom_signatures = [
        tuple(
            (
                property_.name,
                property_.declared_type_code,
                property_.components_per_atom,
            )
            for property_ in schema.atom_properties
        )
        for schema, inspection in zip(schemas, inspections)
        if inspection.structure_sample is not None
    ]
    header_signatures = [
        tuple(field.name for field in schema.structure_header_fields)
        for schema, inspection in zip(schemas, inspections)
        if inspection.structure_sample is not None
    ]
    field_counts = [
        len(inspection.sidecar_sample.fields)
        for inspection in inspections
        if inspection.sidecar_sample is not None
    ]
    sidecar_rows = [
        inspection.sidecar_sample.fields
        for inspection in inspections
        if inspection.sidecar_sample is not None
    ]
    max_field_count = max(field_counts, default=0)
    empty_counts = tuple(
        sum(position < len(row) and row[position] == "" for row in sidecar_rows)
        for position in range(max_field_count)
    )

    return Oc20SampleConsistency(
        sample_indices=indices,
        structure_samples_found=structure_found,
        sidecar_samples_found=sidecar_found,
        atom_property_schema_consistent=_is_consistent(
            atom_signatures, structure_found
        ),
        header_field_names_consistent=_is_consistent(
            header_signatures, structure_found
        ),
        sidecar_field_count_consistent=_is_consistent(field_counts, sidecar_found),
        sidecar_empty_field_counts=empty_counts,
        issues=tuple(issues),
    )


def _is_consistent(signatures: list[Any], found_count: int) -> bool | None:
    if found_count == 0:
        return None
    return len(set(signatures)) == 1
