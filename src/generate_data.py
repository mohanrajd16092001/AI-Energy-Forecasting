from pathlib import Path

import numpy as np
import pandas as pd


# Find the project folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "simulated_energy.csv"

# A fixed seed makes the generated data repeatable.
rng = np.random.default_rng(42)

# Create one timestamp per hour for 120 days.
timestamps = pd.date_range(
    start="2025-01-01",
    periods=120 * 24,
    freq="h",
)

# Describe working hours and weekdays.
working_hours = (timestamps.hour >= 8) & (timestamps.hour < 18)
weekdays = timestamps.dayofweek < 5

# Invent consumption patterns for a simulated building.
# Energy represents electricity consumed during each hour, in kWh.
base_consumption = 18
working_hour_usage = 14 * working_hours
weekday_usage = 8 * (working_hours & weekdays)
random_variation = rng.normal(0, 2, len(timestamps))

energy = (
    base_consumption
    + working_hour_usage
    + weekday_usage
    + random_variation
)

# Keep consumption nonnegative.
energy = np.maximum(energy, 0)

data = pd.DataFrame({
    "Datetime": timestamps,
    "Energy": energy,
})

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(OUTPUT_FILE, index=False)

print("SIMULATED DATA — not real building measurements")
print(f"Saved {len(data)} hourly records to: {OUTPUT_FILE}")
print("Energy unit: kWh per hourly interval")
print(data.head())