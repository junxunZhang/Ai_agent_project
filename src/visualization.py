from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .config import FIGURES_DIR, CORE_ABSORBANCE_COLUMNS, TARGET_COLUMNS

sns.set_theme(style='whitegrid')


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
        ax.set_title(f'Linear Fit: {primary_feature} vs {target}')
        ax.set_xlabel(primary_feature)
        ax.set_ylabel(target)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
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
