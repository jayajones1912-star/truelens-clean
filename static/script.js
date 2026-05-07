document.getElementById("videoInput").addEventListener("change", function () {
    const file = this.files[0];
    const video = document.getElementById("videoPreview");

    if (file) {
        video.src = URL.createObjectURL(file);
        video.style.display = "block";
    }
});


async function submitInput() {

    const text = document.getElementById("userInput").value;
    const video = document.getElementById("videoInput").files[0];

    const formData = new FormData();
    formData.append("input", text);

    if (video) {
        formData.append("video", video);
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("resultCard").classList.add("hidden");

    const response = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("loading").classList.add("hidden");


    // =========================
    // RESULT + RISK DISPLAY
    // =========================
    const resultText = document.getElementById("resultText");
    resultText.innerText = data.result;


    // =========================
    // CONFIDENCE SCORE
    // =========================
    document.getElementById("confidence").innerText = data.confidence;

    let score = parseInt(data.confidence.split("/")[0]);
    let percent = (score / 7) * 100;
    document.getElementById("scoreBar").style.width = percent + "%";


    // =========================
    // COLOR CODING
    // =========================
    resultText.classList.remove("low-risk", "medium-risk", "high-risk");

    if (data.result === "Low Risk") {
        resultText.classList.add("low-risk");
    } else if (data.result === "Medium Risk") {
        resultText.classList.add("medium-risk");
    } else if (data.result === "High Risk") {
        resultText.classList.add("high-risk");
    }


    // =========================
    // EXPLAINABLE INDICATORS
    // =========================
    const container = document.getElementById("noteContainer");
    container.innerHTML = "";

    data.note.forEach(item => {

        const div = document.createElement("div");
        div.classList.add("note-item");

        div.innerHTML = `
            <strong>${item.title} (+${item.score})</strong><br>
            <small><b>Why detected:</b> ${item.reason}</small><br>
            <small><b>Impact:</b> ${item.impact}</small>
        `;

        div.onclick = () => {
            alert(
                item.title +
                "\n\nReason: " + item.reason +
                "\n\nImpact: " + item.impact +
                "\n\nThis contributes to the final risk score."
            );
        };

        container.appendChild(div);
    });


    document.getElementById("resultCard").classList.remove("hidden");
}


function loadExample() {
    document.getElementById("userInput").value =
        "Example: deepfake video analysis for authenticity detection.";
}