import requests
import time
import hmac
import hashlib
from Utils.globals import use_testnet, api_key, api_secret  # Globals'tan import ediyoruz

def set_isolated_mode(symbol):
    base_url = "https://testnet.binancefuture.com" if use_testnet else "https://fapi.binance.com"
    endpoint = "/fapi/v1/marginType"
    timestamp = int(time.time() * 1000)

    params = f"symbol={symbol}&marginType=ISOLATED&timestamp={timestamp}"
    signature = hmac.new(api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {
        "X-MBX-APIKEY": api_key
    }

    url = f"{base_url}{endpoint}?{params}&signature={signature}"

    try:
        response = requests.post(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            return True  # İzole moda başarıyla geçti
        elif data.get("code") == -4046:
            return True  # Zaten izole, bu da kabul
        else:
            return False  # Diğer tüm durumlar hata sayılır
    except Exception:
        return False
