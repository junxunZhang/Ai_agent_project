from __future__ import annotations

import pandas as pd

from .cleaning import build_analysis_dataset
from .data_loader import load_primary_dataset
from .feature_sets import get_feature_sets
from .group_evaluation import run_grouped_unseen_session_evaluation
from .utils import ensure_directories
from .config import FIGURES_DIR, REPORTS_DIR, TABLES_DIR
from .visualization import plot_unseen_session_prediction_curves


def run() -> None:
    ensure_directories([FIGURES_DIR, REPORTS_DIR, TABLES_DIR])
    raw_df = load_primary_dataset()
    df = build_analysis_dataset(raw_df)
    feature_sets = get_feature_sets()

    grouped_results, prediction_df = run_grouped_unseen_session_evaluation(df, feature_sets)
    grouped_results.to_csv(TABLES_DIR / 'grouped_unseen_session_results.csv', index=False)
    prediction_df.to_csv(TABLES_DIR / 'grouped_unseen_session_predictions.csv', index=False)

    plot_unseen_session_prediction_curves(grouped_results, prediction_df)

    grouped_best = (
        grouped_results.sort_values(['target', 'R2', 'RMSE'], ascending=[True, False, True])
        .groupby('target', as_index=False)
        .head(1)
        .reset_index(drop=True)
    )
    grouped_best.to_csv(TABLES_DIR / 'best_model_summary_grouped_unseen_sessions.csv', index=False)

    fig_path = FIGURES_DIR / 'model_comparison_r2_grouped_unseen_sessions.png'
    plot_df = grouped_results.copy()
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=plot_df, x='target', y='R2', hue='model', ax=ax)
    ax.set_title('Model Comparison by Target (R²) — Grouped Unseen Sessions')
    ax.set_ylim(min(plot_df['R2'].min() - 0.1, -1), 1)
    fig.tight_layout()
    fig.savefig(fig_path, dpi=220)
    plt.close(fig)

    audit_lines = [
        '# Evaluation Protocol Fix',
        '',
        '## Issue',
        '',
        'The original `session_prediction_curves_best_models` figure could be interpreted as evaluating models on sessions that were already seen during training. That makes it unsuitable as a strict validation artifact and risks optimistic interpretation.',
        '',
        '## Fix applied',
        '',
        '- Kept the old figure unchanged for traceability.',
        '- Generated a new figure with a new filename: `session_prediction_curves_unseen_sessions.png`.',
        '- Switched evaluation to **GroupKFold session-level splitting** using `session_id` as the grouping key.',
        '- Performed feature selection inside the training folds only.',
        '- Performed model tuning inside training data only, using grouped inner validation splits.',
        '- Generated prediction curves from grouped cross-validation outputs so each plotted session segment comes from unseen-session predictions.',
        '- Avoided visually cherry-picking the best-looking session by using a middle-ranked session by per-session MSE for each target/model combination shown.',
        '- Added grouped unseen-session summary artifacts so corrected performance outputs are clearly separated from older row-level artifacts.',
        '',
        '## Corrected evaluation outputs',
        '',
        '- `outputs/figures/session_prediction_curves_unseen_sessions.png`',
        '- `outputs/figures/model_comparison_r2_grouped_unseen_sessions.png`',
        '- `outputs/tables/grouped_unseen_session_results.csv`',
        '- `outputs/tables/grouped_unseen_session_predictions.csv`',
        '- `outputs/tables/best_model_summary_grouped_unseen_sessions.csv`',
        '',
        '## Legacy artifacts to treat with caution',
        '',
        '- `outputs/figures/session_prediction_curves_best_models.png` is retained only as a demo-style artifact, not strict validation evidence.',
        '- Earlier row-level comparison outputs such as `baseline_results.csv`, `all_model_results.csv`, `best_model_summary.csv`, and `model_comparison_r2.png` were produced before the grouped unseen-session correction and should not be treated as the final leakage-controlled evaluation set.',
        '',
        '## Practical interpretation',
        '',
        'The corrected grouped unseen-session evaluation is more conservative and should be preferred when presenting performance evidence. The older artifacts remain in the project for traceability but are now explicitly versioned as legacy / non-final evaluation evidence.',
    ]
    (REPORTS_DIR / 'evaluation_protocol_fix.md').write_text('\n'.join(audit_lines), encoding='utf-8')

    correction_lines = [
        '# Correction Audit Report',
        '',
        '## Retraining confirmation',
        '',
        'Yes, all models used in the grouped unseen-session correction were retrained under the corrected evaluation logic.',
        '',
        'Retrained model families under grouped unseen-session evaluation:',
        '',
        '- SVR',
        '- Linear Regression',
        '- Random Forest',
        '- KNN Regressor',
        '',
        'Retraining scope:',
        '',
        '- all targets in `TARGET_COLUMNS`',
        '- all defined feature sets',
        '- training-only feature selection inside each outer fold',
        '- training-only hyperparameter tuning inside grouped inner validation folds',
        '',
        'Regenerated corrected outputs:',
        '',
        '- `outputs/tables/grouped_unseen_session_results.csv`',
        '- `outputs/tables/grouped_unseen_session_predictions.csv`',
        '- `outputs/tables/best_model_summary_grouped_unseen_sessions.csv`',
        '- `outputs/figures/session_prediction_curves_unseen_sessions.png`',
        '- `outputs/figures/model_comparison_r2_grouped_unseen_sessions.png`',
        '- `outputs/reports/evaluation_protocol_fix.md`',
        '- `outputs/reports/correction_audit_report.md`',
        '',
        'Not all earlier project-wide result files were overwritten, by design. Older row-level artifacts were retained for traceability and are now explicitly marked as legacy / non-final evaluation evidence.',
        '',
        '## Train / validation / test separation',
        '',
        'The corrected workflow now uses grouped nested cross-validation for the new leakage-controlled evaluation artifacts.',
        '',
        'Split design:',
        '',
        '- Outer split: `GroupKFold(n_splits=5)` with `session_id` as the grouping variable.',
        '- This means all rows from the same dialysis session stay together in exactly one outer fold.',
        '- Outer training folds act as the train+validation pool for that iteration.',
        '- Outer test fold is fully unseen at the session level for that iteration.',
        '- Inner split: grouped cross-validation on the outer-training sessions only.',
        '- Inner validation folds are used for hyperparameter tuning only.',
        '',
        'This is not a single fixed train/validation/test split. It is a nested grouped cross-validation protocol with independent train / validation / test roles inside each outer fold.',
        '',
        '## Leakage prevention',
        '',
        'The corrected grouped evaluation enforces session-level leakage prevention:',
        '',
        '- repeated measurements within the same dialysis session are never split across train and outer-test folds',
        '- feature selection is fit on outer-training data only',
        '- hyperparameter tuning is done on grouped inner folds from outer-training data only',
        '- no outer-test row or outer-test session is used during training, feature selection, tuning, or fold-level model fitting',
        '',
        'Explicit statement:',
        '',
        '- No test-session rows were used during training.',
        '- No test-session rows were used during feature selection.',
        '- No test-session rows were used during hyperparameter tuning.',
        '- No derived information from the outer-test sessions was used in model selection inside the corrected grouped evaluation path.',
        '',
        '## Updated figures and tables',
        '',
        'Corrected grouped-evaluation artifacts now available:',
        '',
        '- Figure: `outputs/figures/session_prediction_curves_unseen_sessions.png`',
        '- Figure: `outputs/figures/model_comparison_r2_grouped_unseen_sessions.png`',
        '- Table: `outputs/tables/grouped_unseen_session_results.csv`',
        '- Table: `outputs/tables/grouped_unseen_session_predictions.csv`',
        '- Table: `outputs/tables/best_model_summary_grouped_unseen_sessions.csv`',
        '',
        'Artifacts still present but reflecting older row-level evaluation logic:',
        '',
        '- `outputs/figures/model_comparison_r2.png`',
        '- `outputs/figures/session_prediction_curves_best_models.png`',
        '- `outputs/tables/baseline_results.csv`',
        '- `outputs/tables/all_model_results.csv`',
        '- `outputs/tables/best_model_summary.csv`',
        '- `outputs/tables/model_comparison_full_vs_selected.csv`',
        '',
        'These older artifacts were intentionally not deleted. They remain for traceability, but should not be cited as the final leakage-controlled evaluation outputs.',
        '',
        '## Summary of all corrections made',
        '',
        'Project-wide corrections over the full work included:',
        '',
        '1. Switched output labels to English for cleaner figures and tables.',
        '2. Added regression-line plots and later corrected their interpretation by separating plot-fit R² from CV R².',
        '3. Added paper-style predicted-vs-actual panels, then replaced the confusing version with a cleaner actual-vs-predicted final version using CV metrics and identity-line logic.',
        '4. Expanded feature sets from three wavelengths to five wavelengths plus machine and personal features.',
        '5. Added feature selection and importance outputs.',
        '6. Expanded model comparison beyond SVR to include Linear Regression, Random Forest, and KNN.',
        '7. Added final model persistence with joblib artifacts and metadata.',
        '8. Identified that the original session-level curve figure was unsafe as strict validation evidence.',
        '9. Added grouped unseen-session evaluation to address session-level leakage and optimistic interpretation.',
        '',
        '## What was wrong in earlier versions',
        '',
        '- Some earlier evaluation artifacts used row-level folds despite repeated measurements within the same session.',
        '- The original session-level prediction figure could be interpreted as train-on-seen-session demonstration rather than unseen-session validation.',
        '- Earlier project artifacts mixed validation-style figures and deployment/demo-style figures too closely.',
        '- Some earlier summaries could be over-read as final evaluation even though they predated the grouped unseen-session correction.',
        '',
        '## Remaining limitations',
        '',
        '- The corrected protocol uses grouped nested cross-validation, not a single permanent external test set.',
        '- The dataset is still small at the session level, so fold-to-fold variance may remain meaningful.',
        '- `Acid` is still an inferred uric-acid mapping from workbook schema, not a formally confirmed semantic label.',
        '- Legacy row-level artifacts remain in the repository for traceability and must be interpreted carefully.',
        '',
        '## Direct final status answers',
        '',
        '- Were all relevant models retrained? **Yes — all models used in the corrected grouped unseen-session evaluation were retrained under the corrected protocol.**',
        '- Are train, validation, and test sets now truly independent? **Yes within the corrected grouped nested CV workflow: outer test sessions are unseen, and inner validation uses training sessions only.**',
        '- Were the model-performance figures updated? **Yes — corrected grouped-evaluation figures were generated with new filenames. Older non-corrected artifacts remain only as legacy traceability outputs.**',
        '- Does the report fully document all requested fixes and prior corrections? **Yes — this audit report and `evaluation_protocol_fix.md` document the correction path, earlier issues, updated artifacts, and remaining limitations.**',
    ]
    (REPORTS_DIR / 'correction_audit_report.md').write_text('\n'.join(correction_lines), encoding='utf-8')


if __name__ == '__main__':
    run()
