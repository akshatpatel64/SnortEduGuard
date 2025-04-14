## About the Project: SnortEduGuard – Student Integrity Surveillance System

As a Teaching Assistant at the University of Maryland, I often oversee lab sessions, in-class quizzes, and exams. Over time, I noticed a recurring issue students frequently attempt to bypass academic integrity policies by using generative AI tools, cheating platforms, or VPNs to evade detection.

While institutions rely on browser lockdown software like LockDown Browser or proctoring tools, these are not foolproof. As someone passionate about cybersecurity, I wanted to design a system that works at the network level, giving instructors real-time visibility into potentially unauthorized activity.

That motivation led to the creation of **SnortEduGuard**, a production-ready academic intrusion detection system (IDS) that detects, logs, filters, and summarizes network traffic during exams or classroom sessions. The goal was to build a system that’s not only technically sound, but also useful in real-world academic settings.

The project is powered by **Snort 3**, a modern packet inspection engine. I wrote custom rules to detect specific categories of traffic that may indicate academic dishonesty or misuse of resources. These included:

- Generative AI tools (e.g., ChatGPT, Bard, Claude, Perplexity)
- Study-help platforms (Chegg, CourseHero, Quizlet)
- VPN tools (NordVPN, ProtonVPN, Psiphon)
- Collaboration platforms (Discord, Slack, WhatsApp)
- Command-and-control (C2) patterns and Nmap port scans

For safe and allowed domains like `umd.edu`, `canvas.instructure.com`, and `zoom.us`, I wrote **whitelist rules** to differentiate authorized traffic from violations.

Snort writes all detected alerts to a log file called `alert.fast`. I developed a Python script (`parse_alerts.py`) that uses regular expressions to extract useful metadata from each alert such as timestamp, IPs, protocol, SID, and priority and then writes that data to a structured JSON file (`parsed_alerts.json`). This JSON powers the real-time dashboard.

The **dashboard** itself is built using **Flask**, **Chart.js**, and **Bootstrap 5**. It:

- Auto-refreshes every 10 seconds
- Color-codes alerts by priority
- Allows instructors to search, filter, and export to CSV or PDF
- Visualizes alert distributions with interactive charts
- Supports instructor login and custom UI branding for Bitcamp 2025 and UMD

To elevate functionality, I implemented a **Smart Search AI Assistant**. This lets instructors use natural language prompts like:

> "Show Chegg activity in the last 30 minutes"

or

> "AI access logs today"

Under the hood, the query is parsed using **spaCy NLP** (`parse_query.py`), categorized and timestamped, and passed to `smart_filter.py`, which filters matching logs. Summaries are generated using a custom summarizer (`summarizer.py`) to output human-readable alerts like:

> “192.168.1.105 attempted to access ChatGPT at 10:42 AM.”

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/c4b2e569-f319-48c4-a9f1-8afa37045b02" width="600" alt="Architecture Diagram">
</p>

---

One of the biggest technical challenges was configuring Snort 3 logging on macOS especially using Lua configs and preserving logs with `tee` without blocking. Designing the parser to safely monitor logs in near real-time also required careful engineering.

The AI integration also took substantial effort - ensuring natural queries mapped accurately to underlying Snort rules and timestamps.

Through this project, I gained hands-on experience in:

- Packet inspection and Snort rule design
- Real-time log parsing and structured data modeling
- AI-enhanced log summarization and dashboard design
- Building usable, security-focused tooling for educators

**SnortEduGuard** is more than just a demo. It's deployable in real classrooms, labs, and test settings. Rather than punish or surveil, it promotes awareness, integrity, and accountability in academic environments using cybersecurity as a foundation.

**Demo and Write-Up**

YouTube Demo (20 minutes): https://youtu.be/F4_onsXjv2s

Medium Technical Breakdown: https://medium.com/@patelaksht24/what-if-your-exam-had-a-firewall-building-snorteduguard-at-bitcamp-2025-ab2a11989283



