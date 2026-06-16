#!/usr/bin/env python3
"""Check whether an SVG appears to contain editable text nodes."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()

    tree = ET.parse(args.svg)
    root = tree.getroot()
    text_nodes = [node for node in root.iter() if node.tag.endswith("text")]
    path_nodes = [node for node in root.iter() if node.tag.endswith("path")]
    print(f"file: {args.svg}")
    print(f"text_nodes: {len(text_nodes)}")
    print(f"path_nodes: {len(path_nodes)}")
    print(f"editable_text_likely: {len(text_nodes) > 0}")


if __name__ == "__main__":
    main()
