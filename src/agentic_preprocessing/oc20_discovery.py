"""Read-only discovery and shard-pair validation for a local OC20 subset."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_STRUCTURE_SHARD_RE = re.compile(r"^(?P<stem>\d+)\.extxyz\.xz$")
_SIDECAR_SHARD_RE = re.compile(r"^(?P<stem>\d+)\.txt\.xz$")
_METADATA_MAPPING_NAME = "oc20_data_mapping.pkl"
_CLEAN_SLAB_MAPPING_NAME = "mapping_adslab_slab.pkl"


@dataclass(frozen=True)
class ShardPair:
    """Files discovered for one numeric OC20 shard stem.

    The individual file lists are retained so an ambiguous stem is reported as
    evidence instead of silently selecting one file.
    """

    numeric_stem: int
    structure_files: tuple[str, ...]
    sidecar_files: tuple[str, ...]

    @property
    def missing_counterparts(self) -> tuple[str, ...]:
        """Counterpart kinds absent for this numeric stem."""

        missing: list[str] = []
        if not self.structure_files:
            missing.append("structure")
        if not self.sidecar_files:
            missing.append("sidecar")
        return tuple(missing)

    @property
    def duplicate_counterparts(self) -> tuple[str, ...]:
        """Counterpart kinds that have more than one file for this stem."""

        duplicates: list[str] = []
        if len(self.structure_files) > 1:
            duplicates.append("structure")
        if len(self.sidecar_files) > 1:
            duplicates.append("sidecar")
        return tuple(duplicates)

    @property
    def is_valid_pair(self) -> bool:
        """Whether exactly one structure and sidecar file were found."""

        return not self.missing_counterparts and not self.duplicate_counterparts

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable record of the pairing result."""

        return {
            "numeric_stem": self.numeric_stem,
            "structure_files": list(self.structure_files),
            "sidecar_files": list(self.sidecar_files),
            "missing_counterparts": list(self.missing_counterparts),
            "duplicate_counterparts": list(self.duplicate_counterparts),
            "is_valid_pair": self.is_valid_pair,
        }


@dataclass(frozen=True)
class Oc20Discovery:
    """JSON-serialisable inventory from a read-only OC20 filesystem scan."""

    root: str
    readme_files: tuple[str, ...]
    structure_shards: tuple[str, ...]
    sidecar_shards: tuple[str, ...]
    metadata_mapping_files: tuple[str, ...]
    clean_slab_mapping_files: tuple[str, ...]
    shard_pairs: tuple[ShardPair, ...]

    @property
    def valid_shard_pair_count(self) -> int:
        """Number of stems with exactly one structure and sidecar file."""

        return sum(pair.is_valid_pair for pair in self.shard_pairs)

    def to_dict(self) -> dict[str, Any]:
        """Return the complete discovery result using JSON-native values."""

        return {
            "root": self.root,
            "readme_files": list(self.readme_files),
            "structure_shards": list(self.structure_shards),
            "sidecar_shards": list(self.sidecar_shards),
            "mapping_pickles": {
                "oc20_data_mapping": list(self.metadata_mapping_files),
                "mapping_adslab_slab": list(self.clean_slab_mapping_files),
            },
            "shard_pairs": [pair.to_dict() for pair in self.shard_pairs],
            "valid_shard_pair_count": self.valid_shard_pair_count,
        }


def discover_oc20(dataset_root: str | Path) -> Oc20Discovery:
    """Discover supported OC20 files and validate numeric shard counterparts.

    The function only lists file paths. It neither decompresses shards nor
    loads mapping pickles, keeping source data immutable and safe to inspect.
    Returned paths are relative to ``dataset_root`` for reproducible output.
    """

    root = Path(dataset_root)
    if not root.is_dir():
        raise ValueError(f"OC20 dataset root is not a directory: {root}")

    readmes: list[Path] = []
    structures_by_stem: dict[int, list[Path]] = {}
    sidecars_by_stem: dict[int, list[Path]] = {}
    metadata_mappings: list[Path] = []
    clean_slab_mappings: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        name = path.name
        if name.casefold().startswith("readme") and path.suffix.casefold() == ".md":
            readmes.append(path)
        if name == _METADATA_MAPPING_NAME:
            metadata_mappings.append(path)
        elif name == _CLEAN_SLAB_MAPPING_NAME:
            clean_slab_mappings.append(path)

        structure_match = _STRUCTURE_SHARD_RE.fullmatch(name)
        if structure_match:
            structures_by_stem.setdefault(int(structure_match["stem"]), []).append(path)
            continue

        sidecar_match = _SIDECAR_SHARD_RE.fullmatch(name)
        if sidecar_match:
            sidecars_by_stem.setdefault(int(sidecar_match["stem"]), []).append(path)

    def relative_paths(paths: list[Path]) -> tuple[str, ...]:
        return tuple(sorted(path.relative_to(root).as_posix() for path in paths))

    all_stems = sorted(structures_by_stem.keys() | sidecars_by_stem.keys())
    shard_pairs = tuple(
        ShardPair(
            numeric_stem=stem,
            structure_files=relative_paths(structures_by_stem.get(stem, [])),
            sidecar_files=relative_paths(sidecars_by_stem.get(stem, [])),
        )
        for stem in all_stems
    )

    return Oc20Discovery(
        root=str(root),
        readme_files=relative_paths(readmes),
        structure_shards=relative_paths(
            [path for paths in structures_by_stem.values() for path in paths]
        ),
        sidecar_shards=relative_paths(
            [path for paths in sidecars_by_stem.values() for path in paths]
        ),
        metadata_mapping_files=relative_paths(metadata_mappings),
        clean_slab_mapping_files=relative_paths(clean_slab_mappings),
        shard_pairs=shard_pairs,
    )
