# Slide Content Draft

## 1. Question Description
- Build a baseline regression project for hemodialysis toxin estimation.
- Use structured clinical data and absorbance features from the provided Excel dataset.
- Deliver a reproducible, GitHub-ready, interview-friendly submission.

## 2. Dataset and Verified Schema Mapping
- Primary sheet: `刪除異常值`
- Verified six target mapping from workbook headers.
- Full wavelength set used: 255nm, 275nm, 285nm, 295nm, 310nm.
- All dialysis machine parameters included in the expanded analysis.

## 3. Solution Overview
- Data profiling and cleaning pipeline
- Three feature settings:
  - all absorbance only
  - all absorbance + machine
  - all absorbance + machine + personal
- Main baseline: SVR
- Comparison models:
  - Linear Regression
  - Random Forest Regressor
  - KNN Regressor
- Five-fold CV with MAE, MSE, RMSE, R²

## 4. Feature Selection Workflow
- Mutual information regression for candidate feature ranking
- Permutation importance for post-selection importance analysis
- Performance comparison between full features and selected subsets
- Transparent reporting when selected subsets help interpretation but not accuracy

## 5. Demo Result
- Strongest results came from full-feature SVR models for urea, creatinine, phosphorus, and inferred uric acid
- KNN performed best for potassium and beta2-microglobulin in the expanded comparison
- Full feature sets generally outperformed absorbance-only models
- Important predictive features repeatedly included 285nm, 310nm, current ultrafiltration volume, and several machine/context variables depending on target
- Session-level predicted-vs-actual concentration curves and paper-style predicted-vs-actual panels were generated for the strongest model per target

## 6. Limitations and Next Steps
- Small repeated-measure dataset
- `Acid` target requires domain confirmation
- Feature selection improved explainability more than predictive performance in this run
- Future improvement: grouped CV, tuning, and richer interpretability
