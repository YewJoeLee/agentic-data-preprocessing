"""Agentic scientific data preprocessing research prototype."""

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
    "Oc20SampleConsistency",
    "Oc20SampleSchema",
    "Oc20Profile",
    "MappingKeyValidation",
    "MetadataRecordProfile",
    "ShardPair",
    "ShardPairInspection",
    "__version__",
    "discover_oc20",
    "inspect_oc20_shard_pair",
    "profile_oc20_sample",
    "profile_oc20_dataset",
    "profile_oc20_sample_consistency",
    "profile_trusted_metadata_record",
    "validate_oc20_mapping_keys",
]
