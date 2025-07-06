from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])  # Allow both localhost variants

print("Starting lightweight Python backend...")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Python AI Backend is running (lightweight mode)",
        "model": "keyword-based"
    })

@app.route('/predict-intent', methods=['POST'])
def predict_intent():
    data = request.get_json()
    query = data.get('text', '').strip().lower()

    if not query:
        return jsonify({"error": "Missing input text"}), 400

    # Use keyword-based intent extraction (fast and reliable)
    intent = extract_keyword_intent(query)
    price = extract_price_from_text(query)
    
    print(f"Query: '{query}' -> Intent: '{intent}'")
    
    return jsonify({
        "intent": intent,
        "score": 0.9 if intent else 0.0,  # High confidence for keyword match
        "price": price,
        "method": "keyword"
    })

def extract_keyword_intent(text):
    """Extract intent using simple keyword matching"""
    # Create a mapping of keywords to intents
    keyword_mapping = {
        'jeans': 'jeans',
        'denim': 'jeans',
        'saree': 'saree',
        'sari': 'saree',
        'kurti': 'kurti',
        'kurta': 'kurta',
        'lehenga': 'lehenga',
        'tshirt': 'tshirt',
        't-shirt': 'tshirt',
        'shirt': 'tshirt',
        'pant': 'pant',
        'pants': 'pant',
        'trousers': 'pant',
        'checkout': 'checkout',
        'buy': 'buy',
        'purchase': 'buy',
        'order': 'buy',
        'cancel': 'cancel order',
        'return': 'cancel order'
    }
    
    # Check for exact matches first
    for keyword, intent in keyword_mapping.items():
        if keyword in text:
            return intent
    
    return ""

def extract_price_from_text(text):
    match = re.search(r"(under|below|less than|under ₹?)\s*([\d]+)", text.lower())
    if match:
        return int(match.group(2))
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)