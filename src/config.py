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

ID_COLUMNS = ['Date', 'Patient ID', 'Collection time']
TARGET_COLUMNS = ['Urea', 'Creatinine', 'Acid', 'Potassium', 'Phosphorus', 'β2-microglobulin']
CORE_ABSORBANCE_COLUMNS = ['255nm', '275nm', '310nm']
EXTRA_ABSORBANCE_COLUMNS = ['285nm', '295nm']
ALL_ABSORBANCE_COLUMNS = CORE_ABSORBANCE_COLUMNS + EXTRA_ABSORBANCE_COLUMNS
MACHINE_COLUMNS = ['靜脈壓', '膜內外壓', '動脈流速', '每小時脫水量', '目標脫水量', '當前脫水量', '當前藥水流速', '藥水離子濃度']
PERSONAL_COLUMNS = ['透析年長', '乾體重', '身高', '年齡', '膜面積', '透析日']

RANDOM_STATE = 42
N_SPLITS = 5
