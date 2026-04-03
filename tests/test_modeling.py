import pandas as pd

from src.modeling import run_baselines


def test_run_baselines_returns_metrics():
    rows = []
    for i in range(10):
        rows.append(
            {
                'urea': i + 1,
                'creatinine': i + 2,
                'acid_inferred_uric_acid': i + 0.5,
                'potassium': 2.0 + i * 0.1,
                'phosphorus': 1.0 + i * 0.05,
                'beta2_microglobulin': 100 + i,
                'absorbance_255nm': 0.1 * i,
                'absorbance_275nm': 0.2 * i,
                'absorbance_310nm': 0.3 * i,
                'dialysis_vintage_years': 1.0,
                'dry_weight': 60.0,
                'height_m': 1.7,
                'age': 50,
                'membrane_area': 1.8,
                'dialysis_day_type': 1,
                'venous_pressure': 100,
                'transmembrane_pressure': 80,
                'arterial_flow_rate': 300,
                'hourly_ultrafiltration_volume': 500,
                'target_ultrafiltration_volume': 3000,
                'current_ultrafiltration_volume': 100 + i,
                'current_dialysate_flow_rate': 450,
                'dialysate_ionic_concentration': 140,
            }
        )
    df = pd.DataFrame(rows)
    feature_sets = {
        'absorbance_only': ['absorbance_255nm', 'absorbance_275nm', 'absorbance_310nm'],
    }
    results = run_baselines(df, feature_sets)
    assert not results.empty
    assert {'MAE', 'MSE', 'RMSE', 'R2'}.issubset(results.columns)
