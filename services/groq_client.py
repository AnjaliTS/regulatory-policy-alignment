import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt, retries=3):
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        for attempt in range(retries):
            try:
                response = requests.post(self.url, headers=self.headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]

                else:
                    print(f"⚠️ Attempt {attempt+1} failed:", response.text)

            except Exception as e:
                print(f"❌ Error on attempt {attempt+1}:", str(e))

            # ⏳ backoff (wait before retry)
            time.sleep(2 * (attempt + 1))

        # 🔁 fallback response (VERY IMPORTANT for project)
        return {
            "error": "AI service unavailable",
            "is_fallback": True
        }