#!/usr/bin/env python3
"""Build a starter publication figure bundle and run baseline QA."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("figure_bundle"))
    parser.add_argument("--journal", default="general-publication")
    parser.add_argument("--intent", default="discovery")
    parser.add_argument("--mode", choices=["draft", "revision", "submission"], default="draft")
    parser.add_argument("--core-conclusion", default="")
    parser.add_argument("--panels", type=int, default=1)
    parser.add_argument("--archetype", action="append", default=["quantitative-comparison"])
    parser.add_argument("--width-mm", type=float, default=89.0)
    parser.add_argument("--height-mm", type=float, default=70.0)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--font", default="Arial")
    parser.add_argument("--formats", nargs="+", default=["svg", "pdf", "png", "tiff"])
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    contract = args.output_dir / "panel_contract.json"
    qa = args.output_dir / "figure_qa.md"

    run(
        [
            sys.executable,
            str(SCRIPT_DIR / "generate_panel_contract.py"),
            "--journal",
            args.journal,
            "--intent",
            args.intent,
            "--mode",
            args.mode,
            "--core-conclusion",
            args.core_conclusion,
            "--panels",
            str(args.panels),
            "--width-mm",
            str(args.width_mm),
            "--dpi",
            str(args.dpi),
            "--font",
            args.font,
            "--formats",
            *args.formats,
            "--output",
            str(contract),
        ]
    )
    run([sys.executable, str(SCRIPT_DIR / "validate_panel_contract.py"), str(contract)])

    export_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "export_matplotlib_bundle.py"),
        "--output-dir",
        str(args.output_dir),
        "--width-mm",
        str(args.width_mm),
        "--height-mm",
        str(args.height_mm),
        "--dpi",
        str(args.dpi),
        "--font",
        args.font,
        "--journal",
        args.journal,
        "--formats",
        *args.formats,
    ]
    if args.data:
        export_cmd.extend(["--data", str(args.data)])
    run(export_cmd)

    config = args.output_dir / "plot_config.json"
    run(
        [
            sys.executable,
            str(SCRIPT_DIR / "generate_qa_report.py"),
            "--contract",
            str(contract),
            "--config",
            str(config),
            "--bundle-dir",
            str(args.output_dir),
            "--output",
            str(qa),
        ]
    )

    manifest = {
        "bundle_dir": str(args.output_dir),
        "contract": str(contract),
        "config": str(config),
        "qa_report": str(qa),
    }
    (args.output_dir / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote complete bundle to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
