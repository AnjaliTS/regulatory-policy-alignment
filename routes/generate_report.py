from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import re

from services.groq_client import GroqClient
from services.security import sanitize_input, detect_prompt_injection

report_bp = Blueprint("report", __name__)
client = GroqClient()


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()

        # Validate input
        if not data or "input" not in data:
            return jsonify({"error": "Input is required"}), 400

        user_input = data.get("input", "")

        # 🔐 Sanitize input
        clean_input = sanitize_input(user_input)

        # 🔐 Detect prompt injection
        if detect_prompt_injection(clean_input):
            return jsonify({"error": "Prompt injection detected"}), 400

        # 🧠 AI Prompt
        prompt = f"""
        Generate a structured regulatory compliance report based on the policy below.

        Policy:
        {clean_input}

        Return ONLY valid JSON (no markdown, no explanation):
        {{
          "title": "...",
          "summary": "...",
          "overview": "...",
          "key_items": ["...", "..."],
          "recommendations": ["...", "..."]
        }}
        """

        # 🔌 Call AI
        ai_response = client.generate_response(prompt)

        # 🧹 Clean markdown if present
        cleaned = re.sub(r"```json|```", "", ai_response).strip()

        # 🔄 Convert string → JSON
        try:
            report_json = json.loads(cleaned)
        except Exception:
            report_json = {
                "error": "Failed to parse AI response",
                "raw": ai_response
            }

        # ✅ Final response
        return jsonify({
            "report": report_json,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500