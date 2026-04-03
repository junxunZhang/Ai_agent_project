from __future__ import annotations

from pathlib import Path

import pandas as pd

from .cleaning import build_analysis_dataset
from .config import FIGURES_DIR, OUTPUT_DIR, REPORTS_DIR, TABLES_DIR
from .data_loader import load_primary_dataset
from .evaluation import summarize_best_models
from .feature_sets import get_feature_sets
from .modeling import run_baselines
from .profiling import descriptive_statistics, missing_values_table, session_summary, summarize_dataset
from .reporting import write_analysis_summary, write_dataset_profile, write_limitations_report
from .utils import ensure_directories
from .visualization import (
    plot_absorbance_scatter_grid,
    plot_core_wavelength_regression_grid,
    plot_correlation_heatmap,
    plot_linear_regression_lines_by_target,
    plot_missing_values,
    plot_model_comparison,
    plot_target_distributions,
)


def run() -> None:
    ensure_directories([OUTPUT_DIR, FIGURES_DIR, REPORTS_DIR, TABLES_DIR])

    raw_df = load_primary_dataset()
    analysis_df = build_analysis_dataset(raw_df)

    summary = summarize_dataset(analysis_df)
    missing_table = missing_values_table(analysis_df)
    desc_stats = descriptive_statistics(analysis_df)
    sessions = session_summary(analysis_df)

    feature_sets = get_feature_sets()
    results = run_baselines(analysis_df, feature_sets)
    best_models = summarize_best_models(results)

    analysis_df.head(20).to_csv(TABLES_DIR / 'cleaned_dataset_preview.csv', index=False)
    pd.DataFrame([
        {'feature_set': name, 'features': ', '.join(cols)} for name, cols in feature_sets.items()
    ]).to_csv(TABLES_DIR / 'feature_metadata.csv', index=False)
    missing_table.to_csv(TABLES_DIR / 'missing_values.csv', index=False)
    desc_stats.to_csv(TABLES_DIR / 'descriptive_stats.csv')
    sessions.to_csv(TABLES_DIR / 'session_summary.csv', index=False)
    results.to_csv(TABLES_DIR / 'baseline_results.csv', index=False)
    best_models.to_csv(TABLES_DIR / 'best_model_summary.csv', index=False)

    write_dataset_profile(summary)
    write_analysis_summary(results, best_models)
    write_limitations_report()

    plot_missing_values(missing_table)
    plot_target_distributions(analysis_df)
    plot_correlation_heatmap(analysis_df)
    plot_absorbance_scatter_grid(analysis_df)
    plot_linear_regression_lines_by_target(analysis_df)
    plot_core_wavelength_regression_grid(analysis_df)
    if not results.empty:
        plot_model_comparison(results)


if __name__ == '__main__':
    run()
