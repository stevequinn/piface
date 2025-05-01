# Interface with pi-hole v5.0+
import os
import requests
import dotenv
import argparse

dotenv.load_dotenv()

# load url from .env
PIHOLE_URL = os.getenv('PIHOLE_URL')

def setup_parser():
    parser = argparse.ArgumentParser(description='Pi-Face Ad Blocker Pi-hole API interface')
    parser.add_argument('--enable', action='store_true', help='Enable Pi-hole blocking')
    parser.add_argument('--disable', action='store_true', help='Disable Pi-hole blocking')
    parser.add_argument('--status', action='store_true', help='Get the status of Pi-hole')
    parser.add_argument('--stats', action='store_true', help='Get all the stats of Pi-hole')

    return parser

def auth_request(url: str):
    """Bascially just bolts the authkey to the url, requests it, and returns the response"""
    API_TOKEN = os.getenv('PIHOLE_TOKEN')
    response = requests.get(
        f"{url}&auth={API_TOKEN}"
    )
    response.raise_for_status()  # Raise an error for bad status codes
    return response

def get_stats():
    response = auth_request(f'{PIHOLE_URL}/admin/api.php?summary')
    return response.json()

def get_status():
    response = get_stats()
    return response['status']

def enable_pihole():
    """
    Enable Pi-hole blocking via API.
    Returns the JSON response from the API.
    """
    try:
        response = auth_request(f"{PIHOLE_URL}/admin/api.php?enable")
        return response.json()
    except requests.RequestException as e:
        print(f"Error enabling Pi-hole: {e}")
        return None

def disable_pihole():
    """
    Disable Pi-hole blocking via API.
    Returns the JSON response from the API.
    """
    try:
        url = f"{PIHOLE_URL}/admin/api.php?disable"
        response = auth_request(url)
        return response.json()
    except requests.RequestException as e:
        print(f"Error disabling Pi-hole: {e}")
        return None

def main():
    parser= setup_parser()
    res = f"{parser.format_help()}\n\nPiFace is {get_status()}\n"
    args = parser.parse_args()

    if args.enable:
        res = enable_pihole()
    elif args.disable:
        res = disable_pihole()
    elif args.stats:
        res = get_stats()
    elif args.status:
        res = get_status()

    print(res)

if __name__ == '__main__':
    main()
