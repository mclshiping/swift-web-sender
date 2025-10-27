
from flask import Flask, request, jsonify
from teller_api import send_payment
from swift_generator import generate_swift_message

app = Flask(__name__)

@app.route("/send_payment", methods=["POST"])
def handle_payment():
    data = request.json
    required = ["account_id", "amount", "currency", "description", "recipient"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    code, res = send_payment(
        account_id=data["account_id"],
        amount=data["amount"],
        currency=data["currency"],
        description=data["description"],
        recipient=data["recipient"]
    )
    return jsonify(res), code

@app.route("/generate_swift", methods=["POST"])
def generate_swift():
    data = request.json
    message_type = data.get("type")
    payload = data.get("payload")
    if not message_type or not payload:
        return jsonify({"error": "Missing message type or payload"}), 400
    try:
        output = generate_swift_message(message_type, payload)
        return jsonify({"swift_message": output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
