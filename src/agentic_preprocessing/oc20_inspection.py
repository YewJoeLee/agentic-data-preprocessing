"""Read-only, bounded inspection of paired OC20 compressed shards."""

from __future__ import annotations

import csv
import lzma
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

_PROPERTIES_RE = re.compile(r'(?:^|\s)Properties=(?P<value>"[^"]*"|\S+)')


@dataclass(frozen=True)
class InspectionIssue:
    """A non-destructive inspection problem, recorded as evidence."""

    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


@dataclass(frozen=True)
class StructureSample:
    """A bounded observation from one extended-XYZ record."""

    record_index: int
    atom_count: int
    header: str
    property_names: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_index": self.record_index,
            "atom_count": self.atom_count,
            "header": self.header,
            "property_names": list(self.property_names),
        }


@dataclass(frozen=True)
class SidecarSample:
    """The raw CSV fields from one sidecar row."""

    row_index: int
    fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"row_index": self.row_index, "fields": list(self.fields)}


@dataclass(frozen=True)
class ShardPairInspection:
    """Serializable evidence from one structure shard and sidecar shard."""

    structure_path: str
    sidecar_path: str
    sample_index: int
    structure_record_count: int
    sidecar_row_count: int
    structure_scan_complete: bool
    sidecar_scan_complete: bool
    structure_sample: StructureSample | None
    sidecar_sample: SidecarSample | None
    issues: tuple[InspectionIssue, ...]

    @property
    def row_counts_match(self) -> bool | None:
        """Whether complete scans observed the same record and row count."""

        if not (self.structure_scan_complete and self.sidecar_scan_complete):
            return None
        return self.structure_record_count == self.sidecar_row_count

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native output with raw sample values left uncoerced."""

        return {
            "structure_path": self.structure_path,
            "sidecar_path": self.sidecar_path,
            "sample_index": self.sample_index,
            "structure_record_count": self.structure_record_count,
            "sidecar_row_count": self.sidecar_row_count,
            "structure_scan_complete": self.structure_scan_complete,
            "sidecar_scan_complete": self.sidecar_scan_complete,
            "row_counts_match": self.row_counts_match,
            "structure_sample": (
                None
                if self.structure_sample is None
                else self.structure_sample.to_dict()
            ),
            "sidecar_sample": (
                None if self.sidecar_sample is None else self.sidecar_sample.to_dict()
            ),
            "issues": [issue.to_dict() for issue in self.issues],
        }


def inspect_oc20_shard_pair(
    structure_path: str | Path,
    sidecar_path: str | Path,
    *,
    sample_index: int = 0,
) -> ShardPairInspection:
    """Stream one compressed shard pair and validate its record/row counts.

    ``sample_index`` selects a single same-position structure and sidecar row
    for evidence. The complete streams are read only to count records and rows;
    no data is extracted, transformed, or written to disk.
    """

    return inspect_oc20_shard_pair_samples(
        structure_path, sidecar_path, sample_indices=(sample_index,)
    )[0]


def inspect_oc20_shard_pair_samples(
    structure_path: str | Path,
    sidecar_path: str | Path,
    *,
    sample_indices: Iterable[int],
) -> tuple[ShardPairInspection, ...]:
    """Stream one shard pair once while collecting several requested samples."""

    indices = tuple(sample_indices)
    if not indices or any(index < 0 for index in indices):
        raise ValueError("sample_indices must be non-empty and non-negative")
    if len(set(indices)) != len(indices):
        raise ValueError("sample_indices must be unique")

    structure = Path(structure_path)
    sidecar = Path(sidecar_path)
    (
        structure_record_count,
        structure_samples,
        structure_scan_complete,
        structure_issues,
    ) = _scan_structures(structure, set(indices))
    (
        sidecar_row_count,
        sidecar_samples,
        sidecar_scan_complete,
        sidecar_issues,
    ) = _scan_sidecar(sidecar, set(indices))
    issues = structure_issues + sidecar_issues
    if (
        structure_scan_complete
        and sidecar_scan_complete
        and structure_record_count != sidecar_row_count
    ):
        issues.append(
            InspectionIssue(
                "row_count_mismatch",
                "Structure-record and sidecar-row counts differ for the selected pair.",
            )
        )

    return tuple(
        ShardPairInspection(
            structure_path=str(structure),
            sidecar_path=str(sidecar),
            sample_index=index,
            structure_record_count=structure_record_count,
            sidecar_row_count=sidecar_row_count,
            structure_scan_complete=structure_scan_complete,
            sidecar_scan_complete=sidecar_scan_complete,
            structure_sample=structure_samples.get(index),
            sidecar_sample=sidecar_samples.get(index),
            issues=tuple(issues),
        )
        for index in indices
    )


def _scan_structures(
    path: Path, sample_indices: set[int]
) -> tuple[int, dict[int, StructureSample], bool, list[InspectionIssue]]:
    record_count = 0
    samples: dict[int, StructureSample] = {}
    issues: list[InspectionIssue] = []

    try:
        with lzma.open(path, mode="rt", encoding="utf-8") as stream:
            while atom_count_line := stream.readline():
                record_index = record_count
                try:
                    atom_count = int(atom_count_line.strip())
                except ValueError:
                    issues.append(
                        InspectionIssue(
                            "invalid_atom_count",
                            f"Structure record {record_index} has an invalid atom count.",
                        )
                    )
                    return record_count, samples, False, issues

                if atom_count < 0:
                    issues.append(
                        InspectionIssue(
                            "negative_atom_count",
                            f"Structure record {record_index} has a negative atom count.",
                        )
                    )
                    return record_count, samples, False, issues

                header_line = stream.readline()
                if not header_line:
                    issues.append(
                        InspectionIssue(
                            "missing_structure_header",
                            f"Structure record {record_index} has no header line.",
                        )
                    )
                    return record_count, samples, False, issues

                header = header_line.rstrip("\n")
                expected_atom_field_count = _expected_atom_field_count(header)
                for atom_row_index in range(atom_count):
                    atom_row = stream.readline()
                    if not atom_row:
                        issues.append(
                            InspectionIssue(
                                "truncated_structure_record",
                                "Structure record "
                                f"{record_index} ends before atom row {atom_row_index}.",
                            )
                        )
                        return record_count, samples, False, issues
                    if (
                        expected_atom_field_count is not None
                        and len(atom_row.split()) != expected_atom_field_count
                    ):
                        issues.append(
                            InspectionIssue(
                                "atom_row_property_count_mismatch",
                                "Structure record "
                                f"{record_index} atom row {atom_row_index} has "
                                f"{len(atom_row.split())} fields; expected "
                                f"{expected_atom_field_count} from Properties.",
                            )
                        )

                if record_index in sample_indices:
                    samples[record_index] = StructureSample(
                        record_index=record_index,
                        atom_count=atom_count,
                        header=header,
                        property_names=_property_names(header),
                    )
                record_count += 1
    except (OSError, UnicodeDecodeError, lzma.LZMAError) as error:
        issues.append(
            InspectionIssue("structure_read_error", f"Could not read {path}: {error}")
        )
        return record_count, samples, False, issues

    return record_count, samples, True, issues


def _scan_sidecar(
    path: Path, sample_indices: set[int]
) -> tuple[int, dict[int, SidecarSample], bool, list[InspectionIssue]]:
    row_count = 0
    samples: dict[int, SidecarSample] = {}
    issues: list[InspectionIssue] = []

    try:
        with lzma.open(path, mode="rt", encoding="utf-8", newline="") as stream:
            for row in csv.reader(stream):
                row_index = row_count
                if len(row) != 3:
                    issues.append(
                        InspectionIssue(
                            "invalid_sidecar_field_count",
                            f"Sidecar row {row_index} has {len(row)} fields; expected 3.",
                        )
                    )
                if row_index in sample_indices:
                    samples[row_index] = SidecarSample(
                        row_index=row_index, fields=tuple(row)
                    )
                row_count += 1
    except (OSError, UnicodeDecodeError, lzma.LZMAError, csv.Error) as error:
        issues.append(
            InspectionIssue("sidecar_read_error", f"Could not read {path}: {error}")
        )
        return row_count, samples, False, issues

    return row_count, samples, True, issues


def _property_names(header: str) -> tuple[str, ...]:
    """Extract declared extended-XYZ property names without parsing values."""

    match = _PROPERTIES_RE.search(header)
    if match is None:
        return ()
    declaration = match["value"].strip('"')
    return tuple(declaration.split(":")[::3])


def _expected_atom_field_count(header: str) -> int | None:
    """Return declared atom-row fields when ``Properties`` is well formed."""

    match = _PROPERTIES_RE.search(header)
    if match is None:
        return None
    components = match["value"].strip('"').split(":")
    if not components or len(components) % 3 != 0:
        return None
    try:
        counts = [int(value) for value in components[2::3]]
    except ValueError:
        return None
    if any(count < 1 for count in counts):
        return None
    return sum(counts)
