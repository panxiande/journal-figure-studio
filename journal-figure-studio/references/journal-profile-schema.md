# Journal Profile Schema

Use this structure when extending `static/profiles/`.

```yaml
profile: nature
scope: main figure
rule_layers:
  required:
    - rule: ""
      source_type: official
      confidence: high
      last_verified: "2026-06-16"
      source_url: ""
      applies_to: all
  recommended: []
  style_observed: []
  unknown_or_verify: []
canvas: {}
typography: {}
layout_grammar: {}
palette: {}
export: {}
integrity: {}
caption_notes: {}
verification: {}
```

## Constraint Strength

- `required`: official author guide or publisher requirement.
- `recommended`: official advice or high-confidence publication practice.
- `style_observed`: visual tendency from published figures or editorial taste; never present as hard compliance.
- `unknown_or_verify`: access-limited, unverified, venue-specific, or likely to change.
