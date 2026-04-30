from flask import Blueprint, request, jsonify
from datetime import datetime

from services.groq_client import GroqClient
from services.security import sanitize_input, detect_prompt_injection

# Create Blueprint
describe_bp = Blueprint("describe", __name__)

# Initialize Groq client
client = GroqClient()


@describe_bp.route("/describe", methods=["POST"])
def describe():
    try:
        data = request.get_json()

        # Check if input exists
        if not data or "input" not in data:
            return jsonify({"error": "Input is required"}), 400

        user_input = data.get("input", "")

        # Sanitize input
        clean_input = sanitize_input(user_input)

        # Detect prompt injection
        if detect_prompt_injection(clean_input):
            return jsonify({"error": "Prompt injection detected"}), 400

        # Call AI
        ai_response = client.generate_response(
            f"Explain the following regulatory policy in simple terms:\n{clean_input}"
        )

        # Handle fallback case
        if isinstance(ai_response, dict) and ai_response.get("is_fallback"):
            return jsonify(ai_response), 200

        return jsonify({
            "description": ai_response,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500