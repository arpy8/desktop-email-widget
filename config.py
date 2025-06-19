import os
import json


def load_config():
    """Load configuration from user_config.json or fallback to .env"""
    config = {}
    
    if os.path.exists("user_config.json"):
        try:
            with open("user_config.json", "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading user_config.json: {e}")
    
    return config

def has_config():
    """Check if configuration exists"""
    return os.path.exists("user_config.json")


_config = load_config()

USER_EMAIL = _config.get("USER_EMAIL")
USER_PASSWORD = _config.get("USER_PASSWORD")
GEMINI_API_KEY = _config.get("GEMINI_API_KEY")

LLM_INSTRUCTIONS = """
Analyze this email and provide:
1. A brief summary of the important parts (max 100 words)
2. Priority level (high/medium/low) based on urgency, deadlines, opportunities, or importance

Email Subject: {email_subject}
Email From: {email_from}
Email Body: {email_body}
Email Date: {email_date}

Respond with JSON only:
{{
    "summary": "brief summary here",
    "priority": "high/medium/low",
    "date": "date and time in IST format (e.g., 'Thu, 19 Jun 2025 14:15:23' (the time should be in IST))"
}}
"""

COLOR_MAP = {
    'high': 'red',
    'medium': 'yellow',
    'low': 'green',
    'default': 'white',
    'zs': '#ed7b08'
}