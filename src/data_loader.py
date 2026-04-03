from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import DATA_FILE, PRIMARY_SHEET, SECONDARY_SHEET


@dataclass
class WorkbookSummary:
    sheet_name: str
    rows: int
    columns: int
    column_names: List[str]


def load_workbook_sheets() -> Dict[str, pd.DataFrame]:
    return {
        PRIMARY_SHEET: pd.read_excel(DATA_FILE, sheet_name=PRIMARY_SHEET),
        SECONDARY_SHEET: pd.read_excel(DATA_FILE, sheet_name=SECONDARY_SHEET),
    }


def get_sheet_summaries() -> List[WorkbookSummary]:
    sheets = load_workbook_sheets()
    return [
        WorkbookSummary(
            sheet_name=name,
            rows=int(df.shape[0]),
            columns=int(df.shape[1]),
            column_names=df.columns.tolist(),
        )
        for name, df in sheets.items()
    ]


def load_primary_dataset() -> pd.DataFrame:
    return pd.read_excel(DATA_FILE, sheet_name=PRIMARY_SHEET)
