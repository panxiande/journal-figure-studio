# Clinical Evidence

For forest plots, Kaplan-Meier curves, CONSORT flow diagrams, subgroup plots, and adverse-event summaries.

## Required Data Contract

- Effect estimate, CI, group labels, sample size, event counts, and model/test details.
- For survival: time, event indicator, censoring, groups, risk table.
- For flow: counts at each stage and exclusion reasons.

## Visual Encoding

- Use interval plots for estimates and confidence intervals.
- Include risk tables for Kaplan-Meier when feasible.
- Make denominators visible.

## Statistics

- State model, adjustment set, censoring, subgroup definitions, and multiplicity when relevant.

## QA Checks

- Missing denominators and CI are serious risks.
- Subgroup plots can imply unsupported interaction effects.
- Flow diagrams must conserve counts.
