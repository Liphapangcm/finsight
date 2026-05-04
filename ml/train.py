"""
Trains the FinSight credit scoring model.
Run this script offline whenever you want to retrain.
Usage: python -m ml.train
"""

import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import shap

from ml.simulate_data import simulate_dataset
from core.features import FEATURE_COLUMNS

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)


def train():
    print("▶ Generating synthetic data...")
    df = simulate_dataset(n_samples=8000)
    df.to_csv("ml/data/processed/training_data.csv", index=False)

    X = df[FEATURE_COLUMNS]
    y = df["credit_score"]

    # ── Train/test split ──────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ── Preprocessing: scale continuous features ──────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ── Model: XGBoost Regressor ──────────────────────────────────
    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train_scaled,
        y_train,
        eval_set=[(X_test_scaled, y_test)],
        verbose=50,
    )

    # ── Evaluation ────────────────────────────────────────────────
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # BUG FIX: cross_val_score needs the scaler applied first.
    # We scale the full X before passing to CV, since cross_val_score
    # does NOT call fit_transform internally — it uses the already-fitted
    # model. This avoids data leakage while keeping the CV valid.
    X_scaled_full = scaler.transform(X)
    cv_scores = cross_val_score(model, X_scaled_full, y, cv=5, scoring="r2")

    print(f"\n{'─' * 40}")
    print(f"  MAE    : {mae:.2f} points")
    print(f"  R²     : {r2:.4f}")
    print(f"  CV R²  : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"{'─' * 40}\n")

    # ── SHAP explainer ────────────────────────────────────────────
    print("▶ Fitting SHAP explainer...")
    explainer = shap.TreeExplainer(model)

    # ── Save artifacts ────────────────────────────────────────────
    print("▶ Saving model artifacts...")
    with open(MODELS_DIR / "model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(MODELS_DIR / "preprocessor.pkl", "wb") as f:
        pickle.dump(scaler, f)

    with open(MODELS_DIR / "explainer.pkl", "wb") as f:
        pickle.dump(explainer, f)

    print("✅ Training complete. Artifacts saved to /models")
    return mae, r2


if __name__ == "__main__":
    train()
