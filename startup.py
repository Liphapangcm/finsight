"""
Runs on server startup.
Trains the model if artifacts are missing (first deploy).
"""
import os
from pathlib import Path


def ensure_model_exists():
    model_path = Path("models/model.pkl")

    if not model_path.exists():
        print("▶ No model found — training now...")
        from ml.train import train
        train()
        print("✅ Model trained and saved.")
    else:
        print("✅ Model artifacts found — skipping training.")


if __name__ == "__main__":
    ensure_model_exists()