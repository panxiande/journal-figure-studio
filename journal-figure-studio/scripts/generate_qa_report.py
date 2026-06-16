#!/usr/bin/env python3
"""Create a starter QA report from a panel contract and optional plot config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path | None) -> dict:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figure_qa.md"))
    args = parser.parse_args()

    contract = load_json(args.contract)
    config = load_json(args.config)
    figure = contract.get("figure", {})
    panels = contract.get("panels", [])
    export = figure.get("export_contract", {})

    lines = [
        "# Figure QA Report",
        "",
        f"- Journal profile: {figure.get('journal_profile', 'unknown')}",
        f"- Mode: {figure.get('mode', 'unknown')}",
        f"- Intent: {figure.get('figure_intent', 'unknown')}",
        f"- Width: {export.get('width_mm', 'unknown')} mm",
        f"- DPI target: {export.get('dpi', 'unknown')}",
        f"- Font: {export.get('font', 'unknown')}",
        f"- Formats: {', '.join(export.get('formats', [])) or 'unknown'}",
        "",
        "## Core Conclusion",
        "",
        figure.get("core_conclusion") or "Unspecified.",
        "",
        "## Baseline Checks",
        "",
        "- [ ] Final dimensions match profile.",
        "- [ ] Text is readable and does not overlap.",
        "- [ ] SVG/PDF text remains editable unless target profile requires otherwise.",
        "- [ ] Raster elements meet dpi expectations at final size.",
        "- [ ] Color encoding is accessible and not red/green-only.",
        "- [ ] Statistics include n, repeat type, error definition, test, correction, and comparison.",
        "- [ ] Source data paths are recorded.",
        "- [ ] Image panels have scale bars, crop notes, and processing notes.",
        "- [ ] Captions and long methods are outside the figure file.",
        "",
        "## Panel Checks",
        "",
    ]

    for panel in panels:
        lines.extend(
            [
                f"### Panel {panel.get('id', '?')}",
                "",
                f"- Role: {panel.get('role', '')}",
                f"- Archetype: {panel.get('archetype', '')}",
                f"- Key message: {panel.get('key_message', '') or 'Unspecified'}",
                f"- Data source: {panel.get('data_source', '') or 'Unspecified'}",
                f"- Risks: {', '.join(panel.get('risk', [])) or 'None recorded'}",
                "",
            ]
        )

    if config:
        lines.extend(["## Config Snapshot", "", "```json", json.dumps(config, indent=2), "```", ""])

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
