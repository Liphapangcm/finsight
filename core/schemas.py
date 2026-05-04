"""
Data contracts for FinSight.
All input/output between layers uses these dataclasses — never raw dicts.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────────────────────


class EmploymentType(str, Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"


class PaymentRegularity(str, Enum):
    ALWAYS = "always"
    SOMETIMES = "sometimes"
    RARELY = "rarely"


class MobileMoneyFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NEVER = "never"


class ScoreBand(str, Enum):
    POOR = "Poor"
    FAIR = "Fair"
    GOOD = "Good"
    EXCELLENT = "Excellent"


class RiskLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    VERY_LOW = "Very Low"


class RecommendationCategory(str, Enum):
    DEBT = "debt"
    SAVINGS = "savings"
    INCOME = "income"
    BEHAVIOUR = "behaviour"
    EXPENSES = "expenses"


# ── Input Schema ──────────────────────────────────────────────────────────────


@dataclass
class AssessmentInput:
    """
    Raw form input from the user.
    Validated before passing to the feature engineering pipeline.
    """

    # Personal
    age: int
    employment_type: str
    num_dependents: int
    district: str = "Maseru"

    # Income
    monthly_income: float = 0.0

    # Expenses
    housing_expense: float = 0.0
    food_expense: float = 0.0
    transport_expense: float = 0.0
    utilities_expense: float = 0.0
    other_expense: float = 0.0

    # Debt
    total_debt: float = 0.0
    num_active_loans: int = 0
    has_defaulted: bool = False
    payment_regularity: str = "always"

    # Savings
    has_savings: bool = False
    monthly_savings: float = 0.0

    # Behaviour
    mobile_money_frequency: str = "weekly"

    def validate(self) -> List[str]:
        """
        Returns list of validation error messages.
        Empty list = valid input.
        """
        errors = []

        if not (18 <= self.age <= 100):
            errors.append("Age must be between 18 and 100.")

        if self.monthly_income <= 0:
            errors.append("Monthly income must be greater than 0.")

        if self.monthly_income > 500_000:
            errors.append("Monthly income seems unusually high. Please check.")

        total_exp = (
            self.housing_expense
            + self.food_expense
            + self.transport_expense
            + self.utilities_expense
            + self.other_expense
        )
        if total_exp > self.monthly_income * 3:
            errors.append("Total expenses are more than 3× your income. Please check.")

        if self.total_debt < 0:
            errors.append("Total debt cannot be negative.")

        if self.monthly_savings < 0:
            errors.append("Monthly savings cannot be negative.")

        if self.monthly_savings > self.monthly_income:
            errors.append("Monthly savings cannot exceed monthly income.")

        if self.num_dependents < 0:
            errors.append("Number of dependents cannot be negative.")

        if self.employment_type not in [e.value for e in EmploymentType]:
            errors.append(f"Invalid employment type: {self.employment_type}")

        if self.payment_regularity not in [p.value for p in PaymentRegularity]:
            errors.append(f"Invalid payment regularity: {self.payment_regularity}")

        if self.mobile_money_frequency not in [m.value for m in MobileMoneyFrequency]:
            errors.append(
                f"Invalid mobile money frequency: {self.mobile_money_frequency}"
            )

        return errors

    def to_dict(self) -> dict:
        return self.__dict__.copy()


# ── Output Schemas ────────────────────────────────────────────────────────────


@dataclass
class Recommendation:
    priority: int
    category: str
    title: str
    description: str
    impact_estimate: str


@dataclass
class FinancialKPIs:
    monthly_income: float
    total_expenses: float
    net_cash_flow: float
    debt_to_income: float  # percentage
    savings_rate: float  # percentage
    expense_ratio: float  # percentage
    affordability_index: float  # percentage
    is_in_deficit: bool


@dataclass
class SHAPExplanation:
    feature_names: List[str]
    shap_values: List[float]
    base_value: float


@dataclass
class ScoreResult:
    """
    Complete output returned to the Streamlit UI.
    One object contains everything needed to render the results page.
    """

    # Core score
    credit_score: int
    score_band: str
    risk_level: str
    score_color: str

    # Explanation
    shap_explanation: SHAPExplanation

    # Financial health
    kpis: FinancialKPIs

    # Recommendations
    recommendations: List[Recommendation]

    # Metadata
    model_version: str
    assessment_id: str
