"""
Generates synthetic but statistically realistic financial profiles
for Lesotho-context credit scoring model training.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass

np.random.seed(42)


def simulate_dataset(n_samples: int = 5000) -> pd.DataFrame:
    records = []

    for _ in range(n_samples):
        profile = _generate_profile()
        record  = _compute_features(profile)
        record['credit_score'] = _assign_score(record)
        records.append(record)

    df = pd.DataFrame(records)
    return df


def _generate_profile() -> dict:
    """
    Simulate raw form inputs with realistic Lesotho distributions.
    Income distribution based on Lesotho Bureau of Statistics data.
    """
    employment = np.random.choice(
        ['employed', 'self_employed', 'unemployed', 'student'],
        p=[0.45, 0.30, 0.15, 0.10]
    )

    # Income by employment type (LSL per month)
    income_map = {
        'employed':     np.random.lognormal(mean=8.5, sigma=0.5),
        'self_employed':np.random.lognormal(mean=8.1, sigma=0.7),
        'unemployed':   np.random.lognormal(mean=6.5, sigma=0.6),
        'student':      np.random.lognormal(mean=6.8, sigma=0.4),
    }
    income = np.clip(income_map[employment], 800, 80000)

    # Expenses: correlated with income but with noise
    expense_fraction = np.random.beta(a=5, b=2)       # Skews toward 0.7–0.9
    total_expenses   = income * expense_fraction

    # Expense breakdown (proportions that sum to 1)
    proportions = np.random.dirichlet([3, 2.5, 1.5, 1, 1])
    housing     = total_expenses * proportions[0]
    food        = total_expenses * proportions[1]
    transport   = total_expenses * proportions[2]
    utilities   = total_expenses * proportions[3]
    other       = total_expenses * proportions[4]

    # Debt (correlated with employment + income)
    max_debt        = income * np.random.uniform(0, 4)
    total_debt      = np.random.exponential(scale=max_debt * 0.4)
    total_debt      = np.clip(total_debt, 0, max_debt)
    num_loans       = np.random.poisson(lam=1.2)

    # Default history (more likely for unemployed, high debt)
    default_prob    = 0.10
    if employment == 'unemployed': default_prob += 0.25
    if total_debt / (income + 1) > 1.5: default_prob += 0.20
    has_defaulted   = int(np.random.random() < default_prob)

    # Payment regularity
    if has_defaulted:
        pay_reg = np.random.choice(
            ['always','sometimes','rarely'], p=[0.1, 0.4, 0.5])
    else:
        pay_reg = np.random.choice(
            ['always','sometimes','rarely'], p=[0.6, 0.3, 0.1])

    # Savings
    has_savings     = int(np.random.random() < 0.45)
    savings         = (income * np.random.uniform(0.02, 0.25)
                       if has_savings else 0.0)

    # Mobile money
    mm_freq = np.random.choice(
        ['daily','weekly','monthly','never'], p=[0.25, 0.40, 0.25, 0.10])

    return {
        'monthly_income':        round(income, 2),
        'housing_expense':       round(housing, 2),
        'food_expense':          round(food, 2),
        'transport_expense':     round(transport, 2),
        'utilities_expense':     round(utilities, 2),
        'other_expense':         round(other, 2),
        'total_debt':            round(total_debt, 2),
        'num_active_loans':      min(num_loans, 8),
        'has_defaulted':         has_defaulted,
        'payment_regularity':    pay_reg,
        'has_savings':           has_savings,
        'monthly_savings':       round(savings, 2),
        'mobile_money_frequency':mm_freq,
        'age':                   int(np.random.randint(18, 65)),
        'employment_type':       employment,
        'num_dependents':        int(np.random.poisson(lam=2.1)),
    }


def _compute_features(p: dict) -> dict:
    """Derive engineered features from raw profile."""
    income       = p['monthly_income'] + 1e-9   # avoid div by zero
    total_exp    = (p['housing_expense'] + p['food_expense'] +
                    p['transport_expense'] + p['utilities_expense'] +
                    p['other_expense'])
    essential    = (p['housing_expense'] + p['food_expense'] +
                    p['utilities_expense'])

    dti          = p['total_debt'] / income
    exp_ratio    = total_exp / income
    sav_rate     = p['monthly_savings'] / income
    housing_burd = p['housing_expense'] / income
    disc_ratio   = (income - essential) / income
    net_flow     = income - total_exp - p['monthly_savings']
    afford_idx   = net_flow / income
    dsr          = (p['total_debt'] * 0.03) / income
    sav_consist  = int(p['has_savings']) * sav_rate

    pay_map      = {'always': 1.0, 'sometimes': 0.5, 'rarely': 0.0}
    mm_map       = {'daily': 1.0, 'weekly': 0.75, 'monthly': 0.4, 'never': 0.0}
    emp_map      = {'employed': 3, 'self_employed': 2,
                    'student': 1, 'unemployed': 0}

    dep_burden   = p['num_dependents'] / (income / 1000 + 1e-9)

    features = {**p}   # include raw inputs too (for saving to DB)
    features.update({
        'total_expenses':        round(total_exp, 2),
        'debt_to_income_ratio':  round(dti, 4),
        'expense_ratio':         round(exp_ratio, 4),
        'savings_rate':          round(sav_rate, 4),
        'housing_burden':        round(housing_burd, 4),
        'discretionary_ratio':   round(disc_ratio, 4),
        'net_monthly_cash_flow': round(net_flow, 2),
        'affordability_index':   round(afford_idx, 4),
        'debt_service_ratio':    round(dsr, 4),
        'savings_consistency':   round(sav_consist, 4),
        'payment_score':         pay_map[p['payment_regularity']],
        'mobile_money_score':    mm_map[p['mobile_money_frequency']],
        'employment_encoded':    emp_map[p['employment_type']],
        'dependency_burden':     round(dep_burden, 4),
        'high_debt_flag':        int(dti > 0.43),
        'deficit_flag':          int(net_flow < 0),
        'overextended_flag':     int(p['num_active_loans'] >= 3),
        'housing_stress_flag':   int(housing_burd > 0.30),
    })
    return features


def _assign_score(f: dict) -> int:
    """
    Rule-based score assignment for training labels.
    Encodes domain knowledge about creditworthiness.
    Score range: 300–850 (industry standard).
    """
    score = 600   # baseline

    # --- Payment behaviour (most weighted) ---
    score += f['payment_score'] * 120
    score -= f['has_defaulted'] * 150

    # --- Debt burden ---
    dti = f['debt_to_income_ratio']
    if dti < 0.20:   score += 60
    elif dti < 0.35: score += 30
    elif dti < 0.50: score -= 30
    else:            score -= 80

    # --- Cash flow health ---
    ai = f['affordability_index']
    if ai > 0.20:    score += 50
    elif ai > 0.10:  score += 25
    elif ai > 0:     score += 0
    else:            score -= 70    # deficit living

    # --- Savings discipline ---
    sr = f['savings_rate']
    if sr > 0.15:    score += 50
    elif sr > 0.08:  score += 25
    elif sr > 0:     score += 10

    # --- Employment stability ---
    emp = f['employment_encoded']
    score += (emp - 1) * 20         # employed=+40, unemployed=-20

    # --- Mobile money engagement ---
    score += f['mobile_money_score'] * 30

    # --- Risk flags ---
    score -= f['high_debt_flag']      * 40
    score -= f['deficit_flag']        * 50
    score -= f['overextended_flag']   * 35
    score -= f['housing_stress_flag'] * 20

    # --- Dependency burden ---
    score -= min(f['dependency_burden'] * 5, 40)

    # Add realistic noise
    score += np.random.normal(0, 15)

    return int(np.clip(score, 300, 850))


if __name__ == "__main__":
    df = simulate_dataset(5000)
    df.to_csv("ml/data/raw/synthetic_profiles.csv", index=False)
    print(f"Generated {len(df)} profiles")
    print(df[['monthly_income','credit_score','employment_type']].describe())