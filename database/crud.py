import uuid
from sqlalchemy.orm import Session
from database.models import Assessment, Score, RecommendationRecord
from core.schemas import AssessmentInput, ScoreResult


def save_assessment(db: Session, inp: AssessmentInput) -> str:
    assessment_id = str(uuid.uuid4())
    record = Assessment(id=assessment_id, **inp.to_dict())
    db.add(record)
    db.commit()
    return assessment_id


def save_score(db: Session, result: ScoreResult) -> str:
    score_id = str(uuid.uuid4())

    score = Score(
        id                  = score_id,
        assessment_id       = result.assessment_id,
        credit_score        = result.credit_score,
        score_band          = result.score_band,
        risk_level          = result.risk_level,
        debt_to_income      = result.kpis.debt_to_income,
        savings_rate        = result.kpis.savings_rate,
        expense_ratio       = result.kpis.expense_ratio,
        affordability_index = result.kpis.affordability_index,
        model_version       = result.model_version,
        confidence          = 0.0,   # placeholder for now
    )
    db.add(score)

    for rec in result.recommendations:
        db.add(RecommendationRecord(
            id              = str(uuid.uuid4()),
            score_id        = score_id,
            priority        = rec.priority,
            category        = rec.category,
            title           = rec.title,
            description     = rec.description,
            impact_estimate = rec.impact_estimate,
        ))

    db.commit()
    return score_id


def get_recent_scores(db: Session, limit: int = 10):
    return (db.query(Score)
              .order_by(Score.created_at.desc())
              .limit(limit)
              .all())