import httpx as rx
import argparse
import os
import sys
import json
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

ENV_KEY = os.environ.get('NETBOX_QUERY_KEY')

KEY = ENV_KEY if ENV_KEY else 'bBwJHwNj02E0MW9yBYkuEYN9dVkHT25KKYEsXu3mwrQ='

fernet = Fernet(KEY.encode())

config_path = os.path.expanduser("~")

Path(config_path).mkdir(parents=True, exist_ok=True)

config_fname = ".netbox_query_config.encrypted"
config_fpath = os.path.join(config_path, config_fname)

class NetBoxRX:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            }

    def get_devices(self, params=None):
        """Fetches devices from NetBox with optional query parameters."""
        response = rx.get(
            f"{self.base_url}/api/dcim/devices/",
            params=params,
            headers=self.headers,
            verify=False,
        )
        try:
            response.raise_for_status()
            return response.json()
        except:
            return {'error': 'Failed to fetch devices', 'status_code': response.status_code}

def load_config():
    try:
        with open(config_fpath, 'rb') as file:
            encrypted_data = file.read()
        data = fernet.decrypt(encrypted_data)
        return json.loads(data)
    except FileNotFoundError:
        return {}
    except InvalidToken:
        return {}

def save_config(config_d):
    """Saves configuration to a JSON file."""
    data = json.dumps(config_d).encode()
    encrypted_data = fernet.encrypt(data)
    with open(config_fpath, 'wb') as file:
        file.write(encrypted_data)
    return

def main():

    parser = argparse.ArgumentParser(description='A CLI client for querying NetBox devices')

    parser.add_argument('--base-url', type=str, help='Base URL of the NetBox instance')
    parser.add_argument('--token', type=str, help='API token for NetBox')

    parser.add_argument('--params', nargs='*', help='Query parameters for device search e.g., q=Server1 status=active')

    args = parser.parse_args()

    user_config = {"base_url": args.base_url, "token": args.token}

    config0 = load_config()

    configF = {}

    for k, v in user_config.items():
        if v:
            configF[k] = v
        else:
            configF[k] = config0.get(k)

        if not configF.get(k):
            raise Exception(f"Missing {k.upper()}")



    netbox_rx = NetBoxRX(base_url=configF['base_url'], token=configF['token'])

    query_params = {}
    if args.params:
        for param in args.params:
            key, value = param.split('=')
            if value.startswith('[') and value.endswith(']'):
                value = value.strip('[]')
                value = [v.strip() for v in value.split(',')]
            query_params[key] = value

    default_limit = 9999
    limit = query_params.setdefault('limit', default_limit)

    r_d = netbox_rx.get_devices(params=query_params)
    devices_li = r_d.get('results', [])
    if 'error' in r_d:
        print(f"Error: {r_d['error']} (Status code: {r_d['status_code']})")
        sys.exit(1)

    for device_d in devices_li:
        print(device_d.get('name', None))

    if any([config0.get(k) != v for k, v in configF.items()]):
        save_config(configF)

if __name__ == '__main__':
    main()
