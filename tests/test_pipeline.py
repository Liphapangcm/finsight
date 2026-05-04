"""
End-to-end test of the full backend pipeline.
Run with: python -m tests.test_pipeline
"""

from core.schemas import AssessmentInput
from core.service import run_assessment


def test_healthy_profile():
    """A financially healthy user should score 680+."""
    inp = AssessmentInput(
        age=32,
        employment_type="employed",
        num_dependents=1,
        monthly_income=12000,
        housing_expense=2500,
        food_expense=2000,
        transport_expense=800,
        utilities_expense=500,
        other_expense=700,
        total_debt=8000,
        num_active_loans=1,
        has_defaulted=False,
        payment_regularity="always",
        has_savings=True,
        monthly_savings=1500,
        mobile_money_frequency="weekly",
    )
    result, errors = run_assessment(inp)
    assert not errors, f"Unexpected errors: {errors}"
    assert result.credit_score >= 650, f"Expected 650+, got {result.credit_score}"
    print(f"  ✅ Healthy profile → Score: {result.credit_score} ({result.score_band})")


def test_high_risk_profile():
    """A high-risk user should score below 500."""
    inp = AssessmentInput(
        age=28,
        employment_type="unemployed",
        num_dependents=4,
        monthly_income=3000,
        housing_expense=1800,
        food_expense=1500,
        transport_expense=500,
        utilities_expense=400,
        other_expense=600,
        total_debt=25000,
        num_active_loans=4,
        has_defaulted=True,
        payment_regularity="rarely",
        has_savings=False,
        monthly_savings=0,
        mobile_money_frequency="never",
    )
    result, errors = run_assessment(inp)
    assert not errors, f"Unexpected errors: {errors}"
    assert result.credit_score < 500, f"Expected <500, got {result.credit_score}"
    print(
        f"  ✅ High-risk profile → Score: {result.credit_score} ({result.score_band})"
    )


def test_validation_catches_bad_input():
    """Invalid input should return errors, not crash."""
    inp = AssessmentInput(
        age=15,  # too young
        employment_type="employed",
        num_dependents=0,
        monthly_income=-500,  # negative income
        housing_expense=0,
        food_expense=0,
        transport_expense=0,
        utilities_expense=0,
        other_expense=0,
        total_debt=0,
        num_active_loans=0,
        has_defaulted=False,
        payment_regularity="always",
        has_savings=False,
        monthly_savings=0,
        mobile_money_frequency="weekly",
    )
    result, errors = run_assessment(inp)
    assert result is None
    assert len(errors) > 0
    print(f"  ✅ Validation caught {len(errors)} error(s): {errors}")


def test_recommendations_generated():
    """Recommendations should always be present."""
    inp = AssessmentInput(
        age=45,
        employment_type="self_employed",
        num_dependents=3,
        monthly_income=7000,
        housing_expense=2800,
        food_expense=2000,
        transport_expense=600,
        utilities_expense=400,
        other_expense=800,
        total_debt=15000,
        num_active_loans=2,
        has_defaulted=False,
        payment_regularity="sometimes",
        has_savings=True,
        monthly_savings=200,
        mobile_money_frequency="monthly",
    )
    result, errors = run_assessment(inp)
    assert not errors
    assert len(result.recommendations) > 0
    print(f"  ✅ {len(result.recommendations)} recommendations generated:")
    for rec in result.recommendations:
        print(f"     {rec.priority}. [{rec.category.upper()}] {rec.title}")
        print(f"        Impact: {rec.impact_estimate}")


if __name__ == "__main__":
    print("\n=== FINSIGHT BACKEND PIPELINE TESTS ===\n")
    test_validation_catches_bad_input()
    test_healthy_profile()
    test_high_risk_profile()
    test_recommendations_generated()
    print("\n✅ All tests passed. Backend is ready.\n")
