from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import pandas as pd

from .config import OUTPUT_DIR
from .modeling import _resolve_features, make_pipeline

MODELS_DIR = OUTPUT_DIR / 'models'


def save_final_models(
    df: pd.DataFrame,
    best_models: pd.DataFrame,
    feature_sets: Dict[str, List[str]],
    selected_map: Dict[Tuple[str, str], List[str]] | None = None,
) -> pd.DataFrame:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []

    for _, row in best_models.iterrows():
        target = row['target']
        feature_set_name = row['feature_set']
        feature_scope = row.get('feature_scope', 'full')
        model_name = row['model']
        subset = df.dropna(subset=[target]).copy()
        features = _resolve_features(subset, target, feature_set_name, feature_sets, selected_map, feature_scope)
        if not features:
            continue

        pipeline = make_pipeline(model_name)
        pipeline.fit(subset[features], subset[target])

        model_path = MODELS_DIR / f'{target}_model.joblib'
        meta_path = MODELS_DIR / f'{target}_metadata.json'
        joblib.dump(pipeline, model_path)
        metadata = {
            'target': target,
            'model': model_name,
            'feature_set': feature_set_name,
            'feature_scope': feature_scope,
            'features': features,
            'metrics': {
                'R2': float(row['R2']),
                'RMSE': float(row['RMSE']),
                'MAE': float(row['MAE']),
            },
        }
        meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        manifest_rows.append({
            'target': target,
            'model_path': str(model_path.relative_to(OUTPUT_DIR.parent)),
            'metadata_path': str(meta_path.relative_to(OUTPUT_DIR.parent)),
            'model': model_name,
            'feature_set': feature_set_name,
            'feature_scope': feature_scope,
            'n_features': len(features),
            'R2': float(row['R2']),
            'RMSE': float(row['RMSE']),
            'MAE': float(row['MAE']),
        })

    manifest = pd.DataFrame(manifest_rows)
    manifest.to_csv(MODELS_DIR / 'model_manifest.csv', index=False)
    return manifest


def load_model_bundle(target: str):
    model_path = MODELS_DIR / f'{target}_model.joblib'
    meta_path = MODELS_DIR / f'{target}_metadata.json'
    model = joblib.load(model_path)
    metadata = json.loads(meta_path.read_text(encoding='utf-8'))
    return model, metadata


def build_session_predictions_from_saved_models(
    df: pd.DataFrame,
    best_models: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:
    predictions: Dict[str, pd.DataFrame] = {}
    for _, row in best_models.iterrows():
        target = row['target']
        model, metadata = load_model_bundle(target)
        features = metadata['features']
        subset = df.dropna(subset=[target]).copy()
        available_features = [feature for feature in features if feature in subset.columns]
        if len(available_features) != len(features):
            continue
        session_df = subset[['session_id', 'collection_time_min', target] + features].copy()
        session_df['predicted'] = model.predict(session_df[features])
        predictions[target] = session_df[['session_id', 'collection_time_min', target, 'predicted']].rename(columns={target: 'actual'})
    return predictions
