#!/usr/bin/env python3
"""Starter Matplotlib exporter for publication figure bundles.

Adapt `draw_figure` to the user's data. This script intentionally creates a
minimal demo when no data are supplied so the export path can be smoke-tested.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from PIL import Image

from figure_layout import SHAPES, resolve_size


def configure(font: str) -> None:
    mpl.rcParams.update(
        {
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.family": "sans-serif",
            "font.sans-serif": [font, "Arial", "Helvetica", "DejaVu Sans"],
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "savefig.bbox": "tight",
        }
    )


def resolved_font_name(font: str) -> str:
    properties = font_manager.FontProperties(family=[font, "Arial", "Helvetica", "DejaVu Sans"])
    path = font_manager.findfont(properties, fallback_to_default=True)
    return font_manager.FontProperties(fname=path).get_name()


def load_data(path: Path | None) -> pd.DataFrame:
    if path is None:
        rng = np.random.default_rng(7)
        return pd.DataFrame(
            {
                "group": np.repeat(["Control", "Treatment"], 18),
                "value": np.r_[rng.normal(1.0, 0.22, 18), rng.normal(1.45, 0.25, 18)],
            }
        )
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def draw_figure(df: pd.DataFrame, width_mm: float, height_mm: float) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))
    groups = list(dict.fromkeys(df["group"].astype(str)))
    palette = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]
    rng = np.random.default_rng(11)
    for i, group in enumerate(groups):
        values = df.loc[df["group"].astype(str) == group, "value"].astype(float).to_numpy()
        x = np.full(values.shape, i) + rng.normal(0, 0.035, size=values.shape)
        ax.scatter(x, values, s=18, color=palette[i % len(palette)], alpha=0.85, linewidths=0)
        mean = float(np.mean(values))
        sem = float(np.std(values, ddof=1) / np.sqrt(len(values))) if len(values) > 1 else 0.0
        ax.errorbar(i, mean, yerr=sem, color="black", capsize=3, marker="_", markersize=18, lw=0.8)
    ax.set_xticks(range(len(groups)), groups)
    ax.set_ylabel("Value")
    ax.set_title("")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(-0.22, 1.04, "a", transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")
    fig.tight_layout(pad=0.5)
    return fig


def flatten_alpha(path: Path, dpi: int) -> None:
    if not path.exists():
        return
    with Image.open(path) as im:
        if im.mode in {"RGBA", "LA"} or "transparency" in im.info:
            background = Image.new("RGB", im.size, "white")
            rgba = im.convert("RGBA")
            background.paste(rgba, mask=rgba.getchannel("A"))
            background.save(path, dpi=(dpi, dpi))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("figure_bundle"))
    parser.add_argument("--width-mm", type=float)
    parser.add_argument("--height-mm", type=float)
    parser.add_argument("--shape", choices=SHAPES, default="auto")
    parser.add_argument("--panels", type=int, default=1)
    parser.add_argument("--archetype", action="append")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--font", default="Arial")
    parser.add_argument("--journal", default="general-publication")
    parser.add_argument("--formats", nargs="+", default=["svg", "pdf", "png"])
    args = parser.parse_args()
    archetypes = args.archetype or ["quantitative-comparison"]
    size = resolve_size(args.shape, args.journal, args.panels, archetypes, args.width_mm, args.height_mm)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    configure(args.font)
    actual_font = resolved_font_name(args.font)
    df = load_data(args.data)
    fig = draw_figure(df, size.width_mm, size.height_mm)

    formats = {item.lower().lstrip(".") for item in args.formats}
    if "svg" in formats:
        fig.savefig(args.output_dir / "figure.svg")
    if "pdf" in formats:
        fig.savefig(args.output_dir / "figure.pdf")
    preview = args.output_dir / "figure_preview.png"
    fig.savefig(preview, dpi=args.dpi, facecolor="white")
    flatten_alpha(preview, args.dpi)
    if "png" in formats:
        png = args.output_dir / "figure.png"
        fig.savefig(png, dpi=args.dpi, facecolor="white")
        flatten_alpha(png, args.dpi)
    if "tif" in formats or "tiff" in formats:
        tiff = args.output_dir / "figure.tiff"
        fig.savefig(tiff, dpi=args.dpi, facecolor="white")
        flatten_alpha(tiff, args.dpi)
    df.to_csv(args.output_dir / "figure_source_data.csv", index=False)
    shutil.copyfile(Path(__file__), args.output_dir / "plot_script.py")
    config = {
        "journal_profile": args.journal,
        "width_mm": size.width_mm,
        "height_mm": size.height_mm,
        "shape": size.shape,
        "panels": args.panels,
        "archetypes": archetypes,
        "dpi": args.dpi,
        "font": args.font,
        "actual_font": actual_font,
        "editable_text": True,
        "formats": sorted(formats),
        "input_data": str(args.data) if args.data else "demo",
    }
    (args.output_dir / "plot_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    plt.close(fig)
    print(f"Wrote bundle to {args.output_dir}")


if __name__ == "__main__":
    main()
