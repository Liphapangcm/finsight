# core/service.py
"""
Service layer — orchestrates the full scoring pipeline.
This is the ONLY file that Streamlit imports from core/.
Single entry point keeps the UI completely decoupled from ML logic.
"""

import uuid
from core.schemas import AssessmentInput, ScoreResult, FinancialKPIs
from core.predictor import predict
from core.explainer import explain
from core.recommender import generate_recommendations
from config import config


def run_assessment(inp: AssessmentInput) -> tuple[ScoreResult | None,
                                                   list[str]]:
    """
    Main entry point for the scoring pipeline.

    Args:
        inp: Validated AssessmentInput from the form

    Returns:
        (ScoreResult, [])           on success
        (None, [error messages])    on validation failure
    """

    # ── Step 1: Validate input ────────────────────────────────────
    errors = inp.validate()
    if errors:
        return None, errors

    # ── Step 2: Run ML prediction ─────────────────────────────────
    pred = predict(inp)

    # ── Step 3: Generate SHAP explanation ────────────────────────
    explanation = explain(pred['feature_df'])

    # ── Step 4: Generate recommendations ─────────────────────────
    recommendations = generate_recommendations(
        inp         = inp,
        explanation = explanation,
        credit_score= pred['credit_score'],
        kpis        = pred['kpis'],
    )

    # ── Step 5: Assemble KPIs ─────────────────────────────────────
    k = pred['kpis']
    kpis = FinancialKPIs(
        monthly_income      = k['monthly_income'],
        total_expenses      = k['total_expenses'],
        net_cash_flow       = k['net_cash_flow'],
        debt_to_income      = k['debt_to_income'],
        savings_rate        = k['savings_rate'],
        expense_ratio       = k['expense_ratio'],
        affordability_index = k['affordability_index'],
        is_in_deficit       = k['is_in_deficit'],
    )

    # ── Step 6: Assemble final result ─────────────────────────────
    result = ScoreResult(
        credit_score     = pred['credit_score'],
        score_band       = pred['score_band'],
        risk_level       = pred['risk_level'],
        score_color      = pred['score_color'],
        shap_explanation = explanation,
        kpis             = kpis,
        recommendations  = recommendations,
        model_version    = config.MODEL_VERSION,
        assessment_id    = str(uuid.uuid4()),
    )

    # ── Step 7: Persist to database ───────────────────────────────
    try:
        from database.connection import SessionLocal, init_db
        from database import crud

        init_db()
        db = SessionLocal()
        crud.save_assessment(db, inp)
        crud.save_score(db, result)
        db.close()
    except Exception as e:
        # DB failure should never crash the UI — log and continue
        print(f"[WARNING] Database save failed: {e}")

    return result, []