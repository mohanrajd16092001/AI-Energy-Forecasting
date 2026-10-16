from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "simulated_energy.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "cleaned_energy.csv"


def clean_data():
    data = pd.read_csv(INPUT_FILE)

    required_columns = {"Datetime", "Energy"}
    if not required_columns.issubset(data.columns):
        raise ValueError("The CSV must contain Datetime and Energy columns.")

    data["Datetime"] = pd.to_datetime(data["Datetime"], errors="coerce")
    data["Energy"] = pd.to_numeric(data["Energy"], errors="coerce")

    if data["Datetime"].isna().any():
        raise ValueError("Some timestamps are missing or invalid.")

    if (data["Energy"].dropna() < 0).any():
        raise ValueError("Energy consumption cannot be negative.")

    if data["Datetime"].duplicated().any():
        raise ValueError("Duplicate timestamps found. Check the input data.")

    data = data.sort_values("Datetime").set_index("Datetime")

    # This simulated dataset contains one measurement per hour.
    # Add any missing hourly timestamps.
    data = data[["Energy"]].asfreq("h")

    missing_before = int(data["Energy"].isna().sum())
    print(f"Missing hourly readings before cleaning: {missing_before}")

    # Fill a missing reading using the most recent earlier reading.
    data["Energy"] = data["Energy"].ffill()

    # A missing first reading has no earlier value to use.
    if data["Energy"].isna().any():
        raise ValueError("Starting readings are missing and cannot be filled.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index_label="Datetime")

    print("SIMULATED DATA — cleaned successfully")
    print(f"Hourly records: {len(data)}")
    print(f"Missing readings after cleaning: {data['Energy'].isna().sum()}")
    print(f"Saved to: {OUTPUT_FILE}")
    print(data.head())


if __name__ == "__main__":
    clean_data()