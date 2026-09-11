"""Agentic scientific data preprocessing research prototype."""

from typing import Any

__version__ = "0.1.0"

from .oc20_consistency import Oc20SampleConsistency, profile_oc20_sample_consistency
from .oc20_discovery import Oc20Discovery, ShardPair, discover_oc20
from .oc20_inspection import ShardPairInspection, inspect_oc20_shard_pair
from .oc20_mappings import MappingKeyValidation, validate_oc20_mapping_keys
from .oc20_metadata import MetadataRecordProfile, profile_trusted_metadata_record
from .oc20_profile import Oc20Profile, profile_oc20_dataset
from .oc20_schema import Oc20SampleSchema, profile_oc20_sample

__all__ = [
    "Oc20Discovery",
    "Oc20AcceptanceEvaluation",
    "Oc20SampleConsistency",
    "Oc20SampleSchema",
    "Oc20Profile",
    "MappingKeyValidation",
    "MetadataRecordProfile",
    "ShardPair",
    "ShardPairInspection",
    "__version__",
    "discover_oc20",
    "evaluate_oc20_acceptance",
    "format_oc20_acceptance_summary",
    "inspect_oc20_shard_pair",
    "profile_oc20_sample",
    "profile_oc20_dataset",
    "profile_oc20_sample_consistency",
    "profile_trusted_metadata_record",
    "validate_oc20_mapping_keys",
]

_ACCEPTANCE_EXPORTS = frozenset(
    {
        "Oc20AcceptanceEvaluation",
        "evaluate_oc20_acceptance",
        "format_oc20_acceptance_summary",
    }
)


def __getattr__(name: str) -> Any:
    """Load acceptance helpers lazily for module-command compatibility."""

    if name not in _ACCEPTANCE_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from .oc20_acceptance import (
        Oc20AcceptanceEvaluation,
        evaluate_oc20_acceptance,
        format_oc20_acceptance_summary,
    )

    exports = {
        "Oc20AcceptanceEvaluation": Oc20AcceptanceEvaluation,
        "evaluate_oc20_acceptance": evaluate_oc20_acceptance,
        "format_oc20_acceptance_summary": format_oc20_acceptance_summary,
    }
    globals().update(exports)
    return exports[name]
