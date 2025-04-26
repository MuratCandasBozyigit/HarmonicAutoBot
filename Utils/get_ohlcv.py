import pandas as pd
import Utils.globals as globals
from tkinter import messagebox

def get_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=300):
    try:
        ohlcv = globals.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        df = df.dropna()
        return df if not df.empty else None
    except Exception as e:
        messagebox.showerror("Hata", f"Veri çekilirken hata oluştu:\n{str(e)}")
        return None
