import os
import ccxt
from dotenv import load_dotenv

def load_env():
    load_dotenv()  # .env dosyasını yeniden yükle

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

# API / Binance Ayarları
load_env()  # .env dosyasını yükle

# Testnet mi, gerçek mi kullanacağını belirle
api_key = os.getenv("TEST_API_KEY") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_KEY")
api_secret = os.getenv("TEST_API_SECRET") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_SECRET")

# Testnet kullanma durumu
use_testnet = os.getenv("USE_TESTNET", "True") == "True"

# Kullanıcı tarafından ayarlanan miktar ve kaldıraç
usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))  # USDT miktarı
leverage = int(os.getenv("LEVERAGE", "10"))  # Kaldıraç

# Binance bağlantısı (ccxt kullanarak)
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}  # Futures ticareti yapacak şekilde ayarlandı
})

# Testnet modunu ayarla
exchange.set_sandbox_mode(use_testnet)

