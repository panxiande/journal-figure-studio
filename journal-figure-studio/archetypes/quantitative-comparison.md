# Quantitative Comparison

For bar, grouped bar, dot plus summary, box, violin, raincloud, and distribution comparisons.

## Required Data Contract

- Numeric outcome column with units.
- Group/condition column.
- Replicate/sample identifier and n definition.
- Optional batch, pairing, timepoint, or covariates.

## Visual Encoding

- Prefer raw points plus summary for small/moderate n.
- Use box/violin/raincloud when distribution shape matters.
- Use color for condition and shape/line for paired or batch structure when needed.
- For a single simple comparison panel, prefer a tall single-column aspect unless group count, label length, or multipanel composition requires a wider layout.

## Statistics

- State center, error/spread definition, n, repeat type, test/model, correction, and comparison target.
- Prefer effect size and confidence intervals when useful.

## QA Checks

- Bar-only summaries hide distributions.
- Technical replicates may be misused as biological n.
- Error bars and p-value stars need definitions.
