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
                f"- {row['target']}: {row['model']} with {row['feature_set']} | "
                f"MAE={row['MAE']:.4f}, RMSE={row['RMSE']:.4f}, R²={row['R2']:.4f}"
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
        '- `Acid` is mapped cautiously to uric acid based on workbook structure, not explicit labeling.',
        '- Some patient-level fields appear inconsistent across records and should be reviewed with domain knowledge.',
        '- This project emphasizes a clean baseline rather than full hyperparameter optimization.',
        '',
        '## Next steps',
        '',
        '- Add grouped cross-validation by session or patient.',
        '- Confirm biochemical label semantics with domain experts.',
        '- Evaluate the contribution of extra absorbance wavelengths (285nm, 295nm).',
        '- Add permutation importance and residual diagnostics for deeper interpretability.',
    ]
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path
