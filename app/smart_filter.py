# File: smart_filter.py

import re
from datetime import datetime
from parse_query import parse_user_query

# Update with your actual alert log file
ALERT_FILE = "/var/log/snort/alert.fast"

# Category keyword mapping for matching alert lines
CATEGORY_KEYWORDS = {
    "ai": ["chatgpt", "openai", "bard", "claude", "poe", "perplexity", "you.com"],
    "vpn": ["vpn", "nord", "protonvpn", "psiphon", "expressvpn", "surfshark"],
    "cheating": ["chegg", "coursehero", "quizlet", "studocu", "brainly", "slader"]
}

# Format example: '04/12-13:23:56.799105'
def parse_alert_line(line):
    alert_pattern = re.compile(r"(\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d{6}).*?\[\*\*\] (.*?) \[\*\*\].*?\{(\w+)\} (.*?) -> (.*?)$")
    match = alert_pattern.search(line)
    if not match:
        return None

    time_str, msg, proto, src, dst = match.groups()
    try:
        ts = datetime.strptime(time_str, "%m/%d-%H:%M:%S.%f")
        ts = ts.replace(year=datetime.now().year)
    except:
        return None

    return {
        "timestamp": ts,
        "timestamp_iso": ts.isoformat(),
        "msg": msg,
        "protocol": proto,
        "src": src,
        "dst": dst
    }

def filter_alerts(user_query):
    parsed = parse_user_query(user_query)
    matched_alerts = []

    with open(ALERT_FILE, 'r') as f:
        for line in f:
            alert = parse_alert_line(line.strip())
            if not alert:
                continue

            # Filter by category keywords
            if parsed['category']:
                keywords = CATEGORY_KEYWORDS.get(parsed['category'], [])
                if not any(kw in alert['msg'].lower() for kw in keywords):
                    continue

            # Filter by time
            if parsed['time_filter']:
                ts_filter = datetime.fromisoformat(parsed['time_filter'])
                if alert['timestamp'] < ts_filter:
                    continue

            matched_alerts.append(alert)

    return matched_alerts

