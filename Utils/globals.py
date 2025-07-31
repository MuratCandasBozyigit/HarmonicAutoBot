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
        f.write(f"USDT_AMOUNT={usdt_amount}\n")
        f.write(f"LEVERAGE={leverage}\n")
        f.write(f"TP_PERCENT={tp_percent}\n")
        f.write(f"SL_PERCENT={sl_percent}\n")
        f.write(f"EXCHANGE={exchange_name}\n")
        print("\n--- Ayarlar .env Dosyasına Kaydedildi ---")


def update_globals():
    global tp_percent, sl_percent, usdt_amount, leverage, api_key, api_secret, use_testnet, exchange, exchange_name

    load_env()

    use_testnet = os.getenv("USE_TESTNET", "False") == "True"
    api_key = os.getenv("TEST_API_KEY") if use_testnet else os.getenv("REAL_API_KEY")
    api_secret = os.getenv("TEST_API_SECRET") if use_testnet else os.getenv("REAL_API_SECRET")
    exchange_name = os.getenv("EXCHANGE", "Binance").strip().lower()

    usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))
    leverage = int(os.getenv("LEVERAGE", "10"))
    tp_percent = float(os.getenv("TP_PERCENT", "0.7"))
    sl_percent = float(os.getenv("SL_PERCENT", "1.5"))

    # Exchange konfigürasyonu
    exchange_config = {
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    }

    # Desteklenen exchange'ler
    exchanges = {
        'binance': ccxt.binance,
        'bybit': ccxt.bybit,
        'mexc': ccxt.mexc,
        'bitget': ccxt.bitget,
        'okx': ccxt.okx,
        'gate.io': ccxt.gateio,
        'kucoin': ccxt.kucoin
    }

    if exchange_name not in exchanges:
        raise ValueError(f"Desteklenmeyen borsa: {exchange_name}")

    exchange = exchanges[exchange_name](exchange_config)
    exchange.set_sandbox_mode(use_testnet)

    # Exchange'e özel ayarlar
    if exchange_name == 'bitget':
        exchange.options['defaultSubType'] = 'linear'
    elif exchange_name == 'kucoin':
        exchange.load_markets()


# UI ve Diğer Global Değişkenler
root = None
chart_frame = None
limit_var = None
symbol_var = None
timeframe_var = None
should_auto_refresh = None
refresh_job = None
_drag_data = {'x': 0, 'y': 0}

# Trade Değişkenleri
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

# Varsayılan Ayarlar
tp_percent = 0.7
sl_percent = 1.5

# İlk Yükleme
load_env()
update_globals()  # Exchange'i ve tüm ayarları yükle