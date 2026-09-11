"""Deterministic, non-executing readiness plans from OC20 profile evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .oc20_inspection import InspectionIssue
from .oc20_profile import Oc20Profile

_BLOCKING_PROFILE_ISSUES = frozenset(
    {
        "atom_row_property_count_mismatch",
        "invalid_atom_count",
        "invalid_properties_declaration",
        "invalid_property_component_count",
        "invalid_sidecar_field_count",
        "mapping_load_error",
        "missing_system_id",
        "negative_atom_count",
        "missing_properties_declaration",
        "missing_sidecar_sample",
        "missing_structure_header",
        "missing_structure_sample",
        "requested_shard_is_invalid",
        "row_count_mismatch",
        "sidecar_read_error",
        "structure_read_error",
        "truncated_structure_record",
    }
)


@dataclass(frozen=True)
class DownstreamGoal:
    """A caller-supplied downstream goal retained without interpretation."""

    text: str

    def to_dict(self) -> dict[str, str]:
        """Return JSON-native goal evidence."""

        return {"text": self.text}


@dataclass(frozen=True)
class PlanEvidence:
    """One aggregate observation cited by a readiness plan."""

    path: str
    observation: str

    def to_dict(self) -> dict[str, str]:
        """Return JSON-native plan evidence."""

        return {"path": self.path, "observation": self.observation}


@dataclass(frozen=True)
class ProposedCheck:
    """A review-only check proposed without executing an operation."""

    code: str
    rationale: str
    requires_review: bool

    def to_dict(self) -> dict[str, str | bool]:
        """Return JSON-native proposed-check evidence."""

        return {
            "code": self.code,
            "rationale": self.rationale,
            "requires_review": self.requires_review,
        }


@dataclass(frozen=True)
class Oc20ReadinessPlan:
    """Serializable non-executing plan grounded in a deterministic profile."""

    goal: DownstreamGoal
    status: Literal["ready_for_review", "blocked"]
    evidence: tuple[PlanEvidence, ...]
    proposed_checks: tuple[ProposedCheck, ...]
    assumptions: tuple[str, ...]
    risks: tuple[str, ...]
    validation_checks: tuple[str, ...]
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native plan evidence without source-record values."""

        return {
            "goal": self.goal.to_dict(),
            "status": self.status,
            "evidence": [item.to_dict() for item in self.evidence],
            "proposed_checks": [item.to_dict() for item in self.proposed_checks],
            "assumptions": list(self.assumptions),
            "risks": list(self.risks),
            "validation_checks": list(self.validation_checks),
            "issues": [issue.to_dict() for issue in self.issues],
        }


def build_oc20_readiness_plan(
    profile: Oc20Profile,
    goal: DownstreamGoal,
) -> Oc20ReadinessPlan:
    """Build a review-only plan from aggregate deterministic profile evidence."""

    if not goal.text.strip():
        raise ValueError("goal text must not be empty")

    profile_issue_codes = tuple(sorted({issue.code for issue in profile.issues}))
    evidence = _profile_evidence(profile)
    blockers = _BLOCKING_PROFILE_ISSUES | {"no_valid_shard_pair"}
    is_blocked = profile.selected_numeric_stem is None or bool(
        blockers.intersection(profile_issue_codes)
    )
    assumptions = (
        "No source data or derived output is modified by this readiness plan.",
    )
    validation_checks = tuple(
        sorted(
            {
                "Re-run the deterministic profiler with the same declared sample policy before any future operation.",
                "Verify explicit group/split and sequence-order constraints before any future operation.",
            }
        )
    )
    if is_blocked:
        issue = InspectionIssue(
            "profile_not_ready_for_planning",
            "The profile has no valid selected shard pair for readiness planning.",
        )
        return Oc20ReadinessPlan(
            goal=goal,
            status="blocked",
            evidence=evidence,
            proposed_checks=(
                ProposedCheck(
                    "resolve_profile_blocker",
                    "Resolve the profiler blocker before planning.",
                    True,
                ),
            ),
            assumptions=assumptions,
            risks=tuple(f"profile_issue:{code}" for code in profile_issue_codes),
            validation_checks=validation_checks,
            issues=(issue,),
        )

    unresolved_fields = _unresolved_unit_fields(profile)
    checks = [
        ProposedCheck(
            "review_profile_evidence",
            "Review aggregate deterministic profile evidence before selecting an operation.",
            False,
        ),
        ProposedCheck(
            "define_output_scope",
            "Define a non-destructive output scope before any future operation.",
            False,
        ),
    ]
    checks.extend(
        ProposedCheck(
            "resolve_unit_evidence",
            f"Record an authoritative unit convention for {field!r}.",
            True,
        )
        for field in unresolved_fields
    )
    risks = sorted(
        {
            *(f"profile_issue:{code}" for code in profile_issue_codes),
            *(f"unresolved_unit:{field}" for field in unresolved_fields),
        }
    )
    return Oc20ReadinessPlan(
        goal=goal,
        status="ready_for_review",
        evidence=evidence,
        proposed_checks=tuple(
            sorted(checks, key=lambda item: (item.code, item.rationale))
        ),
        assumptions=assumptions,
        risks=tuple(risks),
        validation_checks=validation_checks,
        issues=(),
    )


def _profile_evidence(profile: Oc20Profile) -> tuple[PlanEvidence, ...]:
    """Extract aggregate profile facts without retaining source-record values."""

    selected_stem = profile.selected_numeric_stem
    selected_observation = (
        "No numeric shard pair is selected."
        if selected_stem is None
        else f"Selected numeric shard stem: {selected_stem}."
    )
    evidence = (
        PlanEvidence(
            "discovery.valid_shard_pair_count",
            f"Valid numeric shard pairs discovered: {profile.discovery.valid_shard_pair_count}.",
        ),
        PlanEvidence("selected_numeric_stem", selected_observation),
    )
    return tuple(sorted(evidence, key=lambda item: item.path))


def _unresolved_unit_fields(profile: Oc20Profile) -> tuple[str, ...]:
    """Return only named unresolved unit fields from serialised profile evidence."""

    unit_evidence = profile.to_dict()["unit_evidence"]
    return tuple(
        sorted(
            {item["field"] for item in unit_evidence if item["status"] == "unresolved"}
        )
    )
