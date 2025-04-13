#!/bin/bash

echo "[*] Cleaning old logs..."
rm -f /var/log/snort/alert.fast
rm -f ~/snort_logs/parsed_alerts.json

echo "[*] Starting Snort fresh..."
sudo bash -c 'snort -c /usr/local/etc/snort/snort.lua -i en0 -A alert_fast | tee /var/log/snort/alert.fast'
