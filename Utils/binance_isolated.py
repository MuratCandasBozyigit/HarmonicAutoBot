import requests
import time
import hmac
import hashlib
from Utils.globals import use_testnet, api_key, api_secret  # Globals'tan import ediyoruz

def set_isolated_mode(symbol):
    # Testnet/mainnet kontrolü
    base_url = "https://testnet.binancefuture.com" if use_testnet else "https://fapi.binance.com"
    endpoint = "/fapi/v1/marginType"
    timestamp = int(time.time() * 1000)

    params = f"symbol={symbol}&marginType=ISOLATED&timestamp={timestamp}"
    signature = hmac.new(api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {
        "X-MBX-APIKEY": api_key  # Artık globals'tan alıyoruz
    }

    url = f"{base_url}{endpoint}?{params}&signature={signature}"
    
    try:
        response = requests.post(url, headers=headers)
        print("İzolasyon modu sonucu:", response.status_code, response.text)
        return response.json()
    except Exception as e:
        print("İzolasyon hatası:", str(e))
        return None