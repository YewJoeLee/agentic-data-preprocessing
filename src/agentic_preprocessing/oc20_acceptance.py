"""Read-only acceptance evidence for the deterministic OC20 profiler."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from .oc20_consistency import Oc20SampleConsistency, profile_oc20_sample_consistency
from .oc20_profile import Oc20Profile, profile_oc20_dataset


@dataclass(frozen=True)
class Oc20AcceptanceEvaluation:
    """Serializable aggregate evidence from a fixed OC20 profiler run."""

    profile: Oc20Profile
    sample_consistency: Oc20SampleConsistency | None
    consistency_indices: tuple[int, ...]
    pickle_loading_authorised: bool

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-native acceptance evidence."""

        return {
            "profile": self.profile.to_dict(),
            "sample_consistency": (
                None
                if self.sample_consistency is None
                else self.sample_consistency.to_dict()
            ),
            "consistency_indices": list(self.consistency_indices),
            "pickle_loading_authorised": self.pickle_loading_authorised,
        }


def evaluate_oc20_acceptance(
    dataset_root: str | Path,
    *,
    shard_stem: int | None = 0,
    sample_index: int = 0,
    consistency_indices: Iterable[int] = (0, 1, 2),
    allow_pickle_load: bool = False,
) -> Oc20AcceptanceEvaluation:
    """Collect profile and fixed-sample evidence without modifying OC20 data."""

    indices = tuple(consistency_indices)
    if (
        not indices
        or any(index < 0 for index in indices)
        or len(set(indices)) != len(indices)
    ):
        raise ValueError(
            "consistency_indices must be unique, non-negative, and non-empty"
        )
    root = Path(dataset_root)
    profile = profile_oc20_dataset(
        root,
        shard_stem=shard_stem,
        sample_index=sample_index,
        allow_pickle_load=allow_pickle_load,
    )
    pair = next(
        (
            item
            for item in profile.discovery.shard_pairs
            if item.numeric_stem == profile.selected_numeric_stem and item.is_valid_pair
        ),
        None,
    )
    consistency = None
    if pair is not None:
        consistency = profile_oc20_sample_consistency(
            root / pair.structure_files[0],
            root / pair.sidecar_files[0],
            sample_indices=indices,
        )
    return Oc20AcceptanceEvaluation(
        profile=profile,
        sample_consistency=consistency,
        consistency_indices=indices,
        pickle_loading_authorised=allow_pickle_load,
    )


def format_oc20_acceptance_summary(evaluation: Oc20AcceptanceEvaluation) -> str:
    """Format a deterministic aggregate summary without source-record values."""

    profile = evaluation.profile
    consistency = evaluation.sample_consistency
    issue_codes = {issue.code for issue in profile.issues}
    if consistency is not None:
        issue_codes.update(issue.code for issue in consistency.issues)
    unit_statuses = sorted(
        {item["status"] for item in profile.to_dict()["unit_evidence"]}
    )
    lines = [
        f"Valid shard pairs: {profile.discovery.valid_shard_pair_count}",
        f"Selected numeric stem: {profile.selected_numeric_stem}",
        "Mapping pickle loading: "
        + ("enabled" if evaluation.pickle_loading_authorised else "disabled"),
        "Unit evidence: " + ", ".join(unit_statuses),
        "Issue codes: " + (", ".join(sorted(issue_codes)) if issue_codes else "none"),
    ]
    if consistency is None:
        lines.append("Fixed consistency samples: unavailable")
    else:
        lines.append(
            "Fixed consistency samples: "
            f"structures {consistency.structure_samples_found}/"
            f"{len(evaluation.consistency_indices)}, sidecars "
            f"{consistency.sidecar_samples_found}/"
            f"{len(evaluation.consistency_indices)}"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the acceptance evaluation and write its selected report to stdout."""

    parser = argparse.ArgumentParser(
        description="Run the read-only deterministic OC20 profiler acceptance check."
    )
    parser.add_argument("--dataset-root", required=True, type=Path)
    parser.add_argument("--shard-stem", default=0, type=int)
    parser.add_argument("--sample-index", default=0, type=int)
    parser.add_argument("--consistency-indices", default=(0, 1, 2), nargs="+", type=int)
    parser.add_argument("--allow-pickle-load", action="store_true")
    parser.add_argument("--format", choices=("json", "summary"), default="summary")
    arguments = parser.parse_args(argv)
    if not arguments.dataset_root.is_dir():
        parser.error(f"OC20 dataset root is not a directory: {arguments.dataset_root}")

    try:
        evaluation = evaluate_oc20_acceptance(
            arguments.dataset_root,
            shard_stem=arguments.shard_stem,
            sample_index=arguments.sample_index,
            consistency_indices=arguments.consistency_indices,
            allow_pickle_load=arguments.allow_pickle_load,
        )
    except ValueError as error:
        parser.error(str(error))
    if arguments.format == "json":
        print(json.dumps(evaluation.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_oc20_acceptance_summary(evaluation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
