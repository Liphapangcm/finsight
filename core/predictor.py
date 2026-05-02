"""
Loads saved model artifacts and runs credit score inference.
Singleton pattern — artifacts are loaded once at startup, not per request.
"""

import pickle
import numpy as np
from pathlib import Path
from functools import lru_cache

from config import config
from core.features import engineer_features, compute_kpis
from core.schemas import AssessmentInput


# Add to core/predictor.py — replace the _load_artifacts function

@lru_cache(maxsize=1)
def _load_artifacts():
    """
    Loads model artifacts with clear error messages if files are missing.
    """
    missing = []
    for path in [config.MODEL_PATH,
                 config.PREPROCESSOR_PATH,
                 config.EXPLAINER_PATH]:
        if not Path(path).exists():
            missing.append(path)

    if missing:
        raise FileNotFoundError(
            f"Model artifacts not found: {missing}\n"
            f"Run `python -m ml.train` first to generate them."
        )

    with open(config.MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(config.PREPROCESSOR_PATH, "rb") as f:
        scaler = pickle.load(f)
    with open(config.EXPLAINER_PATH, "rb") as f:
        explainer = pickle.load(f)

    return model, scaler, explainer

# ── Score band helper ─────────────────────────────────────────────────────────

def get_score_band(score: int) -> tuple[str, str, str]:
    """Returns (band_label, risk_level, hex_color) for a given score."""
    for (low, high), (band, risk, color) in config.SCORE_BANDS.items():
        if low <= score <= high:
            return band, risk, color
    return "Poor", "High", config.DANGER_COLOR


# ── Main prediction function ──────────────────────────────────────────────────

def predict(inp: AssessmentInput) -> dict:
    """
    Takes a validated AssessmentInput and returns raw prediction data.
    Called by the service layer — not called directly by Streamlit.

    Returns:
        {
            'credit_score': int,
            'score_band':   str,
            'risk_level':   str,
            'score_color':  str,
            'kpis':         dict,
            'feature_df':   pd.DataFrame,   ← used by explainer
            'scaled_arr':   np.ndarray,     ← used by explainer
        }
    """
    model, scaler, _ = _load_artifacts()

    raw        = inp.to_dict()
    feature_df = engineer_features(raw)
    scaled_arr = scaler.transform(feature_df)

    raw_score    = float(model.predict(scaled_arr)[0])
    credit_score = int(np.clip(round(raw_score), 300, 850))
    band, risk, color = get_score_band(credit_score)
    kpis         = compute_kpis(raw)

    return {
        'credit_score': credit_score,
        'score_band':   band,
        'risk_level':   risk,
        'score_color':  color,
        'kpis':         kpis,
        'feature_df':   feature_df,
        'scaled_arr':   scaled_arr,
    }