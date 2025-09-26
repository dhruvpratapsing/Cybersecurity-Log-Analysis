# SecureLog Analyzer

**SecureLog Analyzer** is a simple internship-level cybersecurity project that demonstrates real-time log monitoring, pattern-based threat detection, alert storage, and a web dashboard for viewing alerts. It's designed to be easy to run locally and explainable in interviews.

---
## Project Structure
```
SecureLogAnalyzer/
│
├── app.py                # Flask web dashboard to view alerts
├── monitor.py            # Log monitoring and detection script (run in separate terminal)
├── database.py           # SQLite DB setup and helper functions
├── generate_attacks.py   # Demo script that appends "attack" lines to the sample log
├── config.json           # Config file (patterns, thresholds, email settings)
├── requirements.txt      # Python dependencies
├── README.md             # This file (detailed explanation below)
├── data/
│   └── securelog.db      # (created at runtime)
├── templates/
│   └── index.html        # Web dashboard template
└── logs/
    └── sample.log        # Sample system log (used for demo)
```

---
## Quick Start (run locally)

1. Create a Python virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Initialize the database (optional: database will auto-init on first run):
```bash
python3 database.py
```

3. Start the monitor (in one terminal). This watches `logs/sample.log`:
```bash
python3 monitor.py
```

4. Start the web dashboard (in another terminal):
```bash
python3 app.py
```

5. (Optional) Simulate malicious activity for demo:
```bash
python3 generate_attacks.py
```

6. Open your browser to `http://localhost:5000` to see alerts.

---
## How the detection works (plain explanation you can use in interviews)

1. **Log Input**: The monitor script tails a log file (by default `logs/sample.log`) and reads new lines as they are appended.
2. **Pattern Matching**: Each new log line is compared against several regex patterns defined in `config.json`. Patterns include things like:
   - Repeated failed login attempts (Brute force)
   - SQL injection signatures like `' OR 1=1`, `UNION SELECT`, or inline SQL comments/terminators
   - Port scan markers or repeated connection attempts
3. **Aggregation & Thresholds**: For events that need aggregation (e.g., failed login attempts from the same IP), the monitor keeps a small in-memory sliding window of timestamps and counts occurrences within a configurable time window. When a configured threshold is exceeded (for example, 5 failed attempts within 60 seconds), an **alert** is raised.
4. **Alert Storage**: Alerts get stored in a SQLite database (`data/securelog.db`) along with metadata: timestamp, event type, IP, count, sample log line, and a short description.
5. **Dashboard**: The Flask app reads alerts from the DB and displays them in a simple table. This helps visualize and review incidents quickly.
6. **Email Alerting (Configurable)**: The code contains a placeholder for sending email alerts via SMTP. It's disabled by default and must be configured before use.

---
## Files of interest (explainable snippets)
- **monitor.py**: The core logic; loads `config.json`, tails the log, matches patterns, maintains counters, and inserts alerts.
- **database.py**: Simple wrapper around SQLite with functions: `init_db()`, `insert_alert(...)`, and `get_alerts(...)`.
- **app.py**: Minimal Flask application that serves `templates/index.html` and shows alerts.
- **generate_attacks.py**: A helper that appends crafted lines to `logs/sample.log` so you can demo alerts without real logs.
- **config.json**: Where detection rules and thresholds live. To customize detection behavior, edit this file.

---
## How to explain the project's strengths to recruiters/interviewers
- Demonstrates knowledge of **monitoring**, **pattern matching (regex)**, **stateful detection logic**, and **alerting**.
- Shows practical experience with **Python**, **SQLite**, and **Flask** — common tools in many SOC and security engineering roles.
- The code is designed to be modular: rules (patterns) are configurable and the storage layer is separated — good software engineering practice.
- Easy to expand: add threat-intel feeds, enrich alerts with geo-IP, push alerts to Slack/Teams, or containerize.

---
## Next steps / extensions (ideas to impress)
- Integrate a free **Threat Intelligence** feed to automatically populate the blacklist.
- Add **GeoIP** enrichment using an IP lookup library.
- Visualizations: charts showing attack trends over time.
- Deploy on a small VM or containerize using Docker for demo deployment.

---
## Contact / Attribution
Made for learning & demo purposes. No production guarantees — only a teaching tool.
