from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .config import ID_COLUMNS, TARGET_COLUMNS


def summarize_dataset(df: pd.DataFrame) -> Dict[str, object]:
    session_counts = (
        df.groupby(['Patient ID', 'Date'], dropna=False)
        .size()
        .reset_index(name='rows_per_session')
    )
    collection_times = sorted(df['Collection time'].dropna().unique().tolist()) if 'Collection time' in df.columns else []

    return {
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'missing_values': df.isna().sum().to_dict(),
        'duplicate_rows': int(df.duplicated().sum()),
        'unique_patients': int(df['Patient ID'].nunique(dropna=True)) if 'Patient ID' in df.columns else 0,
        'target_missing': df[TARGET_COLUMNS].isna().sum().to_dict(),
        'session_count': int(session_counts.shape[0]),
        'collection_times': collection_times,
    }


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include='all').transpose()


def missing_values_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df.isna().sum().reset_index()
    table.columns = ['column_name', 'missing_count']
    table['missing_pct'] = table['missing_count'] / len(df)
    return table.sort_values(['missing_count', 'column_name'], ascending=[False, True]).reset_index(drop=True)


def session_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(['Patient ID', 'Date'], dropna=False)
        .agg(rows_per_session=('Collection time', 'size'), min_time=('Collection time', 'min'), max_time=('Collection time', 'max'))
        .reset_index()
        .sort_values(['Patient ID', 'Date'])
    )


def target_correlation(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    available = [col for col in columns if col in df.columns]
    return df[available].corr(numeric_only=True)
