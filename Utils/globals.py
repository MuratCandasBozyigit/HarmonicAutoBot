import os
import ccxt
from dotenv import load_dotenv

def load_env():
    if getattr(os, 'frozen', False):
        env_path = os.path.join(os._MEIPASS, ".env")
    else:
        env_path = ".env"
    load_dotenv(env_path, override=True)

def update_globals():
    global tp_percent, sl_percent, usdt_amount, leverage
    global api_key, api_secret, use_testnet
    global exchange_name, exchange
    global root, chart_frame, limit_var, symbol_var, timeframe_var
    global should_auto_refresh, refresh_job, _drag_data
    global open_positions, emir_acik, short_emir_acik, aktif_emir_id
    global last_candle_time, df, canvas, fig, ax, symbol, timeframe

    load_env()

    # ENV AYARLARI
    use_testnet = os.getenv("USE_TESTNET", "True") == "True"

    if use_testnet:
        api_key = os.getenv("TEST_API_KEY", "")
        api_secret = os.getenv("TEST_API_SECRET", "")
    else:
        api_key = os.getenv("REAL_API_KEY", "")
        api_secret = os.getenv("REAL_API_SECRET", "")

    usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))
    leverage = int(os.getenv("LEVERAGE", "10"))
    tp_percent = float(os.getenv("TP_PERCENT", "0.7"))
    sl_percent = float(os.getenv("SL_PERCENT", "1.5"))

    # EXCHANGE SEÇİMİ
    exchange_name = os.getenv("EXCHANGE", "Binance").lower()
    exchange_class = getattr(ccxt, exchange_name, None)
    if exchange_class is None:
        raise ValueError(f"❌ Desteklenmeyen borsa: {exchange_name}")

    exchange = exchange_class({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })

    if hasattr(exchange, 'set_sandbox_mode'):
        exchange.set_sandbox_mode(use_testnet)

# UI NESNELERİ
root = None
chart_frame = None
limit_var = None
symbol_var = None
timeframe_var = None
should_auto_refresh = None
refresh_job = None
_drag_data = {'x': 0, 'y': 0}

# TRADING DEĞİŞKENLERİ
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

# VARSAYILAN DEĞERLER
tp_percent = 0.7
sl_percent = 1.5

# ENV YÜKLEME VE EXCHANGE OLUŞTURMA
update_globals()
