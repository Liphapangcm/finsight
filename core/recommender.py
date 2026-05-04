# core/recommender.py
"""
Recommendation engine.
Combines SHAP-identified weak spots with rule-based financial logic
to produce prioritised, plain-language recommendations.
"""

from core.schemas import AssessmentInput, Recommendation, SHAPExplanation


def generate_recommendations(
    inp: AssessmentInput,
    explanation: SHAPExplanation,
    credit_score: int,
    kpis: dict,
) -> list[Recommendation]:
    """
    Returns up to 5 prioritised recommendations.
    Priority 1 = most impactful to fix first.
    """
    candidates: list[Recommendation] = []

    income = inp.monthly_income + 1e-9
    total_exp = (
        inp.housing_expense
        + inp.food_expense
        + inp.transport_expense
        + inp.utilities_expense
        + inp.other_expense
    )
    dti = inp.total_debt / income
    sav_rate = inp.monthly_savings / income
    net_flow = income - total_exp - inp.monthly_savings

    # ── Rule 1: Previous default ──────────────────────────────────
    if inp.has_defaulted:
        candidates.append(
            Recommendation(
                priority=1,
                category="behaviour",
                title="Resolve Your Previous Loan Default",
                description=(
                    "You have a recorded loan default. This is the single biggest "
                    "factor reducing your score. Contact the lender to negotiate a "
                    "repayment plan or settlement. Even partial resolution signals "
                    "commitment and can improve your score significantly."
                ),
                impact_estimate="+80 to +120 points upon resolution",
            )
        )

    # ── Rule 2: Payment regularity ────────────────────────────────
    if inp.payment_regularity == "rarely":
        candidates.append(
            Recommendation(
                priority=1,
                category="behaviour",
                title="Pay All Bills and Loans On Time",
                description=(
                    "Payment history is one of the most powerful factors in your "
                    "score. Set up reminders or automatic payments for all loans, "
                    "rent, and utilities. Consistent on-time payment for 3 months "
                    "will noticeably improve your score."
                ),
                impact_estimate="+40 to +70 points over 3 months",
            )
        )
    elif inp.payment_regularity == "sometimes":
        candidates.append(
            Recommendation(
                priority=2,
                category="behaviour",
                title="Improve Payment Consistency",
                description=(
                    "You pay on time sometimes but not always. Try to pay at least "
                    "the minimum on all obligations before the due date each month. "
                    "Use mobile money reminders to stay on track."
                ),
                impact_estimate="+20 to +40 points over 3 months",
            )
        )

    # ── Rule 3: High debt-to-income ratio ─────────────────────────
    if dti > 0.50:
        target_debt = income * 0.35
        reduction_needed = inp.total_debt - target_debt
        candidates.append(
            Recommendation(
                priority=1,
                category="debt",
                title="Reduce Your Total Debt Load",
                description=(
                    f"Your debt (M{inp.total_debt:,.0f}) is {dti * 100:.0f}% of your "
                    f"monthly income. The healthy maximum is 43%. Aim to reduce "
                    f"total debt by at least M{reduction_needed:,.0f}. Focus on "
                    f"clearing the smallest loan first (debt snowball method) to "
                    f"free up cash flow quickly."
                ),
                impact_estimate="+30 to +50 points when below 43%",
            )
        )
    elif dti > 0.35:
        candidates.append(
            Recommendation(
                priority=2,
                category="debt",
                title="Work Toward Reducing Your Debt",
                description=(
                    f"Your debt-to-income ratio is {dti * 100:.0f}%. While not "
                    f"critical, reducing it below 35% will strengthen your profile. "
                    f"Avoid taking on new loans until existing ones are cleared."
                ),
                impact_estimate="+15 to +30 points when below 35%",
            )
        )

    # ── Rule 4: Living in deficit ─────────────────────────────────
    if net_flow < 0:
        candidates.append(
            Recommendation(
                priority=1,
                category="expenses",
                title="You Are Spending More Than You Earn",
                description=(
                    f"Your expenses exceed your income by M{abs(net_flow):,.0f} "
                    f"per month. This is unsustainable and is a major risk signal. "
                    f"Review your 'other expenses' category first — this is usually "
                    f"where the easiest cuts are. Reducing expenses by even 10% "
                    f"would significantly improve your financial health score."
                ),
                impact_estimate="+40 to +60 points when cash flow is positive",
            )
        )

    # ── Rule 5: No savings ────────────────────────────────────────
    if not inp.has_savings or sav_rate < 0.03:
        candidates.append(
            Recommendation(
                priority=3,
                category="savings",
                title="Start a Regular Savings Habit",
                description=(
                    "Not having savings is a risk flag for lenders — it suggests "
                    "no financial buffer for emergencies. Start saving even M200 "
                    "per month. Use a separate mobile money wallet or M-Pesa savings "
                    "account. Aim for 10% of income (M"
                    f"{income * 0.10:,.0f}/month) over time."
                ),
                impact_estimate="+15 to +25 points when saving ≥10% of income",
            )
        )
    elif sav_rate < 0.08:
        candidates.append(
            Recommendation(
                priority=3,
                category="savings",
                title="Increase Your Monthly Savings Rate",
                description=(
                    f"You save {sav_rate * 100:.1f}% of your income. Lenders prefer "
                    f"to see at least 10%. Try increasing savings by M"
                    f"{(income * 0.10 - inp.monthly_savings):,.0f}/month. "
                    f"Even small increases compound over time."
                ),
                impact_estimate="+10 to +20 points when above 10%",
            )
        )

    # ── Rule 6: Too many active loans ─────────────────────────────
    if inp.num_active_loans >= 3:
        candidates.append(
            Recommendation(
                priority=2,
                category="debt",
                title="Reduce Number of Active Loans",
                description=(
                    f"You currently have {inp.num_active_loans} active loans. "
                    f"Having 3 or more open loans signals financial overextension "
                    f"to lenders. Focus on fully closing at least one loan before "
                    f"considering any new credit."
                ),
                impact_estimate="+20 to +35 points when below 3 active loans",
            )
        )

    # ── Rule 7: Mobile money engagement ──────────────────────────
    if inp.mobile_money_frequency == "never":
        candidates.append(
            Recommendation(
                priority=4,
                category="behaviour",
                title="Use Mobile Money Regularly",
                description=(
                    "Regular mobile money usage creates a digital financial "
                    "footprint that alternative lenders use to assess "
                    "creditworthiness. Using M-Pesa or EcoCash weekly, even for "
                    "small transactions, builds your financial identity."
                ),
                impact_estimate="+5 to +15 points over 2 months",
            )
        )

    # ── Rule 8: High housing burden ──────────────────────────────
    if inp.housing_expense / income > 0.40:
        candidates.append(
            Recommendation(
                priority=3,
                category="expenses",
                title="Your Housing Costs Are High",
                description=(
                    f"You spend {inp.housing_expense / income * 100:.0f}% of your "
                    f"income on housing. The recommended maximum is 30%. Consider "
                    f"sharing accommodation costs, negotiating rent, or relocating "
                    f"to a lower-cost area to free up financial breathing room."
                ),
                impact_estimate="+10 to +20 points if reduced below 30%",
            )
        )

    # ── Sort by priority, return top 5 ───────────────────────────
    candidates.sort(key=lambda r: r.priority)

    # Re-number priorities sequentially for clean display
    for i, rec in enumerate(candidates[:5], start=1):
        rec.priority = i

    return candidates[:5]
