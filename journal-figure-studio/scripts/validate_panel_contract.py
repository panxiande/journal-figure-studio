#!/usr/bin/env python3
"""Validate a Journal Figure Studio panel contract JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIGURE_FIELDS = {
    "core_conclusion",
    "journal_profile",
    "figure_intent",
    "mode",
    "export_contract",
}

REQUIRED_EXPORT_FIELDS = {"formats", "shape", "width_mm", "height_mm", "dpi", "font", "editable_text"}

REQUIRED_PANEL_FIELDS = {
    "id",
    "role",
    "archetype",
    "key_message",
    "data_source",
    "required_annotations",
    "statistical_notes",
    "integrity_notes",
    "journal_overrides",
    "risk",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_type(errors: list[str], value: Any, expected: type, name: str) -> None:
    if not isinstance(value, expected):
        errors.append(f"{name} must be {expected.__name__}")


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    figure = contract.get("figure")
    panels = contract.get("panels")

    require_type(errors, figure, dict, "figure")
    require_type(errors, panels, list, "panels")
    if not isinstance(figure, dict) or not isinstance(panels, list):
        return errors

    missing_figure = sorted(REQUIRED_FIGURE_FIELDS - set(figure))
    if missing_figure:
        errors.append(f"figure missing required fields: {', '.join(missing_figure)}")

    export = figure.get("export_contract")
    require_type(errors, export, dict, "figure.export_contract")
    if isinstance(export, dict):
        missing_export = sorted(REQUIRED_EXPORT_FIELDS - set(export))
        if missing_export:
            errors.append(f"figure.export_contract missing required fields: {', '.join(missing_export)}")
        if "formats" in export and not isinstance(export["formats"], list):
            errors.append("figure.export_contract.formats must be list")
        if "shape" in export and export["shape"] not in {"auto", "tall", "wide", "square"}:
            errors.append("figure.export_contract.shape must be one of: auto, tall, wide, square")
        for number_field in ["width_mm", "height_mm", "dpi"]:
            if number_field in export and not isinstance(export[number_field], (int, float)):
                errors.append(f"figure.export_contract.{number_field} must be number")

    if not panels:
        errors.append("panels must contain at least one panel")

    seen_ids: set[str] = set()
    for index, panel in enumerate(panels):
        name = f"panels[{index}]"
        if not isinstance(panel, dict):
            errors.append(f"{name} must be object")
            continue
        missing_panel = sorted(REQUIRED_PANEL_FIELDS - set(panel))
        if missing_panel:
            errors.append(f"{name} missing required fields: {', '.join(missing_panel)}")
        panel_id = panel.get("id")
        if not isinstance(panel_id, str) or not panel_id:
            errors.append(f"{name}.id must be non-empty string")
        elif panel_id in seen_ids:
            errors.append(f"duplicate panel id: {panel_id}")
        else:
            seen_ids.add(panel_id)
        for list_field in [
            "required_annotations",
            "statistical_notes",
            "integrity_notes",
            "journal_overrides",
            "risk",
        ]:
            if list_field in panel and not isinstance(panel[list_field], list):
                errors.append(f"{name}.{list_field} must be list")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()

    errors = validate_contract(load_json(args.contract))
    if errors:
        print(f"INVALID: {args.contract}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {args.contract}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
