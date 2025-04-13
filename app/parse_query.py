import spacy
import re
from datetime import datetime, timedelta

nlp = spacy.load("en_core_web_sm")

def parse_user_query(query):
    doc = nlp(query.lower())

    # CATEGORY detection
    category_keywords = {
        "ai": [
            "chatgpt", "bard", "claude", "poe", "perplexity", "you.com", "terp ai",
            "openai", "gemini", "anthropic", "api-iam", "login.microsoftonline.com"
        ],
        "cheating": [
            "chegg", "coursehero", "quizlet", "studocu", "brainly", "slader"
        ],
        "vpn": [
            "vpn", "nordvpn", "protonvpn", "psiphon", "expressvpn", "tunnelbear",
            "windscribe", "hotspotshield", "surfshark"
        ],
        "collab": [
            "discord", "slack", "telegram", "whatsapp", "signal"
        ],
        "c2": [
            "c2", "dns tunneling", "http beacon", "203.0.113.100"
        ],
        "whitelist": [
            "umd.edu", "canvas", "canvas.instructure.com", "zoom.us", "zoom"
        ]
    }

    detected_category = None
    for cat, keywords in category_keywords.items():
        if any(word in query.lower() for word in keywords):
            detected_category = cat
            break

    # TIME RANGE detection (e.g., "last 30 minutes")
    time_match = re.search(r"last\s+(\d+)\s+(minute|hour)", query)
    time_range = None
    if time_match:
        value, unit = int(time_match.group(1)), time_match.group(2)
        if unit == "minute":
            time_range = datetime.now() - timedelta(minutes=value)
        elif unit == "hour":
            time_range = datetime.now() - timedelta(hours=value)

    return {
        "category": detected_category,
        "time_filter": time_range.isoformat() if time_range else None
    }

