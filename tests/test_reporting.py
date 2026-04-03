from pathlib import Path

import pandas as pd

from src.reporting import write_analysis_summary


def test_write_analysis_summary_creates_file(tmp_path: Path):
    results = pd.DataFrame([
        {
            'target': 'urea',
            'feature_set': 'all_absorbance_only',
            'feature_scope': 'full',
            'model': 'svr_rbf',
            'MAE': 1.0,
            'MSE': 1.2,
            'RMSE': 1.0954,
            'R2': 0.8,
        }
    ])
    best_models = results.copy()
    output = tmp_path / 'analysis_summary.md'
    write_analysis_summary(results, best_models, output)
    assert output.exists()
    assert 'urea' in output.read_text(encoding='utf-8')
