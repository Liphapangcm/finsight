# tests/test_features.py
"""
Unit tests for core/features.py
Tests feature engineering in isolation — no Streamlit, no model.
"""
import pytest
import pandas as pd
from core.features import engineer_features, compute_kpis, FEATURE_COLUMNS


def _raw(overrides: dict = None) -> dict:
    """Return a valid raw input dict, with optional overrides."""
    base = {
        "monthly_income":        10000,
        "housing_expense":       2000,
        "food_expense":          1500,
        "transport_expense":     500,
        "utilities_expense":     300,
        "other_expense":         400,
        "total_debt":            5000,
        "num_active_loans":      1,
        "has_defaulted":         False,
        "payment_regularity":    "always",
        "has_savings":           True,
        "monthly_savings":       1000,
        "mobile_money_frequency":"weekly",
        "age":                   30,
        "employment_type":       "employed",
        "num_dependents":        1,
    }
    if overrides:
        base.update(overrides)
    return base


class TestEngineerFeatures:

    def test_returns_dataframe(self):
        df = engineer_features(_raw())
        assert isinstance(df, pd.DataFrame)

    def test_correct_columns(self):
        df = engineer_features(_raw())
        assert list(df.columns) == FEATURE_COLUMNS

    def test_single_row(self):
        df = engineer_features(_raw())
        assert len(df) == 1

    def test_no_null_values(self):
        df = engineer_features(_raw())
        assert not df.isnull().any().any(), \
            "Feature DataFrame contains null values"

    def test_debt_to_income_ratio_zero_debt(self):
        """Zero debt must produce DTI of exactly 0, never negative."""
        df = engineer_features(_raw({"total_debt": 0}))
        dti = df["debt_to_income_ratio"].iloc[0]
        assert dti >= 0, f"DTI should be >= 0, got {dti}"
        assert dti == 0.0, f"Zero debt should give DTI=0, got {dti}"

    def test_debt_service_ratio_zero_debt(self):
        """Zero debt must produce debt service ratio of 0."""
        df = engineer_features(_raw({"total_debt": 0}))
        dsr = df["debt_service_ratio"].iloc[0]
        assert dsr >= 0, f"DSR should be >= 0, got {dsr}"

    def test_deficit_flag_set_when_overspending(self):
        """Deficit flag must be 1 when expenses > income."""
        raw = _raw({
            "monthly_income":    3000,
            "housing_expense":   2000,
            "food_expense":      1500,   # total > income
            "monthly_savings":   0,
        })
        df = engineer_features(raw)
        assert df["deficit_flag"].iloc[0] == 1

    def test_no_deficit_when_under_budget(self):
        """Deficit flag must be 0 when income > expenses."""
        df = engineer_features(_raw())
        assert df["deficit_flag"].iloc[0] == 0

    def test_high_debt_flag(self):
        """High debt flag fires when DTI > 43%."""
        # DTI = 5000/10000 = 50% → flag should be 1
        df = engineer_features(_raw({"total_debt": 5000,
                                     "monthly_income": 10000}))
        assert df["high_debt_flag"].iloc[0] == 1

    def test_no_high_debt_flag_zero_debt(self):
        """High debt flag must be 0 when there is no debt."""
        df = engineer_features(_raw({"total_debt": 0}))
        assert df["high_debt_flag"].iloc[0] == 0

    def test_payment_score_always(self):
        df = engineer_features(_raw({"payment_regularity": "always"}))
        assert df["payment_score"].iloc[0] == 1.0

    def test_payment_score_rarely(self):
        df = engineer_features(_raw({"payment_regularity": "rarely"}))
        assert df["payment_score"].iloc[0] == 0.0

    def test_employment_encoded_employed(self):
        df = engineer_features(_raw({"employment_type": "employed"}))
        assert df["employment_encoded"].iloc[0] == 3

    def test_employment_encoded_unemployed(self):
        df = engineer_features(_raw({"employment_type": "unemployed"}))
        assert df["employment_encoded"].iloc[0] == 0

    def test_savings_consistency_no_savings(self):
        df = engineer_features(_raw({
            "has_savings": False, "monthly_savings": 0
        }))
        assert df["savings_consistency"].iloc[0] == 0.0


class TestComputeKpis:

    def test_returns_dict(self):
        kpis = compute_kpis(_raw())
        assert isinstance(kpis, dict)

    def test_required_keys_present(self):
        kpis = compute_kpis(_raw())
        required = [
            "monthly_income", "total_expenses", "net_cash_flow",
            "debt_to_income", "savings_rate", "expense_ratio",
            "is_in_deficit", "affordability_index",
        ]
        for key in required:
            assert key in kpis, f"Missing key: {key}"

    def test_dti_never_negative(self):
        """DTI must be >= 0 even with floating point edge cases."""
        kpis = compute_kpis(_raw({"total_debt": 0}))
        assert kpis["debt_to_income"] >= 0

    def test_is_in_deficit_true(self):
        raw = _raw({
            "monthly_income":   2000,
            "housing_expense":  1500,
            "food_expense":     1000,
            "monthly_savings":  0,
        })
        kpis = compute_kpis(raw)
        assert kpis["is_in_deficit"] is True

    def test_is_in_deficit_false(self):
        kpis = compute_kpis(_raw())
        assert kpis["is_in_deficit"] is False

    def test_savings_rate_zero_when_no_savings(self):
        kpis = compute_kpis(_raw({"monthly_savings": 0}))
        assert kpis["savings_rate"] == 0.0