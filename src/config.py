from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / 'shin_clinical_data.xlsx'
PRIMARY_SHEET = '刪除異常值'
SECONDARY_SHEET = 'ALL DATA'

OUTPUT_DIR = PROJECT_ROOT / 'outputs'
FIGURES_DIR = OUTPUT_DIR / 'figures'
REPORTS_DIR = OUTPUT_DIR / 'reports'
TABLES_DIR = OUTPUT_DIR / 'tables'
PPT_DIR = PROJECT_ROOT / 'ppt'
ASSETS_DIR = PROJECT_ROOT / 'assets'
DOCS_DIR = PROJECT_ROOT / 'docs'

RAW_ID_COLUMNS = ['Date', 'Patient ID', 'Collection time']
RAW_TARGET_COLUMNS = ['Urea', 'Creatinine', 'Acid', 'Potassium', 'Phosphorus', 'β2-microglobulin']
RAW_CORE_ABSORBANCE_COLUMNS = ['255nm', '275nm', '310nm']
RAW_EXTRA_ABSORBANCE_COLUMNS = ['285nm', '295nm']
RAW_ALL_ABSORBANCE_COLUMNS = RAW_CORE_ABSORBANCE_COLUMNS + RAW_EXTRA_ABSORBANCE_COLUMNS
RAW_MACHINE_COLUMNS = ['靜脈壓', '膜內外壓', '動脈流速', '每小時脫水量', '目標脫水量', '當前脫水量', '當前藥水流速', '藥水離子濃度']
RAW_PERSONAL_COLUMNS = ['透析年長', '乾體重', '身高', '年齡', '膜面積', '透析日']

RANDOM_STATE = 42
N_SPLITS = 5

ENGLISH_COLUMN_MAP = {
    'Date': 'date',
    'Patient ID': 'patient_id',
    'Collection time': 'collection_time_min',
    'Urea': 'urea',
    'Creatinine': 'creatinine',
    'Acid': 'acid_inferred_uric_acid',
    'Potassium': 'potassium',
    'Phosphorus': 'phosphorus',
    'β2-microglobulin': 'beta2_microglobulin',
    '255nm': 'absorbance_255nm',
    '275nm': 'absorbance_275nm',
    '285nm': 'absorbance_285nm',
    '295nm': 'absorbance_295nm',
    '310nm': 'absorbance_310nm',
    '靜脈壓': 'venous_pressure',
    '膜內外壓': 'transmembrane_pressure',
    '動脈流速': 'arterial_flow_rate',
    '每小時脫水量': 'hourly_ultrafiltration_volume',
    '目標脫水量': 'target_ultrafiltration_volume',
    '當前脫水量': 'current_ultrafiltration_volume',
    '當前藥水流速': 'current_dialysate_flow_rate',
    '藥水離子濃度': 'dialysate_ionic_concentration',
    '透析年長': 'dialysis_vintage_years',
    '乾體重': 'dry_weight',
    '身高': 'height_m',
    '年齡': 'age',
    '膜面積': 'membrane_area',
    '透析日': 'dialysis_day_type',
}

ID_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_ID_COLUMNS]
TARGET_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_TARGET_COLUMNS]
CORE_ABSORBANCE_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_CORE_ABSORBANCE_COLUMNS]
EXTRA_ABSORBANCE_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_EXTRA_ABSORBANCE_COLUMNS]
ALL_ABSORBANCE_COLUMNS = CORE_ABSORBANCE_COLUMNS + EXTRA_ABSORBANCE_COLUMNS
MACHINE_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_MACHINE_COLUMNS]
PERSONAL_COLUMNS = [ENGLISH_COLUMN_MAP[c] for c in RAW_PERSONAL_COLUMNS]
