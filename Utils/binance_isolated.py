import requests
import time
import hmac
import hashlib
from functools import lru_cache
from Utils.globals import use_testnet, api_key, api_secret  # Globals'tan import ediyoruz

# Tek bir session objesi ile tekrar bağlantı kurmaktan kaçınıyoruz
session = requests.Session()
session.headers.update({"X-MBX-APIKEY": api_key})

# API secret encode edilmiş hali (her seferinde encode etmemek için)
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

        if response.status_code == 200 or data.get("code") == -4046:
            return True  # Başarılı veya zaten izole
        return False
    except requests.exceptions.RequestException:
        return False
