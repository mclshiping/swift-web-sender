
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from swift_generator import generate_swift_message
import requests

app = Flask(__name__, static_url_path="", static_folder=".")
app.secret_key = "your-very-secret-key"  # Change this in production!

users = {
    "admin": "password123",  # Example user
    "user": "pass456"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if users.get(username) == password:
            session["user"] = username
            return jsonify({"message": "Login successful."})
        return jsonify({"error": "Invalid credentials."}), 401
    return send_from_directory(".", "login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.before_request
def require_login():
    if request.endpoint not in ("login", "static") and not session.get("user"):
        return redirect("/login")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/generate_swift", methods=["POST"])
def generate_swift():
    try:
        data = request.get_json()
        mt_type = data.get("type")
        payload = data.get("payload", {})
        swift_msg = generate_swift_message(mt_type, payload)
        return jsonify({"swift_message": swift_msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/send_payment", methods=["POST"])
def send_payment():
    try:
        data = request.get_json()
        account_id = data.get("account_id")
        payload = {
            "amount": {
                "currency": data["currency"],
                "value": data["amount"]
            },
            "description": data.get("description", "SWIFT Payment"),
            "destination": {
                "type": "external_account",
                "name": data["recipient"]["name"],
                "account_number": data["recipient"]["account"]
            }
        }
        headers = {
            "Authorization": "Bearer YOUR_TELLER_TOKEN",
            "Content-Type": "application/json"
        }
        url = f"https://api.teller.io/accounts/{account_id}/payments"
        r = requests.post(url, json=payload, headers=headers)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
