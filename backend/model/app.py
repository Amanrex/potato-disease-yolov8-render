import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "model/best.pt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"❌ Model not found at {MODEL_PATH}. "
        "Place your trained model as backend/model/best.pt"
    )

# Load YOLO model once
model = YOLO(MODEL_PATH)

# Remedies dictionary
REMEDIES = {
    "Potato___healthy": {
        "status": "Healthy ✅",
        "remedy": "No disease detected. Maintain good irrigation, nutrients, and regular monitoring."
    },
    "Potato___Early_blight": {
        "status": "Diseased ❌",
        "remedy": "Remove infected leaves, apply fungicide (mancozeb/chlorothalonil), avoid overhead watering, and rotate crops."
    },
    "Potato___Late_blight": {
        "status": "Diseased ❌",
        "remedy": "Remove infected plants immediately, avoid excess moisture, improve airflow, and use fungicide (metalaxyl-based)."
    }
}


@app.route("/", methods=["GET"])
def home():
    return "✅ Potato Disease Detection API is running!"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded. Use key 'image'."}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        img = Image.open(save_path).convert("RGB")

        results = model.predict(img)

        probs = results[0].probs
        class_id = int(probs.top1)
        confidence = float(probs.top1conf)

        class_name = results[0].names[class_id]

        remedy_info = REMEDIES.get(class_name, {
            "status": "Unknown ⚠️",
            "remedy": "No remedy available for this prediction."
        })

        return jsonify({
            "predicted_class": class_name,
            "confidence": round(confidence * 100, 2),
            "status": remedy_info["status"],
            "remedy": remedy_info["remedy"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # local run only
    app.run(host="0.0.0.0", port=5000, debug=True)
