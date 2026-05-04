"""
Feature engineering pipeline.
Same logic used in training AND in live prediction — single source of truth.
"""

from dataclasses import dataclass
from typing import Dict
import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    'debt_to_income_ratio', 'expense_ratio', 'savings_rate',
    'housing_burden', 'discretionary_ratio', 'affordability_index',
    'debt_service_ratio', 'savings_consistency', 'net_monthly_cash_flow',
    'num_active_loans', 'num_dependents', 'age', 'payment_score',
    'mobile_money_score', 'has_defaulted', 'high_debt_flag',
    'deficit_flag', 'overextended_flag', 'housing_stress_flag',
    'employment_encoded', 'dependency_burden',
]

PAYMENT_MAP    = {'always': 1.0, 'sometimes': 0.5, 'rarely': 0.0}
MM_MAP         = {'daily': 1.0, 'weekly': 0.75, 'monthly': 0.4, 'never': 0.0}
EMPLOYMENT_MAP = {'employed': 3, 'self_employed': 2,
                  'student': 1, 'unemployed': 0}


def engineer_features(raw: dict) -> pd.DataFrame:
    """
    Takes raw form input dict, returns a single-row DataFrame
    with all engineered features ready for model inference.
    """
    income    = raw['monthly_income'] + 1e-9
    total_exp = (raw['housing_expense'] + raw['food_expense'] +
                 raw['transport_expense'] + raw['utilities_expense'] +
                 raw['other_expense'])
    essential = (raw['housing_expense'] + raw['food_expense'] +
                 raw['utilities_expense'])

    net_flow  = income - total_exp - raw.get('monthly_savings', 0)
    dti       = raw['total_debt'] / income
    sav_rate  = raw.get('monthly_savings', 0) / income

    features = {
        'debt_to_income_ratio':  dti,
        'expense_ratio':         total_exp / income,
        'savings_rate':          sav_rate,
        'housing_burden':        raw['housing_expense'] / income,
        'discretionary_ratio':   (income - essential) / income,
        'affordability_index':   net_flow / income,
        'debt_service_ratio':    max(0, (raw['total_debt'] * 0.03) / income),
        'savings_consistency':   int(raw.get('has_savings', 0)) * sav_rate,
        'net_monthly_cash_flow': net_flow,
        'num_active_loans':      raw['num_active_loans'],
        'num_dependents':        raw['num_dependents'],
        'age':                   raw['age'],
        'payment_score':         PAYMENT_MAP[raw['payment_regularity']],
        'mobile_money_score':    MM_MAP[raw['mobile_money_frequency']],
        'has_defaulted':         int(raw['has_defaulted']),
        'high_debt_flag':        int(dti > 0.43),
        'deficit_flag':          int(net_flow < 0),
        'overextended_flag':     int(raw['num_active_loans'] >= 3),
        'housing_stress_flag':   int(raw['housing_expense'] / income > 0.30),
        'employment_encoded':    EMPLOYMENT_MAP[raw['employment_type']],
        'dependency_burden':     raw['num_dependents'] / (income / 1000),
    }

    return pd.DataFrame([features])[FEATURE_COLUMNS]


def compute_kpis(raw: dict) -> dict:
    """Compute human-readable KPIs shown on the dashboard."""
    income    = raw['monthly_income'] + 1e-9
    total_exp = (raw['housing_expense'] + raw['food_expense'] +
                 raw['transport_expense'] + raw['utilities_expense'] +
                 raw['other_expense'])
    net_flow  = income - total_exp - raw.get('monthly_savings', 0)

    return {
        'monthly_income':       raw['monthly_income'],
        'total_expenses':       total_exp,
        'net_cash_flow':        net_flow,
        'debt_to_income':  round(max(0, raw['total_debt'] / income) * 100, 1),
        'savings_rate':         round(raw.get('monthly_savings', 0)
                                      / income * 100, 1),
        'expense_ratio':        round(total_exp / income * 100, 1),
        'is_in_deficit':        net_flow < 0,
        'affordability_index':  round(net_flow / income * 100, 1),
    }