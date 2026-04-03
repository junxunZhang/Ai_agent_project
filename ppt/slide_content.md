# Slide Content Draft

## 1. Question Description
- Build a baseline regression project for hemodialysis toxin estimation.
- Use structured clinical data and absorbance features from the provided Excel dataset.
- Deliver a reproducible, GitHub-ready, interview-friendly submission.

## 2. Dataset and Verified Schema Mapping
- Primary sheet: `刪除異常值`
- Verified six target mapping from workbook headers.
- Core absorbance features present: 255nm, 275nm, 310nm.
- Additional context includes patient features and dialysis machine parameters.

## 3. Solution Overview
- Data profiling and cleaning pipeline
- Two feature settings: absorbance-only vs absorbance + context
- Main baseline: SVR
- Five-fold CV with MAE, MSE, RMSE, R²

## 4. Agent Workflow
- Requirement analysis
- Dataset inspection and target verification
- Code generation and testing
- Analysis execution and report generation
- PPT preparation

## 5. Demo Result
- Data dictionary and missing-value summary
- EDA figures
- Baseline metrics table
- Best-model summary by toxin target

## 6. Limitations and Next Steps
- Small repeated-measure dataset
- `Acid` target requires domain confirmation
- Future improvement: grouped CV and stronger interpretability
