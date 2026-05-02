"""
Loan Eligibility Simulator.
Pure financial calculation logic — no ML model needed.
Takes a credit score + financial profile and simulates loan outcomes.
"""

from dataclasses import dataclass
from typing import List, Optional
import math


# ── Loan product definitions (Lesotho context) ────────────────────────────────

LOAN_PRODUCTS = [
    {
        "name":        "Micro Emergency Loan",
        "provider":    "Mobile Money / MFI",
        "min_score":   300,
        "max_amount":  5_000,
        "min_term":    1,
        "max_term":    6,
        "base_rate":   0.28,   # 28% annual
        "description": "Short-term emergency finance. "
                        "Available to most applicants.",
    },
    {
        "name":        "Personal Loan",
        "provider":    "Commercial Bank / MFI",
        "min_score":   450,
        "max_amount":  50_000,
        "min_term":    6,
        "max_term":    36,
        "base_rate":   0.22,
        "description": "General purpose personal finance.",
    },
    {
        "name":        "Small Business Loan",
        "provider":    "Development Bank / LNDC",
        "min_score":   550,
        "max_amount":  150_000,
        "min_term":    12,
        "max_term":    60,
        "base_rate":   0.18,
        "description": "For registered small businesses "
                        "with trading history.",
    },
    {
        "name":        "Home Improvement Loan",
        "provider":    "Commercial Bank",
        "min_score":   600,
        "max_amount":  200_000,
        "min_term":    24,
        "max_term":    84,
        "base_rate":   0.155,
        "description": "Secured lending for property improvement.",
    },
    {
        "name":        "Premium Personal Loan",
        "provider":    "Top-tier Commercial Bank",
        "min_score":   700,
        "max_amount":  500_000,
        "min_term":    12,
        "max_term":    84,
        "base_rate":   0.12,
        "description": "Best rates for excellent credit profiles.",
    },
]


# ── Output schemas ────────────────────────────────────────────────────────────

@dataclass
class MonthlyBreakdown:
    month:            int
    payment:          float
    principal:        float
    interest:         float
    balance:          float


@dataclass
class LoanProduct:
    name:             str
    provider:         str
    eligible:         bool
    reason:           str         # why eligible or not
    interest_rate:    float       # annual %
    monthly_payment:  float
    total_repayable:  float
    total_interest:   float


@dataclass
class AffordabilityResult:
    max_affordable_monthly:  float   # max monthly payment user can afford
    max_affordable_loan:     float   # max loan amount given term
    debt_service_ratio:      float   # current DSR after new loan
    is_affordable:           bool
    affordability_message:   str


@dataclass
class SimulationResult:
    # Input echo
    loan_amount:          float
    loan_term_months:     int
    requested_rate:       float

    # Affordability
    affordability:        AffordabilityResult

    # Approval
    approval_probability: float      # 0.0 – 1.0
    approval_label:       str        # "Likely" / "Possible" / "Unlikely"
    approval_color:       str        # hex color

    # Payment details
    monthly_payment:      float
    total_repayable:      float
    total_interest:       float
    effective_rate:       float      # adjusted for credit score

    # Products
    eligible_products:    List[LoanProduct]

    # Amortisation schedule (first 12 months shown)
    schedule:             List[MonthlyBreakdown]

    # Advice
    tips:                 List[str]


# ── Core calculation functions ────────────────────────────────────────────────

def _monthly_payment(principal: float,
                     annual_rate: float,
                     term_months: int) -> float:
    """Standard amortising loan monthly payment formula."""
    if annual_rate == 0:
        return principal / term_months
    r = annual_rate / 12
    return principal * (r * (1 + r)**term_months) / ((1 + r)**term_months - 1)


def _effective_rate(base_rate: float, credit_score: int) -> float:
    """
    Adjusts base interest rate based on credit score.
    Better score = lower rate (risk-based pricing).
    """
    if credit_score >= 750:   adjustment = -0.04
    elif credit_score >= 700: adjustment = -0.02
    elif credit_score >= 650: adjustment = -0.01
    elif credit_score >= 580: adjustment =  0.00
    elif credit_score >= 500: adjustment =  0.03
    elif credit_score >= 450: adjustment =  0.06
    else:                     adjustment =  0.10
    return round(max(0.08, base_rate + adjustment), 4)


def _approval_probability(credit_score: int,
                           dti: float,
                           is_affordable: bool,
                           has_defaulted: bool) -> float:
    """
    Calculates loan approval probability (0–1).
    Based on industry-standard underwriting criteria.
    """
    score = 0.0

    # Credit score component (50% weight)
    if credit_score >= 700:   score += 0.50
    elif credit_score >= 650: score += 0.42
    elif credit_score >= 580: score += 0.32
    elif credit_score >= 500: score += 0.20
    elif credit_score >= 450: score += 0.12
    else:                     score += 0.04

    # DTI component (30% weight)
    if dti < 0.30:   score += 0.30
    elif dti < 0.43: score += 0.22
    elif dti < 0.55: score += 0.12
    else:            score += 0.03

    # Affordability (15% weight)
    if is_affordable: score += 0.15

    # Default history (5% weight — severe penalty)
    if not has_defaulted: score += 0.05
    else:                 score -= 0.20

    return round(max(0.0, min(1.0, score)), 2)


def _build_schedule(principal: float,
                    annual_rate: float,
                    term_months: int,
                    monthly_pmt: float) -> List[MonthlyBreakdown]:
    """Generates amortisation schedule."""
    schedule = []
    balance  = principal
    r        = annual_rate / 12

    for month in range(1, min(term_months + 1, 13)):  # show max 12 months
        interest   = balance * r
        principal_ = monthly_pmt - interest
        balance    = max(0, balance - principal_)
        schedule.append(MonthlyBreakdown(
            month     = month,
            payment   = round(monthly_pmt, 2),
            principal = round(principal_, 2),
            interest  = round(interest, 2),
            balance   = round(balance, 2),
        ))
    return schedule


def _check_product_eligibility(
    product: dict,
    credit_score: int,
    loan_amount: float,
    loan_term: int,
) -> LoanProduct:
    """Checks if user qualifies for a specific loan product."""
    eligible = True
    reason   = "✅ You meet the requirements for this product."

    if credit_score < product['min_score']:
        eligible = False
        gap      = product['min_score'] - credit_score
        reason   = (f"❌ Requires a minimum score of {product['min_score']}. "
                    f"You need +{gap} points.")
    elif loan_amount > product['max_amount']:
        eligible = False
        reason   = (f"❌ Maximum loan for this product is "
                    f"M{product['max_amount']:,.0f}.")
    elif loan_term < product['min_term']:
        eligible = False
        reason   = (f"❌ Minimum term is {product['min_term']} months.")
    elif loan_term > product['max_term']:
        eligible = False
        reason   = (f"❌ Maximum term is {product['max_term']} months.")

    rate    = _effective_rate(product['base_rate'], credit_score)
    pmt     = _monthly_payment(loan_amount, rate, loan_term)
    total   = pmt * loan_term
    interest= total - loan_amount

    return LoanProduct(
        name            = product['name'],
        provider        = product['provider'],
        eligible        = eligible,
        reason          = reason,
        interest_rate   = round(rate * 100, 2),
        monthly_payment = round(pmt, 2),
        total_repayable = round(total, 2),
        total_interest  = round(interest, 2),
    )


def _generate_tips(result: 'SimulationResult',
                   credit_score: int,
                   has_defaulted: bool) -> List[str]:
    tips = []

    if result.approval_probability < 0.5:
        tips.append(
            f"💡 Improving your score by 50 points could raise your "
            f"approval chance to "
            f"{min(result.approval_probability + 0.20, 1.0)*100:.0f}%."
        )
    if result.affordability.debt_service_ratio > 0.43:
        tips.append(
            "⚠️ This loan would push your debt-service ratio above 43% — "
            "the maximum most lenders accept. Consider a smaller amount "
            "or longer term."
        )
    if has_defaulted:
        tips.append(
            "🔴 Your previous default is significantly reducing approval "
            "chances. Resolving it is the single highest-impact action "
            "you can take."
        )
    if result.loan_term_months < 12 and result.loan_amount > 20_000:
        tips.append(
            "📅 Extending your loan term would reduce monthly payments "
            "and improve affordability scores with lenders."
        )
    if result.approval_probability >= 0.75:
        tips.append(
            "✅ Your profile looks strong for this loan. Compare at least "
            "3 lenders before signing — rates vary significantly in Lesotho."
        )
    if not tips:
        tips.append(
            "📊 Your financial profile is being evaluated against "
            "standard Lesotho lending criteria."
        )
    return tips


# ── Main simulation function ──────────────────────────────────────────────────

def simulate_loan(
    loan_amount:   float,
    loan_term:     int,            # months
    credit_score:  int,
    monthly_income:float,
    total_expenses:float,
    monthly_savings:float,
    total_debt:    float,
    has_defaulted: bool,
) -> SimulationResult:
    """
    Main entry point for loan simulation.
    Called by the Streamlit UI.
    """
    income   = monthly_income + 1e-9
    net_flow = monthly_income - total_expenses - monthly_savings

    # ── Affordability ─────────────────────────────────────────────
    # Max 40% of disposable income goes to new debt service
    max_monthly     = max(0, net_flow * 0.40)
    base_rate_guess = 0.20   # use 20% as affordability estimate
    if max_monthly > 0:
        # Max affordable loan given term
        r = base_rate_guess / 12
        if r > 0:
            max_loan = max_monthly * ((1+r)**loan_term - 1) / (r*(1+r)**loan_term)
        else:
            max_loan = max_monthly * loan_term
    else:
        max_loan = 0

    # Compute rate for requested loan
    eff_rate   = _effective_rate(0.20, credit_score)
    monthly_pmt= _monthly_payment(loan_amount, eff_rate, loan_term)

    # New DTI after adding this loan
    existing_dsr  = (total_debt * 0.03)
    new_dsr       = (existing_dsr + monthly_pmt) / income
    is_affordable = (monthly_pmt <= max_monthly) and (new_dsr < 0.50)

    afford_msg = (
        f"M{monthly_pmt:,.0f}/month fits within your budget."
        if is_affordable else
        f"M{monthly_pmt:,.0f}/month exceeds your safe repayment capacity "
        f"of M{max_monthly:,.0f}/month."
    )

    affordability = AffordabilityResult(
        max_affordable_monthly = round(max_monthly, 2),
        max_affordable_loan    = round(max_loan, 2),
        debt_service_ratio     = round(new_dsr, 4),
        is_affordable          = is_affordable,
        affordability_message  = afford_msg,
    )

    # ── Approval probability ──────────────────────────────────────
    dti      = total_debt / income
    prob     = _approval_probability(
        credit_score, dti, is_affordable, has_defaulted
    )

    if prob >= 0.70:
        label = "Likely Approved"
        color = "#43A047"
    elif prob >= 0.45:
        label = "Possible — Not Guaranteed"
        color = "#FB8C00"
    else:
        label = "Unlikely to be Approved"
        color = "#E53935"

    # ── Payment details ───────────────────────────────────────────
    total_repay = monthly_pmt * loan_term
    total_int   = total_repay - loan_amount

    # ── Product eligibility ───────────────────────────────────────
    products = [
        _check_product_eligibility(p, credit_score, loan_amount, loan_term)
        for p in LOAN_PRODUCTS
    ]

    # ── Amortisation schedule ─────────────────────────────────────
    schedule = _build_schedule(loan_amount, eff_rate, loan_term, monthly_pmt)

    # ── Assemble result ───────────────────────────────────────────
    result = SimulationResult(
        loan_amount          = loan_amount,
        loan_term_months     = loan_term,
        requested_rate       = round(eff_rate * 100, 2),
        affordability        = affordability,
        approval_probability = prob,
        approval_label       = label,
        approval_color       = color,
        monthly_payment      = round(monthly_pmt, 2),
        total_repayable      = round(total_repay, 2),
        total_interest       = round(total_int, 2),
        effective_rate       = round(eff_rate * 100, 2),
        eligible_products    = products,
        schedule             = schedule,
        tips                 = [],
    )
    result.tips = _generate_tips(result, credit_score, has_defaulted)
    return result