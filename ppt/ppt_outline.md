# Final PPT Structure

## Total slides: 17

1. Title / Project Overview
2. Clinical Background and Motivation
3. Problem Statement
4. Research Goal and Expected Outcome
5. Original Experiment Design from Prior Study
6. Dataset Verification and Real Workbook Schema
7. Feature Design: Optical, Machine, and Personal Features
8. Modeling Workflow and OpenClaw Collaboration Flow
9. Early Baseline Results and Why They Were Not Enough
10. Key Issue 1: Output Interpretation Problems in Early Figures
11. Key Issue 2: Session-Level Leakage and Unsafe Evaluation Logic
12. Key Issue 3: Test-Set Model Selection Problem
13. Corrected Final Evaluation Protocol
14. Final Model Selection Results
15. Final Trustworthy Evaluation Figures
16. Discussion, Limitations, and What Changed vs the Paper
17. Reflection, Learnings, and Final Takeaway

## Presentation logic

This deck is intentionally structured as a project story rather than a flat methods summary:

- what the original problem was
- what the prior paper did
- what the real dataset actually looked like
- how the pipeline was built
- what went wrong during implementation
- how each issue was detected and corrected
- what the final trustworthy evidence is
- what was learned from the debugging and correction process

## Core visual groups used in the deck

### Reports
- `outputs/reports/data_dictionary_inference.md`
- `outputs/reports/analysis_summary.md`
- `outputs/reports/feature_selection_report.md`
- `outputs/reports/final_comparison_report.md`
- `outputs/reports/evaluation_protocol_fix.md`
- `outputs/reports/correction_audit_report.md`
- `outputs/reports/methodology_correction_report.md`

### Tables
- `outputs/tables/best_model_summary.csv`
- `outputs/tables/grouped_unseen_session_results.csv`
- `outputs/tables/best_model_summary_grouped_unseen_sessions.csv`
- `outputs/tables/model_selection_validation_sessions_v1.csv`
- `outputs/tables/best_model_selection_validation_sessions_v1.csv`
- `outputs/tables/test_results_trainvaltest_sessions_v1.csv`
- `outputs/tables/feature_selection_summary.csv`
- `outputs/tables/selected_features_by_target.csv`

### Figures
- `outputs/figures/full_feature_correlation_heatmap.png`
- `outputs/figures/feature_importance_by_target.png`
- `outputs/figures/feature_selection_comparison.png`
- `outputs/figures/model_comparison_r2_grouped_unseen_sessions_v2.png`
- `outputs/figures/predicted_vs_actual_panels_grouped_unseen_sessions_v3.png`
- `outputs/figures/session_prediction_curves_unseen_sessions.png`
- `outputs/figures/model_comparison_r2_trainvaltest_sessions_v1.png`
- `outputs/figures/predicted_vs_actual_panels_trainvaltest_sessions_v1.png`
- `outputs/figures/session_prediction_curves_test_sessions_v1.png`

## Additional PPT export still useful

No new scientific figures are strictly required to tell the story.

Optional polish items if you want a prettier final deck later:
- crop individual panels out of composite figures for larger slide readability
- convert key tables into cleaner PowerPoint-native summary tables
- create one comparison slide with side-by-side “exploratory grouped-CV” vs “final held-out test” visuals
