"""
Runs on server startup.
Creates required directories and trains the model if artifacts are missing.
"""

from pathlib import Path


def ensure_directories():
    """Create all required directories if they don't exist."""
    dirs = [
        "models",
        "ml/data/raw",
        "ml/data/processed",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("✅ Directories verified.")


def ensure_model_exists():
    ensure_directories()

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
