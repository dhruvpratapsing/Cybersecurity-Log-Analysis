import time, random, os
log_path = os.path.join(os.path.dirname(__file__), "logs", "sample.log")

def append(line):
    with open(log_path, "a") as f:
        f.write(line + "\n")

def simulate_bruteforce(ip="192.168.1.100", attempts=6, delay=0.5):
    for i in range(attempts):
        append(f"Failed password for invalid user root from {ip} port 22 ssh2")
        time.sleep(delay)

def simulate_sql_injection(ip="203.0.113.5"):
    append(f"GET /vulnerable.php?id=1 OR 1=1 -- from {ip} - -")

def simulate_port_scan(ip="198.51.100.7", attempts=4):
    for i in range(attempts):
        append(f"{ip} - - [Scan] SYN Packet detected")
        time.sleep(0.3)

if __name__ == '__main__':
    # Run a demo sequence
    print("Appending simulated malicious lines to logs/sample.log")
    simulate_bruteforce()
    time.sleep(1)
    simulate_sql_injection()
    time.sleep(1)
    simulate_port_scan()
    print("Done. Check monitor.py output or open the dashboard at http://localhost:5000")
