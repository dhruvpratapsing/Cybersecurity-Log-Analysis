import re, time, json, os
from collections import defaultdict, deque
import database
import datetime

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DB_PATH = os.path.join(BASE_DIR, "data", "securelog.db")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def tail_f(filename):
    """Simple generator that yields new lines as they are appended to filename."""
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.rstrip('\n')

def extract_ip(match, line):
    # If regex uses named group 'ip', use it; otherwise attempt fallback
    if match and match.groupdict().get("ip"):
        return match.groupdict().get("ip")
    # Fallback: look for an IPv4 in the line
    m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
    return m.group(1) if m else "unknown"

def now_ts():
    return int(time.time())

def main():
    cfg = load_config()
    log_path = os.path.join(BASE_DIR, cfg.get("log_path", "logs/sample.log"))
    if not os.path.exists(log_path):
        print("Log file not found. Creating sample log at", log_path)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        open(log_path, "a").close()

    # Init DB
    database.init_db(DB_PATH)

    # Precompile patterns
    patterns = {}
    for name, info in cfg["patterns"].items():
        patterns[name] = {
            "re": re.compile(info["regex"], re.IGNORECASE),
            "threshold": info.get("threshold", 1),
            "window": info.get("window_seconds", 0),
            "description": info.get("description", "")
        }

    # Sliding windows: dict of deque of timestamps per (pattern_name, ip)
    windows = defaultdict(lambda: deque())

    print("Starting monitor. Watching:", log_path)
    for line in tail_f(log_path):
        ts = now_ts()
        for pname, pinfo in patterns.items():
            m = pinfo["re"].search(line)
            if m:
                ip = extract_ip(m, line)
                key = (pname, ip)
                window = windows[key]
                window.append(ts)
                # prune old timestamps
                if pinfo["window"] > 0:
                    cutoff = ts - pinfo["window"]
                    while window and window[0] < cutoff:
                        window.popleft()

                count = len(window)
                # If threshold met or pattern triggers instantly (window 0 and threshold 1)
                if count >= pinfo["threshold"]:
                    # Insert alert and clear the window for that key to avoid duplicate alerts
                    database.insert_alert(DB_PATH, ts, pname, ip, count, pinfo["description"], line)
                    # Also print to console
                    print(f"[ALERT] {datetime.datetime.fromtimestamp(ts)} - {pname} - {ip} - count={count}")
                    windows[key].clear()

        # Also check blacklisted IPs
        for b_ip in cfg.get("blacklist_ips", []):
            if b_ip in line:
                ts = now_ts()
                database.insert_alert(DB_PATH, ts, "blacklist_ip", b_ip, 1, "Blacklisted IP seen in logs", line)
                print(f"[ALERT] {datetime.datetime.fromtimestamp(ts)} - blacklist_ip - {b_ip}")

if __name__ == "__main__":
    main()
