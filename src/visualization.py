from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from .config import FIGURES_DIR, CORE_ABSORBANCE_COLUMNS, TARGET_COLUMNS

sns.set_theme(style='whitegrid')


def _add_r2_annotation(ax, subset: pd.DataFrame, x_col: str, y_col: str) -> None:
    if subset.empty:
        return
    model = LinearRegression()
    X = subset[[x_col]].to_numpy()
    y = subset[y_col].to_numpy()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    ax.text(
        0.03,
        0.95,
        f'R² = {r2:.3f}',
        transform=ax.transAxes,
        ha='left',
        va='top',
        fontsize=10,
        bbox={'boxstyle': 'round,pad=0.25', 'facecolor': 'white', 'alpha': 0.8, 'edgecolor': 'gray'},
    )


def plot_missing_values(missing_table: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'missing_values_bar.png'
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_df = missing_table.sort_values('missing_count', ascending=False)
    sns.barplot(data=plot_df, x='missing_count', y='column_name', ax=ax, color='#4C72B0')
    ax.set_title('Missing Values by Column')
    ax.set_xlabel('Missing Count')
    ax.set_ylabel('Column')
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_target_distributions(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'target_distributions.png'
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for ax, col in zip(axes, TARGET_COLUMNS):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color='#55A868')
        ax.set_title(col)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_correlation_heatmap(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'correlation_heatmap.png'
    corr_cols = CORE_ABSORBANCE_COLUMNS + TARGET_COLUMNS
    corr = df[corr_cols].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Heatmap: Core Absorbance and Targets')
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_full_feature_correlation_heatmap(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'full_feature_correlation_heatmap.png'
    corr = df.select_dtypes(include='number').corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(16, 14))
    sns.heatmap(corr, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Full Feature Correlation Heatmap')
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def plot_absorbance_scatter_grid(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'absorbance_target_scatter.png'
    pairs = [(abs_col, target) for abs_col in CORE_ABSORBANCE_COLUMNS for target in TARGET_COLUMNS[:2]]
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()
    for ax, (x_col, y_col) in zip(axes, pairs):
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax, s=25, alpha=0.7)
        ax.set_title(f'{x_col} vs {y_col}')
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_linear_regression_lines_by_target(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'linear_regression_lines_by_target.png'
    primary_feature = CORE_ABSORBANCE_COLUMNS[0]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes = axes.flatten()

    for ax, target in zip(axes, TARGET_COLUMNS):
        subset = df[[primary_feature, target]].dropna()
        sns.regplot(
            data=subset,
            x=primary_feature,
            y=target,
            ax=ax,
            scatter_kws={'s': 24, 'alpha': 0.7},
            line_kws={'color': 'red', 'linewidth': 2},
        )
        _add_r2_annotation(ax, subset, primary_feature, target)
        ax.set_title(f'Linear Fit: {primary_feature} vs {target}')
        ax.set_xlabel(primary_feature)
        ax.set_ylabel(target)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_core_wavelength_regression_grid(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'core_wavelength_regression_grid.png'
    fig, axes = plt.subplots(len(TARGET_COLUMNS), len(CORE_ABSORBANCE_COLUMNS), figsize=(16, 24))

    for row_idx, target in enumerate(TARGET_COLUMNS):
        for col_idx, feature in enumerate(CORE_ABSORBANCE_COLUMNS):
            ax = axes[row_idx, col_idx]
            subset = df[[feature, target]].dropna()
            sns.regplot(
                data=subset,
                x=feature,
                y=target,
                ax=ax,
                scatter_kws={'s': 16, 'alpha': 0.55},
                line_kws={'color': 'red', 'linewidth': 1.8},
            )
            _add_r2_annotation(ax, subset, feature, target)
            if row_idx == 0:
                ax.set_title(feature)
            if col_idx == 0:
                ax.set_ylabel(target)
            else:
                ax.set_ylabel('')
            if row_idx == len(TARGET_COLUMNS) - 1:
                ax.set_xlabel(feature)
            else:
                ax.set_xlabel('')

    fig.suptitle('Linear Regression Comparison Across Core Wavelengths and Toxin Targets', y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def plot_model_comparison(results: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'model_comparison_r2.png'
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=results, x='target', y='R2', hue='model', ax=ax)
    ax.set_title('Model Comparison by Target (R²)')
    ax.set_ylim(min(results['R2'].min() - 0.1, -1), 1)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_feature_selection_comparison(results: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'feature_selection_comparison.png'
    plot_df = pd.concat([
        results[['target', 'feature_set', 'model', 'R2_full']].rename(columns={'R2_full': 'R2'}).assign(feature_scope='full'),
        results[['target', 'feature_set', 'model', 'R2_selected']].rename(columns={'R2_selected': 'R2'}).assign(feature_scope='selected'),
    ], ignore_index=True)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(data=plot_df, x='target', y='R2', hue='feature_scope', ax=ax)
    ax.set_title('Model Performance Before and After Feature Selection (R²)')
    ax.set_ylim(min(plot_df['R2'].min() - 0.1, -1), 1)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def plot_feature_importance_by_target(importance_df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'feature_importance_by_target.png'
    targets = importance_df['target'].dropna().unique().tolist()
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for ax, target in zip(axes, targets[:6]):
        subset = (
            importance_df[importance_df['target'] == target]
            .sort_values('permutation_importance_mean', ascending=False)
            .head(8)
        )
        sns.barplot(data=subset, x='permutation_importance_mean', y='feature', ax=ax, color='#8172B2')
        ax.set_title(target)
        ax.set_xlabel('Permutation Importance (mean ΔR²)')
        ax.set_ylabel('Feature')

    for idx in range(len(targets[:6]), len(axes)):
        axes[idx].axis('off')

    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def plot_session_prediction_curves(session_predictions: dict[str, pd.DataFrame], output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'session_prediction_curves_best_models.png'
    ordered_targets = [target for target in TARGET_COLUMNS if target in session_predictions]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for ax, target in zip(axes, ordered_targets):
        df = session_predictions[target].copy()
        session_error = (
            df.groupby('session_id')
            .apply(lambda g: ((g['actual'] - g['predicted']) ** 2).mean())
            .sort_values()
        )
        session_id = session_error.index[0]
        plot_df = df[df['session_id'] == session_id].sort_values('collection_time_min')
        ax.plot(plot_df['collection_time_min'], plot_df['predicted'], color='black', linewidth=1.8, label='Predicted conc.')
        ax.scatter(plot_df['collection_time_min'], plot_df['actual'], color='red', s=26, marker='^', label='Actual conc.')
        ax.set_title(target)
        ax.set_xlabel('HD time (min)')
        ax.set_ylabel('Concentration')
        ax.text(
            0.03,
            0.08,
            f'session: {session_id}',
            transform=ax.transAxes,
            ha='left',
            va='bottom',
            fontsize=9,
            bbox={'boxstyle': 'round,pad=0.2', 'facecolor': 'white', 'alpha': 0.75, 'edgecolor': 'gray'},
        )
        ax.legend(loc='best', fontsize=8, frameon=False)

    for idx in range(len(ordered_targets), len(axes)):
        axes[idx].axis('off')

    fig.suptitle('Best-Model Predicted vs Actual Concentration Curves by HD Session', y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path


def plot_unseen_session_prediction_curves(results_df: pd.DataFrame, prediction_df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'session_prediction_curves_unseen_sessions.png'
    ordered_targets = [target for target in TARGET_COLUMNS if target in prediction_df['target'].unique()]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for ax, target in zip(axes, ordered_targets):
        target_results = results_df[results_df['target'] == target].sort_values(['R2', 'RMSE'], ascending=[False, True])
        if target_results.empty:
            ax.axis('off')
            continue
        best_row = target_results.iloc[0]
        target_preds = prediction_df[
            (prediction_df['target'] == target)
            & (prediction_df['feature_set'] == best_row['feature_set'])
            & (prediction_df['model'] == best_row['model'])
        ].copy()
        if target_preds.empty:
            ax.axis('off')
            continue

        session_error = (
            target_preds.groupby('session_id')
            .apply(lambda g: ((g['actual'] - g['predicted']) ** 2).mean())
            .sort_values()
        )
        median_idx = len(session_error) // 2
        session_id = session_error.index[median_idx]
        plot_df = target_preds[target_preds['session_id'] == session_id].sort_values('collection_time_min')

        ax.plot(plot_df['collection_time_min'], plot_df['predicted'], color='black', linewidth=1.8, label='Predicted conc.')
        ax.scatter(plot_df['collection_time_min'], plot_df['actual'], color='red', s=26, marker='^', label='Actual conc.')
        ax.set_title(target)
        ax.set_xlabel('HD time (min)')
        ax.set_ylabel('Concentration')
        ax.text(
            0.03,
            0.08,
            f"session: {session_id}\nmodel: {best_row['model']}\nR²: {best_row['R2']:.3f}",
            transform=ax.transAxes,
            ha='left',
            va='bottom',
            fontsize=8.5,
            bbox={'boxstyle': 'round,pad=0.2', 'facecolor': 'white', 'alpha': 0.78, 'edgecolor': 'gray'},
        )
        ax.legend(loc='best', fontsize=8, frameon=False)

    for idx in range(len(ordered_targets), len(axes)):
        axes[idx].axis('off')

    fig.suptitle('Unseen-Session Prediction Curves from Grouped Cross-Validation', y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    fig.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close(fig)
    return output_path


def plot_predicted_vs_actual_panels_grouped_unseen(prediction_df: pd.DataFrame, results_df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'predicted_vs_actual_panels_grouped_unseen_sessions.png'
    ordered_targets = [target for target in TARGET_COLUMNS if target in prediction_df['target'].unique()]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    panel_labels = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

    for ax, target, panel in zip(axes, ordered_targets, panel_labels):
        target_results = results_df[results_df['target'] == target].sort_values(['R2', 'RMSE'], ascending=[False, True])
        if target_results.empty:
            ax.axis('off')
            continue
        best_row = target_results.iloc[0]
        subset = prediction_df[
            (prediction_df['target'] == target)
            & (prediction_df['feature_set'] == best_row['feature_set'])
            & (prediction_df['model'] == best_row['model'])
        ].dropna(subset=['predicted', 'actual']).copy()
        if subset.empty:
            ax.axis('off')
            continue

        sns.scatterplot(data=subset, x='actual', y='predicted', ax=ax, color='black', s=16, edgecolor='none')
        min_val = min(subset['actual'].min(), subset['predicted'].min())
        max_val = max(subset['actual'].max(), subset['predicted'].max())
        ax.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='gray', linewidth=1.2)
        ax.text(0.03, 0.95, panel, transform=ax.transAxes, ha='left', va='top', fontsize=12, fontweight='bold')
        ax.text(0.05, 0.88, target, transform=ax.transAxes, ha='left', va='top', fontsize=11, fontweight='bold')
        ax.text(0.05, 0.79, f"model: {best_row['model']}", transform=ax.transAxes, ha='left', va='top', fontsize=9)
        ax.text(0.05, 0.72, f"features: {best_row['feature_set']}", transform=ax.transAxes, ha='left', va='top', fontsize=8)
        ax.text(0.55, 0.10, f"Grouped CV R² = {best_row['R2']:.3f}\nRMSE = {best_row['RMSE']:.3f}", transform=ax.transAxes, ha='left', va='bottom', fontsize=10)
        ax.set_xlim(min_val, max_val)
        ax.set_ylim(min_val, max_val)
        ax.set_xlabel('Actual concentration')
        ax.set_ylabel('Predicted concentration')

    for idx in range(len(ordered_targets), len(axes)):
        axes[idx].axis('off')

    fig.suptitle('Predicted vs Actual — Grouped Unseen Sessions', y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    fig.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close(fig)
    return output_path


def plot_model_comparison_r2_grouped_clean(results_df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'model_comparison_r2_grouped_unseen_sessions_v2.png'
    plot_df = results_df.copy()
    plot_df['R2_clipped_for_display'] = plot_df['R2'].clip(lower=-1.0)
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(data=plot_df, x='target', y='R2_clipped_for_display', hue='model', ax=ax)
    ax.axhline(0, color='gray', linewidth=1, linestyle='--')
    ax.set_title('Model Comparison by Target (R²) — Grouped Unseen Sessions')
    ax.set_ylabel('R² (negative values are valid and indicate worse-than-mean performance)')
    ax.set_xlabel('Target')
    ax.set_ylim(min(plot_df['R2_clipped_for_display'].min() - 0.1, -1.0), 1.0)
    ax.legend(title='Model', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    for tick in ax.get_xticklabels():
        tick.set_rotation(20)
        tick.set_ha('right')
    fig.tight_layout()
    fig.savefig(output_path, dpi=240, bbox_inches='tight')
    plt.close(fig)
    return output_path


def plot_predicted_vs_actual_panels(prediction_df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / 'predicted_vs_actual_panels_final.png'
    ordered_targets = [target for target in TARGET_COLUMNS if target in prediction_df['target'].unique()]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    panel_labels = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

    for ax, target, panel in zip(axes, ordered_targets, panel_labels):
        subset = prediction_df[prediction_df['target'] == target].dropna(subset=['predicted', 'actual']).copy()
        sns.scatterplot(data=subset, x='actual', y='predicted', ax=ax, color='black', s=18, edgecolor='none')
        if len(subset) >= 2:
            min_val = min(subset['actual'].min(), subset['predicted'].min())
            max_val = max(subset['actual'].max(), subset['predicted'].max())
            ax.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='gray', linewidth=1.2)
            best_model = subset['model'].iloc[0] if 'model' in subset.columns and not subset.empty else 'unknown'
            feature_set = subset['feature_set'].iloc[0] if 'feature_set' in subset.columns and not subset.empty else 'unknown'
            cv_r2 = subset['cv_r2'].iloc[0] if 'cv_r2' in subset.columns else float('nan')
            cv_rmse = subset['cv_rmse'].iloc[0] if 'cv_rmse' in subset.columns else float('nan')
            ax.text(0.03, 0.95, panel, transform=ax.transAxes, ha='left', va='top', fontsize=12, fontweight='bold')
            ax.text(0.05, 0.88, target, transform=ax.transAxes, ha='left', va='top', fontsize=11, fontweight='bold')
            ax.text(0.05, 0.79, f'model: {best_model}', transform=ax.transAxes, ha='left', va='top', fontsize=9)
            ax.text(0.05, 0.72, f'features: {feature_set}', transform=ax.transAxes, ha='left', va='top', fontsize=8)
            ax.text(
                0.55,
                0.10,
                f'CV R² = {cv_r2:.3f}\nRMSE = {cv_rmse:.3f}',
                transform=ax.transAxes,
                ha='left',
                va='bottom',
                fontsize=10,
            )
            ax.set_xlim(min_val, max_val)
            ax.set_ylim(min_val, max_val)
        ax.set_xlabel('Actual concentration')
        ax.set_ylabel('Predicted concentration')

    for idx in range(len(ordered_targets), len(axes)):
        axes[idx].axis('off')

    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path
