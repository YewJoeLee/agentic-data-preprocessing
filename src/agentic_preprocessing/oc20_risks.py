"""Deterministic risk evidence for explicit group/split assignments."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from .oc20_inspection import InspectionIssue


@dataclass(frozen=True)
class GroupSplitAssignment:
    """One caller-supplied relationship between a record, group, and split."""

    record_id: str
    group_id: str | None
    split: str | None


@dataclass(frozen=True)
class GroupSplitRisk:
    """Aggregate evidence for one group that spans multiple split labels."""

    group_id: str
    splits: tuple[str, ...]
    assignment_count: int

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native aggregate risk evidence."""

        return {
            "group_id": self.group_id,
            "splits": list(self.splits),
            "assignment_count": self.assignment_count,
        }


@dataclass(frozen=True)
class GroupSplitRiskReport:
    """Serializable aggregate group/split risk evidence."""

    assignment_count: int
    group_count: int
    missing_group_id_count: int
    missing_split_count: int
    cross_split_groups: tuple[GroupSplitRisk, ...]
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native evidence without exposing source record IDs."""

        return {
            "assignment_count": self.assignment_count,
            "group_count": self.group_count,
            "missing_group_id_count": self.missing_group_id_count,
            "missing_split_count": self.missing_split_count,
            "cross_split_groups": [risk.to_dict() for risk in self.cross_split_groups],
            "issues": [issue.to_dict() for issue in self.issues],
        }


def analyse_group_split_risks(
    assignments: Iterable[GroupSplitAssignment],
) -> GroupSplitRiskReport:
    """Report explicit groups whose supplied assignments span multiple splits."""

    assignment_items = tuple(assignments)
    grouped_splits: dict[str, list[str]] = {}
    issues: list[InspectionIssue] = []
    missing_group_id_count = 0
    missing_split_count = 0

    for assignment in assignment_items:
        has_group_id = bool(assignment.group_id)
        has_split = bool(assignment.split)
        if not has_group_id:
            missing_group_id_count += 1
            issues.append(
                InspectionIssue(
                    "missing_group_id",
                    "The assignment has no explicit group ID.",
                )
            )
        if not has_split:
            missing_split_count += 1
            issues.append(
                InspectionIssue(
                    "missing_split_label",
                    "The assignment has no explicit split label.",
                )
            )
        if not (has_group_id and has_split):
            continue
        grouped_splits.setdefault(assignment.group_id, []).append(assignment.split)

    cross_split_groups = tuple(
        GroupSplitRisk(
            group_id=group_id,
            splits=tuple(sorted(set(splits))),
            assignment_count=len(splits),
        )
        for group_id, splits in sorted(grouped_splits.items())
        if len(set(splits)) > 1
    )
    issues.extend(
        InspectionIssue(
            "group_spans_multiple_splits",
            f"Group {risk.group_id!r} spans: {', '.join(risk.splits)}.",
        )
        for risk in cross_split_groups
    )
    return GroupSplitRiskReport(
        assignment_count=len(assignment_items),
        group_count=len(grouped_splits),
        missing_group_id_count=missing_group_id_count,
        missing_split_count=missing_split_count,
        cross_split_groups=cross_split_groups,
        issues=tuple(issues),
    )
