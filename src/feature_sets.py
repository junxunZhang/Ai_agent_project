from __future__ import annotations

from typing import Dict, List

from .config import CORE_ABSORBANCE_COLUMNS, MACHINE_COLUMNS, PERSONAL_COLUMNS


FEATURE_SETS: Dict[str, List[str]] = {
    'absorbance_only': CORE_ABSORBANCE_COLUMNS,
    'absorbance_plus_context': CORE_ABSORBANCE_COLUMNS + PERSONAL_COLUMNS + MACHINE_COLUMNS,
}


def get_feature_sets() -> Dict[str, List[str]]:
    return FEATURE_SETS.copy()
