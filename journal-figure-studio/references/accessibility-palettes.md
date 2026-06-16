# Accessibility Palettes

Prefer colorblind-safe palettes and redundant encodings.

## Defaults

- Categorical: Okabe-Ito `#0072B2`, `#D55E00`, `#009E73`, `#CC79A7`, `#E69F00`, `#56B4E9`, `#F0E442`, `#000000`.
- Sequential: perceptually uniform maps such as `viridis`, `magma`, `cividis`.
- Diverging: balanced maps centered at a meaningful reference such as zero.

## Avoid

- Red/green as the only distinction.
- Rainbow colormaps for quantitative heatmaps.
- Too many categorical colors without direct labels or grouping.
- Low-contrast annotations on image panels.
