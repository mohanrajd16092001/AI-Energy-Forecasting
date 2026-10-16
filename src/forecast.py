from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def forecast_energy():
    data = pd.read_csv(
        PROJECT_ROOT / "outputs" / "energy_features.csv",
        parse_dates=["Datetime"],
    )
    data = data.sort_values("Datetime")

    model = joblib.load(
        PROJECT_ROOT / "models" / "energy_forecast_model.pkl"
    )

    # Evaluation is complete. Fit the final model to all available data.
    print("Training the final model on all simulated records...")
    model.fit(data[["hour", "day"]], data["Energy"])

    final_model_path = (
        PROJECT_ROOT / "models" / "energy_forecast_final.pkl"
    )
    joblib.dump(model, final_model_path)

    # Begin one hour after the last recorded timestamp.
    future_times = pd.date_range(
        start=data["Datetime"].max() + pd.Timedelta(hours=1),
        periods=24,
        freq="h",
    )

    future_inputs = pd.DataFrame({
        "hour": future_times.hour,
        "day": future_times.dayofweek,
    })

    predictions = model.predict(future_inputs)

    forecast = pd.DataFrame({
        "Datetime": future_times,
        "Predicted": predictions,
    })

    forecast_path = PROJECT_ROOT / "outputs" / "future_forecast.csv"
    forecast.to_csv(forecast_path, index=False)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        forecast["Datetime"],
        forecast["Predicted"],
        marker="o",
        label="MLP forecast",
    )

    ax.set_title("Next 24 Hours After Dataset Ends — SIMULATED DATA")
    ax.set_xlabel("Date and hour")
    ax.set_ylabel("Predicted hourly energy consumption (kWh)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()

    graph_path = PROJECT_ROOT / "images" / "future_forecast.png"
    fig.savefig(graph_path, dpi=150)
    plt.close(fig)

    print("SIMULATED DATA — 24-hour forecast generated")
    print(forecast.to_string(index=False))
    print(f"Saved final model: {final_model_path}")
    print(f"Saved forecast: {forecast_path}")
    print(f"Saved graph: {graph_path}")


if __name__ == "__main__":
    forecast_energy()