# End-to-End Examples

## Quantitative Multipanel

1. Load CSV with columns such as `group`, `value`, `time`, `replicate`, `condition`.
2. Build a contract with one context panel, one main dot-summary panel, one trend panel, and one robustness/correlation panel.
3. Use `matplotlib.gridspec` or `subplot_mosaic` for stable layout.
4. Export SVG/PDF/PNG plus source data and QA.
5. QA: raw points visible, n defined, error definition present, test/correction described, panel labels readable.

## Image Plate Plus Quant

1. Load source images without destructive edits.
2. Record crop and processing notes.
3. Add scale bars based on pixel calibration.
4. Use a paired quantification panel with raw points.
5. Export a high-dpi raster plus editable SVG/PDF where text and vector annotations remain editable.
6. QA: scale bar, channel labels, contrast notes, source images, crop notes, quantification source data.
