# Python-First Workflow

Use Python unless the user explicitly asks for another backend or gives non-Python code that must remain authoritative.

## Standard Stack

- Data: `pandas`, `numpy`.
- Statistics: `scipy`, `statsmodels` when available.
- Plotting: `matplotlib`, `seaborn`.
- Layout: `matplotlib.gridspec`, `subplot_mosaic`, or `svgutils` if installed.
- Images: `Pillow`, `scikit-image` when available.
- Export: SVG/PDF first, TIFF/PNG for raster submission targets.

## Reproducibility Requirements

- Set a random seed when jitter, sampling, clustering initialization, or layout randomness is used.
- Keep input paths, output paths, dimensions, dpi, fonts, palette, and journal profile in a config file.
- Keep source data unchanged. Derive cleaned/summary data in code and export source-data tables when useful.
- Preserve editable vector text unless a profile requires otherwise.

## Matplotlib Defaults

```python
import matplotlib as mpl

mpl.rcParams.update({
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.family": "Arial",
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "savefig.bbox": "tight",
})
```

## Export Bundle

Export at least:

- `figure.svg`
- `figure.pdf`
- `figure_preview.png`
- profile-specific `figure.tiff` or `figure.png`
- `plot_script.py`
- `plot_config.yaml` or `.json`
- `panel_contract.yaml` or `.json`
- `figure_qa.md`

## Fallbacks

If a package is missing, use installed equivalents first. If the figure cannot be made faithfully without installing packages, report the blocker and request installation permission rather than silently changing the scientific output.
