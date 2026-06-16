#!/usr/bin/env python3
"""Starter Matplotlib exporter for publication figure bundles.

Adapt `draw_figure` to the user's data. This script intentionally creates a
minimal demo when no data are supplied so the export path can be smoke-tested.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("figure_bundle"))
    parser.add_argument("--width-mm", type=float, default=89.0)
    parser.add_argument("--height-mm", type=float, default=70.0)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--font", default="Arial")
    parser.add_argument("--journal", default="general-publication")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    configure(args.font)
    df = load_data(args.data)
    fig = draw_figure(df, args.width_mm, args.height_mm)

    fig.savefig(args.output_dir / "figure.svg")
    fig.savefig(args.output_dir / "figure.pdf")
    fig.savefig(args.output_dir / "figure_preview.png", dpi=args.dpi)
    fig.savefig(args.output_dir / "figure.png", dpi=args.dpi)
    df.to_csv(args.output_dir / "figure_source_data.csv", index=False)
    config = {
        "journal_profile": args.journal,
        "width_mm": args.width_mm,
        "height_mm": args.height_mm,
        "dpi": args.dpi,
        "font": args.font,
        "editable_text": True,
        "input_data": str(args.data) if args.data else "demo",
    }
    (args.output_dir / "plot_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    plt.close(fig)
    print(f"Wrote bundle to {args.output_dir}")


if __name__ == "__main__":
    main()
