#!/usr/bin/env python3
"""Report raster image size and effective dpi at a requested print width."""

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
    parser.add_argument("--target-dpi", type=float, default=300.0)
    args = parser.parse_args()
    config_path = args.config or args.image.with_name("plot_config.json")
    width_mm = args.width_mm or load_width_from_config(config_path) or 89.0

    with Image.open(args.image) as im:
        width_px, height_px = im.size
        mode = im.mode
        embedded_dpi = im.info.get("dpi")

    width_in = width_mm / 25.4
    effective_dpi = width_px / width_in
    print(f"file: {args.image}")
    print(f"pixels: {width_px} x {height_px}")
    print(f"mode: {mode}")
    print(f"embedded_dpi: {embedded_dpi}")
    print(f"print_width_mm: {width_mm:.2f}")
    print(f"effective_dpi_at_width: {effective_dpi:.1f}")
    print(f"target_dpi: {args.target_dpi:.1f}")
    print(f"passes_target: {effective_dpi >= args.target_dpi}")


if __name__ == "__main__":
    main()
