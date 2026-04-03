# 3-Minute Demo Script

## Opening (0:00-0:20)

Hello, this project builds a reproducible AI-assisted baseline for hemodialysis toxin estimation using optoelectronic absorbance signals, dialysis machine parameters, and patient features from the provided clinical Excel dataset.

## Problem framing (0:20-0:45)

The goal is to estimate six toxin targets during hemodialysis:

- urea
- creatinine
- uric-acid-related target inferred as `Acid`
- beta-2 microglobulin
- phosphorus
- potassium

I first inspected the real workbook schema instead of assuming the paper structure, then built the analysis pipeline around the verified columns.

## Dataset and methodology (0:45-1:20)

The final pipeline uses:

- all five absorbance wavelengths: 255, 275, 285, 295, and 310 nm
- all available dialysis machine parameters
- personalized patient features when available

I compared multiple models:

- SVR
- Linear Regression
- Random Forest
- KNN

I also applied feature selection using mutual information and permutation importance, then compared full-feature models versus selected-feature models under 5-fold cross-validation.

## Results (1:20-2:15)

The best-performing setup was generally the full feature set including absorbance, machine, and personal features.

Key findings:

- SVR performed best for urea, creatinine, phosphorus, and the inferred uric-acid target
- KNN performed best for potassium and beta-2 microglobulin
- feature selection improved interpretability, but did not consistently improve predictive performance over the full feature sets

The strongest R-squared values were approximately:

- urea: 0.938
- creatinine: 0.903
- acid-related target: 0.914
- phosphorus: 0.876
- potassium: 0.685
- beta-2 microglobulin: 0.872

## Visual evidence (2:15-2:45)

The project also generates:

- feature importance plots
- model comparison plots
- full correlation heatmaps
- paper-style actual-vs-predicted panels

I also saved the final per-target models so the pipeline supports reproducible inference instead of only one-off analysis.

## Closing (2:45-3:00)

Overall, this project demonstrates end-to-end AI-agent assistance across requirement analysis, coding, debugging, evaluation, documentation, and presentation preparation, while also highlighting where research-style figures can diverge from rigorous validation practice.
