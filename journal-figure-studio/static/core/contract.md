# Figure Contract

Create the contract before drawing, revising, or auditing. Keep it short enough to stay useful, but explicit enough that every panel has a job.

## Required Fields

```yaml
figure:
  core_conclusion: ""
  journal_profile: general-publication
  figure_intent: discovery
  mode: draft
  width_class: double-column
  export_contract:
    formats: [svg, pdf, png]
    dpi: 300
    editable_text: true
    source_data: requested
panels:
  - id: a
    role: discovery
    archetype: quantitative-comparison
    key_message: ""
    data_source: ""
    required_annotations: []
    statistical_notes: []
    integrity_notes: []
    journal_overrides: []
    risk: []
```

## Contract Rules

- Make the core conclusion a claim, not a topic.
- Give each panel one evidence function. If a panel has no function, remove it or move it to supplement/extended data.
- Mark uncertainty honestly: unknown sample size, missing scale bar, unclear error-bar definition, unverified journal rule.
- Do not use visual polish to hide weak statistics, overcropped images, missing source data, or unverifiable processing.
- Keep captions and long method notes out of the figure unless the target venue explicitly expects in-figure legends.

## Panel Decisions

Use the contract to decide panel weight:

- **Hero panel**: carries the main result or visual evidence.
- **Support panel**: validates, quantifies, or explains the hero panel.
- **Context panel**: gives experimental design, cohort flow, or method setup.
- **Risk panel**: useful but underpowered, exploratory, or too dense; consider extended data.
