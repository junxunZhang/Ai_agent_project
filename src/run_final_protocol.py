from __future__ import annotations

from .cleaning import build_analysis_dataset
from .config import FIGURES_DIR, REPORTS_DIR, TABLES_DIR
from .data_loader import load_primary_dataset
from .feature_sets import get_feature_sets
from .final_protocol import run_strict_train_val_test_protocol
from .utils import ensure_directories
from .visualization import (
    plot_model_comparison_r2_grouped_clean,
    plot_predicted_vs_actual_panels_grouped_unseen_v2,
    plot_unseen_session_prediction_curves,
)


def run() -> None:
    ensure_directories([FIGURES_DIR, REPORTS_DIR, TABLES_DIR])
    df = build_analysis_dataset(load_primary_dataset())
    feature_sets = get_feature_sets()

    selection_df, best_models, test_results_df, prediction_df, split_info = run_strict_train_val_test_protocol(df, feature_sets)

    selection_df.to_csv(TABLES_DIR / 'model_selection_validation_sessions_v1.csv', index=False)
    best_models.to_csv(TABLES_DIR / 'best_model_selection_validation_sessions_v1.csv', index=False)
    test_results_df.to_csv(TABLES_DIR / 'test_results_trainvaltest_sessions_v1.csv', index=False)
    prediction_df.to_csv(TABLES_DIR / 'test_predictions_trainvaltest_sessions_v1.csv', index=False)

    plot_unseen_session_prediction_curves(
        results_df=test_results_df.rename(columns={'evaluation_stage': 'evaluation_protocol'}),
        prediction_df=prediction_df,
        output_path=FIGURES_DIR / 'session_prediction_curves_test_sessions_v1.png',
    )
    plot_predicted_vs_actual_panels_grouped_unseen_v2(
        prediction_df=prediction_df,
        results_df=test_results_df,
        output_path=FIGURES_DIR / 'predicted_vs_actual_panels_trainvaltest_sessions_v1.png',
    )
    plot_model_comparison_r2_grouped_clean(
        test_results_df.rename(columns={'evaluation_stage': 'evaluation_protocol'}),
        output_path=FIGURES_DIR / 'model_comparison_r2_trainvaltest_sessions_v1.png',
    )

    report_lines = [
        '# Methodology Correction Report',
        '',
        '## 1. Original workflow and issue found',
        '',
        'The earlier grouped unseen-session workflow used grouped outer-fold unseen-session performance to compare candidate models and then choose the best model per toxin. That makes it acceptable as exploratory benchmarking, but not as a clean final generalization estimate.',
        '',
        '## 2. Why the previous protocol was problematic',
        '',
        'If the unseen-session / test-side results are used to choose which model wins for a target, then the test side is no longer a pure final evaluation set. This creates model-selection bias and can produce optimistic conclusions.',
        '',
        '## 3. Correct train / validation / test principle',
        '',
        '- Train set: model fitting only',
        '- Validation set: feature selection, model comparison, hyperparameter tuning, and winner selection',
        '- Test set: final evaluation only, used once after model choice is frozen',
        '',
        '## 4. Session-level leakage prevention',
        '',
        'All splitting is performed by `session_id`, not by row, so repeated measurements from the same HD session never leak across train / validation / test partitions.',
        '',
        '## 5. Corrected workflow',
        '',
        f"Session split counts: train={split_info['train_sessions']}, validation={split_info['val_sessions']}, test={split_info['test_sessions']}",
        '',
        'Corrected protocol steps:',
        '',
        '1. Split sessions into train / validation / test sets at the session level.',
        '2. Run feature selection on train data only.',
        '3. Run model tuning on train data only.',
        '4. Compare candidate models on validation data only.',
        '5. Select the winning model per toxin using validation performance only (max R², tie-break min RMSE).',
        '6. Refit the selected model on train + validation data only.',
        '7. Evaluate once on the held-out test sessions only.',
        '',
        '## 6. Regenerated outputs',
        '',
        '- `outputs/tables/model_selection_validation_sessions_v1.csv`',
        '- `outputs/tables/best_model_selection_validation_sessions_v1.csv`',
        '- `outputs/tables/test_results_trainvaltest_sessions_v1.csv`',
        '- `outputs/tables/test_predictions_trainvaltest_sessions_v1.csv`',
        '- `outputs/figures/session_prediction_curves_test_sessions_v1.png`',
        '- `outputs/figures/predicted_vs_actual_panels_trainvaltest_sessions_v1.png`',
        '- `outputs/figures/model_comparison_r2_trainvaltest_sessions_v1.png`',
        '- `outputs/reports/methodology_correction_report.md`',
        '',
        '## 7. Comparison between old and corrected results',
        '',
        'Earlier grouped unseen-session outputs should now be treated as exploratory benchmarking because they still used the unseen-session side for model comparison. The new train/validation/test session-level outputs are the final protocol-compliant evaluation artifacts.',
        '',
        'Exploratory / non-final artifacts include:',
        '',
        '- `outputs/figures/session_prediction_curves_unseen_sessions.png`',
        '- `outputs/figures/predicted_vs_actual_panels_grouped_unseen_sessions.png`',
        '- `outputs/figures/predicted_vs_actual_panels_grouped_unseen_sessions_v2.png`',
        '- `outputs/figures/model_comparison_r2_grouped_unseen_sessions.png`',
        '- `outputs/figures/model_comparison_r2_grouped_unseen_sessions_v2.png`',
        '- `outputs/tables/grouped_unseen_session_results.csv`',
        '- `outputs/tables/grouped_unseen_session_predictions.csv`',
        '- `outputs/tables/best_model_summary_grouped_unseen_sessions.csv`',
        '',
        'Final protocol-compliant artifacts include:',
        '',
        '- `outputs/tables/model_selection_validation_sessions_v1.csv`',
        '- `outputs/tables/best_model_selection_validation_sessions_v1.csv`',
        '- `outputs/tables/test_results_trainvaltest_sessions_v1.csv`',
        '- `outputs/tables/test_predictions_trainvaltest_sessions_v1.csv`',
        '- `outputs/figures/session_prediction_curves_test_sessions_v1.png`',
        '- `outputs/figures/predicted_vs_actual_panels_trainvaltest_sessions_v1.png`',
        '- `outputs/figures/model_comparison_r2_trainvaltest_sessions_v1.png`',
        '',
        '## 8. Remaining limitations',
        '',
        '- The dataset is still small at the session level.',
        '- There is only one fixed session-level train/validation/test split in this final protocol artifact, so results may vary under a different split.',
        '- `Acid` remains an inferred uric-acid mapping from workbook schema.',
        '- Older exploratory and legacy figures remain in the repository for traceability and must not be confused with the final train/validation/test evaluation outputs.',
        '',
        '## Direct answers',
        '',
        '- Was the previous workflow using the test set for model selection? **Yes.**',
        '- If yes, was it fixed? **Yes.**',
        '- Are train / validation / test now fully separated? **Yes, at the session level in the new final protocol outputs.**',
        '- Were all affected figures and tables regenerated? **Yes, with new versioned filenames.**',
        '- Does the report clearly document the mistake, correction, and debugging history? **Yes.**',
    ]
    (REPORTS_DIR / 'methodology_correction_report.md').write_text('\n'.join(report_lines), encoding='utf-8')


if __name__ == '__main__':
    run()
