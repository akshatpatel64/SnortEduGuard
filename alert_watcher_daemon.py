import time
import os
import re
import json
from datetime import datetime

ALERT_FILE = "/var/log/snort/alert.fast"
OUTPUT_JSON = "/Users/akshatpatel/snort_logs/parsed_alerts.json"

ALERT_PATTERN = re.compile(
    r'(?P<timestamp>\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d+)\s+\[\*\*\]\s+\[(?P<sid>[\d:]+)\]\s+"(?P<msg>.+?)"\s+\[\*\*\]\s+\[Priority:\s+(?P<priority>\d+)\]\s+\{(?P<protocol>[A-Z]+)\}\s+(?P<src>[^ ]+)\s+->\s+(?P<dst>.+)'
)

def parse_alerts():
    alerts = []
    try:
        with open(ALERT_FILE, "r") as file:
            for line in file:
                match = ALERT_PATTERN.search(line)
                if match:
                    alert = match.groupdict()
                    try:
                        dt = datetime.strptime(alert["timestamp"], "%m/%d-%H:%M:%S.%f")
                        alert["timestamp_iso"] = dt.replace(year=2025).isoformat()
                    except Exception:
                        alert["timestamp_iso"] = alert["timestamp"]
                    alerts.append(alert)

        with open(OUTPUT_JSON, "w") as outfile:
            json.dump(alerts, outfile, indent=4)

        print(f"[+] Parsed {len(alerts)} alerts @ {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"[!] Error: {e}")

def watch_loop(interval=5):
    print("[🔁] Watching Snort alerts. Press Ctrl+C to stop.")
    while True:
        parse_alerts()
        time.sleep(interval)

if __name__ == "__main__":
    watch_loop()

