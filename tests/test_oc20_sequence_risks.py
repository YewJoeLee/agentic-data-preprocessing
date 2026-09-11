"""Tests for explicit ordered-group sequence risk evidence."""

from __future__ import annotations

import json

from agentic_preprocessing.oc20_sequence_risks import (
    DuplicateSequencePosition,
    SequenceAssignment,
    analyse_sequence_risks,
)


def test_analyser_reports_duplicate_and_non_monotonic_positions() -> None:
    report = analyse_sequence_risks(
        [
            SequenceAssignment("record-a", "group-1", 0),
            SequenceAssignment("record-b", "group-1", 2),
            SequenceAssignment("record-c", "group-1", 2),
            SequenceAssignment("record-d", "group-1", 1),
            SequenceAssignment("record-e", "group-2", 0),
        ]
    )

    assert report.assignment_count == 5
    assert report.group_count == 2
    assert report.duplicate_positions == (DuplicateSequencePosition("group-1", 2, 2),)
    assert report.non_monotonic_group_ids == ("group-1",)
    assert [issue.code for issue in report.issues] == [
        "duplicate_sequence_position",
        "non_monotonic_sequence_position",
    ]


def test_analyser_accepts_strictly_increasing_positions() -> None:
    report = analyse_sequence_risks(
        [
            SequenceAssignment("record-a", "group-1", 0),
            SequenceAssignment("record-b", "group-1", 1),
            SequenceAssignment("record-c", "group-2", 0),
        ]
    )

    assert report.duplicate_positions == ()
    assert report.non_monotonic_group_ids == ()
    assert report.issues == ()


def test_analyser_reports_missing_and_negative_evidence_without_aggregation() -> None:
    report = analyse_sequence_risks(
        [
            SequenceAssignment("record-a", None, 0),
            SequenceAssignment("record-b", "", 1),
            SequenceAssignment("record-c", "group-1", None),
            SequenceAssignment("record-d", "group-2", -1),
        ]
    )

    assert report.group_count == 0
    assert report.missing_group_id_count == 2
    assert report.missing_position_count == 1
    assert report.negative_position_count == 1
    assert [issue.code for issue in report.issues] == [
        "missing_sequence_group_id",
        "missing_sequence_group_id",
        "missing_sequence_position",
        "negative_sequence_position",
    ]


def test_analyser_serialisation_is_stable_and_omits_record_ids() -> None:
    assignments = [
        SequenceAssignment("record-d", "group-2", 1),
        SequenceAssignment("record-c", "group-1", 1),
        SequenceAssignment("record-b", "group-2", 1),
        SequenceAssignment("record-a", "group-1", 1),
    ]

    report = analyse_sequence_risks(assignments)
    first = json.dumps(report.to_dict(), sort_keys=True)
    second = json.dumps(analyse_sequence_risks(assignments).to_dict(), sort_keys=True)

    assert first == second
    assert [item.group_id for item in report.duplicate_positions] == [
        "group-1",
        "group-2",
    ]
    assert "record-a" not in first
    assert "record-d" not in first
