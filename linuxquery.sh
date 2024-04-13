#!/bin/bash

# Define the range of IP addresses to ping
start_ip="5.62.113.0"
end_ip="5.62.114.0"

# Loop through the IP addresses in the range
for (( i=1; i<=10; i++ )); do
    ip="$start_ip.$i"
    echo "Pinging $ip..."
    # Ping the IP address once and suppress output
    ping -c 1 "$ip" > /dev/null 2>&1
    # Check the exit status of the ping command
    if [ $? -eq 0 ]; then
        echo "Packet received from $ip"
    else
        echo "No response from $ip"
    fi
done
