from core.loan_simulator import (
    _effective_rate,
    _approval_probability,
    simulate_loan,
)


def test_effective_rate_bounds():
    # Very high score should reduce rate but not below floor 0.08
    r_high = _effective_rate(0.20, 800)
    assert 0.08 <= r_high <= 0.20


def test_approval_probability_range():
    p = _approval_probability(700, 0.2, True, False)
    assert 0.0 <= p <= 1.0


def test_simulate_loan_basic():
    res = simulate_loan(
        loan_amount=10000,
        loan_term=12,
        credit_score=700,
        monthly_income=8000,
        total_expenses=3000,
        monthly_savings=500,
        total_debt=2000,
        has_defaulted=False,
    )

    assert res.monthly_payment > 0
    assert 0.0 <= res.approval_probability <= 1.0
    assert isinstance(res.affordability.max_affordable_monthly, float)
