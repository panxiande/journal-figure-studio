#!/usr/bin/env python3
"""Inspect a raster figure and print common publication QA signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def load_width_from_config(path: Path | None) -> float | None:
    if not path or not path.exists():
        return None
    config = json.loads(path.read_text(encoding="utf-8"))
    width = config.get("width_mm")
    return float(width) if width else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--width-mm", type=float)
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()
    config_path = args.config or args.image.with_name("plot_config.json")
    width_mm = args.width_mm or load_width_from_config(config_path) or 89.0

    with Image.open(args.image) as im:
        width_px, height_px = im.size
        mode = im.mode
        has_alpha = mode in {"RGBA", "LA"} or "transparency" in im.info
        dpi = im.info.get("dpi")

    effective_dpi = width_px / (width_mm / 25.4)
    warnings = []
    if effective_dpi < 300:
        warnings.append("effective dpi below 300 at requested width")
    if has_alpha:
        warnings.append("alpha channel may be rejected by some submission systems")
    if mode not in {"RGB", "L", "RGBA"}:
        warnings.append(f"unusual color mode: {mode}")

    print(f"file: {args.image}")
    print(f"pixels: {width_px} x {height_px}")
    print(f"mode: {mode}")
    print(f"embedded_dpi: {dpi}")
    print(f"effective_dpi_at_{width_mm:g}mm: {effective_dpi:.1f}")
    print("warnings:")
    for warning in warnings or ["none"]:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
