#!/usr/bin/env python3
"""Generate a starter panel contract JSON for Journal Figure Studio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from figure_layout import SHAPES, resolve_size


def panel_id(index: int) -> str:
    letters = "abcdefghijklmnopqrstuvwxyz"
    if index < len(letters):
        return letters[index]
    return f"p{index + 1}"


def build_contract(args: argparse.Namespace) -> dict:
    size = resolve_size(args.shape, args.journal, args.panels, args.archetype, args.width_mm, args.height_mm)
    panels = []
    for i in range(args.panels):
        archetype = args.archetype[min(i, len(args.archetype) - 1)]
        panels.append(
            {
                "id": panel_id(i),
                "role": args.intent,
                "archetype": archetype,
                "key_message": "",
                "data_source": "",
                "required_annotations": [],
                "statistical_notes": [],
                "integrity_notes": [],
                "journal_overrides": [],
                "risk": [],
            }
        )

    return {
        "figure": {
            "core_conclusion": args.core_conclusion,
            "journal_profile": args.journal,
            "figure_intent": args.intent,
            "mode": args.mode,
            "export_contract": {
                "formats": args.formats,
                "shape": size.shape,
                "width_mm": size.width_mm,
                "height_mm": size.height_mm,
                "dpi": args.dpi,
                "font": args.font,
                "editable_text": True,
                "source_data": "requested",
            },
            "risk_register": [],
        },
        "panels": panels,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--journal", default="general-publication")
    parser.add_argument("--intent", default="discovery")
    parser.add_argument("--mode", choices=["draft", "revision", "submission"], default="draft")
    parser.add_argument("--core-conclusion", default="")
    parser.add_argument("--panels", type=int, default=1)
    parser.add_argument("--archetype", action="append", default=["quantitative-comparison"])
    parser.add_argument("--formats", nargs="+", default=["svg", "pdf", "png"])
    parser.add_argument("--shape", choices=SHAPES, default="auto")
    parser.add_argument("--width-mm", type=float)
    parser.add_argument("--height-mm", type=float)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--font", default="Arial")
    parser.add_argument("--output", type=Path, default=Path("panel_contract.json"))
    args = parser.parse_args()

    contract = build_contract(args)
    args.output.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
