from flask import Flask, request, jsonify
from predictor import predict

# ============================================================
# SCAMSHIELD — api.py
# Flask REST API
# ============================================================

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "ScamShield API is running!",
        "endpoint": "/predict",
        "method": "POST"
    })

@app.route('/predict', methods=['POST'])
def predict_route():
    # Request se text lo
    data = request.get_json()
    
    # Validation
    if not data or 'text' not in data:
        return jsonify({
            "error": "Please provide 'text' in request body"
        }), 400
    
    text = data['text'].strip()
    
    if len(text) < 10:
        return jsonify({
            "error": "Text too short — please provide full job post"
        }), 400
    
    # Prediction karo
    result = predict(text)
    
    return jsonify({
        "verdict":     result['verdict'],
        "trust_score": result['trust_score'],
        "emoji":       result['emoji'],
        "ml_score":    result['ml_score'],
        "rule_score":  result['rule_score'],
        "flags":       result['flags']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)