from __future__ import annotations

import pandas as pd

from .config import ENGLISH_COLUMN_MAP


def to_english_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=ENGLISH_COLUMN_MAP)
