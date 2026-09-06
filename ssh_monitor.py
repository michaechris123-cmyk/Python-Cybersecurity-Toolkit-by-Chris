import re
import time
from collections import defaultdict

# Path to your SSH log file on Kali
log_file = "/var/log/auth.log" 

# Track failed attempts per IP
failed_attempts = defaultdict(int)
THRESHOLD = 3  # Alert if more than 3 attempts

def monitor_log(file_path):
    print(f"[*] Monitoring {file_path} for brute-force attempts...")
    print("[*] Press CTRL+C to stop monitoring.\n")
    
    # This regex looks for "Failed password" lines and captures the IP
    pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")

    # Open the file and move to the end to read new lines
    with open(file_path, "r") as f:
        f.seek(0, 2) 
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5) # Wait a bit for new logs
                continue
            
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                failed_attempts[ip] += 1
                
                # Alert if the IP hit the threshold
                if failed_attempts[ip] == THRESHOLD:
                    print(f"[!!!] ALERT: Potential SSH Brute-force detected from {ip}!")
                    print(f"      Blocking {ip} using iptables... (simulated)")
                elif failed_attempts[ip] > THRESHOLD:
                    print(f"[!] More attempts from {ip} ({failed_attempts[ip]} total)")

if __name__ == "__main__":
    monitor_log(log_file)
