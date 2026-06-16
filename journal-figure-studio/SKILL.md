---
name: journal-figure-studio
description: Create, revise, audit, and export publication-ready scientific figures for academic papers in journal-specific styles such as Nature, Science, Cell/Cell Press, PLOS, JCB, Elsevier, IEEE, ACS, medical journals, and ML conferences. Use when Codex needs to make paper figures, multi-panel scientific plots, manuscript-ready SVG/PDF/TIFF/PNG outputs, journal-style figure layouts, source-data traceability, image-integrity checks, statistics legends, existing-figure diagnostics, or Chinese requests such as 论文配图、科研绘图、SCI作图、期刊风格Figure、Nature风格图、Cell风格图、Science风格图.
---

# Journal Figure Studio

Default to Python. Do not ask the user to choose Python or R unless they explicitly request a non-Python backend, provide existing non-Python plotting code that must be preserved, or the task cannot reasonably be completed with the available Python stack.

Use this skill to turn data, sketches, existing figures, or review comments into publication-ready scientific figure bundles. Always treat the figure as scientific evidence first and visual styling second.

## Workflow

1. Route the request by journal profile, plot archetype, and figure intent.
2. Establish a figure contract before drawing or revising.
3. Use Python to generate or inspect the figure, with explicit input paths, sizes, fonts, dpi, palettes, and random seeds.
4. Export an editable/vector-first bundle where possible: SVG, PDF, TIFF or PNG, preview PNG, source data when available, plot script, config, panel contract, and QA report.
5. Run automated and human QA appropriate to the mode: draft, revision, or submission.

## Routing

Infer missing dimensions when they do not block a useful draft. Ask one concise question only when the answer changes hard constraints such as final journal, print size, or image integrity treatment.

- **Journal profile**: read the matching file in `static/profiles/`. Use `general-publication.md` when the user only says paper figure, SCI figure, or high-impact journal. Read `science.md` for Science-style requests, but treat hard specifications as `unknown_or_verify`.
- **Plot archetype**: read one or more files in `archetypes/`. A multipanel figure can combine archetypes, for example `image-plate-quant` plus `quantitative-comparison`.
- **Figure intent**: read one file in `intents/`. Default to `discovery` for exploratory first drafts, `validation` for confirmatory plots, `comparison` for method or group comparisons, and `graphical-summary` for non-evidence conceptual visuals.
- **Cross-rules**: if a matching file exists in `overrides/`, read it after the journal and archetype files.

## Modes

- **Draft mode**: use when the user asks to make, draw, sketch, or create an initial figure. Prioritize core conclusion, panel composition, readable layout, and obvious QA risks.
- **Revision mode**: use when the user asks to modify, restyle, rearrange, respond to comments, or polish an existing figure. Preserve editability and state what changed.
- **Submission mode**: use when the user asks for final, submission, compliance, journal check, or upload-ready output. Perform strict size, dpi, font, format, source-data, statistics, image-integrity, and author-guide verification reminders.

## Figure Contract

Before plotting, create a concise contract in prose or with `scripts/generate_panel_contract.py`. Include:

- Core conclusion: one sentence the figure should support.
- Evidence chain: how each panel supports the conclusion.
- Target journal profile, figure type, width class, and mode.
- Shape/aspect strategy: use `auto` unless the user specifies otherwise. For a single quantitative-comparison panel such as a bar, dot-plus-summary, box, or violin plot, prefer a tall single-column layout; reserve wide layouts for multi-panel rows, many groups, long labels, or explicitly wide journal compositions.
- Archetype and intent for each panel.
- Export contract: formats, size, dpi, fonts, source data, and editability.
- Risk register: statistics, image integrity, resolution, color accessibility, caption/source-data risks.

For the schema and examples, read `static/core/contract.md` and `references/panel-contract-schema.md`.

## Python-First Rendering

Use `static/core/python-first-workflow.md` before implementing a new plotting script. Configure Matplotlib for editable text:

```python
import matplotlib as mpl
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
```

Use `scripts/export_matplotlib_bundle.py` as a starter when a task needs a reproducible bundle. Adapt it to the user's data rather than hand-editing exported graphics.

For a simple end-to-end starter bundle, prefer `scripts/build_figure_bundle.py`. It creates a panel contract, validates it, exports the figure files, and writes a QA report in one run.

## Existing Figure Diagnostics

When auditing a supplied figure, inspect scientific logic, layout hierarchy, journal fit, plot-specific risks, integrity/statistics, and a panel-level action plan. Use this output shape:

```text
Overall verdict:
Top risks:
Panel-by-panel comments:
Journal-profile mismatches:
Plot-archetype issues:
Recommended revision plan:
```

Read `static/core/qa-baseline.md`, the relevant profile, and the relevant archetype before giving final diagnostic advice.

## QA and Delivery

Every completed figure task should include, when applicable:

- `figure.svg`, `figure.pdf`, and profile-appropriate `figure.tiff` or `figure.png`.
- `figure_preview.png`.
- `figure_source_data.csv` or `.xlsx` when source data are provided or generated.
- `plot_script.py`, `plot_config.yaml` or `.json`, `panel_contract.yaml` or `.json`.
- `figure_qa.md` covering size, fonts, dpi, text overlap, statistics, source data, color accessibility, scale bars, and image integrity.

Use these utilities when helpful:

- `scripts/build_figure_bundle.py`: create a starter contract, exported figure bundle, manifest, and QA report.
- `scripts/generate_panel_contract.py`: create a starter contract JSON.
- `scripts/validate_panel_contract.py`: validate required contract fields before plotting or delivery.
- `scripts/generate_qa_report.py`: create a starter QA report from config and contract files.
- `scripts/dpi_size_report.py`: inspect raster size and print-size dpi.
- `scripts/check_svg_text.py`: detect whether SVG text remains editable.
- `scripts/inspect_figure.py`: summarize image dimensions, mode, and likely QA concerns.

## Reference Map

- Core workflow: `static/core/contract.md`, `static/core/python-first-workflow.md`, `static/core/qa-baseline.md`.
- Journal profile schema and source policy: `references/journal-profile-schema.md`, `references/source-links.md`.
- Plot and panel schemas: `references/archetype-profile-schema.md`, `references/panel-contract-schema.md`.
- Statistics and integrity: `references/statistics-legend.md`, `references/image-integrity.md`.
- Color and chart patterns: `references/accessibility-palettes.md`, `references/chart-patterns.md`.
- End-to-end examples: `references/python-workflow.md`.
- Structured starter rules: `assets/templates/profile_rules.json`, `assets/templates/plot_config.json`.
