from __future__ import annotations

import pandas as pd

from .cleaning import build_analysis_dataset
from .config import FIGURES_DIR, OUTPUT_DIR, REPORTS_DIR, TABLES_DIR
from .data_loader import load_primary_dataset
from .evaluation import summarize_best_models
from .feature_selection import (
    build_selected_feature_map,
    compute_permutation_importance,
    select_top_features_mutual_info,
)
from .feature_sets import get_feature_sets
from .modeling import build_session_predictions, run_baselines
from .profiling import descriptive_statistics, missing_values_table, session_summary, summarize_dataset
from .reporting import (
    write_analysis_summary,
    write_dataset_profile,
    write_feature_selection_report,
    write_limitations_report,
)
from .utils import ensure_directories
from .visualization import (
    plot_absorbance_scatter_grid,
    plot_core_wavelength_regression_grid,
    plot_correlation_heatmap,
    plot_feature_importance_by_target,
    plot_feature_selection_comparison,
    plot_full_feature_correlation_heatmap,
    plot_linear_regression_lines_by_target,
    plot_missing_values,
    plot_model_comparison,
    plot_session_prediction_curves,
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
    feature_metadata = pd.DataFrame([
        {'feature_set': name, 'features': ', '.join(cols)} for name, cols in feature_sets.items()
    ])

    full_results = run_baselines(analysis_df, feature_sets, feature_scope='full')
    selection_summary, selected_features = select_top_features_mutual_info(analysis_df, feature_sets)
    selected_map = build_selected_feature_map(selected_features)
    selected_results = run_baselines(analysis_df, feature_sets, selected_map=selected_map, feature_scope='selected')
    all_results = pd.concat([full_results, selected_results], ignore_index=True)
    best_models = summarize_best_models(all_results)
    session_predictions = build_session_predictions(analysis_df, best_models, feature_sets)
    importance_df = compute_permutation_importance(analysis_df, selected_map)

    comparison = full_results.merge(
        selected_results,
        on=['target', 'feature_set', 'model'],
        suffixes=('_full', '_selected'),
    )
    comparison['delta_R2'] = comparison['R2_selected'] - comparison['R2_full']
    comparison['delta_RMSE'] = comparison['RMSE_selected'] - comparison['RMSE_full']

    analysis_df.head(20).to_csv(TABLES_DIR / 'cleaned_dataset_preview.csv', index=False)
    missing_table.to_csv(TABLES_DIR / 'missing_values.csv', index=False)
    desc_stats.to_csv(TABLES_DIR / 'descriptive_stats.csv')
    sessions.to_csv(TABLES_DIR / 'session_summary.csv', index=False)
    feature_metadata.to_csv(TABLES_DIR / 'feature_metadata.csv', index=False)
    full_results.to_csv(TABLES_DIR / 'baseline_results.csv', index=False)
    selected_results.to_csv(TABLES_DIR / 'selected_feature_results.csv', index=False)
    all_results.to_csv(TABLES_DIR / 'all_model_results.csv', index=False)
    best_models.to_csv(TABLES_DIR / 'best_model_summary.csv', index=False)
    selection_summary.to_csv(TABLES_DIR / 'feature_selection_summary.csv', index=False)
    selected_features.to_csv(TABLES_DIR / 'selected_features_by_target.csv', index=False)
    comparison.to_csv(TABLES_DIR / 'model_comparison_full_vs_selected.csv', index=False)
    importance_df.to_csv(TABLES_DIR / 'feature_importance_by_target.csv', index=False)

    write_dataset_profile(summary)
    write_analysis_summary(all_results, best_models)
    write_feature_selection_report(selected_features, importance_df, comparison)
    write_limitations_report()

    plot_missing_values(missing_table)
    plot_target_distributions(analysis_df)
    plot_correlation_heatmap(analysis_df)
    plot_full_feature_correlation_heatmap(analysis_df)
    plot_absorbance_scatter_grid(analysis_df)
    plot_linear_regression_lines_by_target(analysis_df)
    plot_core_wavelength_regression_grid(analysis_df)
    if not all_results.empty:
        plot_model_comparison(all_results)
        plot_feature_selection_comparison(comparison)
    if not importance_df.empty:
        plot_feature_importance_by_target(importance_df)
    if session_predictions:
        plot_session_prediction_curves(session_predictions)


if __name__ == '__main__':
    run()
