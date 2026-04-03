import pandas as pd

from src.cleaning import build_analysis_dataset, clean_dataset


def test_clean_dataset_drops_empty_rows_and_sorts():
    df = pd.DataFrame(
        [
            {'Date': '2023-01-02', 'Patient ID': 2, 'Collection time': 15, 'Urea': 1.0},
            {'Date': '2023-01-02', 'Patient ID': 2, 'Collection time': 0, 'Urea': 2.0},
            {'Date': None, 'Patient ID': None, 'Collection time': None, 'Urea': None},
        ]
    )
    cleaned = clean_dataset(df)
    assert len(cleaned) == 2
    assert cleaned.iloc[0]['collection_time_min'] == 0


def test_build_analysis_dataset_creates_session_id():
    df = pd.DataFrame([
        {'Date': '2023-01-02', 'Patient ID': 2, 'Collection time': 0, 'Urea': 1.0}
    ])
    result = build_analysis_dataset(df)
    assert 'session_id' in result.columns
    assert result.iloc[0]['session_id'] == '2_20230102'
    assert 'patient_id' in result.columns
