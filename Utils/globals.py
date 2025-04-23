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
short_emir_acik = False
aktif_emir_id = None
last_candle_time = None
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None

tp_percent = 0.7  # Take-profit yüzdesi (örneğin %0.5)
sl_percent = 1.5  # Stop-loss yüzdesi (örneğin %0.3)

# API / Binance Ayarları
load_dotenv()

# Gerçek API anahtarlarını kullanıyoruz çünkü USE_TESTNET False
api_key = os.getenv("REAL_API_KEY")  # Gerçek API anahtarı
api_secret = os.getenv("REAL_API_SECRET")  # Gerçek API gizli anahtarı
use_testnet = False  # Gerçek hesap için testnet kullanılmaz
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
