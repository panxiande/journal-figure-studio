#!/usr/bin/env python3
"""Figure shape and size helpers for Journal Figure Studio scripts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


SHAPES = ("auto", "tall", "wide", "square")

TALL_ARCHETYPES = {"quantitative-comparison", "clinical-evidence"}
SQUARE_ARCHETYPES = {"relationship-scatter", "matrix-heatmap", "omics-embedding"}


@dataclass(frozen=True)
class FigureSize:
    shape: str
    width_mm: float
    height_mm: float


def infer_shape(requested: str, panels: int, archetypes: Sequence[str]) -> str:
    if requested != "auto":
        return requested
    normalized = {item.strip().lower() for item in archetypes if item}
    if panels <= 1:
        if normalized & TALL_ARCHETYPES:
            return "tall"
        if normalized & SQUARE_ARCHETYPES:
            return "square"
    return "wide"


def default_width_mm(journal: str, shape: str, panels: int) -> float:
    journal = journal.lower()
    if shape == "wide" and panels > 1:
        if journal == "plos":
            return 171.0
        if journal in {"nature", "general-publication"}:
            return 183.0
        if journal == "jcb":
            return 177.8
        return 183.0
    if shape == "wide":
        return 120.0
    if journal == "plos":
        return 83.0
    return 89.0


def resolve_size(
    requested_shape: str,
    journal: str,
    panels: int,
    archetypes: Sequence[str],
    width_mm: float | None,
    height_mm: float | None,
) -> FigureSize:
    shape = infer_shape(requested_shape, panels, archetypes)
    width = width_mm if width_mm is not None else default_width_mm(journal, shape, panels)

    if height_mm is not None:
        height = height_mm
    elif shape == "tall":
        height = width * 1.25
    elif shape == "square":
        height = width
    else:
        height = width * 0.66

    return FigureSize(shape=shape, width_mm=round(width, 1), height_mm=round(height, 1))
