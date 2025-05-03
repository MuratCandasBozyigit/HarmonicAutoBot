import os
import requests
import time
import hmac
import hashlib
from functools import lru_cache
from dotenv import load_dotenv

# .env dosyasını yükle
def load_env():
    load_dotenv(override=True)

# API anahtarlarını al
def get_api_credentials():
    load_env()
    use_testnet = os.getenv("USE_TESTNET", "True") == "True"
    api_key = os.getenv("TEST_API_KEY") if use_testnet else os.getenv("REAL_API_KEY")
    api_secret = os.getenv("TEST_API_SECRET") if use_testnet else os.getenv("REAL_API_SECRET")

    # Anahtarlar kontrol ediliyor
    if not api_key or not api_secret:
        raise RuntimeError("❌ API anahtarları yüklenemedi. .env dosyasını kontrol edin veya eksik değerleri tamamlayın.")

    return use_testnet, api_key, api_secret

# API anahtarlarını al ve oturumu başlat
use_testnet, api_key, api_secret = get_api_credentials()

session = requests.Session()
session.headers.update({"X-MBX-APIKEY": api_key})

# Gizli anahtarı encode et
api_secret_bytes = api_secret.encode()

# Sadece 1 kez ayarlamak için önbellekli margin tipi ayarlayıcı
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

        # 200: başarı, -4046: zaten ISOLATED ise sorun yok
        if response.status_code == 200 or data.get("code") == -4046:
            return True
        else:
            print(f"❌ Margin tipi ayarlanamadı: {data}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ API bağlantı hatası: {e}")
        return False
