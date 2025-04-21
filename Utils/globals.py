import os
from dotenv import load_dotenv
import tkinter as tk

load_dotenv()  # .env dosyasını yükle

symbol_var = None
timeframe_var = None

emir_acik = False
aktif_emir_id = None
last_candle_time = None 
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None

# .env'den ayarları çek
api_key = os.getenv("TEST_API_KEY") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_KEY")
api_secret = os.getenv("TEST_API_SECRET") if os.getenv("USE_TESTNET", "True") == "True" else os.getenv("REAL_API_SECRET")

use_testnet = os.getenv("USE_TESTNET", "True") == "True"
usdt_amount = float(os.getenv("USDT_AMOUNT", "15"))
leverage = int(os.getenv("LEVERAGE", "10"))

