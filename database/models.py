# database/models.py
from datetime import datetime
from sqlalchemy import (Column, String, Integer, Float,
                        Boolean, DateTime, ForeignKey)
from database.connection import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id                      = Column(String,  primary_key=True)
    created_at              = Column(DateTime, default=datetime.utcnow)

    # Personal
    age                     = Column(Integer)
    employment_type         = Column(String)
    district                = Column(String)
    num_dependents          = Column(Integer)

    # Income & Expenses
    monthly_income          = Column(Float)
    housing_expense         = Column(Float)
    food_expense            = Column(Float)
    transport_expense       = Column(Float)
    utilities_expense       = Column(Float)
    other_expense           = Column(Float)

    # Debt & Credit
    total_debt              = Column(Float)
    num_active_loans        = Column(Integer)
    has_defaulted           = Column(Boolean)
    payment_regularity      = Column(String)

    # Savings
    has_savings             = Column(Boolean)
    monthly_savings         = Column(Float)

    # Behaviour
    mobile_money_frequency  = Column(String)


class Score(Base):
    __tablename__ = "scores"

    id                  = Column(String, primary_key=True)
    assessment_id       = Column(String, ForeignKey("assessments.id"))
    created_at          = Column(DateTime, default=datetime.utcnow)

    credit_score        = Column(Integer)
    score_band          = Column(String)
    risk_level          = Column(String)
    debt_to_income      = Column(Float)
    savings_rate        = Column(Float)
    expense_ratio       = Column(Float)
    affordability_index = Column(Float)
    model_version       = Column(String)
    confidence          = Column(Float)


class RecommendationRecord(Base):
    __tablename__ = "recommendations"

    id               = Column(String, primary_key=True)
    score_id         = Column(String, ForeignKey("scores.id"))
    priority         = Column(Integer)
    category         = Column(String)
    title            = Column(String)
    description      = Column(String)
    impact_estimate  = Column(String)