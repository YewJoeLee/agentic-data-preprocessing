"""Evidence-only schema profiling for an inspected OC20 shard sample."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .oc20_inspection import InspectionIssue, ShardPairInspection

_HEADER_FIELD_RE = re.compile(r'(?P<name>\w+)=(?P<value>"[^"]*"|\S+)')
_PROPERTIES_RE = re.compile(r'(?:^|\s)Properties=(?P<value>"[^"]*"|\S+)')
_PROPERTY_TYPE_NAMES = {
    "S": "string",
    "R": "real",
    "I": "integer",
    "L": "boolean",
}
_SIDECAR_FIELD_NAMES = ("system_id", "frame_number", "reference_energy")


@dataclass(frozen=True)
class FieldProfile:
    """A field's observed lexical type, without coercing its source value."""

    name: str
    location: str
    observed_type: str
    raw_value: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "location": self.location,
            "observed_type": self.observed_type,
            "raw_value": self.raw_value,
        }


@dataclass(frozen=True)
class AtomPropertyProfile:
    """One field declared by the extended-XYZ ``Properties`` descriptor."""

    name: str
    declared_type_code: str
    declared_value_type: str
    components_per_atom: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "declared_type_code": self.declared_type_code,
            "declared_value_type": self.declared_value_type,
            "components_per_atom": self.components_per_atom,
        }


@dataclass(frozen=True)
class Oc20SampleSchema:
    """Serializable schema evidence derived from a bounded shard sample."""

    structure_header_fields: tuple[FieldProfile, ...]
    atom_properties: tuple[AtomPropertyProfile, ...]
    sidecar_fields: tuple[FieldProfile, ...]
    issues: tuple[InspectionIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "structure_header_fields": [
                field.to_dict() for field in self.structure_header_fields
            ],
            "atom_properties": [
                property_.to_dict() for property_ in self.atom_properties
            ],
            "sidecar_fields": [field.to_dict() for field in self.sidecar_fields],
            "issues": [issue.to_dict() for issue in self.issues],
        }


def profile_oc20_sample(inspection: ShardPairInspection) -> Oc20SampleSchema:
    """Profile schema facts already captured by :func:`inspect_oc20_shard_pair`.

    This function performs no additional file I/O. It retains source values as
    strings and infers only lexical data types, so a profile is not a claim
    about scientific units or semantics.
    """

    header_fields: list[FieldProfile] = []
    atom_properties: list[AtomPropertyProfile] = []
    sidecar_fields: list[FieldProfile] = []
    issues: list[InspectionIssue] = []

    if inspection.structure_sample is None:
        issues.append(
            InspectionIssue(
                "missing_structure_sample",
                "The selected structure sample was not available for schema profiling.",
            )
        )
    else:
        header = inspection.structure_sample.header
        header_fields = [
            FieldProfile(
                name=match["name"],
                location="structure_header",
                observed_type=_infer_lexical_type(match["value"]),
                raw_value=match["value"],
            )
            for match in _HEADER_FIELD_RE.finditer(header)
        ]
        atom_properties, property_issues = _profile_atom_properties(header)
        issues.extend(property_issues)

    if inspection.sidecar_sample is None:
        issues.append(
            InspectionIssue(
                "missing_sidecar_sample",
                "The selected sidecar row was not available for schema profiling.",
            )
        )
    else:
        sidecar_fields = [
            FieldProfile(
                name=(
                    _SIDECAR_FIELD_NAMES[position]
                    if position < len(_SIDECAR_FIELD_NAMES)
                    else f"extra_field_{position + 1}"
                ),
                location="sidecar_row",
                observed_type=_infer_lexical_type(value),
                raw_value=value,
            )
            for position, value in enumerate(inspection.sidecar_sample.fields)
        ]

    return Oc20SampleSchema(
        structure_header_fields=tuple(header_fields),
        atom_properties=tuple(atom_properties),
        sidecar_fields=tuple(sidecar_fields),
        issues=tuple(issues),
    )


def _profile_atom_properties(
    header: str,
) -> tuple[list[AtomPropertyProfile], list[InspectionIssue]]:
    match = _PROPERTIES_RE.search(header)
    if match is None:
        return [], [
            InspectionIssue(
                "missing_properties_declaration",
                "The structure header has no Properties declaration.",
            )
        ]

    declaration = match["value"].strip('"')
    components = declaration.split(":")
    if len(components) % 3 != 0 or not declaration:
        return [], [
            InspectionIssue(
                "invalid_properties_declaration",
                "The Properties declaration must contain name:type:components groups.",
            )
        ]

    profiles: list[AtomPropertyProfile] = []
    issues: list[InspectionIssue] = []
    for offset in range(0, len(components), 3):
        name, type_code, raw_component_count = components[offset : offset + 3]
        try:
            component_count = int(raw_component_count)
        except ValueError:
            issues.append(
                InspectionIssue(
                    "invalid_property_component_count",
                    f"Property {name!r} has an invalid component count.",
                )
            )
            continue
        if component_count < 1:
            issues.append(
                InspectionIssue(
                    "invalid_property_component_count",
                    f"Property {name!r} must have at least one component.",
                )
            )
            continue
        profiles.append(
            AtomPropertyProfile(
                name=name,
                declared_type_code=type_code,
                declared_value_type=_PROPERTY_TYPE_NAMES.get(type_code, "unknown"),
                components_per_atom=component_count,
            )
        )

    return profiles, issues


def _infer_lexical_type(raw_value: str) -> str:
    """Infer a lexical type while retaining the exact source string."""

    value = raw_value.strip('"')
    values = value.split()
    if len(values) > 1:
        component_types = {_infer_scalar_type(component) for component in values}
        if len(component_types) == 1:
            return f"{component_types.pop()}_vector"
        return "string"
    return _infer_scalar_type(value)


def _infer_scalar_type(value: str) -> str:
    if value in {"T", "F"}:
        return "boolean"
    try:
        int(value)
    except ValueError:
        try:
            float(value)
        except ValueError:
            return "string"
        return "real"
    return "integer"
