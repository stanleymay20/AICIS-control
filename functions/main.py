from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
import functions_framework
from werkzeug.middleware.proxy_fix import ProxyFix  # ✅ Fix for Firebase requests

# Initialize Firebase Admin SDK
cred = credentials.Certificate("aicis-control-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create Flask App
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)  # ✅ Fix: Ensure Firebase handles requests properly

# ✅ API Root
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AICIS API is running!"})

# ✅ Trades Route
@app.route("/api/trades", methods=["GET"])
def get_trades():
    trades = [
        {"pair": "BTC/USD", "action": "BUY", "price": 45000, "profit": "+5%"},
        {"pair": "ETH/USD", "action": "SELL", "price": 3000, "profit": "-2%"},
    ]
    return jsonify(trades)

# ✅ Proper Firebase Function Handler
@functions_framework.http
def api(request):
    """Firebase Cloud Function Wrapper"""
    return app(request)
