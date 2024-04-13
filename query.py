import subprocess

def ping_ip(ip):
    # Ping the IP address with 1 packet and a timeout of 1 second
    result = subprocess.call(['ping', '-n', '1', ip],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             shell=True)
    return result == 0  # Return True if ping was successful, False otherwise

def scan_ips(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))

    current = start[:]
    found_ips = []  # List to store found IP addresses
    while current <= end:
        ip = ".".join(map(str, current))
        print("Scanning IP:", ip)
        if ping_ip(ip):
            print("Found:", ip)
            found_ips.append(ip)  # Add the found IP to the list
            
            # Write the found IP to the file immediately
            with open("found_ips.txt", "a") as file:
                file.write(ip + "\n")
        current[3] += 1
        for i in range(3, 0, -1):
            if current[i] == 256:
                current[i] = 0
                current[i - 1] += 1


if __name__ == "__main__":
    start_ip = "5.62.0.0"
    end_ip = "5.62.255.255"
    scan_ips(start_ip, end_ip)
