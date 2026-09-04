# OC20 200K data understanding

## Purpose and scope

This note records the first manual inspection of the local **OC20 S2EF 200K
training subset**. It is the evidence base for the initial deterministic
profiler; it is not a claim of support for all OC20 formats or tasks.

The raw source remains under `data/raw/` and must not be modified or committed.
The inspected inputs are:

```text
data/raw/
  s2ef_train_200K/
    README_s2ef_train_200K.md
    s2ef_train_200K/
      0.extxyz.xz ... 39.extxyz.xz
      0.txt.xz    ... 39.txt.xz
  oc20_data_mapping.pkl
  mapping_adslab_slab.pkl
```

## File inventory and relationships

| Artefact | Role | Confirmed relationship |
| --- | --- | --- |
| `N.extxyz.xz` | Compressed extended-XYZ structures | Each file contains 5,000 atomistic structures. |
| `N.txt.xz` | Compressed sidecar metadata | Line *i* describes structure *i* in `N.extxyz.xz`. |
| `oc20_data_mapping.pkl` | System-level scientific metadata | Keyed by OC20 adsorbate--catalyst `system_id`. |
| `mapping_adslab_slab.pkl` | Adsorbate--catalyst to clean-slab relationship | Maps a `system_id` to its corresponding clean-slab system ID. |

There are 40 numbered pairs, yielding 200,000 S2EF frames. The sidecar row
format is:

```text
system_id,frame_number,reference_energy
```

`frame_number` is an index in the source relaxation trajectory. It does **not**
mean neighbouring records within an `.extxyz.xz` shard are consecutive frames
of the same system: the supplied README states that its 5,000 structures are
from different adsorbate--catalyst systems.

## Exact raw-file structures

The following describes the local raw files as inspected on 2026-09-05. It
describes their on-disk structure and loaded Python types; it does not imply
that every value has been scientifically validated.

### Root-level local files

| Path | On-disk format | Loaded or textual structure |
| --- | --- | --- |
| `data/raw/.gitkeep` | Empty Git placeholder | Not scientific data. |
| `data/raw/.DS_Store` and nested `.DS_Store` files | macOS Finder metadata | Not scientific data; ignore during discovery. |
| `data/raw/s2ef_train_200K/README_s2ef_train_200K.md` | Markdown text | Dataset-supplied description of the 200K S2EF subset and its paired-shard contract. |
| `data/raw/oc20_data_mapping.pkl` | Python pickle binary | `dict[str, MetadataRecord]`, with 1,281,041 entries. Requires NumPy while unpickling. |
| `data/raw/mapping_adslab_slab.pkl` | Python pickle binary | `dict[str, str]`, with 964,277 entries mapping an adsorbate--catalyst system ID to a clean-slab system ID. |

### `N.extxyz.xz` structure shards

The directory `s2ef_train_200K/s2ef_train_200K/` contains exactly 40 LZMA-
compressed extended-XYZ text files named `0.extxyz.xz` through
`39.extxyz.xz`. Each compressed file contains 5,000 concatenated structure
records, for 200,000 records in total.

One uncompressed extended-XYZ record is exactly:

```text
<atom_count>\n
Lattice="<9 real values>" Properties=species:S:1:pos:R:3:move_mask:L:1:tags:I:1:forces:R:3 energy=<real> free_energy=<real> pbc="<logical> <logical> <logical>"\n
<species> <x> <y> <z> <move_mask> <tag> <fx> <fy> <fz>\n
... exactly <atom_count> atom rows ...
```

To inspect a selected raw record directly from a compressed shard without
creating an extracted copy, run:

```bash
uv run python -c 'import lzma; from pathlib import Path; p=Path("data/raw/s2ef_train_200K/s2ef_train_200K/0.extxyz.xz"); f=lzma.open(p,"rt"); n=int(next(f)); print(n); print(next(f), end=""); [print(next(f), end="") for _ in range(n)]'
```

The header's `Properties` declaration defines the nine atom-row columns:

| Column | Extended-XYZ declaration | Raw representation | Shape per record |
| --- | --- | --- | --- |
| `species` | `S:1` | Element symbol string, for example `Ca` or `O` | `atom_count` strings |
| `pos` | `R:3` | Three real-valued Cartesian coordinates | `atom_count × 3` |
| `move_mask` | `L:1` | `T` or `F` logical flag | `atom_count` booleans |
| `tags` | `I:1` | Integer tag | `atom_count` integers |
| `forces` | `R:3` | Three real-valued force components | `atom_count × 3` |

Structure-level header fields are:

| Field | Raw representation | Shape |
| --- | --- | --- |
| `Lattice` | Nine space-separated real values inside a quoted string | 3 × 3 cell matrix when parsed |
| `Properties` | Extended-XYZ property declaration | Fixed schema above in this subset |
| `energy` | Real scalar | One value per structure |
| `free_energy` | Real scalar | One value per structure |
| `pbc` | Three `T`/`F` values inside a quoted string | Three periodic-boundary flags |

The file itself does not encode units alongside these values. Unit conventions
must therefore be sourced from OC20 documentation and reported separately from
the raw field types.

### `N.txt.xz` sidecar shards

There are exactly 40 LZMA-compressed sidecar text files named `0.txt.xz`
through `39.txt.xz`. Each contains 5,000 headerless CSV rows, one for each
structure in the same-numbered extended-XYZ shard:

```text
system_id,frame_number,reference_energy
```

The exact row schema is:

| Position | Field | Raw type and pattern | Example |
| --- | --- | --- | --- |
| 1 | `system_id` | String identifier, observed as `random<integer>` | `random<integer>` |
| 2 | `frame_number` | String identifier, observed as `frame<integer>` | `frame<integer>` |
| 3 | `reference_energy` | Decimal-parsable real number | `<real>` |

The sidecar has no header row. Row *i* in `N.txt.xz` belongs to record *i* in
`N.extxyz.xz`, and the README guarantees equal row and structure counts. The
`frame_number` refers to the system's source relaxation trajectory; adjacent
records in a shard are different adsorbate--catalyst systems.

The profiler must preserve the distinction between a structure's header
`energy` and its sidecar `reference_energy`; neither may be silently
substituted for the other.

### `oc20_data_mapping.pkl` metadata dictionary

After loading verified source data with NumPy available, this file is a Python
dictionary with the following fixed schema:

```text
dict[str, MetadataRecord]

MetadataRecord = {
  "ads_id": int,
  "ads_symbols": str,
  "adsorption_site": tuple[tuple[numpy.float64, numpy.float64, numpy.float64], ...],
  "anomaly": int,
  "bulk_id": int,
  "bulk_mpid": str,
  "bulk_symbols": str,
  "class": int,
  "miller_index": tuple[int, int, int],
  "shift": float,
  "split": str,
  "top": bool,
}
```

All 1,281,041 loaded metadata records contain the 12 fields above. The keys
are system IDs in the `random<integer>` form. Observed domains and shapes are:

| Field | Exact loaded type/shape | Observed domain or cardinality |
| --- | --- | --- |
| `ads_id`, `bulk_id`, `anomaly`, `class` | `int` | `anomaly`: 0--4; `class`: 0--3 |
| `ads_symbols`, `bulk_mpid`, `bulk_symbols`, `split` | `str` | `split`: `train`, `val_is`, `val_oos_ads`, `val_oos_bulk`, `val_oos_ads_bulk`, `test_is`, `test_oos_ads`, `test_oos_bulk`, `test_oos_ads_bulk` |
| `miller_index` | `tuple[int, int, int]` | Always three integers |
| `shift` | `float` | Scalar |
| `top` | `bool` | Scalar |
| `adsorption_site` | Tuple of one or two coordinate triples containing `numpy.float64` values | 1 coordinate triple in 1,160,858 records; 2 coordinate triples in 120,183 records |

### `mapping_adslab_slab.pkl` relationship dictionary

After loading verified source data, this file is:

```text
dict[str, str]
```

Each key is an adsorbate--catalyst system ID; its value is the linked clean-slab
system ID. All 964,277 relationship keys are present in
`oc20_data_mapping.pkl`. The metadata mapping has an additional 316,764 keys
without a clean-slab relationship entry, so a missing relationship must be
represented as missing evidence, not fabricated.

## Manual-inspection finding

The notebook dynamically joins a selected structure record, its same-position
sidecar row, its metadata, and—when available—its clean-slab relationship. No
source-record values are stored in this documentation. This inspection confirms
that structure-header `energy` and sidecar `reference_energy` are distinct
fields and must not be silently substituted for one another.

Anomaly codes are dataset warning flags. The profiler should retain the raw
code and report a documented label only with the relevant source and version.

## Viewing the data

The raw inputs are compressed or binary. Use copies in `/private/tmp` for
interactive viewing; do not decompress into `data/raw/`.

The reproducible visual reconnaissance companion is
`notebooks/01_oc20_reconnaissance.ipynb`. Run it with the installed JupyterLab
environment; it is also compatible with a separately installed classic Jupyter
Notebook interface. The notebook streams one record from a compressed shard and
renders a static atomistic figure without writing derived data.

### README and sidecar metadata

```bash
open data/raw/s2ef_train_200K/README_s2ef_train_200K.md
xz -dc data/raw/s2ef_train_200K/s2ef_train_200K/0.txt.xz | sed -n '1,20p'
```

To open a text copy in an editor:

```bash
xz -dc data/raw/s2ef_train_200K/s2ef_train_200K/0.txt.xz > /private/tmp/oc20-0.txt
```

### Three-dimensional structures

ASE GUI provides an interactive atomistic view. The local environment needs a
Python build with Tk support; the current exploration environment uses
Homebrew Python 3.12.14 with Tk 9.0.4.

```bash
xz -dc data/raw/s2ef_train_200K/s2ef_train_200K/0.extxyz.xz > /private/tmp/oc20-0.extxyz
uv run --with ase ase gui /private/tmp/oc20-0.extxyz@0
```

`@0` opens only the first structure. The dashed box is the periodic simulation
cell; crossed atoms represent constrained atoms from the movement-mask field.
Use `@0:10` only to inspect several independent structures, not as a physical
relaxation movie.

### Mapping dictionaries

Pickle files are binary and must not be opened as text. Before loading them,
verify their provenance and checksum against the official OC20 release. Python
pickle may execute code during loading, so only load verified files from the
trusted source.

```bash
uv run python
```

```python
from pathlib import Path
import pickle
from pprint import pprint

system_id = "<system_id from a paired .txt.xz row>"

with Path("data/raw/oc20_data_mapping.pkl").open("rb") as file:
    metadata = pickle.load(file)

with Path("data/raw/mapping_adslab_slab.pkl").open("rb") as file:
    relationships = pickle.load(file)

pprint(metadata[system_id])
print(relationships[system_id])
```

The metadata pickle contains NumPy values, so NumPy is a required project
dependency for this supported OC20 input.

## Initial profiler contract

The first implementation slice must:

1. Discover and classify the OC20 README, compressed extended-XYZ shards,
   compressed sidecar shards, and mappings.
2. Pair `N.extxyz.xz` with `N.txt.xz` by exact numeric stem and report missing
   or duplicate counterparts.
3. Inspect a deterministic, documented sample without modifying raw input.
4. Verify that each sampled structure has one sidecar row and emit the joined
   `system_id`, `frame_number`, and `reference_energy` as separate evidence.
5. Extract the extended-XYZ schema, atom count, cell and periodicity, energy
   fields, atom-property fields, and constraints.
6. Join known `system_id` values to mapping metadata and clean-slab
   relationships, recording missing keys and anomaly flags as warnings.
7. Produce a serialisable profile that distinguishes observations, documented
   semantics, and unresolved uncertainty.

## Current limitations and follow-up

- This inspection covers the S2EF 200K training subset only; it does not yet
  establish support for validation/OOD splits, LMDB, IS2RE/IS2RS, or OC20Dense.
- Mapping checksums should be captured in an experiment record before automated
  loading is claimed as reproducible.
- No reviewed fixture or golden profile exists yet.
- ASE was used only as an ephemeral viewing tool, not added as a project
  dependency. NumPy is the only added runtime dependency.

The immediate next coding task is discovery and numeric shard-pair validation,
with tests using small reviewed synthetic fixtures.
