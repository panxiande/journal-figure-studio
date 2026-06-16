# Panel Contract Schema

```json
{
  "figure": {
    "core_conclusion": "",
    "journal_profile": "general-publication",
    "figure_intent": "discovery",
    "mode": "draft",
    "export_contract": {
      "formats": ["svg", "pdf", "png"],
      "width_mm": 183,
      "dpi": 300,
      "font": "Arial",
      "editable_text": true
    },
    "risk_register": []
  },
  "panels": [
    {
      "id": "a",
      "role": "discovery",
      "archetype": "quantitative-comparison",
      "key_message": "",
      "data_source": "",
      "required_annotations": [],
      "statistical_notes": [],
      "integrity_notes": [],
      "journal_overrides": [],
      "risk": []
    }
  ]
}
```

## Example: Quantitative Multipanel

Panels:

- `a`: experimental timeline, `schematic-mechanism`, context.
- `b`: dot plus summary, `quantitative-comparison`, main effect.
- `c`: dose response, `trend-timecourse`, robustness.
- `d`: correlation scatter, `relationship-scatter`, mechanism support.

## Example: Image Plate Plus Quantification

Panels:

- `a`: microscopy plate with channels and scale bar, `image-plate-quant`, visual evidence.
- `b`: zoom crop, `image-plate-quant`, localization detail.
- `c`: dot plus summary quantification, `quantitative-comparison`, measurement support.

## Validation

Use `scripts/validate_panel_contract.py panel_contract.json` before plotting or delivery. A valid contract must include the required figure/export fields and at least one panel with stable panel IDs, archetypes, data source notes, statistical notes, integrity notes, and risk fields.
