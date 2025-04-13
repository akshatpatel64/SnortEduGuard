# File: summarizer.py

from datetime import datetime

def summarize_alert(alert):
    # Try to extract what we can
    src_ip = alert.get("src", "unknown")
    dst_ip = alert.get("dst", "unknown")
    timestamp = alert.get("timestamp")
    readable_time = timestamp.strftime("%I:%M %p") if isinstance(timestamp, datetime) else "unknown time"
    
    # Smart category mapping based on SID or message content
    msg = alert.get("msg", "")
    summary = ""

    if "chegg" in msg.lower():
        summary = f"✉ {src_ip} tried to access Chegg at {readable_time}."
    elif "chatgpt" in msg.lower() or "openai" in msg.lower():
        summary = f"✉ {src_ip} attempted to use ChatGPT at {readable_time}."
    elif "vpn" in msg.lower() or any(v in msg.lower() for v in ["nord", "proton", "expressvpn"]):
        summary = f"⚡ {src_ip} may be using a VPN (alert triggered at {readable_time})."
    elif "quizlet" in msg.lower():
        summary = f"✉ Quizlet accessed by {src_ip} around {readable_time}."
    else:
        summary = f"📡 Alert: {msg} from {src_ip} to {dst_ip} at {readable_time}."

    return summary

