import sys
import socket
import threading

# 1. The FUNCTION that does the work
def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        
        if result == 0:
            # 2. Checking which port it is!
            if port == 21:
                service = "FTP"
            elif port == 22:
                service = "SSH"
            elif port == 23:
                service = "Telnet"
            elif port ==  25:
                service = "SMTP"
            elif port == 80:
                service = "HTTP"
            elif port == 443:
                service = "HTTPS"
            elif port == 3389:
                service = "RDP"
            else:
                service = "Unknown"
            
            # Print the port, the services running
            print(f"Port {port} is OPEN ({service})")
        
        s.close()
    except Exception as e:
        pass  

# 3.  INPUT CHECK
if len(sys.argv) != 2:
    print("Usage: python3 port_scanner_v4.py <target>")
    sys.exit()

# 4.  MAIN SETUP
target = socket.gethostbyname(sys.argv[1])
print("-" * 50)
print(f"Scanning target: {target}")
print("-" * 50)

# 5.  THREADED LOOP
threads = []
for port in range(1, 1025):
    # make a new worker for each port
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()  #  start working 

# 6. Wait for everyone to finish
for t in threads:
    t.join()

print("Scan complete!")
