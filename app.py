from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import re

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # ✅ Enable CORS for all routes

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = ["saree", "kurti", "jeans" , "kurta","lehenga", "tshirt","pant", "checkout", "cancel order", "buy"]

@app.route('/predict-intent', methods=['POST'])
def predict_intent():
    data = request.get_json()
    query = data.get('text', '').strip()

    if not query:
        return jsonify({"error": "Missing input text"}), 400

    result = classifier(query, candidate_labels=CATEGORIES)
    top_label = result['labels'][0]
    top_score = result['scores'][0]
    price = extract_price_from_text(query)

    return jsonify({
        "intent": top_label if top_score > 0.5 else "",
        "score": top_score,
        "price": price
    })

def extract_price_from_text(text):
    match = re.search(r"(under|below|less than|under ₹?)\s*([\d]+)", text.lower())
    if match:
        return int(match.group(2))
    return None

if __name__ == '__main__':
    app.run(port=5001)
