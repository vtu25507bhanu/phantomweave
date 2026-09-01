import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threat_model.pkl")

# మోడల్ ఒకేసారి లోడ్ చేసి memory లో ఉంచుతాం — ప్రతి request కి మళ్ళీ లోడ్ చేయకుండా (performance కోసం)
_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_threat(request_count: int, session_duration: float,
                    failed_login_attempts: int, typing_speed: float,
                    mouse_movement: int) -> dict:
    """
    ఒక విజిటర్ యొక్క behavior డేటా తీసుకుని, threat probability + classification ఇస్తుంది.
    """
    model = load_model()

    features = pd.DataFrame([{
        "request_count": request_count,
        "session_duration": session_duration,
        "failed_login_attempts": failed_login_attempts,
        "typing_speed": typing_speed,
        "mouse_movement": mouse_movement
    }])

    prediction = model.predict(features)[0]          # 0 = safe, 1 = threat
    probabilities = model.predict_proba(features)[0]  # [prob_safe, prob_threat]
    risk_score = float(probabilities[1])              # threat probability

    return {
        "is_threat": bool(prediction == 1),
        "risk_score": round(risk_score, 4),
        "confidence": round(float(max(probabilities)), 4)
    }