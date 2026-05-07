import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================
# EXPLAINABLE RULE ENGINE
# ============================
def analyze_video():

    score = 0
    indicators = []

    # Simulated detection signals (replace later with ML models)
    facial_distortion = True
    lighting_inconsistency = True
    lip_sync_mismatch = False
    metadata_anomaly = True

    # ---------------- FACIAL DISTORTION ----------------
    if facial_distortion:
        score += 2
        indicators.append({
            "title": "Facial Distortion",
            "score": 2,
            "reason": "Irregular facial geometry patterns detected across frames, often linked to synthetic face generation or deepfake blending artifacts.",
            "impact": "High influence on authenticity score"
        })

    # ---------------- LIGHTING INCONSISTENCY ----------------
    if lighting_inconsistency:
        score += 2
        indicators.append({
            "title": "Lighting Inconsistency",
            "score": 2,
            "reason": "Inconsistent lighting direction and shadow mapping detected across frames, suggesting possible video compositing or editing.",
            "impact": "Strong indicator of manipulation"
        })

    # ---------------- LIP SYNC ----------------
    if lip_sync_mismatch:
        score += 2
        indicators.append({
            "title": "Lip-Sync Mismatch",
            "score": 2,
            "reason": "Audio waveform timing does not align with mouth movement patterns, indicating possible synthetic audio or voice replacement.",
            "impact": "High deepfake indicator"
        })

    # ---------------- METADATA ----------------
    if metadata_anomaly:
        score += 1
        indicators.append({
            "title": "Metadata Anomaly",
            "score": 1,
            "reason": "File metadata inconsistencies detected (missing encoder info, altered timestamps, or compression artifacts).",
            "impact": "Moderate reliability concern"
        })

    # ---------------- RISK CLASSIFICATION ----------------
    if score <= 2:
        risk = "Low Risk"
    elif score <= 4:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return score, risk, indicators


# ============================
# ROUTES
# ============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    video = request.files.get("video")

    if video:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        video.save(os.path.join(UPLOAD_FOLDER, video.filename))

    if not video:
        return jsonify({
            "result": "No Video Uploaded",
            "confidence": "0/7",
            "note": []
        })

    score, risk, indicators = analyze_video()

    return jsonify({
        "result": risk,
        "confidence": f"{score}/7",
        "note": indicators
    })


if __name__ == "__main__":
    app.run(debug=True)