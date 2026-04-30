import re

def sanitize_input(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove scripts or suspicious patterns
    text = re.sub(r'(script|alert|onerror|onload)', '', text, flags=re.IGNORECASE)

    return text.strip()

def detect_prompt_injection(text):
    suspicious_patterns = [
        "ignore previous instructions",
        "disregard system prompt",
        "reveal system prompt",
        "bypass security",
        "act as admin",
        "give me secrets"
    ]

    text_lower = text.lower()

    for pattern in suspicious_patterns:
        if pattern in text_lower:
            return True

    return False