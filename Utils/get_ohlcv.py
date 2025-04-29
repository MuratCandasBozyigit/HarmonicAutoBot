import time
import pandas as pd
import Utils.globals as globals
from tkinter import messagebox

_last_fetch_time = 0

def get_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=300, cooldown=1.0):
    global _last_fetch_time
    now = time.time()
    if now - _last_fetch_time < cooldown:
        return None  # Çok sık çağrı, iptal et
    _last_fetch_time = now

    try:
        ohlcv = globals.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv)
        df.dropna(inplace=True)
        df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        return df if not df.empty else None
    except Exception as e:
        if getattr(globals, "debug", False):
            print(f"Veri çekilirken hata oluştu: {str(e)}")
        else:
            messagebox.showerror("Hata", f"Veri çekilirken hata oluştu:\n{str(e)}")
        return None
