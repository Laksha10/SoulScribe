# File: routes/predict.py

from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np
import json
from transformers import RobertaTokenizer
import tensorflow as tf
import os

from db.connection import db
from db.models import JournalEntry
from utils.emotion_responses import generate_companion_response

predict_bp = Blueprint("predict", __name__)

# === Load all model components ===

# ✅ Load model (exported SavedModel format)
model = tf.keras.models.load_model("models/emotional_final_model2")

# ✅ Load tokenizer and labels
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

with open("models/label_list.json", "r") as f:
    label_list = json.load(f)

best_thresholds = np.load("models/best_thresholds.npy")
max_len = 128

# === Inference Logic ===
@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        text = data["text"]

        # Tokenize
        encoding = tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=max_len,
            return_tensors="tf"
        )

        input_ids = encoding["input_ids"]
        attention_mask = encoding["attention_mask"]

        # Predict using SavedModel's serving signature
        outputs = model.signatures["serving_default"](
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        logits = list(outputs.values())[0].numpy()
        binary_preds = (logits[0] > best_thresholds).astype(int)

        predicted_emotions = [label_list[i] for i, val in enumerate(binary_preds) if val == 1]

        # Generate chatbot message
        message = generate_companion_response(predicted_emotions)

        # Save entry to DB
        entry = JournalEntry(
            text=text,
            predicted_emotions=", ".join(predicted_emotions),
            timestamp=datetime.now()
        )
        db.session.add(entry)
        db.session.commit()

        print("✅ Prediction response:", {
            "emotions": predicted_emotions,
            "message": message
        })

        return jsonify({
            "emotions": predicted_emotions,
            "message": message
        }), 200

    except Exception as e:
        print("❌ Error in predict():", str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500
