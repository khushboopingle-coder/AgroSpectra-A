"""
AgroSpectra AI - Crop Classification Model Loader and Predictor
Encapsulates Keras model caching, preprocessing, and inference.
"""

import numpy as np
from PIL import Image
import streamlit as st
from config import MODEL_PATH, EUROSAT_CLASSES


@st.cache_resource(show_spinner="Loading Keras EuroSAT Crop Model...")
def load_crop_model():
    """
    Loads and caches the trained Keras crop model.
    Expected input shape: (1, 64, 64, 3)
    Output: 10-class softmax probabilities
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

    import keras
    model = keras.models.load_model(str(MODEL_PATH))
    return model


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocesses an input image according to the EuroSAT training pipeline:
    1. Convert to RGB (drops alpha / handles grayscale).
    2. Resize to 64x64.
    3. Convert to float32 and scale to [0, 1] (/ 255.0).
    4. Expand batch dimension to (1, 64, 64, 3).
    """
    rgb_img = image.convert("RGB")
    resized_img = rgb_img.resize((64, 64), Image.Resampling.BILINEAR)
    arr = np.array(resized_img, dtype=np.float32) / 255.0
    batch_arr = np.expand_dims(arr, axis=0)
    return batch_arr


def predict_crop(image: Image.Image):
    """
    Runs inference on an image and returns:
    - top_class: str
    - confidence: float (0..100)
    - predictions: list of dicts [{'class': str, 'confidence': float, 'index': int}] sorted desc
    - raw_probs: np.ndarray of shape (10,)
    """
    model = load_crop_model()
    batch_arr = preprocess_image(image)
    raw_preds = model.predict(batch_arr, verbose=0)[0]

    results = []
    for idx, prob in enumerate(raw_preds):
        results.append({
            "index": idx,
            "class": EUROSAT_CLASSES[idx],
            "confidence": float(prob * 100.0),
            "probability": float(prob)
        })

    results.sort(key=lambda x: x["confidence"], reverse=True)
    top_pred = results[0]

    return {
        "top_class": top_pred["class"],
        "top_confidence": top_pred["confidence"],
        "top_index": top_pred["index"],
        "all_predictions": results,
        "raw_probabilities": raw_preds
    }
