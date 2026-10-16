from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_FILE = PROJECT_ROOT / "models" / "energy_forecast_final.pkl"

app = Flask(__name__)

# Load the trained model, including its saved scaling steps.
model = joblib.load(MODEL_FILE)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Energy forecasting API is running",
        "data_source": "SIMULATED DATA",
        "instructions": "Send hour and day as JSON to POST /predict",
        "example": {"hour": 14, "day": 2},
        "weekday_numbering": "Monday=0, Sunday=6",
    })


@app.route("/predict", methods=["POST"])
def predict():
    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return jsonify({
            "error": "Send a JSON object containing hour and day."
        }), 400

    hour = body.get("hour")
    day = body.get("day")

    if type(hour) is not int or not 0 <= hour <= 23:
        return jsonify({
            "error": "hour must be an integer from 0 to 23."
        }), 400

    if type(day) is not int or not 0 <= day <= 6:
        return jsonify({
            "error": "day must be an integer from 0 to 6. Monday=0."
        }), 400

    features = pd.DataFrame({
        "hour": [hour],
        "day": [day],
    })

    prediction = float(model.predict(features)[0])

    return jsonify({
        "hour": hour,
        "day": day,
        "predicted_energy": prediction,
        "unit": "kWh per hourly interval",
        "data_source": "SIMULATED DATA",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)