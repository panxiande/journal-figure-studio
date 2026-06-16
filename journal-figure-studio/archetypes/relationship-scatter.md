# Relationship / Scatter

For scatter, correlation, volcano, MA plot, embedding local relationships, and thresholded point clouds.

## Required Data Contract

- Numeric x and y columns with units or transform definitions.
- Optional group, label, threshold, and replicate columns.

## Visual Encoding

- Use alpha for dense points and direct labels for selected points.
- Add regression/correlation only when method and assumptions are clear.
- For volcano/MA plots, mark thresholds and label key features sparingly.

## Statistics

- State correlation method, regression model, threshold definition, and multiple-testing correction when applicable.

## QA Checks

- Outliers can drive correlations.
- Threshold lines need definitions.
- Dense scatter may require binning or contours.
