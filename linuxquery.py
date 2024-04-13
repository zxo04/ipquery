import subprocess

def scan_ips(start_ip, end_ip):
    cmd = ['nmap', '-n', '-sn', f'{start_ip}-{end_ip}']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    if result.returncode == 0:
        # Parsing the output of nmap to extract the live hosts
        live_hosts = []
        for line in result.stdout.split('\n'):
            if 'Nmap scan report for' in line:
                host = line.split()[-1]
                live_hosts.append(host)
                # Write live host to file immediately
                with open("found_ips.txt", "a") as file:
                    file.write(host + "\n")
    else:
        print("Error occurred while scanning IP range.")

if __name__ == "__main__":
    start_ip = "5.62.0.0"
    end_ip = "5.62.255.255"
    scan_ips(start_ip, end_ip)
