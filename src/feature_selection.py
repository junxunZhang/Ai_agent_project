from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR

from .config import RANDOM_STATE, TARGET_COLUMNS


def select_top_features_mutual_info(
    df: pd.DataFrame,
    feature_sets: Dict[str, List[str]],
    max_features: int = 8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    selected_rows = []

    for target in TARGET_COLUMNS:
        subset = df.dropna(subset=[target]).copy()
        for feature_set_name, features in feature_sets.items():
            available_features = [feature for feature in features if feature in subset.columns]
            if not available_features:
                continue

            X = subset[available_features]
            y = subset[target]
            imputer = SimpleImputer(strategy='median')
            X_imp = imputer.fit_transform(X)
            k = min(max_features, X.shape[1])
            selector = SelectKBest(score_func=mutual_info_regression, k=k)
            selector.fit(X_imp, y)
            scores = selector.scores_
            mask = selector.get_support()

            for feature, score, selected in zip(available_features, scores, mask):
                summary_rows.append({
                    'target': target,
                    'feature_set': feature_set_name,
                    'feature': feature,
                    'mutual_info_score': float(score if score is not None else 0.0),
                    'selected': bool(selected),
                })
                if selected:
                    selected_rows.append({
                        'target': target,
                        'feature_set': feature_set_name,
                        'feature': feature,
                        'selection_method': 'mutual_info_regression',
                        'selection_score': float(score if score is not None else 0.0),
                    })

    return pd.DataFrame(summary_rows), pd.DataFrame(selected_rows)


def build_selected_feature_map(selected_df: pd.DataFrame) -> Dict[Tuple[str, str], List[str]]:
    selected_map: Dict[Tuple[str, str], List[str]] = {}
    if selected_df.empty:
        return selected_map
    for (target, feature_set), group in selected_df.groupby(['target', 'feature_set']):
        selected_map[(target, feature_set)] = group.sort_values('selection_score', ascending=False)['feature'].tolist()
    return selected_map


def compute_permutation_importance(
    df: pd.DataFrame,
    selected_map: Dict[Tuple[str, str], List[str]],
) -> pd.DataFrame:
    rows = []
    for (target, feature_set), features in selected_map.items():
        subset = df.dropna(subset=[target]).copy()
        if not features:
            continue
        X = subset[features]
        y = subset[target]
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('model', SVR(kernel='rbf', C=10.0, epsilon=0.1)),
        ])
        pipeline.fit(X, y)
        importance = permutation_importance(
            pipeline,
            X,
            y,
            n_repeats=10,
            random_state=RANDOM_STATE,
            scoring='r2',
        )
        for feature, mean_imp, std_imp in zip(features, importance.importances_mean, importance.importances_std):
            rows.append({
                'target': target,
                'feature_set': feature_set,
                'feature': feature,
                'permutation_importance_mean': float(mean_imp),
                'permutation_importance_std': float(std_imp),
            })
    return pd.DataFrame(rows)
