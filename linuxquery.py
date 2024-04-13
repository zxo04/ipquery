import subprocess
import asyncio
import aiohttp
import json
import base64
from opengsq.exceptions import ServerNotFoundException
from opengsq.protocol_base import ProtocolBase
from opengsq.socket_async import SocketAsync

class EOS(ProtocolBase):
    """Epic Online Services (EOS) Protocol"""
    full_name = 'Epic Online Services (EOS) Protocol'

    _api_url = 'https://api.epicgames.dev'

    def __init__(self, host: str, port: int, timeout: float = 5, client_id: str = None, client_secret: str = None, deployment_id: str = None):
        super().__init__(host, port, timeout)

        if client_id is None or client_secret is None or deployment_id is None:
            raise ValueError(
                "client_id, client_secret, and deployment_id must not be None")

        self.client_id = client_id
        self.client_secret = client_secret
        self.deployment_id = deployment_id
        self.access_token = None

    async def _get_access_token(self) -> str:
        url = f'{self._api_url}/auth/v1/oauth/token'
        body = f"grant_type=client_credentials&deployment_id={self.deployment_id}"
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=body, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

        return data["access_token"]

    async def _get_matchmaking(self, data: dict):
        if self.access_token is None:
            self.access_token = await self._get_access_token()
            assert self.access_token is not None, "Failed to get access token"

        url = f"{self._api_url}/matchmaking/v1/{self.deployment_id}/filter"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(data), headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

        return data

    async def get_info(self) -> dict:
        address = await SocketAsync.gethostbyname(self._host)
        address_bound_port = f':{self._port}'

        data = await self._get_matchmaking({
            "criteria": [
                {
                    "key": "attributes.ADDRESS_s",
                    "op": "EQUAL",
                    "value": address
                },
                {
                    "key": "attributes.ADDRESSBOUND_s",
                    "op": "CONTAINS",
                    "value": address_bound_port
                },
            ]
        })

        if data["count"] <= 0:
            raise ServerNotFoundException()

        return data['sessions'][0]




import asyncio


async def check_ports_for_ip(ip, ports, client_id, client_secret, deployment_id):
    # Open the file in append mode
    with open("validipport.txt", "a") as file:
        # Loop through the specified ports
        for port in ports:
            try:
                # Initialize EOS instance for each port
                eos = EOS(host=ip, port=port, timeout=5.0, client_id=client_id,
                          client_secret=client_secret, deployment_id=deployment_id)

                # Get info for the EOS instance
                info = await eos.get_info()

                # Print info if obtained successfully
                print(f"Port {port} is valid for IP {ip}: {info}")

                # Write IP and port to the file
                file.write(f"{ip}:{port}\n")

            except Exception as e:
                # Print error if failed to get info
                print(f"Error for port {port} and IP {ip}: {e}")

async def check_ports_for_all_ips(filename, ports, client_id, client_secret, deployment_id):
    # Read IP addresses from the file
    with open(filename, "r") as ip_file:
        ips = ip_file.readlines()
        ips = [ip.strip() for ip in ips]  # Remove newline characters and whitespace

    # Loop through the IP addresses
    for ip in ips:
        await check_ports_for_ip(ip, ports, client_id, client_secret, deployment_id)

# Define the list of specific ports
PORTS = [7777, 7779, 7787, 7791, 7785, 7783, 7781, ]  # Add your desired ports here

# Define your EOS credentials
client_id = 'xyza7891muomRmynIIHaJB9COBKkwj6n'
client_secret = 'PP5UGxysEieNfSrEicaD1N2Bb3TdXuD7xHYcsdUHZ7s'
deployment_id = 'ad9a8feffb3b4b2ca315546f038c3ae2'

# Define your IP address
filename = "ips.txt"

asyncio.run(check_ports_for_all_ips(filename, PORTS, client_id, client_secret, deployment_id))


