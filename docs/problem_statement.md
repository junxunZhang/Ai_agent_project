# Problem Statement

## Objective

Build a reproducible, interview-ready Python project that estimates six hemodialysis toxin measurements from optoelectronic absorbance signals and structured clinical context. The project should demonstrate an end-to-end AI-agent-assisted workflow covering dataset inspection, code generation, testing, analysis, reporting, and presentation preparation.

## Verified dataset context

The workbook `shin_clinical_data.xlsx` contains two sheets:

- `刪除異常值`
- `ALL DATA`

The primary analysis sheet is **`刪除異常值`**, because it includes all six candidate toxin targets required by the research context, including `Urea`.

### Verified target mapping

The prior study targets are:

1. urea nitrogen
2. creatinine
3. uric acid
4. beta-2 microglobulin
5. phosphorus
6. potassium

Verified mapping from workbook headers:

- `Urea` → direct dataset target corresponding to urea / urea nitrogen context
- `Creatinine` → direct dataset target
- `Potassium` → direct dataset target
- `Phosphorus` → direct dataset target
- `β2-microglobulin` → direct dataset target
- `Acid` → cautiously mapped to the paper's uric acid target based on workbook structure and elimination, but this remains an inferred mapping unless confirmed by a domain owner

### Verified feature groups

- **Absorbance features**: `255nm`, `275nm`, `285nm`, `295nm`, `310nm`
- **Core paper absorbance features**: `255nm`, `275nm`, `310nm`
- **Personalized features**: `透析年長`, `乾體重`, `身高`, `年齡`, `膜面積`, `透析日`
- **Dialysis machine features**: `靜脈壓`, `膜內外壓`, `動脈流速`, `每小時脫水量`, `目標脫水量`, `當前脫水量`, `當前藥水流速`, `藥水離子濃度`
- **Session keys**: `Date`, `Patient ID`, `Collection time`

## Problem definition

### Input

Structured tabular data from `shin_clinical_data.xlsx`, primarily the `刪除異常值` sheet, including:

- absorbance measurements at multiple wavelengths
- patient/personalized attributes
- dialysis machine parameters
- repeated session time points

### Output

A reproducible analysis package that produces:

- cleaned analysis-ready dataset
- data profiling outputs and data dictionary
- exploratory visualizations
- cross-validated baseline regression results for each target
- feature-set comparison tables
- summary reports and presentation-ready materials

## Modeling scope

To stay realistic for a 2–3 hour interview homework submission, the project will focus on pragmatic baseline modeling rather than exhaustive optimization.

### Planned baseline comparisons

1. **Absorbance-only**
   - core wavelengths: `255nm`, `275nm`, `310nm`
2. **Absorbance + personalized + machine features**
   - core wavelengths plus verified structured covariates

### Planned models

- Main baseline: **Support Vector Regression (SVR)**
- Comparison baseline: a simpler conventional regressor such as **Linear Regression** or **Random Forest** if feasible within time

The baseline will be implemented as **per-target regression**, one model per toxin target.

## Evaluation metrics

The project will use **five-fold cross-validation** and report:

- MAE
- MSE
- RMSE
- R²

Outputs will be exported into deterministic tables and presentation-ready summaries.

## Assumptions

- `刪除異常值` is the most suitable primary sheet because it retains the required target columns.
- `Acid` is the best available workbook match for the paper's uric acid target, but this is documented as an inference.
- Missing values can be handled conservatively using model-pipeline imputation instead of aggressive row deletion.
- Repeated rows across time points are meaningful dialysis measurements, not duplicates to be removed.
- Outliers should be profiled and documented before any filtering; not all extreme values are errors because patient heterogeneity is clinically plausible.

## Limitations

- Small sample size and repeated-measure structure may limit generalization.
- The workbook does not explicitly label `Acid` as uric acid.
- Some patient-level fields appear inconsistent across records and will require cautious treatment.
- Five-fold CV on repeated clinical sessions may still mix correlated samples unless grouped CV is added later as an extension.
- This submission is intended as a robust baseline and demo-friendly analysis package, not a production clinical model.

## Success criteria

The homework submission is considered successful if it:

- clearly defines the clinical regression problem
- verifies dataset-to-paper mapping rather than inventing schema
- builds a reproducible Python baseline pipeline
- generates figures, metrics tables, and concise reports
- includes tests, documentation, and PPT-ready content
- demonstrates visible AI-agent assistance across the full workflow
