from __future__ import annotations

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

    report_lines = [
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
        '- Performed model tuning inside training data only.',
        '- Generated prediction curves from grouped cross-validation outputs so each plotted session segment comes from unseen-session predictions.',
        '- Avoided visually cherry-picking the best-looking session by using a middle-ranked session by per-session MSE for each target/model combination shown.',
        '',
        '## Practical interpretation',
        '',
        'The new figure is more conservative than the original demo-style curve figure because it reflects out-of-fold predictions from unseen sessions. It should be preferred when presenting evaluation evidence.',
        '',
        '## Output files',
        '',
        '- `outputs/figures/session_prediction_curves_unseen_sessions.png`',
        '- `outputs/tables/grouped_unseen_session_results.csv`',
        '- `outputs/tables/grouped_unseen_session_predictions.csv`',
        '- `outputs/reports/evaluation_protocol_fix.md`',
    ]
    (REPORTS_DIR / 'evaluation_protocol_fix.md').write_text('\n'.join(report_lines), encoding='utf-8')


if __name__ == '__main__':
    run()
