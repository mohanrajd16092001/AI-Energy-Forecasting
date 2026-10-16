from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "outputs" / "energy_features.csv"
MODEL_FILE = PROJECT_ROOT / "models" / "energy_forecast_model.pkl"
TEST_FILE = PROJECT_ROOT / "outputs" / "test_predictions.csv"


def train_model():
    data = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])
    data = data.sort_values("Datetime").reset_index(drop=True)

    # Inputs: hour and weekday. Target: hourly energy consumption.
    X = data[["hour", "day"]]
    y = data["Energy"]

    # Keep later observations separate for testing.
    split = int(len(data) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    # Scale input values before passing them to the neural network.
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(64, 64),
            max_iter=500,
            random_state=42,
        )),
    ])

    # Scale the target during training.
    # Predictions are automatically converted back to kWh.
    model = TransformedTargetRegressor(
        regressor=pipeline,
        transformer=StandardScaler(),
    )

    print("SIMULATED DATA — starting MLP training")
    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    results = pd.DataFrame({
        "Datetime": data["Datetime"].iloc[split:].to_numpy(),
        "Actual": y_test.to_numpy(),
        "Predicted": predictions,
    })

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_FILE)
    results.to_csv(TEST_FILE, index=False)

    print("Training completed.")
    print(f"Saved model: {MODEL_FILE}")
    print(f"Saved test predictions: {TEST_FILE}")
    print(results.head())


if __name__ == "__main__":
    train_model()