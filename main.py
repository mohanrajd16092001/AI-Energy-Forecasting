from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent


def main():
    steps = [
        ("Generate simulated data", "generate_data.py"),
        ("Clean the data", "preprocess.py"),
        ("Create time features", "features.py"),
        ("Train and save the model", "train_model.py"),
        ("Evaluate test predictions", "evaluate.py"),
        ("Create evaluation graphs", "visualize.py"),
        ("Generate the next 24-hour forecast", "forecast.py"),
    ]

    print("AI-Powered Energy Consumption Forecasting")
    print("Data source: SIMULATED DATA", flush=True)

    for number, (description, filename) in enumerate(steps, start=1):
        print(
            f"\nStep {number}/{len(steps)}: {description}",
            flush=True,
        )

        script_path = PROJECT_ROOT / "src" / filename

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_ROOT,
                check=True,
            )
        except subprocess.CalledProcessError:
            print(f"\nStopped because {filename} failed.")
            print("Check the error above before running again.")
            sys.exit(1)

    print("\nAll seven steps completed successfully.")
    print("Results: outputs folder")
    print("Graphs: images folder")
    print("Saved models: models folder")
    print("Start app.py separately to use the prediction API.")


if __name__ == "__main__":
    main()