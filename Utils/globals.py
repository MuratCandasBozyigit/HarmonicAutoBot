import os
import ccxt
from dotenv import load_dotenv
import time

def load_env():
    import sys
    
    if getattr(sys, 'frozen', False):
        env_path = os.path.join(sys._MEIPASS, ".env")
    else:
        env_path = ".env"
    
    load_dotenv(env_path, override=True)

def save_settings():
    with open(".env", "w") as f:
        f.write(f"USE_TESTNET={use_testnet}\n")
        f.write(f"REAL_API_KEY={api_key}\n")
        f.write(f"REAL_API_SECRET={api_secret}\n")
      #  f.write(f"TEST_API_KEY={api_key}\n")  # Test API Key'i değiştirebilirsiniz.
       # f.write(f"TEST_API_SECRET={api_secret}\n")  # Test API Secret'ı değiştirebilirsiniz.
        f.write(f"USDT_AMOUNT={usdt_amount}\n")
        f.write(f"LEVERAGE={leverage}\n")
        f.write(f"TP_PERCENT={tp_percent}\n")
        f.write(f"SL_PERCENT={sl_percent}\n")
        print("\n--- Ayarlar .env Dosyasına Kaydedildi ---")

def update_globals():
    global tp_percent, sl_percent, usdt_amount, leverage, api_key, api_secret, use_testnet
    
    load_env()

    use_testnet = os.getenv("USE_TESTNET", "True") == "True"

    api_key = os.getenv("TEST_API_KEY") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_KEY")
    api_secret = os.getenv("TEST_API_SECRET") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_SECRET")
    

    usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))  # USDT miktarı
    leverage = int(os.getenv("LEVERAGE", "10"))  # Kaldıraç
    
    tp_percent = float(os.getenv("TP_PERCENT", "0.7"))  # Take Profit yüzdesi
    sl_percent = float(os.getenv("SL_PERCENT", "1.5"))  # Stop Loss yüzdesi



# UI Nesneleri
root = None
chart_frame = None
limit_var = None
symbol_var = None
timeframe_var = None
should_auto_refresh = None
refresh_job = None
_drag_data = {'x': 0, 'y': 0}

# Diğer değişkenler
open_positions = set()
emir_acik = False
short_emir_acik = False
aktif_emir_id = None
last_candle_time = None
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None

tp_percent = 0.7  # Take Profit yüzdesi
sl_percent = 1.5  # Stop Loss yüzdesi

load_env()  # .env dosyasını yükle

api_key = os.getenv("TEST_API_KEY") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_KEY")
api_secret = os.getenv("TEST_API_SECRET") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_SECRET")

use_testnet = os.getenv("USE_TESTNET", "True") == "True"

usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))  # USDT miktarı
leverage = int(os.getenv("LEVERAGE", "10"))  # Kaldıraç

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}  # Futures ticareti yapacak şekilde ayarlandı
})

# Testnet modunu ayarla
exchange.set_sandbox_mode(use_testnet)

