from __future__ import annotations

import pandas as pd


METRIC_COLUMNS = ['MAE', 'MSE', 'RMSE', 'R2']


def summarize_best_models(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame(columns=['target', 'feature_set', 'model'] + METRIC_COLUMNS)

    return (
        results.sort_values(['target', 'R2', 'RMSE'], ascending=[True, False, True])
        .groupby('target', as_index=False)
        .head(1)
        .reset_index(drop=True)
    )
