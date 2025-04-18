# binance_isolated.py

import requests
import time
import hmac
import hashlib

def set_isolated_mode(api_key, api_secret, symbol):
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v1/marginType"
    timestamp = int(time.time() * 1000)

    params = f"symbol={symbol}&marginType=ISOLATED&timestamp={timestamp}"
    signature = hmac.new(api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {
        "X-MBX-APIKEY": '991acee08da1311f39d71c52f7d8a12179e1a551096d7047573ed80d8271a8b3'
    }

    url = f"{base_url}{endpoint}?{params}&signature={signature}"
    response = requests.post(url, headers=headers)

    print("İzolasyon modu sonucu:", response.status_code, response.text)
