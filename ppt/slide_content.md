# Detailed Slide Content

---

## Slide 1 — Title / Project Overview

### Slide title
AI-Assisted Hemodialysis Toxin Estimation: From Research Reproduction to Methodological Correction

### Slide purpose
Introduce the project, define the domain, and make clear that this is not only a modeling exercise but also a reproducible AI-agent-assisted engineering and validation workflow.

### Key message
This project started as a reproduction-style hemodialysis toxin prediction baseline and evolved into a deeper methodological audit of how such models should actually be evaluated.

### Speaker explanation / talking points
- This homework project uses the provided hemodialysis clinical dataset to estimate multiple toxin targets from optoelectronic absorbance signals and dialysis context.
- OpenClaw was used across the full lifecycle: requirement analysis, schema inspection, code generation, debugging, testing, figure revision, protocol correction, and presentation preparation.
- The final result is not only a predictive baseline, but also a corrected evaluation workflow with clear separation between exploratory benchmarking and final trustworthy test evidence.

### Linked figures / tables / reports
- `README.md`
- `outputs/reports/methodology_correction_report.md`

### Interpretation notes
This slide sets expectations that the presentation will show both modeling results and the debugging/correction process.

### Caution / limitation notes
Do not oversell this as a production medical device. It is an interview-homework baseline and methodological case study.

---

## Slide 2 — Clinical Background and Motivation

### Slide title
Clinical Background: Why Predict Uremic Toxins During Hemodialysis?

### Slide purpose
Explain the clinical motivation for real-time or near-real-time toxin estimation during dialysis.

### Key message
Conventional biochemical measurement is accurate but slow and discontinuous; an optical sensing + ML approach could make toxin estimation more continuous, faster, and more operationally useful.

### Speaker explanation / talking points
- Hemodialysis treatment removes multiple toxins, but direct blood assays are not continuously available during treatment.
- The prior study used spent dialysate optical sensing to estimate toxin concentration indirectly.
- This motivates a structured regression problem: can we estimate toxin-related variables from absorbance features plus clinical treatment context?

### Linked figures / tables / reports
- `outputs/reports/final_comparison_report.md`

### Interpretation notes
Anchor the audience in the application problem before talking about ML details.

### Caution / limitation notes
This project does not replace lab assays; it studies prediction feasibility.

---

## Slide 3 — Problem Statement

### Slide title
Problem Statement

### Slide purpose
State the task precisely and define the prediction targets.

### Key message
The project aims to estimate six toxin-related targets from structured tabular clinical data collected during hemodialysis.

### Speaker explanation / talking points
- The problem is multivariate clinical regression.
- Targets include:
  - urea
  - creatinine
  - potassium
  - phosphorus
  - beta-2 microglobulin
  - `Acid`, treated cautiously as the workbook counterpart of uric acid
- The challenge is that the dataset contains repeated time points within sessions, mixed feature types, and possible schema ambiguity.

### Linked figures / tables / reports
- `docs/problem_statement.md`
- `outputs/reports/data_dictionary_inference.md`

### Interpretation notes
Use this slide to make clear that the task was verified from the real workbook rather than assumed from the paper alone.

### Caution / limitation notes
Be explicit that `Acid` is an inferred mapping, not a fully confirmed label.

---

## Slide 4 — Research Goal and Expected Outcome

### Slide title
Research Goal and Expected Outcome

### Slide purpose
Define what success looks like in this homework setting.

### Key message
The goal was not only to train a predictive model, but to produce a reproducible, GitHub-ready, presentation-ready workflow with clear validation logic.

### Speaker explanation / talking points
- Expected outputs included code, tests, figures, reports, PPT materials, and demo scripts.
- The project needed to be realistic for a 2–3 hour interview-homework framing, yet still demonstrate end-to-end AI-agent assistance.
- A major final expectation became methodological trustworthiness: not just good-looking plots, but correct separation between train, validation, and test evidence.

### Linked figures / tables / reports
- `README.md`
- `docs/agent_workflow.md`

### Interpretation notes
This slide reframes the project as both a technical deliverable and a scientific reasoning exercise.

### Caution / limitation notes
The initial goal evolved during debugging; this is a strength, not a weakness.

---

## Slide 5 — Original Experiment Design from Prior Study

### Slide title
What the Prior Study Did

### Slide purpose
Summarize the starting reference methodology from the prior document.

### Key message
The paper provided a useful starting point: SVR-centered modeling with core absorbance wavelengths and personalized features.

### Speaker explanation / talking points
- The prior study emphasized three wavelengths: 255nm, 275nm, and 310nm.
- It presented SVR as the best baseline in that setting.
- It also emphasized that absorbance features are essential and personalized features improve performance.
- The paper showed predicted concentration curves and predicted-vs-actual relationship plots, which strongly influenced the initial design direction.

### Linked figures / tables / reports
- `outputs/reports/final_comparison_report.md`

### Interpretation notes
This slide shows respect for the original study while setting up why implementation-time auditing was still necessary.

### Caution / limitation notes
The paper narrative is a clean research story; implementation often reveals hidden assumptions.

---

## Slide 6 — Dataset Verification and Real Workbook Schema

### Slide title
Dataset Verification: What the Real Workbook Actually Contains

### Slide purpose
Show that the project began from direct workbook inspection rather than assumptions.

### Key message
The real workbook differs in important ways from the simplified story in the paper, especially in feature availability.

### Speaker explanation / talking points
- The main usable sheet is `刪除異常值`.
- The workbook contains repeated session measurements keyed by patient/date/time structure.
- The dataset includes all six target columns and multiple structured feature groups.
- This step was crucial because downstream modeling choices depend on what the workbook truly contains.

### Linked figures / tables / reports
- `outputs/reports/data_dictionary_inference.md`
- `outputs/tables/data_dictionary.csv`
- `outputs/tables/session_summary.csv`

### Interpretation notes
This slide justifies the entire downstream pipeline as data-driven rather than assumption-driven.

### Caution / limitation notes
Any ambiguity in schema should be called out early, not hidden until later.

---

## Slide 7 — Feature Design: Optical, Machine, and Personal Features

### Slide title
Feature Design Beyond the Original Three-Wavelength Story

### Slide purpose
Explain how the feature space was defined from the verified dataset.

### Key message
The project expanded beyond the three core wavelengths because the workbook clearly contains five absorbance wavelengths plus machine and personal context.

### Speaker explanation / talking points
- Five wavelengths available:
  - 255nm
  - 275nm
  - 285nm
  - 295nm
  - 310nm
- Dialysis machine variables include pressure, flow, and ultrafiltration-related variables.
- Personal features include age, dry weight, membrane area, and dialysis-related context.
- Three feature sets were used:
  1. absorbance only
  2. absorbance + machine
  3. absorbance + machine + personal

### Linked figures / tables / reports
- `outputs/tables/feature_metadata.csv`
- `outputs/figures/full_feature_correlation_heatmap.png`

### Interpretation notes
This slide explains why the final implementation is broader than the paper.

### Caution / limitation notes
More features do not automatically mean better generalization; that had to be tested.

---

## Slide 8 — Modeling Workflow and OpenClaw Collaboration Flow

### Slide title
How the Modeling Workflow Was Built with OpenClaw

### Slide purpose
Show the AI-agent-assisted workflow across the full project lifecycle.

### Key message
OpenClaw was not used only for code generation; it was used as a working partner for iterative design, debugging, verification, and reporting.

### Speaker explanation / talking points
- Workflow stages included:
  - requirement parsing
  - workbook inspection
  - project scaffolding
  - pipeline implementation
  - testing
  - result review
  - figure correction
  - methodology correction
  - report writing
  - PPT preparation
- This is important because the project changed materially as issues were discovered.

### Linked figures / tables / reports
- `docs/agent_workflow.md`
- `outputs/reports/correction_audit_report.md`

### Interpretation notes
Explain that collaboration here means iterative debugging, not one-shot auto-generation.

### Caution / limitation notes
Emphasize that human oversight remained critical, especially when identifying evaluation flaws.

---

## Slide 9 — Early Baseline Results and Why They Were Not Enough

### Slide title
Early Baselines: Useful, But Not Yet Trustworthy Enough

### Slide purpose
Explain what the early pipeline achieved and why that was still insufficient.

### Key message
The initial multi-model and feature-selection pipeline produced strong-looking results, but later review revealed that some evaluation artifacts were not methodologically strong enough to treat as final evidence.

### Speaker explanation / talking points
- Early comparisons included SVR, linear regression, random forest, and KNN.
- Feature selection was added via mutual information and permutation importance.
- Several early results looked strong and presentation-ready.
- However, later review showed that result quality is not only about metrics — the evaluation protocol matters just as much.

### Linked figures / tables / reports
- `outputs/tables/best_model_summary.csv`
- `outputs/figures/model_comparison_r2.png`
- `outputs/reports/analysis_summary.md`

### Interpretation notes
Use this slide to transition into the debugging story.

### Caution / limitation notes
These earlier outputs remain useful for traceability, but not all are final evidence.

---

## Slide 10 — Key Issue 1: Output Interpretation Problems in Early Figures

### Slide title
Issue 1: Early Predicted-vs-Actual Figures Were Visually Misleading

### Slide purpose
Explain the first major interpretation problem uncovered during collaboration.

### Key message
A figure can look scientific while still mixing incompatible concepts, especially when scatter-fit R² is confused with formal cross-validation R².

### Speaker explanation / talking points
- An earlier predicted-vs-actual panel used scatter-fit style annotation that was easy to confuse with formal model evaluation.
- This created a mismatch between plot-level R² and CV-level R².
- The correction was to redesign the figure using clearer actual-vs-predicted framing and later to separate grouped-CV evidence from final test evidence.

### Linked figures / tables / reports
- `outputs/reports/final_comparison_report.md`
- `outputs/reports/correction_audit_report.md`

### Interpretation notes
Explain that this was not merely a cosmetic issue; it affected scientific interpretation.

### Caution / limitation notes
A strong-looking figure is not necessarily a valid evaluation artifact.

---

## Slide 11 — Key Issue 2: Session-Level Leakage and Unsafe Evaluation Logic

### Slide title
Issue 2: Session-Level Leakage Risk

### Slide purpose
Explain why row-level or train-on-seen-session logic is unsafe for repeated dialysis measurements.

### Key message
Because the data contain repeated measurements within HD sessions, splitting by row can leak session structure and inflate performance.

### Speaker explanation / talking points
- A dialysis session contains multiple related rows over time.
- If rows from one session leak across train and test folds, the model sees correlated information during training.
- This is especially dangerous in quasi-clinical settings because it creates optimistic performance estimates.
- The first correction was to use grouped unseen-session evaluation with `session_id` grouping.

### Linked figures / tables / reports
- `outputs/reports/evaluation_protocol_fix.md`
- `outputs/tables/grouped_unseen_session_results.csv`

### Interpretation notes
This slide explains why session-level grouping became mandatory.

### Caution / limitation notes
Grouped unseen-session evaluation improved things, but it still was not the final protocol if unseen-session performance was then used for model choice.

---

## Slide 12 — Key Issue 3: Test-Set Model Selection Problem

### Slide title
Issue 3: Using Unseen-Session Results to Choose the Best Model

### Slide purpose
Explain the deeper methodological problem that remained even after grouped unseen-session CV was introduced.

### Key message
If unseen-session performance is used to compare models and choose the winner, then the test side is no longer a pure final evaluation set.

### Speaker explanation / talking points
- Grouped unseen-session CV was a valuable correction, but it was still exploratory if those results were used for model choice.
- This is a classic selection-bias problem.
- The right protocol is:
  - train for fitting
  - validation for model selection / tuning / feature selection
  - test only once for final evaluation

### Linked figures / tables / reports
- `outputs/reports/methodology_correction_report.md`
- `outputs/reports/correction_audit_report.md`

### Interpretation notes
This is one of the most important conceptual slides in the whole deck.

### Caution / limitation notes
Do not treat exploratory benchmarking as final generalization evidence.

---

## Slide 13 — Corrected Final Evaluation Protocol

### Slide title
Final Corrected Protocol: Train / Validation / Test at the Session Level

### Slide purpose
Present the final trustworthy evaluation design.

### Key message
The final protocol fixes the model-selection bias by separating train, validation, and test at the session level.

### Speaker explanation / talking points
- Final session split:
  - train: 18 sessions
  - validation: 6 sessions
  - test: 6 sessions
- Train only:
  - model fitting
  - feature selection
  - tuning
- Validation only:
  - model comparison
  - winner selection
- Test only:
  - final one-time evaluation
- All splitting is based on `session_id`.

### Linked figures / tables / reports
- `outputs/reports/methodology_correction_report.md`
- `outputs/tables/model_selection_validation_sessions_v1.csv`
- `outputs/tables/best_model_selection_validation_sessions_v1.csv`

### Interpretation notes
This is the slide that establishes which outputs are final and trustworthy.

### Caution / limitation notes
This final protocol uses one fixed session-level split, so another split could produce different values.

---

## Slide 14 — Final Model Selection Results

### Slide title
Model Selection Results from Validation Only

### Slide purpose
Show how the final best model for each toxin was selected under the corrected protocol.

### Key message
The winning model per toxin is now chosen using validation performance only, not test performance.

### Speaker explanation / talking points
- This slide should show the validation-side selection outputs.
- Explain that this is the only stage where model comparison and winner selection are allowed.
- The selected model per toxin is then frozen before any final test evaluation.

### Linked figures / tables / reports
- `outputs/tables/model_selection_validation_sessions_v1.csv`
- `outputs/tables/best_model_selection_validation_sessions_v1.csv`

### Interpretation notes
This slide separates “which model won?” from “how good is the final test result?”

### Caution / limitation notes
Validation performance is not the final test claim; it is the selection basis only.

---

## Slide 15 — Final Trustworthy Evaluation Figures

### Slide title
Final Held-Out Test Evidence

### Slide purpose
Present the final test-only evaluation outputs that should be treated as the main trustworthy evidence.

### Key message
The final figures on this slide use the corrected session-level train/validation/test workflow and should be treated as the primary evaluation evidence.

### Speaker explanation / talking points
- Show:
  - `predicted_vs_actual_panels_trainvaltest_sessions_v1.png`
  - `session_prediction_curves_test_sessions_v1.png`
  - `model_comparison_r2_trainvaltest_sessions_v1.png`
- Explain that these were generated only after the best model per toxin was chosen on validation data.
- Test sessions were not used in model selection.

### Linked figures / tables / reports
- `outputs/figures/predicted_vs_actual_panels_trainvaltest_sessions_v1.png`
- `outputs/figures/session_prediction_curves_test_sessions_v1.png`
- `outputs/figures/model_comparison_r2_trainvaltest_sessions_v1.png`
- `outputs/tables/test_results_trainvaltest_sessions_v1.csv`

### Interpretation notes
This is the strongest “final result” slide in the deck.

### Caution / limitation notes
This is still a small-session dataset; results are more trustworthy than earlier versions, but not final clinical truth.

---

## Slide 16 — Discussion, Limitations, and What Changed vs the Paper

### Slide title
Discussion: What Changed Relative to the Original Research Story?

### Slide purpose
Compare the final implementation against the paper and explain what was learned.

### Key message
The implementation confirmed the value of optical and contextual features, but also showed that rigorous evaluation and deployment-aware logic matter as much as model choice.

### Speaker explanation / talking points
- Compared with the paper, this project:
  - used five wavelengths instead of only three
  - benchmarked multiple models instead of assuming one winner globally
  - surfaced evaluation and figure-interpretation issues during implementation
  - added reproducible code, tests, saved models, audit reports, and versioned outputs
- The paper gives a clean proof-of-concept story.
- The implementation shows how many methodological choices matter when turning that story into a robust workflow.

### Linked figures / tables / reports
- `outputs/reports/final_comparison_report.md`
- `outputs/reports/methodology_correction_report.md`
- `outputs/reports/correction_audit_report.md`

### Interpretation notes
This slide should feel reflective and mature, not defensive.

### Caution / limitation notes
Avoid implying the paper was “wrong”; say that implementation exposed additional rigor requirements.

---

## Slide 17 — Reflection, Learnings, and Final Takeaway

### Slide title
Reflection and Final Takeaway

### Slide purpose
Close the presentation with the most important lessons from the full OpenClaw collaboration.

### Key message
The project’s final value is not only the model outputs, but the way the workflow became more trustworthy through debugging, challenge, and correction.

### Speaker explanation / talking points
- OpenClaw helped not just by generating code, but by accelerating iteration across:
  - data verification
  - pipeline building
  - figure revision
  - methodological debugging
  - reporting
  - presentation preparation
- The biggest lesson is that good ML work requires both prediction quality and evaluation discipline.
- The final outcome is a reproducible, GitHub-ready, presentation-ready project that documents not only the result, but how the result became more trustworthy.

### Linked figures / tables / reports
- `outputs/reports/methodology_correction_report.md`
- `outputs/reports/correction_audit_report.md`
- `assets/demo_script_5min.md`

### Interpretation notes
End on the learning value and rigor story, not just a score table.

### Caution / limitation notes
The strongest final claim is: “this is a more trustworthy workflow than the early versions,” not “this is clinically deployable today.”
