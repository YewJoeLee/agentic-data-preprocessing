"""Deterministic risk evidence for explicit ordered-group assignments."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from .oc20_inspection import InspectionIssue


@dataclass(frozen=True)
class SequenceAssignment:
    """One caller-supplied record position within an explicitly named group."""

    record_id: str
    group_id: str | None
    position: int | None


@dataclass(frozen=True)
class DuplicateSequencePosition:
    """Aggregate evidence that a group has repeated explicit positions."""

    group_id: str
    position: int
    assignment_count: int

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native duplicate-position evidence."""

        return {
            "group_id": self.group_id,
            "position": self.position,
            "assignment_count": self.assignment_count,
        }


@dataclass(frozen=True)
class SequenceRiskReport:
    """Serializable aggregate evidence for explicit ordered-group assignments."""

    assignment_count: int
    group_count: int
    missing_group_id_count: int
    missing_position_count: int
    negative_position_count: int
    duplicate_positions: tuple[DuplicateSequencePosition, ...]
    non_monotonic_group_ids: tuple[str, ...]
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native evidence without exposing source record IDs."""

        return {
            "assignment_count": self.assignment_count,
            "group_count": self.group_count,
            "missing_group_id_count": self.missing_group_id_count,
            "missing_position_count": self.missing_position_count,
            "negative_position_count": self.negative_position_count,
            "duplicate_positions": [
                item.to_dict() for item in self.duplicate_positions
            ],
            "non_monotonic_group_ids": list(self.non_monotonic_group_ids),
            "issues": [issue.to_dict() for issue in self.issues],
        }


def analyse_sequence_risks(
    assignments: Iterable[SequenceAssignment],
) -> SequenceRiskReport:
    """Report duplicate or decreasing positions in caller-supplied group order."""

    assignment_items = tuple(assignments)
    grouped_positions: dict[str, list[int]] = {}
    issues: list[InspectionIssue] = []
    missing_group_id_count = 0
    missing_position_count = 0
    negative_position_count = 0

    for assignment in assignment_items:
        has_group_id = bool(assignment.group_id)
        has_position = assignment.position is not None
        has_non_negative_position = has_position and assignment.position >= 0

        if not has_group_id:
            missing_group_id_count += 1
            issues.append(
                InspectionIssue(
                    "missing_sequence_group_id",
                    "The assignment has no explicit sequence group ID.",
                )
            )
        if not has_position:
            missing_position_count += 1
            issues.append(
                InspectionIssue(
                    "missing_sequence_position",
                    "The assignment has no explicit sequence position.",
                )
            )
        elif not has_non_negative_position:
            negative_position_count += 1
            issues.append(
                InspectionIssue(
                    "negative_sequence_position",
                    "The assignment has a negative sequence position.",
                )
            )
        if not (has_group_id and has_non_negative_position):
            continue
        grouped_positions.setdefault(assignment.group_id, []).append(
            assignment.position
        )

    duplicate_positions = _duplicate_positions(grouped_positions)
    non_monotonic_group_ids = tuple(
        group_id
        for group_id, positions in sorted(grouped_positions.items())
        if any(
            current < previous for previous, current in zip(positions, positions[1:])
        )
    )
    issues.extend(
        InspectionIssue(
            "duplicate_sequence_position",
            "Group "
            f"{item.group_id!r} has {item.assignment_count} assignments at "
            f"position {item.position}.",
        )
        for item in duplicate_positions
    )
    issues.extend(
        InspectionIssue(
            "non_monotonic_sequence_position",
            f"Group {group_id!r} has decreasing supplied sequence positions.",
        )
        for group_id in non_monotonic_group_ids
    )
    return SequenceRiskReport(
        assignment_count=len(assignment_items),
        group_count=len(grouped_positions),
        missing_group_id_count=missing_group_id_count,
        missing_position_count=missing_position_count,
        negative_position_count=negative_position_count,
        duplicate_positions=duplicate_positions,
        non_monotonic_group_ids=non_monotonic_group_ids,
        issues=tuple(issues),
    )


def _duplicate_positions(
    grouped_positions: dict[str, list[int]],
) -> tuple[DuplicateSequencePosition, ...]:
    """Return repeated positions sorted by group and position."""

    duplicates: list[DuplicateSequencePosition] = []
    for group_id, positions in sorted(grouped_positions.items()):
        position_counts: dict[int, int] = {}
        for position in positions:
            position_counts[position] = position_counts.get(position, 0) + 1
        duplicates.extend(
            DuplicateSequencePosition(group_id, position, count)
            for position, count in sorted(position_counts.items())
            if count > 1
        )
    return tuple(duplicates)
