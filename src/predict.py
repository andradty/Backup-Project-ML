"""Inference helper module for Rice Leaf Disease Classification."""

from pathlib import Path
from typing import Union
import joblib
import numpy as np
import pandas as pd
from PIL import Image

from src import MODELS_DIR, CLASSES, CLASS_INFO
from src.preprocessing import (
    extract_features_from_image,
    get_feature_names,
    validate_uploaded_image,
)

MODEL_FILES = {
    "SVM (RBF) — Model Final": MODELS_DIR / "svm_pipeline.joblib",
    "XGBoost": MODELS_DIR / "xgboost_pipeline.joblib",
    "Random Forest": MODELS_DIR / "rf_pipeline.joblib",
}


def load_model(model_name: str = "SVM (RBF) — Model Final"):
    """Load a trained scikit-learn Pipeline from disk."""
    path = MODEL_FILES.get(model_name)
    if path is None or not path.exists():
        default_path = MODELS_DIR / "final_model.joblib"
        if default_path.exists():
            return joblib.load(default_path)
        raise FileNotFoundError(f"Model file tidak ditemukan di {MODELS_DIR}")
    return joblib.load(path)


def predict_image(
    image_input: Union[str, Path, Image.Image],
    model_name: str = "SVM (RBF) — Model Final",
) -> dict:
    """
    Validate image, extract 100 features, run prediction and probability estimation,
    and return a comprehensive dictionary for the Streamlit UI.
    """
    is_valid, msg, diag = validate_uploaded_image(image_input)
    if not is_valid:
        return {"valid": False, "message": msg, "diagnostics": diag}

    feats = extract_features_from_image(image_input)
    feature_names = get_feature_names()
    X_df = pd.DataFrame([feats], columns=feature_names)

    pipeline = load_model(model_name)
    pred_idx = int(pipeline.predict(X_df)[0])
    proba = pipeline.predict_proba(X_df)[0]

    pred_class = CLASSES[pred_idx]
    confidence = float(proba[pred_idx])

    proba_dict = {CLASSES[i]: float(proba[i]) for i in range(len(CLASSES))}
    info = CLASS_INFO[pred_class]

    return {
        "valid": True,
        "message": msg,
        "model_name": model_name,
        "predicted_label": pred_idx,
        "predicted_class": pred_class,
        "nama_id": info["nama_id"],
        "confidence": confidence,
        "confidence_pct": round(confidence * 100.0, 2),
        "probabilities": proba_dict,
        "class_info": info,
        "diagnostics": diag,
        "features": X_df,
    }
