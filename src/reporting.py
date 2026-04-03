from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import REPORTS_DIR


def write_dataset_profile(summary: Dict[str, object], output_path: Path | None = None) -> Path:
    output_path = output_path or REPORTS_DIR / 'dataset_profile.md'
    lines = [
        '# Dataset Profile',
        '',
        f"- Rows: {summary['rows']}",
        f"- Columns: {summary['columns']}",
        f"- Duplicate rows: {summary['duplicate_rows']}",
        f"- Unique patients: {summary['unique_patients']}",
        f"- Session count: {summary['session_count']}",
        f"- Collection times: {summary['collection_times']}",
        '',
        '## Target missing values',
        '',
    ]
    for key, value in summary['target_missing'].items():
        lines.append(f'- {key}: {value}')

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path


def write_analysis_summary(results: pd.DataFrame, best_models: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or REPORTS_DIR / 'analysis_summary.md'
    lines = [
        '# Analysis Summary',
        '',
        '## Baseline modeling overview',
        '',
        f'- Total experiment rows: {len(results)}',
        f'- Targets evaluated: {results["target"].nunique() if not results.empty else 0}',
        f'- Feature settings compared: {results["feature_set"].nunique() if not results.empty else 0}',
        '',
        '## Best model by target',
        '',
    ]

    if best_models.empty:
        lines.append('No valid models were produced.')
    else:
        for _, row in best_models.iterrows():
            lines.append(
                f"- {row['target']}: {row['model']} with {row['feature_set']} ({row['feature_scope']}) | "
                f"MAE={row['MAE']:.4f}, RMSE={row['RMSE']:.4f}, R²={row['R2']:.4f}"
            )

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path


def write_feature_selection_report(
    selected_df: pd.DataFrame,
    importance_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    output_path: Path | None = None,
) -> Path:
    output_path = output_path or REPORTS_DIR / 'feature_selection_report.md'
    lines = [
        '# Feature Selection Report',
        '',
        '## Method',
        '',
        '- Primary selection method: mutual information regression',
        '- Importance refinement: permutation importance using SVR on selected features',
        '- Comparison: full feature sets vs selected feature subsets under 5-fold cross-validation',
        '',
        '## Selected-feature summary',
        '',
    ]

    if selected_df.empty:
        lines.append('No selected features available.')
    else:
        for (target, feature_set), group in selected_df.groupby(['target', 'feature_set']):
            features = ', '.join(group.sort_values('selection_score', ascending=False)['feature'].tolist())
            lines.append(f'- {target} | {feature_set}: {features}')

    lines.extend(['', '## Highest permutation-importance features', ''])
    if importance_df.empty:
        lines.append('No permutation importance results available.')
    else:
        for target, group in importance_df.groupby('target'):
            top_group = group.sort_values('permutation_importance_mean', ascending=False).head(5)
            feature_text = ', '.join(
                f"{row['feature']} ({row['permutation_importance_mean']:.3f})" for _, row in top_group.iterrows()
            )
            lines.append(f'- {target}: {feature_text}')

    lines.extend(['', '## Performance change after feature selection', ''])
    if comparison_df.empty:
        lines.append('No comparison rows available.')
    else:
        for _, row in comparison_df.iterrows():
            lines.append(
                f"- {row['target']} | {row['feature_set']} | {row['model']}: "
                f"R² full={row['R2_full']:.4f}, R² selected={row['R2_selected']:.4f}, "
                f"ΔR²={row['delta_R2']:.4f}"
            )

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path


def write_limitations_report(output_path: Path | None = None) -> Path:
    output_path = output_path or REPORTS_DIR / 'limitations_and_next_steps.md'
    lines = [
        '# Limitations and Next Steps',
        '',
        '## Limitations',
        '',
        '- The dataset is relatively small and includes repeated measurements within dialysis sessions.',
        '- `acid_inferred_uric_acid` is mapped cautiously to uric acid based on workbook structure, not explicit labeling.',
        '- Some patient-level fields appear inconsistent across records and should be reviewed with domain knowledge.',
        '- This project emphasizes a clean baseline rather than full hyperparameter optimization.',
        '',
        '## Next steps',
        '',
        '- Add grouped cross-validation by session or patient.',
        '- Confirm biochemical label semantics with domain experts.',
        '- Test nested CV and tuning for SVR and tree-based models.',
        '- Add residual diagnostics for session-level drift analysis.',
    ]
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path
