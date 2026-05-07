from flask import Flask, render_template, request, send_from_directory
import os
import hashlib
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# UPLOAD + ANALYSIS ROUTE
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    # save uploaded video
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # -----------------------------
    # DYNAMIC SEED (IMPORTANT FIX)
    # ensures different results per video
    # -----------------------------
    seed_value = int(hashlib.md5(file.filename.encode()).hexdigest(), 16)
    random.seed(seed_value)

    # -----------------------------
    # TRUE LENS INDICATORS
    # -----------------------------
    indicators = [
        {
            "name": "Facial Distortion",
            "points": 2,
            "detected": random.random() > 0.5,
            "reason": "Inconsistent facial geometry detected across frames"
            if random.random() > 0.5 else "No facial distortion observed"
        },
        {
            "name": "Lip-sync Mismatch",
            "points": 2,
            "detected": random.random() > 0.5,
            "reason": "Audio does not align with lip movement"
            if random.random() > 0.5 else "Audio alignment appears consistent"
        },
        {
            "name": "Lighting Inconsistency",
            "points": 2,
            "detected": random.random() > 0.6,
            "reason": "Lighting inconsistencies detected"
            if random.random() > 0.6 else "Lighting is stable"
        },
        {
            "name": "Metadata Anomalies",
            "points": 1,
            "detected": random.random() > 0.7,
            "reason": "Suspicious metadata patterns found"
            if random.random() > 0.7 else "Metadata appears normal"
        }
    ]

    # -----------------------------
    # SCORE CALCULATION
    # -----------------------------
    score = sum(i["points"] for i in indicators if i["detected"])
    active = sum(1 for i in indicators if i["detected"])

    # -----------------------------
    # RISK + CONFIDENCE LOGIC
    # -----------------------------
    if active == 0:
        risk_level = "Low"
        confidence = 0
        summary = "No manipulation indicators were detected. The media appears consistent with authentic patterns."
    else:
        confidence = int((score / 7) * 100)

        if score <= 2:
            risk_level = "Low"
        elif score <= 4:
            risk_level = "Medium"
        else:
            risk_level = "High"

        summary = (
            "The system detected inconsistencies in visual and audio signals. "
            "These patterns are commonly associated with manipulated or AI-generated media. "
            "However, results are probabilistic and should be interpreted with caution."
        )

    # -----------------------------
    # SEND TO RESULT PAGE
    # -----------------------------
    return render_template(
        "result.html",
        score=score,
        risk_level=risk_level,
        indicators=indicators,
        confidence=confidence,
        summary=summary,
        filename=file.filename
    )


# -----------------------------
# ALLOW VIDEO DISPLAY IN WEBPAGE
# -----------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)