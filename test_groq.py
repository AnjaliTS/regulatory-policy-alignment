import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-versatile",   # ✅ correct model
    "messages": [
        {"role": "user", "content": "Explain AI in one line"}
    ],
    "temperature": 0.7
}

try:
    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)   # 👈 IMPORTANT for debugging

    response.raise_for_status()

    result = response.json()
    print("\n✅ API Working!")
    print(result["choices"][0]["message"]["content"])

except Exception as e:
    print("\n❌ Error:", str(e))