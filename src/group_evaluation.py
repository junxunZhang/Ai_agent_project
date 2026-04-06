from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, ParameterGrid
from sklearn.pipeline import Pipeline

from .config import TARGET_COLUMNS
from .modeling import make_pipeline


def _metric_dict(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    return {
        'MAE': float(mean_absolute_error(y_true, y_pred)),
        'MSE': float(mse),
        'RMSE': float(np.sqrt(mse)),
        'R2': float(r2_score(y_true, y_pred)),
    }


def _feature_select_on_train(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    max_features: int = 8,
) -> list[str]:
    imputer = SimpleImputer(strategy='median')
    X_imp = imputer.fit_transform(X_train)
    k = min(max_features, X_train.shape[1])
    selector = SelectKBest(score_func=mutual_info_regression, k=k)
    selector.fit(X_imp, y_train)
    mask = selector.get_support()
    return X_train.columns[mask].tolist()


def _param_grid_for_model(model_name: str) -> list[dict]:
    if model_name == 'svr_rbf':
        return list(ParameterGrid({'model__C': [1.0, 10.0], 'model__epsilon': [0.05, 0.1]}))
    if model_name == 'knn_regressor':
        return list(ParameterGrid({'model__n_neighbors': [3, 5, 7], 'model__weights': ['uniform', 'distance']}))
    if model_name == 'random_forest':
        return list(ParameterGrid({'model__n_estimators': [200], 'model__max_depth': [None, 6, 10]}))
    return [{}]


def run_grouped_unseen_session_evaluation(
    df: pd.DataFrame,
    feature_sets: Dict[str, List[str]],
    max_selected_features: int = 8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped_results = []
    prediction_rows = []

    outer_cv = GroupKFold(n_splits=5)

    for target in TARGET_COLUMNS:
        subset = df.dropna(subset=[target]).copy()
        groups = subset['session_id']

        for feature_set_name, features in feature_sets.items():
            available_features = [feature for feature in features if feature in subset.columns]
            if not available_features:
                continue

            X_all = subset[available_features]
            y_all = subset[target]

            for model_name in ['svr_rbf', 'linear_regression', 'random_forest', 'knn_regressor']:
                all_true = []
                all_pred = []
                all_meta = []

                for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X_all, y_all, groups)):
                    X_train_full = X_all.iloc[train_idx].copy()
                    y_train = y_all.iloc[train_idx].copy()
                    X_test_full = X_all.iloc[test_idx].copy()
                    y_test = y_all.iloc[test_idx].copy()
                    session_test = subset.iloc[test_idx]['session_id'].to_numpy()
                    time_test = subset.iloc[test_idx]['collection_time_min'].to_numpy()

                    selected_features = _feature_select_on_train(X_train_full, y_train, max_selected_features)
                    X_train = X_train_full[selected_features]
                    X_test = X_test_full[selected_features]

                    inner_groups = groups.iloc[train_idx]
                    unique_train_sessions = inner_groups.nunique()
                    inner_splits = min(4, unique_train_sessions)
                    if inner_splits < 2:
                        continue
                    inner_cv = GroupKFold(n_splits=inner_splits)

                    best_score = -np.inf
                    best_params = {}
                    for params in _param_grid_for_model(model_name):
                        fold_scores = []
                        for inner_train_idx, inner_val_idx in inner_cv.split(X_train, y_train, inner_groups):
                            pipeline = make_pipeline(model_name)
                            if params:
                                pipeline.set_params(**params)
                            pipeline.fit(X_train.iloc[inner_train_idx], y_train.iloc[inner_train_idx])
                            preds = pipeline.predict(X_train.iloc[inner_val_idx])
                            fold_scores.append(r2_score(y_train.iloc[inner_val_idx], preds))
                        score = float(np.mean(fold_scores)) if fold_scores else -np.inf
                        if score > best_score:
                            best_score = score
                            best_params = params

                    final_pipeline = make_pipeline(model_name)
                    if best_params:
                        final_pipeline.set_params(**best_params)
                    final_pipeline.fit(X_train, y_train)
                    preds = final_pipeline.predict(X_test)

                    all_true.extend(y_test.tolist())
                    all_pred.extend(preds.tolist())
                    for sid, t, a, p in zip(session_test, time_test, y_test.tolist(), preds.tolist()):
                        all_meta.append({
                            'target': target,
                            'feature_set': feature_set_name,
                            'model': model_name,
                            'fold': fold_idx,
                            'session_id': sid,
                            'collection_time_min': t,
                            'actual': a,
                            'predicted': p,
                        })

                if not all_true:
                    continue

                metrics = _metric_dict(np.array(all_true), np.array(all_pred))
                grouped_results.append({
                    'target': target,
                    'feature_set': feature_set_name,
                    'model': model_name,
                    'evaluation_protocol': 'GroupKFold_unseen_sessions',
                    **metrics,
                })
                prediction_rows.extend(all_meta)

    return pd.DataFrame(grouped_results), pd.DataFrame(prediction_rows)
