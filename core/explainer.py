"""
Generates SHAP explanations for a prediction.
Translates raw SHAP values into human-readable feature impacts.
"""

import numpy as np
import pandas as pd
from functools import lru_cache
import pickle

from config import config
from core.schemas import SHAPExplanation
from core.features import FEATURE_COLUMNS

# Human-readable labels for each feature
FEATURE_LABELS = {
    "debt_to_income_ratio": "Debt-to-Income Ratio",
    "expense_ratio": "Expense Ratio",
    "savings_rate": "Savings Rate",
    "housing_burden": "Housing Cost Burden",
    "discretionary_ratio": "Discretionary Income",
    "affordability_index": "Affordability Index",
    "debt_service_ratio": "Debt Repayment Load",
    "savings_consistency": "Savings Consistency",
    "net_monthly_cash_flow": "Monthly Cash Flow",
    "num_active_loans": "Number of Active Loans",
    "num_dependents": "Number of Dependents",
    "age": "Age",
    "payment_score": "Payment Regularity",
    "mobile_money_score": "Mobile Money Usage",
    "has_defaulted": "Previous Loan Default",
    "high_debt_flag": "High Debt Warning",
    "deficit_flag": "Monthly Deficit",
    "overextended_flag": "Too Many Loans",
    "housing_stress_flag": "Housing Stress",
    "employment_encoded": "Employment Stability",
    "dependency_burden": "Dependency Burden",
}


@lru_cache(maxsize=1)
def _load_explainer():
    with open(config.EXPLAINER_PATH, "rb") as f:
        return pickle.load(f)


def explain(feature_df: pd.DataFrame) -> SHAPExplanation:
    """
    Computes SHAP values for a single prediction.
    Returns a SHAPExplanation with human-readable labels,
    sorted by absolute impact (most impactful first).
    """
    explainer = _load_explainer()
    shap_values = explainer.shap_values(feature_df)

    # shap_values shape: (1, n_features) — take first row
    values = shap_values[0] if len(shap_values.shape) > 1 else shap_values
    base = float(explainer.expected_value)

    # Sort by absolute impact
    indices = np.argsort(np.abs(values))[::-1]
    sorted_feat = [
        FEATURE_LABELS.get(FEATURE_COLUMNS[i], FEATURE_COLUMNS[i]) for i in indices
    ]
    sorted_vals = [float(values[i]) for i in indices]

    return SHAPExplanation(
        feature_names=sorted_feat,
        shap_values=sorted_vals,
        base_value=base,
    )


def get_top_negative_features(
    explanation: SHAPExplanation, n: int = 5
) -> list[tuple[str, float]]:
    """
    Returns the top N features that are HURTING the score.
    Used by the recommender to know what to address first.
    """
    pairs = zip(explanation.feature_names, explanation.shap_values)
    negative = [(name, val) for name, val in pairs if val < 0]
    negative.sort(key=lambda x: x[1])  # most negative first
    return negative[:n]


def get_score_narrative(
    result_score: int,
    band: str,
    explanation: "SHAPExplanation",
    kpis: dict,
) -> str:
    """
    Generates a 2–3 sentence plain-language summary of the score.
    Shown at the top of the results page for non-technical users.
    """
    # Find top positive and negative drivers
    pairs = list(zip(explanation.feature_names, explanation.shap_values))
    pos = [(n, v) for n, v in pairs if v > 0]
    neg = [(n, v) for n, v in pairs if v < 0]
    top_pos = sorted(pos, key=lambda x: x[1], reverse=True)
    top_neg = sorted(neg, key=lambda x: x[1])

    band_msgs = {
        "Poor": "Your financial profile currently shows high credit risk.",
        "Fair": "Your financial profile is below average but improvable.",
        "Good": "Your financial profile is solid with room to grow.",
        "Excellent": "Your financial profile is strong — well done.",
    }
    opening = band_msgs.get(band, "Your financial profile has been assessed.")

    # Strengths
    strength_msg = ""
    if top_pos:
        top_feat = top_pos[0][0]
        strength_msg = f" Your strongest factor is **{top_feat}**."

    # Weakness
    weakness_msg = ""
    if top_neg:
        top_weak = top_neg[0][0]
        weakness_msg = (
            f" The biggest drag on your score is "
            f"**{top_weak}** — addressing this "
            f"should be your first priority."
        )

    return opening + strength_msg + weakness_msg
