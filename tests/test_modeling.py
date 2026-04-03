import pandas as pd

from src.modeling import run_baselines


def test_run_baselines_returns_metrics():
    rows = []
    for i in range(10):
        rows.append(
            {
                'Urea': i + 1,
                'Creatinine': i + 2,
                'Acid': i + 0.5,
                'Potassium': 2.0 + i * 0.1,
                'Phosphorus': 1.0 + i * 0.05,
                'β2-microglobulin': 100 + i,
                '255nm': 0.1 * i,
                '275nm': 0.2 * i,
                '310nm': 0.3 * i,
                '透析年長': 1.0,
                '乾體重': 60.0,
                '身高': 1.7,
                '年齡': 50,
                '膜面積': 1.8,
                '透析日': 1,
                '靜脈壓': 100,
                '膜內外壓': 80,
                '動脈流速': 300,
                '每小時脫水量': 500,
                '目標脫水量': 3000,
                '當前脫水量': 100 + i,
                '當前藥水流速': 450,
                '藥水離子濃度': 140,
            }
        )
    df = pd.DataFrame(rows)
    feature_sets = {
        'absorbance_only': ['255nm', '275nm', '310nm'],
    }
    results = run_baselines(df, feature_sets)
    assert not results.empty
    assert {'MAE', 'MSE', 'RMSE', 'R2'}.issubset(results.columns)
