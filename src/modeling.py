from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from .config import N_SPLITS, RANDOM_STATE, TARGET_COLUMNS


MODELS = {
    'linear_regression': LinearRegression(),
    'svr_rbf': SVR(kernel='rbf', C=10.0, epsilon=0.1),
}


def make_pipeline(model_name: str) -> Pipeline:
    model = MODELS[model_name]
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('model', model),
    ])


def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    return {
        'MAE': float(mean_absolute_error(y_true, y_pred)),
        'MSE': float(mse),
        'RMSE': float(np.sqrt(mse)),
        'R2': float(r2_score(y_true, y_pred)),
    }


def run_baselines(df: pd.DataFrame, feature_sets: Dict[str, List[str]]) -> pd.DataFrame:
    rows = []
    cv = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    for target in TARGET_COLUMNS:
        subset = df.dropna(subset=[target]).copy()
        for feature_set_name, features in feature_sets.items():
            available_features = [feature for feature in features if feature in subset.columns]
            X = subset[available_features]
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
                    'model': model_name,
                    'n_samples': int(len(y)),
                    'n_features': int(X.shape[1]),
                    **metrics,
                })

    return pd.DataFrame(rows).sort_values(['target', 'R2', 'RMSE'], ascending=[True, False, True]).reset_index(drop=True)
