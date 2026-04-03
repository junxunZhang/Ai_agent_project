from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from .config import N_SPLITS, RANDOM_STATE, TARGET_COLUMNS


MODELS = {
    'linear_regression': LinearRegression(),
    'svr_rbf': SVR(kernel='rbf', C=10.0, epsilon=0.1),
    'random_forest': RandomForestRegressor(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1),
    'knn_regressor': KNeighborsRegressor(n_neighbors=7, weights='distance'),
}


def make_pipeline(model_name: str) -> Pipeline:
    model = MODELS[model_name]
    steps = [('imputer', SimpleImputer(strategy='median'))]
    if model_name in {'linear_regression', 'svr_rbf', 'knn_regressor'}:
        steps.append(('scaler', StandardScaler()))
    steps.append(('model', model))
    return Pipeline(steps)


def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    return {
        'MAE': float(mean_absolute_error(y_true, y_pred)),
        'MSE': float(mse),
        'RMSE': float(np.sqrt(mse)),
        'R2': float(r2_score(y_true, y_pred)),
    }


def fit_best_models(df: pd.DataFrame, best_models: pd.DataFrame, feature_sets: Dict[str, List[str]]) -> Dict[str, Pipeline]:
    fitted_models: Dict[str, Pipeline] = {}
    for _, row in best_models.iterrows():
        target = row['target']
        feature_set_name = row['feature_set']
        model_name = row['model']
        subset = df.dropna(subset=[target]).copy()
        features = [feature for feature in feature_sets[feature_set_name] if feature in subset.columns]
        if not features:
            continue
        pipeline = make_pipeline(model_name)
        pipeline.fit(subset[features], subset[target])
        fitted_models[target] = pipeline
    return fitted_models


def build_session_predictions(df: pd.DataFrame, best_models: pd.DataFrame, feature_sets: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
    fitted_models = fit_best_models(df, best_models, feature_sets)
    predictions: Dict[str, pd.DataFrame] = {}
    for _, row in best_models.iterrows():
        target = row['target']
        feature_set_name = row['feature_set']
        subset = df.dropna(subset=[target]).copy()
        features = [feature for feature in feature_sets[feature_set_name] if feature in subset.columns]
        if target not in fitted_models or not features:
            continue
        subset = subset[['session_id', 'collection_time_min', target] + features].copy()
        subset['predicted'] = fitted_models[target].predict(subset[features])
        predictions[target] = subset[['session_id', 'collection_time_min', target, 'predicted']].rename(columns={target: 'actual'})
    return predictions


def build_predicted_vs_actual_data(df: pd.DataFrame, best_models: pd.DataFrame, feature_sets: Dict[str, List[str]]) -> pd.DataFrame:
    fitted_models = fit_best_models(df, best_models, feature_sets)
    rows = []
    for _, row in best_models.iterrows():
        target = row['target']
        feature_set_name = row['feature_set']
        subset = df.dropna(subset=[target]).copy()
        features = [feature for feature in feature_sets[feature_set_name] if feature in subset.columns]
        if target not in fitted_models or not features:
            continue
        preds = fitted_models[target].predict(subset[features])
        tmp = pd.DataFrame({
            'target': target,
            'actual': subset[target].to_numpy(),
            'predicted': preds,
            'model': row['model'],
            'feature_set': feature_set_name,
            'feature_scope': row['feature_scope'],
        })
        rows.append(tmp)
    if not rows:
        return pd.DataFrame(columns=['target', 'actual', 'predicted', 'model', 'feature_set', 'feature_scope'])
    return pd.concat(rows, ignore_index=True)


def run_baselines(
    df: pd.DataFrame,
    feature_sets: Dict[str, List[str]],
    selected_map: Dict[Tuple[str, str], List[str]] | None = None,
    feature_scope: str = 'full',
) -> pd.DataFrame:
    rows = []
    cv = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    for target in TARGET_COLUMNS:
        subset = df.dropna(subset=[target]).copy()
        for feature_set_name, features in feature_sets.items():
            if selected_map is None:
                active_features = [feature for feature in features if feature in subset.columns]
            else:
                active_features = [feature for feature in selected_map.get((target, feature_set_name), []) if feature in subset.columns]
            X = subset[active_features]
            y = subset[target]
            if X.empty or len(y) < N_SPLITS:
                continue

            for model_name in MODELS:
                pipeline = make_pipeline(model_name)
                y_pred = cross_val_predict(pipeline, X, y, cv=cv)
                metrics = evaluate_regression(y.to_numpy(), y_pred)
                rows.append({
                    'target': target,
                    'feature_set': feature_set_name,
                    'feature_scope': feature_scope,
                    'model': model_name,
                    'n_samples': int(len(y)),
                    'n_features': int(X.shape[1]),
                    **metrics,
                })

    return pd.DataFrame(rows).sort_values(['target', 'feature_scope', 'R2', 'RMSE'], ascending=[True, True, False, True]).reset_index(drop=True)
