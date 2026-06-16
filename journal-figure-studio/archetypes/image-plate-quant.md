# Image Plate + Quantification

For microscopy, histology, gel/blot, channel overlays, zoom crops, and paired quantification.

## Required Data Contract

- Source image paths and acquisition metadata when available.
- Pixel calibration for scale bars.
- Crop, channel, contrast, and processing notes.
- Quantification table with sample/field/cell identifiers.

## Visual Encoding

- Use consistent grid, channel labels, scale bars, and matched intensity treatment.
- Pair representative images with quantification when making a quantitative claim.
- Use zoom crops with source region markers when needed.

## Statistics and Integrity

- Define unit of analysis: image, field, cell, animal, patient, lane.
- Record global adjustments, pseudocolor, splices, and reused controls.

## QA Checks

- Missing scale bar is a major risk.
- Overcropped blot/gel or cleaned background can be integrity risk.
- Quantification n must not confuse cells/fields with biological replicates.
