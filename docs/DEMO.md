# Project Demo and Proof Guide

## What this project demonstrates

This project generates simulated hourly electricity readings, prepares the data, trains an MLP neural network, evaluates later observations, generates a 24-hour forecast, and serves predictions through a local Flask API.

All results come from simulated data. No real building deployment or measured energy savings are claimed.

## Demonstration sequence

Run commands from the project folder in VS Code.

### 1. Run the workflow

```powershell
.\.venv\Scripts\python.exe main.py
```

Confirm that all seven steps complete successfully.

### 2. Explain the dataset

Open `data/simulated_energy.csv`.

Explain:

- There are 2,880 hourly records covering 120 days.
- Energy is measured in kWh per hourly interval.
- Working hours and weekdays have higher simulated consumption.
- The data is generated with a fixed random seed.

### 3. Explain preparation and training

Open these scripts:

- `src/preprocess.py`: checks timestamps, duplicates, negative readings, and missing values.
- `src/features.py`: extracts hour and weekday.
- `src/train_model.py`: trains on the first 80% of records and predicts the final 20%.

Input and target scaling are fitted during training and saved with the model.

### 4. Show evaluation results

Open `outputs/metrics.json`.

Recorded demonstration results:

| Metric | Value |
|---|---:|
| MAE | 1.6927 kWh |
| RMSE | 2.1078 kWh |
| R² | 0.9588 |
| Test records | 576 |

Use the latest generated file when discussing a new run.

R² is not an accuracy percentage. These scores describe performance on the simulated test records.

### 5. Show the graphs

Open:

- `images/energy_history.png`
- `images/actual_vs_predicted.png`
- `images/future_forecast.png`

The comparison graph shows the final 168 test hours; evaluation uses all 576 test records.

### 6. Explain the future forecast

Open `outputs/future_forecast.csv`.

The 24 predictions cover May 1, 2025, immediately after the dataset ends.

The forecast script fits a separate final model to all available records. The earlier model and held-out evaluation remain separate.

### 7. Start the API

Stop an existing API process with Ctrl+C before restarting it.

```powershell
.\.venv\Scripts\python.exe app.py
```

Restart after retraining so the API loads the updated final model.

### 8. Request predictions

Use a second VS Code PowerShell terminal.

Wednesday at 2 PM:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method Post -ContentType "application/json" -Body '{"hour":14,"day":2}'
```

Sunday at 2 PM:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method Post -ContentType "application/json" -Body '{"hour":14,"day":6}'
```

The demonstrated run returned approximately 40.26 kWh and 32.14 kWh respectively.

## Virtual planning scenario

A simulated building operator reviews the next day's forecast to identify expected periods of higher consumption.

The higher weekday prediction reflects the assumptions built into the generated dataset. An operator could consider that information when planning activities.

This project does not implement equipment scheduling, calculate electricity bills, or verify savings.

## Screenshot proof checklist

Capture actual execution evidence and save it in `images/`.

| Filename | Evidence to capture |
|---|---|
| proof_01_dataset.png | Dataset header and initial rows |
| proof_02_cleaning.png | Cleaning output with record and missing-value counts |
| proof_03_training.png | Successful training output |
| proof_04_metrics.png | MAE, RMSE, R², and simulated-data label |
| proof_05_workflow.png | All seven steps completed successfully |
| proof_06_api_weekday.png | Wednesday API request and response |
| proof_07_api_weekend.png | Sunday API request and response |
| proof_08_repository.png | Published repository and README |

The three generated graph PNGs are additional proof assets.

Capture only work that actually ran. Keep simulated-data labels visible.

## Suggested seven-day learning and commit plan

The original brief proposes a seven-day schedule. Use these as learning checkpoints or as a plan for a future rebuild. The current implementation was completed in one session; retain its actual commit history.

| Day | Focus | Evidence |
|---|---|---|
| 1 | Environment and architecture | Setup notes |
| 2 | Dataset generation and interpretation | Dataset preview |
| 3 | Cleaning and time features | Cleaning output and feature preview |
| 4 | MLP training | Training output |
| 5 | Held-out evaluation | Metrics and comparison graph |
| 6 | Future forecast and API | Forecast graph and API responses |
| 7 | Documentation and publishing | README and repository preview |

Commit changes when they are actually made, using messages that describe those changes.

## Short project explanation

I built a simulated electricity consumption forecasting project in Python. I generated hourly building readings, checked and prepared the data, and trained an MLP using hour and weekday inputs.

I evaluated the model on the latest 20% of records, then fitted a separate final model to all records for forecasting. I saved visualizations and exposed predictions through a local Flask API.

The project demonstrates a complete learning workflow using synthetic data. Real-world performance and business benefits remain untested.