# server.py
from ARsemble_ai import handle_query, generate_quick_recommendations
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import logging
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ARsemble-server")


@app.route("/")
def index():
    # Serve the index.html from the static folder
    return send_from_directory("static", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Expects JSON body: { "message": "<user message>" }
    Calls ARsemble_ai.handle_query(...) which returns a JSON string (or plain text).
    Normalizes into structured JSON:
      { "response": "<assistant text>", "recommendations": [...] }
    """
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        logger.exception("Invalid JSON body received")
        return jsonify({"response": "Invalid JSON body.", "recommendations": []}), 400

    message = payload.get("message") if isinstance(payload, dict) else None
    if message is None:
        return jsonify(
            {"response": "Invalid request — expected JSON with key 'message'.",
                "recommendations": []}
        ), 400

    try:
        # handle_query returns a JSON string or plain text
        raw = handle_query(message)
        parsed = None
        if isinstance(raw, str):
            # try to parse JSON string first
            try:
                parsed = json.loads(raw)
            except Exception:
                # treat as plain text reply
                parsed = {"reply": raw, "recommendations": []}
        elif isinstance(raw, dict):
            parsed = raw
        else:
            parsed = {"reply": str(raw), "recommendations": []}

        # Ensure fields exist and have safe types
        reply_text = parsed.get("reply", "")
        recommendations = parsed.get("recommendations", [])
        if not isinstance(recommendations, list):
            recommendations = []

        return jsonify({"response": reply_text, "recommendations": recommendations})
    except UnboundLocalError as ule:
        # Specific helpful message for the UnboundLocalError you saw earlier
        logger.exception("UnboundLocalError inside handle_query")
        return jsonify(
            {
                "response": "⚠️ Assistant internal error (UnboundLocalError). Check server logs.",
                "recommendations": [],
            }
        ), 500
    except Exception as e:
        logger.exception("Unhandled error while calling handle_query")
        return jsonify(
            {
                "response": f"⚠️ Server error while handling message: {e}",
                "recommendations": [],
            }
        ), 500


# Optional endpoint to fetch quick recommendations for a message directly
@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Returns only recommendations (useful if you want to fetch them separately).
    Body: { "message": "<user message>" }
    """
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"recommendations": []}), 400

    message = payload.get("message") if isinstance(payload, dict) else None
    if not message:
        return jsonify({"recommendations": []}), 400

    try:
        recs = generate_quick_recommendations(message) or []
        if not isinstance(recs, list):
            recs = []
        return jsonify({"recommendations": recs})
    except Exception:
        logger.exception("Error generating recommendations")
        return jsonify({"recommendations": []}), 500


if __name__ == "__main__":
    # Use debug=False for production-like behavior; change to True when debugging locally.
    app.run(host="0.0.0.0", port=5000, debug=False)
