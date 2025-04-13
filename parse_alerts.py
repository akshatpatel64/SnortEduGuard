import re
import json
from datetime import datetime

ALERT_FILE = "/var/log/snort/alert.fast"
OUTPUT_JSON = "/Users/akshatpatel/snort_logs/parsed_alerts.json"

# This regex makes priority optional (some alerts don't have it)
ALERT_PATTERN = re.compile(
    r'(?P<timestamp>\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d+)\s+\[\*\*\]\s+\[(?P<sid>[\d:]+)\]\s+"(?P<msg>.+?)"\s+\[\*\*\](?:\s+\[Priority:\s+(?P<priority>\d+)\])?\s+\{(?P<protocol>[A-Z]+)\}\s+(?P<src>[^ ]+)\s+->\s+(?P<dst>.+)'
)

alerts = []

with open(ALERT_FILE, "r") as file:
    for line in file:
        match = ALERT_PATTERN.search(line)
        if match:
            alert = match.groupdict()

            # Convert timestamp
            try:
                dt = datetime.strptime(alert["timestamp"], "%m/%d-%H:%M:%S.%f")
                alert["timestamp_iso"] = dt.replace(year=2025).isoformat()
            except Exception:
                alert["timestamp_iso"] = alert["timestamp"]

            # Add tag for visual filtering
            alert["tag"] = "unclassified" if "[UNCLASSIFIED]" in alert.get("msg", "") else "classified"

            # Handle priority as integer
            try:
                alert["priority"] = int(alert["priority"])
            except (ValueError, TypeError):
                alert["priority"] = 3 if alert["tag"] == "unclassified" else 2

            alerts.append(alert)

# Save parsed alerts to JSON
with open(OUTPUT_JSON, "w") as out:
    json.dump(alerts, out, indent=4)

print(f"[+] Parsed {len(alerts)} alerts. Output saved to:\n{OUTPUT_JSON}")
