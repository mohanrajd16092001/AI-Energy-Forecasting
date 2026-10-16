from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "cleaned_energy.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "energy_features.csv"


def create_features():
    data = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])

    # These are the two model inputs specified in the document.
    data["hour"] = data["Datetime"].dt.hour
    data["day"] = data["Datetime"].dt.dayofweek

    # Energy remains the target: the value the model will learn to predict.
    data = data[["Datetime", "hour", "day", "Energy"]]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False)

    print("SIMULATED DATA — time features created")
    print(f"Records: {len(data)}")
    print("Inputs: hour and day")
    print("Target: Energy (kWh per hourly interval)")
    print(f"Saved to: {OUTPUT_FILE}")
    print(data.head())


if __name__ == "__main__":
    create_features()