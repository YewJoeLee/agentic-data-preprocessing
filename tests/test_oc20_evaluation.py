"""Regression evidence for the deterministic OC20 profiler baseline."""

from __future__ import annotations

import json
import lzma
from pathlib import Path

from agentic_preprocessing.oc20_profile import profile_oc20_dataset


def write_xz(path: Path, content: str) -> None:
    with lzma.open(path, mode="wt", encoding="utf-8") as stream:
        stream.write(content)


def test_profile_is_reproducible_for_the_same_synthetic_input(tmp_path: Path) -> None:
    write_xz(
        tmp_path / "0.extxyz.xz",
        "0\nProperties=species:S:1 energy=-1.0\n",
    )
    write_xz(tmp_path / "0.txt.xz", "random1,frame2,-1.0\n")

    first = profile_oc20_dataset(tmp_path).to_dict()
    second = profile_oc20_dataset(tmp_path).to_dict()

    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
