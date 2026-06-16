# Distribution

For histograms, density plots, ECDFs, ridgelines, and residual distributions.

## Required Data Contract

- Numeric value column, group column when comparing, units, sample identifiers, and censoring/truncation notes.

## Visual Encoding

- Use histograms or density plots for shape; ECDF for robust comparisons; ridgelines only when labels remain readable.
- Use consistent binning or explicitly chosen bandwidth.

## Statistics

- State bin width, bandwidth, transform, and comparison test if used.

## QA Checks

- Different bin widths can invent or hide patterns.
- Normalized density can hide sample size differences.
