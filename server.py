# server.py
from ARsemble_ai import handle_query
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# import the new wrapper (make sure file is named ARsemble_ai.py)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True)
    message = payload.get("message") if isinstance(payload, dict) else None
    if message is None:
        return jsonify({"response": "Invalid request — expected JSON with key 'message'."}), 400
    try:
        reply = handle_query(message)
        return jsonify({"response": reply})
    except Exception as e:
        # print exception to server console for debugging
        print("[server] error in handle_query:", e)
        return jsonify({"response": f"⚠️ Server error: {e}"}), 500


if __name__ == "__main__":
    # ensure FLASK_SKIP_DOTENV=1 if you have binary .env causing decode errors
    app.run(host="0.0.0.0", port=5000, debug=False)
