import os
from pathlib import Path

# Try Streamlit secrets first, fall back to .env, then defaults
def _get_secret(key: str, default: str = "") -> str:
    # 1. Try Streamlit secrets (production)
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        pass
    # 2. Try environment variable (Render env vars)
    val = os.getenv(key)
    if val:
        return val
    # 3. Fall back to default
    return default


class Config:
    # App
    APP_NAME      = "FinSight"
    APP_VERSION   = "1.0.0"
    MODEL_VERSION = _get_secret("MODEL_VERSION", "v1.0.0")

    # Database
    DATABASE_URL  = _get_secret(
        "DATABASE_URL", "sqlite:///./finsight.db"
    )

    # Model paths
    MODEL_PATH        = "models/model.pkl"
    PREPROCESSOR_PATH = "models/preprocessor.pkl"
    EXPLAINER_PATH    = "models/explainer.pkl"

    # Score bands
    SCORE_BANDS = {
        (300, 449): ("Poor",      "High",     "#E53935"),
        (450, 579): ("Fair",      "Medium",   "#FB8C00"),
        (580, 699): ("Good",      "Low",      "#43A047"),
        (700, 850): ("Excellent", "Very Low", "#00897B"),
    }

    # UI colors
    PRIMARY_COLOR = "#0B1F3A"
    ACCENT_COLOR  = "#00BFA6"
    WARNING_COLOR = "#FB8C00"
    DANGER_COLOR  = "#E53935"
    SUCCESS_COLOR = "#43A047"


config = Config()