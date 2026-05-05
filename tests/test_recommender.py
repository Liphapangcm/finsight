# tests/test_recommender.py
"""
Unit tests for core/recommender.py
Tests recommendation generation in isolation.
"""
import pytest
from core.recommender import generate_recommendations
from core.schemas     import AssessmentInput, SHAPExplanation
from core.features    import FEATURE_COLUMNS


def _make_explanation(n_features: int = 5) -> SHAPExplanation:
    """Minimal SHAP explanation for testing."""
    return SHAPExplanation(
        feature_names = FEATURE_COLUMNS[:n_features],
        shap_values   = [-10.0, 5.0, -3.0, 2.0, -1.0][:n_features],
        base_value    = 600.0,
    )


def _inp(**overrides) -> AssessmentInput:
    defaults = dict(
        age=30, employment_type="employed", num_dependents=1,
        monthly_income=10000,
        housing_expense=2500, food_expense=1500,
        transport_expense=500, utilities_expense=400,
        other_expense=500,
        total_debt=5000, num_active_loans=1,
        has_defaulted=False, payment_regularity="always",
        has_savings=True, monthly_savings=500,
        mobile_money_frequency="weekly",
    )
    defaults.update(overrides)
    return AssessmentInput(**defaults)


class TestGenerateRecommendations:

    def test_returns_list(self):
        recs = generate_recommendations(
            _inp(), _make_explanation(), 650, {}
        )
        assert isinstance(recs, list)

    def test_max_five_recommendations(self):
        recs = generate_recommendations(
            _inp(), _make_explanation(), 500, {}
        )
        assert len(recs) <= 5

    def test_at_least_one_recommendation(self):
        """Even a good profile should get at least one tip."""
        recs = generate_recommendations(
            _inp(), _make_explanation(), 720, {}
        )
        assert len(recs) >= 1

    def test_priorities_are_sequential(self):
        """Priorities must be 1, 2, 3... not arbitrary numbers."""
        recs = generate_recommendations(
            _inp(), _make_explanation(), 500, {}
        )
        priorities = [r.priority for r in recs]
        assert priorities == list(range(1, len(recs) + 1)), \
            f"Priorities not sequential: {priorities}"

    def test_defaulted_user_gets_behaviour_rec(self):
        """A user who defaulted must get a behaviour recommendation."""
        recs = generate_recommendations(
            _inp(has_defaulted=True),
            _make_explanation(), 400, {}
        )
        categories = [r.category for r in recs]
        assert "behaviour" in categories, \
            "Expected behaviour recommendation for defaulted user"

    def test_no_savings_gets_savings_rec(self):
        """A user with no savings must get a savings recommendation."""
        recs = generate_recommendations(
            _inp(has_savings=False, monthly_savings=0),
            _make_explanation(), 550, {}
        )
        categories = [r.category for r in recs]
        assert "savings" in categories, \
            "Expected savings recommendation for user with no savings"

    def test_high_debt_gets_debt_rec(self):
        """A user with DTI > 50% must get a debt recommendation."""
        recs = generate_recommendations(
            _inp(total_debt=8000, monthly_income=10000),
            _make_explanation(), 520, {}
        )
        categories = [r.category for r in recs]
        assert "debt" in categories, \
            "Expected debt recommendation for high-DTI user"

    def test_recommendation_has_required_fields(self):
        """Each recommendation must have all required fields."""
        recs = generate_recommendations(
            _inp(), _make_explanation(), 600, {}
        )
        for rec in recs:
            assert rec.title,           "Missing title"
            assert rec.description,     "Missing description"
            assert rec.impact_estimate, "Missing impact_estimate"
            assert rec.category,        "Missing category"
            assert rec.priority > 0,    "Priority must be > 0"