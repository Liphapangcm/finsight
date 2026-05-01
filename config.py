# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App
    APP_NAME = "FinSight"
    APP_VERSION = "1.0.0"
    MODEL_VERSION = "v1.0.0"

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finsight.db")

    # Model paths
    MODEL_PATH = "models/model.pkl"
    PREPROCESSOR_PATH = "models/preprocessor.pkl"
    EXPLAINER_PATH = "models/explainer.pkl"

    # Score bands
    SCORE_BANDS = {
        (0,   449): ("Poor",      "High",   "#E53935"),
        (450, 579): ("Fair",      "Medium", "#FB8C00"),
        (580, 699): ("Good",      "Low",    "#43A047"),
        (700, 850): ("Excellent", "Very Low","#00897B"),
    }

    # UI
    PRIMARY_COLOR   = "#0B1F3A"
    ACCENT_COLOR    = "#00BFA6"
    WARNING_COLOR   = "#FB8C00"
    DANGER_COLOR    = "#E53935"
    SUCCESS_COLOR   = "#43A047"

config = Config()