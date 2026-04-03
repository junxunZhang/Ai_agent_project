# Hemodialysis Toxin Estimation Baseline Project

This repository is an interview-homework-style, reproducible Python project for baseline clinical regression on hemodialysis data. It uses optoelectronic absorbance features, dialysis machine parameters, and patient context to estimate multiple toxin targets.

## Project goal

Build an end-to-end analysis package around `shin_clinical_data.xlsx` that demonstrates:

- dataset inspection and schema verification
- data dictionary generation
- safe cleaning and analysis-ready dataset construction
- exploratory data analysis
- expanded baseline modeling with all five absorbance wavelengths
- systematic feature selection and before/after comparison
- metrics reporting and figure generation
- AI-agent-assisted workflow documentation
- PPT-ready interview materials

## Verified dataset scope

The workbook contains two sheets:

- `刪除異常值`
- `ALL DATA`

The primary analysis sheet is **`刪除異常值`** because it includes all six candidate toxin targets needed by the research context.

### Verified toxin-target mapping

Paper targets:

1. urea nitrogen
2. creatinine
3. uric acid
4. beta-2 microglobulin
5. phosphorus
6. potassium

Workbook mapping:

- `Urea` → direct match to urea / urea nitrogen context
- `Creatinine` → direct match
- `Potassium` → direct match
- `Phosphorus` → direct match
- `β2-microglobulin` → direct match
- `Acid` → cautiously treated as the workbook counterpart to the paper's uric acid target, but documented as an inferred mapping rather than a guaranteed semantic identity

## Expanded modeling scope

This version uses the full optoelectronic wavelength set:

- `255nm`
- `275nm`
- `285nm`
- `295nm`
- `310nm`

It also includes all verified dialysis machine parameters:

- `靜脈壓`
- `膜內外壓`
- `動脈流速`
- `每小時脫水量`
- `目標脫水量`
- `當前脫水量`
- `當前藥水流速`
- `藥水離子濃度`

### Feature sets compared

1. **Feature Set A**: all five absorbance features only
2. **Feature Set B**: all five absorbance features + all machine parameters
3. **Feature Set C**: all five absorbance features + all machine parameters + personalized features

### Models

- Main baseline: **SVR**
- Comparison models:
  - **Linear Regression**
  - **Random Forest Regressor**
  - **KNN Regressor**

### Feature selection

Systematic feature selection is included using:

- **mutual information regression** for candidate selection
- **permutation importance** for importance ranking on selected features

The project compares **full features vs selected features** under five-fold cross-validation.

## Key result summary

The expanded full-feature models generally outperform absorbance-only models.

Representative best results in the expanded model comparison:

- `urea`: **SVR**, all absorbance + machine + personal, **R² ≈ 0.938**
- `creatinine`: **SVR**, all absorbance + machine + personal, **R² ≈ 0.903**
- `acid_inferred_uric_acid`: **SVR**, all absorbance + machine + personal, **R² ≈ 0.914**
- `phosphorus`: **SVR**, all absorbance + machine + personal, **R² ≈ 0.876**
- `potassium`: **KNN Regressor**, all absorbance + machine + personal, **R² ≈ 0.685**
- `beta2_microglobulin`: **KNN Regressor**, selected absorbance + machine + personal subset, **R² ≈ 0.872**

Important note: the current mutual-information-based selected subsets improve interpretability, but they **do not consistently outperform the full feature models** across all targets. However, selected subsets do help certain targets, especially `beta2_microglobulin` in the expanded model comparison.

## Project structure

```text
Ai_agent_project/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
├── src/
├── tests/
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── docs/
├── ppt/
└── assets/
```

## Main output artifacts

### Tables

- `outputs/tables/data_dictionary.csv`
- `outputs/tables/missing_values.csv`
- `outputs/tables/session_summary.csv`
- `outputs/tables/baseline_results.csv`
- `outputs/tables/selected_feature_results.csv`
- `outputs/tables/feature_selection_summary.csv`
- `outputs/tables/selected_features_by_target.csv`
- `outputs/tables/model_comparison_full_vs_selected.csv`
- `outputs/tables/feature_importance_by_target.csv`
- `outputs/tables/best_model_summary.csv`

### Figures

- `outputs/figures/feature_importance_by_target.png`
- `outputs/figures/feature_selection_comparison.png`
- `outputs/figures/full_feature_correlation_heatmap.png`
- `outputs/figures/model_comparison_r2.png`
- `outputs/figures/session_prediction_curves_best_models.png`
- `outputs/figures/core_wavelength_regression_grid.png`

### Reports

- `outputs/reports/data_dictionary_inference.md`
- `outputs/reports/dataset_profile.md`
- `outputs/reports/analysis_summary.md`
- `outputs/reports/feature_selection_report.md`
- `outputs/reports/final_comparison_report.md`
- `outputs/reports/limitations_and_next_steps.md`

## Setup

Use the Python environment that has the required scientific packages installed.

```bash
python3 -m pip install -r requirements.txt
```

## How to run

```bash
python -m src.main
```

Planned behavior:

- read the Excel workbook
- profile the dataset
- clean and prepare analysis-ready data
- run full-feature and selected-feature models
- save figures, reports, and metric tables under `outputs/`

## AI-agent contribution

This project explicitly demonstrates AI-agent assistance in:

- requirement analysis
- dataset inspection
- schema verification
- code scaffolding
- code generation
- debugging and testing
- report writing
- visualization generation
- presentation content preparation

See `docs/agent_workflow.md` for the full workflow.

## Notes and limitations

- `Acid` is mapped cautiously to the paper's uric acid target and should be presented as an inferred match.
- The dataset contains repeated time points within dialysis sessions, so interpretation should respect session structure.
- Feature selection improves interpretability, but in this baseline run it does not consistently improve predictive performance over the full feature sets.
