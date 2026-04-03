from __future__ import annotations

import pandas as pd

from .config import ID_COLUMNS, TARGET_COLUMNS, ALL_ABSORBANCE_COLUMNS, MACHINE_COLUMNS, PERSONAL_COLUMNS
from .translation import to_english_columns


NUMERIC_COLUMNS = ID_COLUMNS[1:] + TARGET_COLUMNS + ALL_ABSORBANCE_COLUMNS + MACHINE_COLUMNS + PERSONAL_COLUMNS


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = to_english_columns(df.copy())

    cleaned = cleaned.dropna(how='all')

    if 'date' in cleaned.columns:
        cleaned['date'] = pd.to_datetime(cleaned['date'], errors='coerce')

    for col in NUMERIC_COLUMNS:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')

    cleaned = cleaned.dropna(subset=['patient_id', 'collection_time_min'], how='any')
    cleaned = cleaned.sort_values(['patient_id', 'date', 'collection_time_min']).reset_index(drop=True)
    return cleaned


def build_analysis_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_dataset(df)
    cleaned['session_id'] = (
        cleaned['patient_id'].astype(int).astype(str)
        + '_'
        + cleaned['date'].dt.strftime('%Y%m%d')
    )
    return cleaned
