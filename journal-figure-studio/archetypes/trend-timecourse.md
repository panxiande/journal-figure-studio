# Trend / Timecourse

For line plots, longitudinal trends, dose response, growth curves, and repeated measurement data.

## Required Data Contract

- x variable: time, dose, concentration, ordered parameter, or visit.
- Numeric y outcome and units.
- Group/condition column.
- Subject/replicate identifier for repeated measures.

## Visual Encoding

- Use lines for ordered progression, points for observed values, and bands/error bars for uncertainty.
- Mark interventions, baseline, or threshold lines clearly.
- Show individual trajectories when subject-level heterogeneity matters.

## Statistics

- Define repeated-measures handling, fitted model, confidence band, and n per timepoint.

## QA Checks

- Missing timepoint n can mislead.
- Interpolated lines should not imply unobserved measurements.
- Dose axes may need log scale and explicit units.
