#!/usr/bin/env python3
"""Create a starter QA report from a panel contract and optional plot config."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from PIL import Image


def load_json(path: Path | None) -> dict:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile_rules() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "assets" / "templates" / "profile_rules.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_svg_text(svg: Path) -> str:
    if not svg.exists():
        return "missing"
    root = ET.parse(svg).getroot()
    text_nodes = sum(1 for node in root.iter() if node.tag.endswith("text"))
    return f"{text_nodes} text node(s); editable text likely: {text_nodes > 0}"


def inspect_raster(path: Path, width_mm: float, target_dpi: float) -> str:
    if not path.exists():
        return "missing"
    with Image.open(path) as im:
        width_px, height_px = im.size
        mode = im.mode
        embedded_dpi = im.info.get("dpi")
    effective_dpi = width_px / (width_mm / 25.4)
    status = "PASS" if effective_dpi >= target_dpi else "RISK"
    return (
        f"{status}: {width_px} x {height_px}px, mode {mode}, embedded dpi {embedded_dpi}, "
        f"effective dpi {effective_dpi:.1f} at {width_mm:g} mm"
    )


def profile_checks(profile_name: str, export: dict[str, Any], config: dict[str, Any]) -> list[str]:
    rules = load_profile_rules().get(profile_name, {})
    width_mm = float(export.get("width_mm") or config.get("width_mm") or 0)
    height_mm = float(export.get("height_mm") or config.get("height_mm") or 0)
    dpi = float(export.get("dpi") or config.get("dpi") or 0)
    checks: list[str] = []

    max_height = rules.get("max_height_mm")
    if max_height:
        checks.append(f"- Height <= {max_height} mm: {'PASS' if height_mm <= max_height else 'RISK'} ({height_mm:g} mm)")
    min_dpi = rules.get("min_dpi")
    if min_dpi:
        checks.append(f"- DPI target >= {min_dpi}: {'PASS' if dpi >= min_dpi else 'RISK'} ({dpi:g})")

    formats = set(export.get("formats") or config.get("formats") or [])
    preferred = set(rules.get("preferred_formats") or [])
    if preferred:
        overlap = sorted(formats & preferred)
        checks.append(f"- Profile-preferred format present: {'PASS' if overlap else 'RISK'} ({', '.join(overlap) or 'none'})")

    actual_font = config.get("actual_font")
    candidates = set(rules.get("font_candidates") or [])
    if actual_font and candidates:
        checks.append(f"- Resolved font in profile candidates: {'PASS' if actual_font in candidates else 'CHECK'} ({actual_font})")
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--bundle-dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figure_qa.md"))
    args = parser.parse_args()

    contract = load_json(args.contract)
    config = load_json(args.config)
    figure = contract.get("figure", {})
    panels = contract.get("panels", [])
    export = figure.get("export_contract", {})
    bundle_dir = args.bundle_dir
    if bundle_dir is None:
        bundle_dir = args.output.parent
    width_mm = float(export.get("width_mm") or config.get("width_mm") or 183)
    dpi = float(export.get("dpi") or config.get("dpi") or 300)
    profile_name = figure.get("journal_profile", "unknown")

    lines = [
        "# Figure QA Report",
        "",
        f"- Journal profile: {figure.get('journal_profile', 'unknown')}",
        f"- Mode: {figure.get('mode', 'unknown')}",
        f"- Intent: {figure.get('figure_intent', 'unknown')}",
        f"- Width: {export.get('width_mm', 'unknown')} mm",
        f"- Height: {export.get('height_mm', config.get('height_mm', 'unknown'))} mm",
        f"- Shape: {export.get('shape', config.get('shape', 'unknown'))}",
        f"- DPI target: {export.get('dpi', 'unknown')}",
        f"- Font: {export.get('font', 'unknown')}",
        f"- Resolved font: {config.get('actual_font', 'unknown')}",
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
        "## Automated Checks",
        "",
        f"- SVG editable text: {check_svg_text(bundle_dir / 'figure.svg')}",
        f"- Preview raster: {inspect_raster(bundle_dir / 'figure_preview.png', width_mm, dpi)}",
        f"- PNG raster: {inspect_raster(bundle_dir / 'figure.png', width_mm, dpi)}",
        f"- TIFF raster: {inspect_raster(bundle_dir / 'figure.tiff', width_mm, dpi)}",
        f"- Source data file: {'present' if (bundle_dir / 'figure_source_data.csv').exists() else 'missing'}",
        f"- Plot config file: {'present' if (bundle_dir / 'plot_config.json').exists() else 'missing'}",
        f"- Panel contract file: {'present' if args.contract.exists() else 'missing'}",
        "",
        "## Profile Rule Checks",
        "",
        *profile_checks(profile_name, export, config),
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
