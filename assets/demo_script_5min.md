# 5-Minute Demo Script

## 1. Introduction

This project is an interview-homework-style baseline for predicting hemodialysis toxin concentrations using optoelectronic sensing and structured clinical data. The work was built around the real dataset in `shin_clinical_data.xlsx`, not assumptions from the paper alone.

## 2. Problem definition

The target is to estimate six toxin-related variables during hemodialysis:

- urea
- creatinine
- `Acid`, treated cautiously as the workbook counterpart of uric acid
- beta-2 microglobulin
- phosphorus
- potassium

The challenge is that the dataset mixes repeated session measurements, absorbance signals, machine parameters, and patient-level context.

## 3. Dataset verification

The workflow starts by verifying the workbook schema.

Important verified findings:

- the main usable sheet is `刪除異常值`
- the workbook contains five absorbance wavelengths, not only three:
  - 255nm
  - 275nm
  - 285nm
  - 295nm
  - 310nm
- it also contains multiple machine variables such as venous pressure, transmembrane pressure, dialysate flow, and ultrafiltration-related variables

This made it more appropriate to extend the modeling scope beyond the paper's original three-wavelength narrative.

## 4. Pipeline design

The pipeline includes:

- data loading
- safe cleaning
- English renaming for reproducible outputs
- exploratory analysis
- three feature sets
- multi-model benchmarking
- feature selection
- final model persistence

The three feature sets are:

1. all absorbance only
2. all absorbance + all machine parameters
3. all absorbance + all machine parameters + personal features

The models compared are:

- SVR
- Linear Regression
- Random Forest
- KNN

All evaluation uses five-fold cross-validation with:

- MAE
- MSE
- RMSE
- R²

## 5. Feature selection and interpretability

For feature selection, I used:

- mutual information regression
- permutation importance

This produced selected-feature tables and feature-importance figures.

An important takeaway is that 285nm and 310nm repeatedly appeared as informative absorbance features, and several machine variables such as current ultrafiltration volume also showed predictive value.

However, selected feature subsets did not consistently outperform the full feature sets. So the most honest conclusion is that feature selection improved interpretability more than predictive accuracy in this baseline.

## 6. Best results

The strongest models were not identical across all toxins.

Best-performing summary:

- urea → SVR, full absorbance + machine + personal
- creatinine → SVR, full absorbance + machine + personal
- acid-related target → SVR, full absorbance + machine + personal
- phosphorus → SVR, full absorbance + machine + personal
- potassium → KNN, full absorbance + machine + personal
- beta-2 microglobulin → KNN, selected feature subset

Representative R² values:

- urea ≈ 0.938
- creatinine ≈ 0.903
- acid-related target ≈ 0.914
- phosphorus ≈ 0.876
- potassium ≈ 0.685
- beta-2 microglobulin ≈ 0.872

## 7. Important methodological lesson

One of the most useful outcomes of this project is not only the model performance, but also the methodological clarification.

During implementation, I found that some paper-style figures can be visually persuasive while still being risky if they mix:

- cross-validation metrics
- train-on-train predictions
- deployment-style inference
- session-level plots that are not clearly separated from validation evidence

So the final project distinguishes between:

- rigorous validation figures
- saved-model inference artifacts
- demo-oriented examples

## 8. Final deliverables

The project includes:

- source code
- tests
- reproducible outputs
- saved models
- reports
- PPT content
- demo scripts

This makes it not just an analysis notebook, but a GitHub-ready end-to-end submission.

## 9. Closing

In short, this project reproduces the paper idea, extends it to a fuller five-wavelength analysis, compares multiple models instead of assuming one universal winner, and turns the workflow into a reproducible AI-assisted end-to-end project with honest reporting of both strengths and limitations.
