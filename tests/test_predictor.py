# tests/test_predictor.py
"""
Unit tests for core/predictor.py
Tests model inference in isolation.
Requires trained model artifacts in /models.
"""
import pytest
from pathlib import Path
from core.predictor import predict, get_score_band
from core.schemas   import AssessmentInput


# Skip all tests if model hasn't been trained yet
pytestmark = pytest.mark.skipif(
    not Path("models/model.pkl").exists(),
    reason="Model artifacts not found — run `python -m ml.train` first"
)


def _inp(**overrides) -> AssessmentInput:
    defaults = dict(
        age=35, employment_type="employed", num_dependents=2,
        monthly_income=15000,
        housing_expense=3000, food_expense=2500,
        transport_expense=800, utilities_expense=500,
        other_expense=600,
        total_debt=10000, num_active_loans=1,
        has_defaulted=False, payment_regularity="always",
        has_savings=True, monthly_savings=2000,
        mobile_money_frequency="weekly",
    )
    defaults.update(overrides)
    return AssessmentInput(**defaults)


class TestGetScoreBand:

    def test_poor_band(self):
        band, risk, color = get_score_band(350)
        assert band == "Poor"
        assert risk == "High"

    def test_fair_band(self):
        band, risk, color = get_score_band(520)
        assert band == "Fair"

    def test_good_band(self):
        band, risk, color = get_score_band(640)
        assert band == "Good"

    def test_excellent_band(self):
        band, risk, color = get_score_band(750)
        assert band == "Excellent"
        assert risk == "Very Low"

    def test_boundary_300(self):
        band, _, _ = get_score_band(300)
        assert band == "Poor"

    def test_boundary_850(self):
        band, _, _ = get_score_band(850)
        assert band == "Excellent"

    def test_color_is_hex(self):
        _, _, color = get_score_band(700)
        assert color.startswith("#")
        assert len(color) == 7


class TestPredict:

    def test_returns_dict(self):
        result = predict(_inp())
        assert isinstance(result, dict)

    def test_required_keys(self):
        result = predict(_inp())
        for key in ["credit_score", "score_band",
                    "risk_level", "score_color",
                    "kpis", "feature_df", "scaled_arr"]:
            assert key in result, f"Missing key: {key}"

    def test_score_in_range(self):
        result = predict(_inp())
        assert 300 <= result["credit_score"] <= 850

    def test_score_band_valid(self):
        result = predict(_inp())
        assert result["score_band"] in ["Poor", "Fair",
                                        "Good", "Excellent"]

    def test_zero_debt_no_crash(self):
        """Zero debt must not crash or produce out-of-range score."""
        result = predict(_inp(total_debt=0, num_active_loans=0))
        assert 300 <= result["credit_score"] <= 850

    def test_kpis_dti_non_negative(self):
        """DTI in KPIs must never be negative."""
        result = predict(_inp(total_debt=0))
        assert result["kpis"]["debt_to_income"] >= 0

    def test_feature_df_shape(self):
        from core.features import FEATURE_COLUMNS
        result = predict(_inp())
        assert result["feature_df"].shape == (1, len(FEATURE_COLUMNS))