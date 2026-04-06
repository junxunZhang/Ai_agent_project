from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, ParameterGrid

from .config import RANDOM_STATE, TARGET_COLUMNS
from .modeling import make_pipeline


MODELS_TO_COMPARE = ['svr_rbf', 'linear_regression', 'random_forest', 'knn_regressor']


def _metric_dict(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    return {
        'MAE': float(mean_absolute_error(y_true, y_pred)),
        'MSE': float(mse),
        'RMSE': float(np.sqrt(mse)),
        'R2': float(r2_score(y_true, y_pred)),
    }


def _param_grid_for_model(model_name: str) -> list[dict]:
    if model_name == 'svr_rbf':
        return list(ParameterGrid({'model__C': [1.0, 10.0], 'model__epsilon': [0.05, 0.1]}))
    if model_name == 'knn_regressor':
        return list(ParameterGrid({'model__n_neighbors': [3, 5, 7], 'model__weights': ['uniform', 'distance']}))
    if model_name == 'random_forest':
        return list(ParameterGrid({'model__n_estimators': [200], 'model__max_depth': [None, 6, 10]}))
    return [{}]


def _select_features_from_training_only(X_train: pd.DataFrame, y_train: pd.Series, max_features: int = 8) -> list[str]:
    imputer = SimpleImputer(strategy='median')
    X_imp = imputer.fit_transform(X_train)
    k = min(max_features, X_train.shape[1])
    selector = SelectKBest(score_func=mutual_info_regression, k=k)
    selector.fit(X_imp, y_train)
    mask = selector.get_support()
    return X_train.columns[mask].tolist()


def split_sessions_train_val_test(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, int]]:
    sessions = df[['session_id']].drop_duplicates().copy()
    groups = sessions['session_id'].to_numpy()

    gss_test = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_STATE)
    trainval_idx, test_idx = next(gss_test.split(sessions, groups=groups))
    trainval_sessions = sessions.iloc[trainval_idx]['session_id']
    test_sessions = sessions.iloc[test_idx]['session_id']

    trainval_df = df[df['session_id'].isin(trainval_sessions)].copy()
    test_df = df[df['session_id'].isin(test_sessions)].copy()

    gss_val = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=RANDOM_STATE)
    inner_sessions = trainval_df[['session_id']].drop_duplicates().copy()
    inner_groups = inner_sessions['session_id'].to_numpy()
    train_idx, val_idx = next(gss_val.split(inner_sessions, groups=inner_groups))
    train_sessions = inner_sessions.iloc[train_idx]['session_id']
    val_sessions = inner_sessions.iloc[val_idx]['session_id']

    train_df = trainval_df[trainval_df['session_id'].isin(train_sessions)].copy()
    val_df = trainval_df[trainval_df['session_id'].isin(val_sessions)].copy()

    info = {
        'train_sessions': int(train_df['session_id'].nunique()),
        'val_sessions': int(val_df['session_id'].nunique()),
        'test_sessions': int(test_df['session_id'].nunique()),
    }
    return train_df, val_df, test_df, info


def run_strict_train_val_test_protocol(
    df: pd.DataFrame,
    feature_sets: Dict[str, List[str]],
    max_selected_features: int = 8,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, int]]:
    train_df, val_df, test_df, split_info = split_sessions_train_val_test(df)

    selection_rows = []
    test_rows = []
    prediction_rows = []

    for target in TARGET_COLUMNS:
        train_target = train_df.dropna(subset=[target]).copy()
        val_target = val_df.dropna(subset=[target]).copy()
        test_target = test_df.dropna(subset=[target]).copy()

        for feature_set_name, features in feature_sets.items():
            available_features = [feature for feature in features if feature in train_target.columns]
            if not available_features:
                continue

            X_train_full = train_target[available_features]
            y_train = train_target[target]
            X_val_full = val_target[[f for f in available_features if f in val_target.columns]].copy()
            X_test_full = test_target[[f for f in available_features if f in test_target.columns]].copy()
            y_val = val_target[target]
            y_test = test_target[target]

            if X_val_full.empty or X_test_full.empty:
                continue

            selected_features = _select_features_from_training_only(X_train_full, y_train, max_selected_features)
            X_train = X_train_full[selected_features]
            X_val = X_val_full[selected_features]
            X_test = X_test_full[selected_features]

            for model_name in MODELS_TO_COMPARE:
                inner_groups = train_target['session_id']
                unique_sessions = inner_groups.nunique()
                inner_splits = min(4, unique_sessions)
                best_params = {}

                if inner_splits >= 2:
                    inner_cv = GroupKFold(n_splits=inner_splits)
                    best_score = -np.inf
                    for params in _param_grid_for_model(model_name):
                        fold_scores = []
                        for inner_train_idx, inner_val_idx in inner_cv.split(X_train, y_train, groups=inner_groups):
                            pipe = make_pipeline(model_name)
                            if params:
                                pipe.set_params(**params)
                            pipe.fit(X_train.iloc[inner_train_idx], y_train.iloc[inner_train_idx])
                            preds = pipe.predict(X_train.iloc[inner_val_idx])
                            fold_scores.append(r2_score(y_train.iloc[inner_val_idx], preds))
                        score = float(np.mean(fold_scores)) if fold_scores else -np.inf
                        if score > best_score:
                            best_score = score
                            best_params = params

                model = make_pipeline(model_name)
                if best_params:
                    model.set_params(**best_params)
                model.fit(X_train, y_train)
                val_preds = model.predict(X_val)
                val_metrics = _metric_dict(y_val.to_numpy(), val_preds)
                selection_rows.append({
                    'target': target,
                    'feature_set': feature_set_name,
                    'model': model_name,
                    'selection_stage': 'validation_only',
                    'selected_features': ', '.join(selected_features),
                    'n_selected_features': len(selected_features),
                    **val_metrics,
                })

    selection_df = pd.DataFrame(selection_rows)
    best_models = (
        selection_df.sort_values(['target', 'R2', 'RMSE'], ascending=[True, False, True])
        .groupby('target', as_index=False)
        .head(1)
        .reset_index(drop=True)
    )

    for _, row in best_models.iterrows():
        target = row['target']
        feature_set_name = row['feature_set']
        model_name = row['model']
        selected_features = [f.strip() for f in row['selected_features'].split(',') if f.strip()]

        train_target = train_df.dropna(subset=[target]).copy()
        val_target = val_df.dropna(subset=[target]).copy()
        test_target = test_df.dropna(subset=[target]).copy()

        trainval_target = pd.concat([train_target, val_target], ignore_index=True)
        X_trainval = trainval_target[selected_features]
        y_trainval = trainval_target[target]
        X_test = test_target[selected_features]
        y_test = test_target[target]

        model = make_pipeline(model_name)
        model.fit(X_trainval, y_trainval)
        test_preds = model.predict(X_test)
        test_metrics = _metric_dict(y_test.to_numpy(), test_preds)
        test_rows.append({
            'target': target,
            'feature_set': feature_set_name,
            'model': model_name,
            'evaluation_stage': 'test_only',
            'selected_features': ', '.join(selected_features),
            'n_selected_features': len(selected_features),
            **test_metrics,
        })

        for sid, t, a, p in zip(test_target['session_id'], test_target['collection_time_min'], y_test.tolist(), test_preds.tolist()):
            prediction_rows.append({
                'target': target,
                'feature_set': feature_set_name,
                'model': model_name,
                'session_id': sid,
                'collection_time_min': t,
                'actual': a,
                'predicted': p,
            })

    return selection_df, best_models, pd.DataFrame(test_rows), pd.DataFrame(prediction_rows), split_info
