# Omics Embedding

For UMAP, t-SNE, single-cell composition, marker expression maps, and pseudotime layouts.

## Required Data Contract

- Embedding coordinates or expression matrix plus preprocessing metadata.
- Cluster/category labels and sample/batch metadata.
- Marker, condition, or pseudotime variable when used.

## Visual Encoding

- Use small points, alpha, and direct cluster labels.
- Limit categorical colors; group rare categories if needed.
- Use separate panels for marker gradients and categories.

## Statistics

- State preprocessing, embedding method, random seed, clustering method, and batch handling.

## QA Checks

- Do not overinterpret distances between UMAP/t-SNE clusters.
- Category colors can exceed distinguishable limits.
- Batch effects and downsampling should be disclosed.
