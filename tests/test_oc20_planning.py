"""Tests for deterministic OC20 readiness planning."""

from __future__ import annotations

import json
import lzma
from pathlib import Path

import pytest

from agentic_preprocessing.oc20_planning import (
    DownstreamGoal,
    build_oc20_readiness_plan,
)
from agentic_preprocessing.oc20_profile import profile_oc20_dataset


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_planner_returns_reviewable_plan_for_valid_profile(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1 energy=-1.0\n")
    write_xz(tmp_path / "0.txt.xz", "system-secret,frame-1,-1.0\n")

    plan = build_oc20_readiness_plan(
        profile_oc20_dataset(tmp_path),
        DownstreamGoal("Prepare a safe training-data workflow."),
    )

    serialised = plan.to_dict()
    assert plan.status == "ready_for_review"
    assert serialised["goal"] == {"text": "Prepare a safe training-data workflow."}
    assert [item["path"] for item in serialised["evidence"]] == [
        "discovery.valid_shard_pair_count",
        "selected_numeric_stem",
    ]
    assert len(serialised["proposed_checks"]) == 6
    assert (
        sum(
            item["code"] == "resolve_unit_evidence" and item["requires_review"]
            for item in serialised["proposed_checks"]
        )
        == 4
    )
    assert "system-secret" not in json.dumps(serialised, sort_keys=True)
    assert "-1.0" not in json.dumps(serialised, sort_keys=True)


def test_planner_blocks_when_profile_has_no_valid_pair(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")

    plan = build_oc20_readiness_plan(
        profile_oc20_dataset(tmp_path), DownstreamGoal("Prepare data.")
    )

    assert plan.status == "blocked"
    assert [item.code for item in plan.proposed_checks] == ["resolve_profile_blocker"]
    assert [issue.code for issue in plan.issues] == ["profile_not_ready_for_planning"]


def test_planner_rejects_empty_goal(tmp_path: Path) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,frame-1,-1.0\n")

    with pytest.raises(ValueError, match="goal text must not be empty"):
        build_oc20_readiness_plan(profile_oc20_dataset(tmp_path), DownstreamGoal("  "))


def test_planner_serialisation_is_repeatable_and_lexically_sorted(
    tmp_path: Path,
) -> None:
    write_xz(tmp_path / "0.extxyz.xz", "0\nProperties=species:S:1\n")
    write_xz(tmp_path / "0.txt.xz", "system-1,frame-1,-1.0\n")
    profile = profile_oc20_dataset(tmp_path)
    goal = DownstreamGoal("Prepare data.")

    first = json.dumps(
        build_oc20_readiness_plan(profile, goal).to_dict(), sort_keys=True
    )
    second = json.dumps(
        build_oc20_readiness_plan(profile, goal).to_dict(), sort_keys=True
    )
    unit_rationales = [
        item["rationale"]
        for item in json.loads(first)["proposed_checks"]
        if item["code"] == "resolve_unit_evidence"
    ]

    assert first == second
    assert unit_rationales == sorted(unit_rationales)
