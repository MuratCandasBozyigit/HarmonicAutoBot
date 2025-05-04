import os
from unittest import skip
import requests
import time
import hmac
import hashlib
from functools import lru_cache
from dotenv import load_dotenv

# -------------------- ENV DOSYASINI YÜKLE --------------------
def load_env():
    import sys

    # PyInstaller ile paketlendiğinde farklı yol gerekir
    if getattr(sys, 'frozen', False):
        env_path = os.path.join(sys._MEIPASS, ".env")
    else:
        env_path = ".env"

    load_dotenv(env_path, override=True)


# -------------------- API BİLGİLERİNİ YÜKLE --------------------
def get_api_credentials():
    load_env()

    use_testnet = os.getenv("USE_TESTNET", "True") == "True"
    api_key = os.getenv("TEST_API_KEY") if use_testnet else os.getenv("REAL_API_KEY")
    api_secret = os.getenv("TEST_API_SECRET") if use_testnet else os.getenv("REAL_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("❌ API anahtarları yüklenemedi. .env dosyasını kontrol edin.")

    return use_testnet, api_key, api_secret


# -------------------- API OTURUMU OLUŞTUR --------------------
use_testnet, api_key, api_secret = get_api_credentials()

session = requests.Session()
session.headers.update({"X-MBX-APIKEY": api_key})
api_secret_bytes = api_secret.encode()

# -------------------- MARGIN TİPİNİ ISOLATED YAP --------------------
@lru_cache(maxsize=100)
def set_isolated_mode(symbol: str) -> bool:
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
            #print(f"✅ {symbol} için ISOLATED margin tipi başarıyla ayarlandı.")
            return True
        else:
            #print(f"❌ Margin tipi ayarlanamadı: {data}")
            return False

    except requests.exceptions.RequestException as e:
        #print(f"❌ API bağlantı hatası: {e}")
        return False

