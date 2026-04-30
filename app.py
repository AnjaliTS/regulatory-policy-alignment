from flask import Flask

# Import all route blueprints
from routes.policy_describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import report_bp

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Initialize Flask app
app = Flask(__name__)


# 🔐 Rate limiter (30 requests per minute)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)


# 🧩 Register all routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)


# 🏠 Home route
@app.route("/")
def home():
    return {
        "message": "AI Service Running ✅",
        "endpoints": [
            "/describe",
            "/recommend",
            "/generate-report"
        ]
    }


# ❤️ Health check (required for project)
@app.route("/health")
def health():
    return {
        "status": "UP",
        "service": "AI Service",
        "model": "Groq LLaMA"
    }


# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)