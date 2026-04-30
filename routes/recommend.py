from flask import Blueprint, request, jsonify
from datetime import datetime

from services.groq_client import GroqClient
from services.security import sanitize_input, detect_prompt_injection

recommend_bp = Blueprint("recommend", __name__)
client = GroqClient()


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()

        if not data or "input" not in data:
            return jsonify({"error": "Input is required"}), 400

        user_input = data.get("input", "")

        # sanitize
        clean_input = sanitize_input(user_input)

        # detect injection
        if detect_prompt_injection(clean_input):
            return jsonify({"error": "Prompt injection detected"}), 400

        # AI call
        prompt = f"""
        Based on the following policy, give 3 actionable recommendations.

        Policy:
        {clean_input}

        Format:
        [
          {{
            "action_type": "...",
            "description": "...",
            "priority": "High/Medium/Low"
          }}
        ]
        """

        ai_response = client.generate_response(prompt)

        return jsonify({
            "recommendations": ai_response,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500