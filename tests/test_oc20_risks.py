"""Tests for explicit group/split risk evidence."""

from __future__ import annotations

import json

from agentic_preprocessing.oc20_risks import (
    GroupSplitAssignment,
    GroupSplitRisk,
    analyse_group_split_risks,
)


def test_analyser_reports_group_spanning_multiple_splits() -> None:
    report = analyse_group_split_risks(
        [
            GroupSplitAssignment("record-a", "group-1", "train"),
            GroupSplitAssignment("record-b", "group-1", "validation"),
            GroupSplitAssignment("record-c", "group-2", "train"),
        ]
    )

    assert report.assignment_count == 3
    assert report.group_count == 2
    assert report.cross_split_groups == (
        GroupSplitRisk("group-1", ("train", "validation"), 2),
    )
    assert [issue.code for issue in report.issues] == ["group_spans_multiple_splits"]


def test_analyser_accepts_groups_confined_to_one_split() -> None:
    report = analyse_group_split_risks(
        [
            GroupSplitAssignment("record-a", "group-1", "train"),
            GroupSplitAssignment("record-b", "group-1", "train"),
        ]
    )

    assert report.cross_split_groups == ()
    assert report.issues == ()


def test_analyser_reports_missing_group_or_split_without_aggregation() -> None:
    report = analyse_group_split_risks(
        [
            GroupSplitAssignment("record-a", None, "train"),
            GroupSplitAssignment("record-b", "", "validation"),
            GroupSplitAssignment("record-c", "group-1", None),
            GroupSplitAssignment("record-d", "group-2", ""),
        ]
    )

    assert report.group_count == 0
    assert report.missing_group_id_count == 2
    assert report.missing_split_count == 2
    assert [issue.code for issue in report.issues] == [
        "missing_group_id",
        "missing_group_id",
        "missing_split_label",
        "missing_split_label",
    ]


def test_analyser_serialisation_is_repeatable_and_omits_record_ids() -> None:
    assignments = [
        GroupSplitAssignment("record-d", "group-2", "validation"),
        GroupSplitAssignment("record-c", "group-1", "validation"),
        GroupSplitAssignment("record-b", "group-2", "train"),
        GroupSplitAssignment("record-a", "group-1", "train"),
    ]

    report = analyse_group_split_risks(assignments)
    first = json.dumps(report.to_dict(), sort_keys=True)
    second = json.dumps(
        analyse_group_split_risks(assignments).to_dict(), sort_keys=True
    )

    assert first == second
    assert [risk.group_id for risk in report.cross_split_groups] == [
        "group-1",
        "group-2",
    ]
    assert report.cross_split_groups[0].splits == ("train", "validation")
    assert "record-a" not in first
    assert "record-d" not in first
