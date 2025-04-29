import os
import requests
import time
import hmac
import hashlib
from functools import lru_cache
from dotenv import load_dotenv

# .env dosyasını yükler ve çevre değişkenlerini alır
def load_env():
    load_dotenv(override=True)

def get_api_credentials():
    """API anahtarları ve gizli anahtarları almak için fonksiyon."""
    load_env()  # .env dosyasını her zaman yükleriz
    use_testnet = os.getenv("USE_TESTNET", "True") == "True"
    api_key = os.getenv("TEST_API_KEY") if use_testnet else os.getenv("REAL_API_KEY")
    api_secret = os.getenv("TEST_API_SECRET") if use_testnet else os.getenv("REAL_API_SECRET")
    
    return use_testnet, api_key, api_secret

# API anahtarları ve testnet bilgilerini yükle
use_testnet, api_key, api_secret = get_api_credentials()

session = requests.Session()
session.headers.update({"X-MBX-APIKEY": api_key})
api_secret_bytes = api_secret.encode()

@lru_cache(maxsize=100)
def set_isolated_mode(symbol):
    base_url = "https://testnet.binancefuture.com" if use_testnet else "https://fapi.binance.com"
    endpoint = "/fapi/v1/marginType"
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&marginType=ISOLATED&timestamp={timestamp}"
    signature = hmac.new(api_secret_bytes, params.encode(), hashlib.sha256).hexdigest()
    url = f"{base_url}{endpoint}?{params}&signature={signature}"

    try:
        response = session.post(url)
        data = response.json()
        return response.status_code == 200 or data.get("code") == -4046
    except requests.exceptions.RequestException:
        return False
