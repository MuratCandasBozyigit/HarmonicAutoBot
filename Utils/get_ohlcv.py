import pandas as pd
import Utils.globals as globals
from tkinter import messagebox

def get_ohlcv(symbol="BTC/USDT", timeframe="15m", limit=300):
    try:
        ohlcv = globals.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        df = df.dropna()
        if df.empty or len(df) < 100:
            print(f"[get_ohlcv] Veri yetersiz: {len(df)} bar")
            return None
        return df
    except Exception as e:
        messagebox.showerror("Hata", f"Veri çekilirken hata oluştu:\n{str(e)}")
        print(f"[get_ohlcv] {type(e).__name__}: {e}")
        return None
