import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "test_predictions.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "metrics.json"


def evaluate_model():
    data = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])

    actual = data["Actual"]
    predicted = data["Predicted"]

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)

    report = {
        "data_source": "SIMULATED DATA",
        "evaluation": "Last 20% of chronological records",
        "test_records": len(data),
        "test_start": str(data["Datetime"].min()),
        "test_end": str(data["Datetime"].max()),
        "energy_unit": "kWh per hourly interval",
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
    }

    OUTPUT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print("SIMULATED DATA — held-out evaluation")
    print(f"Testing records: {len(data)}")
    print(f"MAE:  {mae:.4f} kWh")
    print(f"RMSE: {rmse:.4f} kWh")
    print(f"R²:   {r2:.4f}")
    print(f"Saved metrics: {OUTPUT_FILE}")


if __name__ == "__main__":
    evaluate_model()