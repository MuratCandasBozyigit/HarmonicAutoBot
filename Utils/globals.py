# globals.py

import os
import ccxt
from dotenv import load_dotenv

# UI Nesneleri
root = None
chart_frame = None
limit_var = None
symbol_var = None
timeframe_var = None
should_auto_refresh = None  # <-- Burayı None bırak

# Diğer değişkenler
emir_acik = False
short_emir_acik=True
aktif_emir_id = None
last_candle_time = None
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None

tp_percent = 0.7   # Take-profit yüzdesi (örneğin %0.5)
sl_percent = 1.5    # Stop-loss yüzdesi (örneğin %0.3)


# API / Binance Ayarları
load_dotenv()
api_key = os.getenv("TEST_API_KEY") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_KEY")
api_secret = os.getenv("TEST_API_SECRET") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_SECRET")
use_testnet = os.getenv("USE_TESTNET", "True") == "True"
usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))
leverage = int(os.getenv("LEVERAGE", "10"))

# Binance bağlantısı
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
exchange.set_sandbox_mode(use_testnet)
