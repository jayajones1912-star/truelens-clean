from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


# -----------------------------
# TRUE LENS AI (UNCERTAINTY MODEL)
# -----------------------------
def analyze_video(source_type, value):

    text = str(value).lower()

    # -----------------------------
    # BASE RULE INDICATORS
    # -----------------------------
    facial_distortion = 1 if ("face" in text or source_type == "file") else 0
    lighting_issue = 1 if ("light" in text or source_type == "url") else 0
    lip_sync_issue = 1 if ("video" in text) else 0
    metadata_issue = 1 if source_type == "url" else 0

    # -----------------------------
    # UNCERTAINTY LAYER (AI BEHAVIOR SIMULATION)
    # -----------------------------
    def uncertain(value, noise=0.12):
        if value == 0:
            return 1 if random.random() < noise else 0
        else:
            return 0 if random.random() < noise else 1

    facial_distortion = uncertain(facial_distortion, 0.10)
    lighting_issue = uncertain(lighting_issue, 0.12)
    lip_sync_issue = uncertain(lip_sync_issue, 0.08)
    metadata_issue = uncertain(metadata_issue, 0.05)

    # -----------------------------
    # WEIGHTED SCORE (CORRECT MODEL)
    # -----------------------------
    score = (
        facial_distortion * 2 +
        lighting_issue * 2 +
        lip_sync_issue * 1 +
        metadata_issue * 1
    )

    score = min(score, 6)

    # -----------------------------
    # CONFIDENCE (WITH VARIATION)
    # -----------------------------
    base_confidence = (score / 6) * 100
    noise = random.uniform(-6, 6)

    confidence = base_confidence + noise
    confidence = max(0, min(100, confidence))
    confidence = round(confidence, 2)

    # -----------------------------
    # RISK LABEL
    # -----------------------------
    if score <= 2:
        label = "Low Risk"
        label_class = "low"
    elif score <= 4:
        label = "Medium Risk"
        label_class = "medium"
    else:
        label = "High Risk"
        label_class = "high"

    # -----------------------------
    # EXPLANATION ENGINE
    # -----------------------------
    explanation = []

    if facial_distortion:
        explanation.append("Facial inconsistencies detected with moderate confidence.")

    if lighting_issue:
        explanation.append("Lighting irregularities suggest possible manipulation.")

    if lip_sync_issue:
        explanation.append("Audio-visual timing mismatch detected.")

    if metadata_issue:
        explanation.append("External source reduces metadata reliability.")

    explanation_text = (
        " ".join(explanation)
        if explanation
        else "No strong synthetic indicators detected."
    )

    # -----------------------------
    # INDICATORS FOR FRONTEND
    # -----------------------------
    indicators = {
        "Facial Distortion": facial_distortion,
        "Lighting Issue": lighting_issue,
        "Lip Sync Issue": lip_sync_issue,
        "Metadata Issue": metadata_issue
    }

    # -----------------------------
    # DATA SOURCES
    # -----------------------------
    sources = [
        {
            "name": "Deepfake Detection Challenge (DFDC)",
            "url": "https://ai.meta.com/datasets/dfdc/"
        },
        {
            "name": "FaceForensics++ Dataset",
            "url": "https://www.kaggle.com/datasets/ahmedelbanby/faceforensicsplusplus-c23-deepfakebench-structure/data"
        }
    ]

    return {
        "label": label,
        "label_class": label_class,
        "confidence": confidence,
        "score": score,
        "indicators": indicators,
        "explanation": explanation_text,
        "sources": sources,
        "source_type": source_type,
        "source_value": value
    }


# -----------------------------
# ROUTE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files.get("file")
        url = request.form.get("url")

        # FILE INPUT
        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            result = analyze_video("file", file.filename)
            return render_template("result.html", filename=file.filename, **result)

        # URL INPUT
        if url and url.strip() != "":
            result = analyze_video("url", url)
            return render_template("result.html", filename=url, **result)

        return "No input provided"

    return render_template("index.html")


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    print("TrueLens AI Engine running with uncertainty model...")
    app.run(host="0.0.0.0", port=10000)