from __future__ import annotations

from typing import Dict, List

from .config import ALL_ABSORBANCE_COLUMNS, MACHINE_COLUMNS, PERSONAL_COLUMNS


FEATURE_SETS: Dict[str, List[str]] = {
    'all_absorbance_only': ALL_ABSORBANCE_COLUMNS,
    'all_absorbance_plus_machine': ALL_ABSORBANCE_COLUMNS + MACHINE_COLUMNS,
    'all_absorbance_plus_machine_plus_personal': ALL_ABSORBANCE_COLUMNS + MACHINE_COLUMNS + PERSONAL_COLUMNS,
}


def get_feature_sets() -> Dict[str, List[str]]:
    return FEATURE_SETS.copy()
