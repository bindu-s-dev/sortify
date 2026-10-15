from flask import Flask, request, jsonify, send_from_directory
import pickle
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "sortify_model.pkl", "rb") as file:
    model = pickle.load(file)


DISPOSAL_GUIDE = {
    "Organic Waste": {
        "method": "Composting or appropriate wet-waste collection",
        "tip": "Separate suitable organic waste for composting."
    },
    "Paper Waste": {
        "method": "Dry-waste recycling collection",
        "tip": "Keep paper clean and dry."
    },
    "Plastic Waste": {
        "method": "Appropriate plastic recycling collection",
        "tip": "Empty and rinse containers, and check local recycling rules."
    },
    "Glass Waste": {
        "method": "Designated glass collection",
        "tip": "Handle broken glass carefully and follow local disposal rules."
    },
    "Metal Waste": {
        "method": "Metal recycling collection",
        "tip": "Separate metal items according to local recycling requirements."
    },
    "Electronic Waste": {
        "method": "Authorized e-waste collection",
        "tip": "Do not place electronic devices in ordinary household waste."
    },
    "Hazardous Waste": {
        "method": "Authorized hazardous-waste collection",
        "tip": "Do not mix chemicals or hazardous items with ordinary waste."
    }
}


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def website_files(filename):
    allowed_files = {"style.css", "script.js"}

    if filename not in allowed_files:
        return "Not found", 404

    return send_from_directory(BASE_DIR, filename)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    item = str(data.get("item", "")).strip()

    if not item:
        return jsonify({"error": "Please enter a waste item."}), 400

    if len(item) > 100:
        return jsonify({"error": "Please enter a shorter waste description."}), 400

    category_probabilities = model.predict_proba([item])[0]
    best_index = category_probabilities.argmax()
    category = model.classes_[best_index]
    confidence = float(category_probabilities[best_index])

    # A conservative threshold for this small demonstration model.
    # This is not a guarantee that the prediction is correct.
    if confidence < 0.35:
        return jsonify({
            "category": "Uncertain",
            "method": "Please check with your local waste-management service.",
            "tip": "The model could not confidently classify this item. Do not rely on this prediction for hazardous waste.",
            "confidence": round(confidence * 100, 1)
        })

    guidance = DISPOSAL_GUIDE[category]

    return jsonify({
        "category": category,
        "method": guidance["method"],
        "tip": guidance["tip"],
        "confidence": round(confidence * 100, 1)
    })


if __name__ == "__main__":
    app.run(debug=True)