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
