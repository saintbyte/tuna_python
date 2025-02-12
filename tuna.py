import subprocess
from os import getenv
import os
import time


def get_tuna_api_key() -> str:
    return getenv("TUNA_API_KEY")


def get_tuna_api_endpoint() -> str:
    return 'https://my.tuna.am/v1/tunnels'


def get_port() -> int:
    """Полуить порт для запуска локального сервера."""
    return int(getenv("SERVER_PORT"))


def kill_tuna():
    os.system("killall tuna")


def run_tuna():
    _ = subprocess.Popen(["tuna", "http", str(get_port())])

def export_env_value(env_value_name: str , value: str):
    os.environ[env_value_name] = value
    os.system(" ".join(["export", f"{env_value_name}={value}"]))

def get_tuna_host_httpx():
    import httpx
    from httpx_auth import HeaderApiKey
    client = httpx.Client()
    headers = {
        'Accept': 'application/json',
    }
    client = httpx.Client()
    headers = {
        'Accept': 'application/json',
    }
    response = client.get(
        get_tuna_api_endpoint(),
        headers=headers,
        auth=HeaderApiKey(f"Bearer {get_tuna_api_key()}", "Authentication")
    )
    data = response.json()
    return data[0]["public_url"]


def get_tuna_host():
    import urllib3
    http = urllib3.PoolManager()
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {get_tuna_api_key()}"
    }
    response = http.request(
        'GET',
        get_tuna_api_endpoint(),
        headers=headers
    )
    data = response.json()
    return data[0]["public_url"]


if __name__ == "__main__":
    kill_tuna()
    time.sleep(2)
    run_tuna()
    time.sleep(2)
    public_url = get_tuna_host()
    export_env_value("APP_BASE_URL", f'"{public_url}"')
    export_env_value("SERVER_URL", f'"{public_url}"')
    print(public_url)
