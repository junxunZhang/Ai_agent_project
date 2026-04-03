# Hemodialysis Toxin Estimation Baseline Project

This repository is an interview-homework-style, reproducible Python project for baseline clinical regression on hemodialysis data. It uses optoelectronic absorbance features, patient context, and dialysis machine parameters to estimate multiple toxin targets.

## Project goal

Build an end-to-end analysis package around `shin_clinical_data.xlsx` that demonstrates:

- dataset inspection and schema verification
- data dictionary generation
- safe cleaning and analysis-ready dataset construction
- exploratory data analysis
- baseline modeling with five-fold cross-validation
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

## Planned modeling comparison

Two feature settings are emphasized:

1. **Absorbance-only**
   - core wavelengths: `255nm`, `275nm`, `310nm`
2. **Absorbance + personalized + machine features**
   - core wavelengths plus verified structured covariates

Main baseline:

- **Support Vector Regression (SVR)**

Evaluation:

- five-fold cross-validation
- MAE
- MSE
- RMSE
- R²

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

## Current deliverables

- verified problem statement
- agent workflow documentation
- data dictionary report
- project scaffolding
- baseline pipeline source code
- tests
- reproducible outputs and figures
- PPT-ready markdown materials

## Setup

Use the Python environment that has the required scientific packages installed.

Example:

```bash
python3 -m pip install -r requirements.txt
```

## How to run

After implementation is complete, the intended command will be:

```bash
python -m src.main
```

Planned behavior:

- read the Excel workbook
- profile the dataset
- clean and prepare analysis-ready data
- run baseline models
- save figures, reports, and metric tables under `outputs/`

## Output artifacts

Expected outputs include:

- `outputs/tables/data_dictionary.csv`
- `outputs/tables/missing_values.csv`
- `outputs/tables/session_summary.csv`
- `outputs/tables/baseline_results.csv`
- `outputs/tables/best_model_summary.csv`
- `outputs/reports/data_dictionary_inference.md`
- `outputs/reports/dataset_profile.md`
- `outputs/reports/analysis_summary.md`
- `outputs/figures/*.png`

## AI-agent contribution

This project explicitly demonstrates AI-agent assistance in:

- requirement analysis
- dataset inspection
- schema verification
- code scaffolding
- code generation
- debugging and testing
- report writing
- presentation content preparation

See `docs/agent_workflow.md` for the full workflow.

## Notes and limitations

- `Acid` is mapped cautiously to the paper's uric acid target and should be presented as an inferred match.
- This project aims for a strong, interview-ready baseline, not exhaustive model optimization.
- The dataset contains repeated time points within dialysis sessions, so interpretation should respect session structure.
