from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_FOLDER = PROJECT_ROOT / "images"


def create_graphs():
    history = pd.read_csv(
        PROJECT_ROOT / "outputs" / "cleaned_energy.csv",
        parse_dates=["Datetime"],
    )

    predictions = pd.read_csv(
        PROJECT_ROOT / "outputs" / "test_predictions.csv",
        parse_dates=["Datetime"],
    )

    IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)

    # Graph 1: All simulated hourly consumption readings.
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        history["Datetime"],
        history["Energy"],
        linewidth=0.8,
        label="Simulated consumption",
    )

    ax.set_title("Energy Consumption History — SIMULATED DATA")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hourly energy consumption (kWh)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(IMAGE_FOLDER / "energy_history.png", dpi=150)
    plt.close(fig)

    # Graph 2: Last 168 test hours, keeping the comparison readable.
    recent = predictions.tail(168)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        recent["Datetime"],
        recent["Actual"],
        label="Actual simulated reading",
        linewidth=1,
    )

    ax.plot(
        recent["Datetime"],
        recent["Predicted"],
        label="MLP prediction",
        linestyle="--",
        linewidth=1.5,
    )

    ax.set_title("Actual vs Predicted — Final Test Week — SIMULATED DATA")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hourly energy consumption (kWh)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(IMAGE_FOLDER / "actual_vs_predicted.png", dpi=150)
    plt.close(fig)

    print("Saved graphs:")
    print(IMAGE_FOLDER / "energy_history.png")
    print(IMAGE_FOLDER / "actual_vs_predicted.png")


if __name__ == "__main__":
    create_graphs()