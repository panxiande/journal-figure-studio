#!/usr/bin/env python3
"""Inspect a raster figure and print common publication QA signals."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--width-mm", type=float, default=183.0)
    args = parser.parse_args()

    with Image.open(args.image) as im:
        width_px, height_px = im.size
        mode = im.mode
        has_alpha = mode in {"RGBA", "LA"} or "transparency" in im.info
        dpi = im.info.get("dpi")

    effective_dpi = width_px / (args.width_mm / 25.4)
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
    print(f"effective_dpi_at_{args.width_mm:g}mm: {effective_dpi:.1f}")
    print("warnings:")
    for warning in warnings or ["none"]:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
