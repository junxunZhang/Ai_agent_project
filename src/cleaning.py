from __future__ import annotations

import pandas as pd

from .config import ID_COLUMNS, TARGET_COLUMNS, ALL_ABSORBANCE_COLUMNS, MACHINE_COLUMNS, PERSONAL_COLUMNS


NUMERIC_COLUMNS = ID_COLUMNS[1:] + TARGET_COLUMNS + ALL_ABSORBANCE_COLUMNS + MACHINE_COLUMNS + PERSONAL_COLUMNS


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned = cleaned.dropna(how='all')

    if 'Date' in cleaned.columns:
        cleaned['Date'] = pd.to_datetime(cleaned['Date'], errors='coerce')

    for col in NUMERIC_COLUMNS:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')

    cleaned = cleaned.dropna(subset=['Patient ID', 'Collection time'], how='any')
    cleaned = cleaned.sort_values(['Patient ID', 'Date', 'Collection time']).reset_index(drop=True)
    return cleaned


def build_analysis_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_dataset(df)
    cleaned['session_id'] = (
        cleaned['Patient ID'].astype(int).astype(str)
        + '_'
        + cleaned['Date'].dt.strftime('%Y%m%d')
    )
    return cleaned
