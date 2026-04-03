from pathlib import Path

import pandas as pd

from src.reporting import write_analysis_summary


def test_write_analysis_summary_creates_file(tmp_path: Path):
    results = pd.DataFrame([
        {
            'target': 'Urea',
            'feature_set': 'absorbance_only',
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
    assert 'Urea' in output.read_text(encoding='utf-8')
