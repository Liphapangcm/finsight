import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score
from core.features import FEATURE_COLUMNS


def evaluate_model():
    df = pd.read_csv("ml/data/processed/training_data.csv")

    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/preprocessor.pkl", "rb") as f:
        scaler = pickle.load(f)

    X = scaler.transform(df[FEATURE_COLUMNS])
    y = df['credit_score']
    y_pred = model.predict(X)

    print("\n=== MODEL EVALUATION ===")
    print(f"MAE         : {mean_absolute_error(y, y_pred):.2f} points")
    print(f"R² Score    : {r2_score(y, y_pred):.4f}")

    # Score band accuracy
    def band(s):
        if s < 450:  return 'Poor'
        if s < 580:  return 'Fair'
        if s < 700:  return 'Good'
        return 'Excellent'

    df['actual_band']    = y.apply(band)
    df['predicted_band'] = pd.Series(y_pred).apply(band)
    band_acc = (df['actual_band'] == df['predicted_band']).mean()
    print(f"Band Accuracy: {band_acc:.2%}")

    # Feature importance
    importance = pd.Series(
        model.feature_importances_,
        index=FEATURE_COLUMNS
    ).sort_values(ascending=False)
    print("\n=== TOP 10 FEATURES ===")
    print(importance.head(10).to_string())


if __name__ == "__main__":
    evaluate_model()