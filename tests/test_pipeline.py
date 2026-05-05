# tests/test_pipeline.py
"""
End-to-end pipeline tests.
Tests only core/ business logic — no Streamlit imports.
All 4 tests must pass on Python 3.11 and 3.12.
"""
from core.schemas import AssessmentInput
from core.service import run_assessment


def _make_input(**overrides) -> AssessmentInput:
    """Base valid input — override any field for specific tests."""
    defaults = dict(
        age=32, employment_type="employed", num_dependents=1,
        monthly_income=12000,
        housing_expense=2500, food_expense=2000,
        transport_expense=800, utilities_expense=500,
        other_expense=700,
        total_debt=8000, num_active_loans=1,
        has_defaulted=False, payment_regularity="always",
        has_savings=True, monthly_savings=1500,
        mobile_money_frequency="weekly",
    )
    defaults.update(overrides)
    return AssessmentInput(**defaults)


def test_healthy_profile():
    """A financially healthy user should score 650+."""
    result, errors = run_assessment(_make_input())
    assert not errors, f"Unexpected errors: {errors}"
    assert result.credit_score >= 650, (
        f"Expected 650+, got {result.credit_score}"
    )
    print(f"  ✅ Healthy → {result.credit_score} ({result.score_band})")


def test_high_risk_profile():
    """A high-risk user should score below 500."""
    result, errors = run_assessment(_make_input(
        age=28, employment_type="unemployed", num_dependents=4,
        monthly_income=3000,
        housing_expense=1800, food_expense=1500,
        transport_expense=500, utilities_expense=400,
        other_expense=600,
        total_debt=25000, num_active_loans=4,
        has_defaulted=True, payment_regularity="rarely",
        has_savings=False, monthly_savings=0,
        mobile_money_frequency="never",
    ))
    assert not errors, f"Unexpected errors: {errors}"
    assert result.credit_score < 500, (
        f"Expected <500, got {result.credit_score}"
    )
    print(f"  ✅ High-risk → {result.credit_score} ({result.score_band})")


def test_validation_catches_bad_input():
    """Invalid input must return errors, not crash."""
    result, errors = run_assessment(_make_input(
        age=15,           # too young
        monthly_income=-500,  # negative
    ))
    assert result is None
    assert len(errors) > 0
    print(f"  ✅ Validation caught {len(errors)} error(s)")


def test_recommendations_generated():
    """Recommendations must always be present."""
    result, errors = run_assessment(_make_input(
        age=45, employment_type="self_employed", num_dependents=3,
        monthly_income=7000,
        housing_expense=2800, food_expense=2000,
        transport_expense=600, utilities_expense=400,
        other_expense=800,
        total_debt=15000, num_active_loans=2,
        has_defaulted=False, payment_regularity="sometimes",
        has_savings=True, monthly_savings=200,
        mobile_money_frequency="monthly",
    ))
    assert not errors
    assert len(result.recommendations) > 0
    print(f"  ✅ {len(result.recommendations)} recommendations")


def test_zero_debt_profile():
    """Zero debt should not produce negative debt-related KPIs."""
    result, errors = run_assessment(_make_input(
        total_debt=0,
        num_active_loans=0,
        has_defaulted=False,
    ))
    assert not errors
    # DTI must never be negative
    assert result.kpis.debt_to_income >= 0, (
        f"DTI should be >= 0, got {result.kpis.debt_to_income}"
    )
    print(f"  ✅ Zero-debt DTI = {result.kpis.debt_to_income}%")


def test_score_within_valid_range():
    """Score must always be between 300 and 850."""
    result, errors = run_assessment(_make_input())
    assert not errors
    assert 300 <= result.credit_score <= 850, (
        f"Score {result.credit_score} out of range 300–850"
    )


def test_score_band_matches_score():
    """Score band must correspond to the numeric score."""
    result, errors = run_assessment(_make_input())
    assert not errors
    score = result.credit_score
    band  = result.score_band
    if score < 450:
        assert band == "Poor",      f"{score} should be Poor, got {band}"
    elif score < 580:
        assert band == "Fair",      f"{score} should be Fair, got {band}"
    elif score < 700:
        assert band == "Good",      f"{score} should be Good, got {band}"
    else:
        assert band == "Excellent", f"{score} should be Excellent, got {band}"
    print(f"  ✅ Score {score} → band {band} ✓")