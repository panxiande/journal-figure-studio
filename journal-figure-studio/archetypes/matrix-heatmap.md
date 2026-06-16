# Matrix / Heatmap

For heatmaps, clustered heatmaps, bubble matrices, enrichment matrices, and annotated matrices.

## Required Data Contract

- Matrix-like values with row and column identifiers.
- Units, transform, normalization, missing-value handling.
- Optional row/column annotations and clustering method.

## Visual Encoding

- Use perceptually meaningful sequential or diverging maps.
- Center diverging palettes on a meaningful reference.
- Add annotation tracks only when they support the message.

## Statistics

- State normalization, scaling, distance metric, linkage, and enrichment test if used.

## QA Checks

- Rainbow maps and clipped scales mislead.
- Row scaling can hide absolute differences.
- Cluster order should not be overinterpreted without support.
