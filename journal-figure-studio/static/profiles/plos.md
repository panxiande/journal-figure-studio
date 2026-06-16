# PLOS Profile

Use for PLOS-family submission checks and PLOS-style multipanel figures.

## Rule Layers

### required

- rule: Figure files should be TIFF or EPS for submission workflows that require those formats.
  source_type: official
  confidence: high
  last_verified: 2026-06-16
  source_url: https://journals.plos.org/plosone/s/figures
  applies_to: all
- rule: Figure images should be 300-600 dpi and within PLOS pixel guidance.
  source_type: official
  confidence: high
  last_verified: 2026-06-16
  source_url: https://journals.plos.org/plosone/s/figures
  applies_to: all
- rule: Fonts should be Arial, Times, or Symbol, typically 8-12 pt.
  source_type: official
  confidence: high
  last_verified: 2026-06-16
  source_url: https://journals.plos.org/plosone/s/figures
  applies_to: all

### recommended

- Put multipanel figures in one file on a single page.
- Do not include captions in the figure file.
- Use RGB or grayscale; avoid alpha channels in TIFF output.

### style_observed

- Clear, less compressed layouts with readable text and unambiguous legends.

### unknown_or_verify

- Target PLOS journal and upload system can refine file size and format constraints.

## Defaults

- Canvas: pixel-first at 300 dpi, width 789-2250 px, height up to 2625 px unless journal-specific guidance differs.
- Typography: Arial, 8-10 pt final.
- Export: TIFF with LZW when possible, EPS/PDF/SVG as editable sources, PNG preview.
- Integrity: source data and statistical transparency are important for reproducibility.
