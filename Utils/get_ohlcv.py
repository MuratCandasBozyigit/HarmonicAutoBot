import Utils.globals as globals
import ccxt
import pandas as pd
from tkinter import ttk, messagebox
exchange = ccxt.binance({
    'apiKey':'991acee08da1311f39d71c52f7d8a12179e1a551096d7047573ed80d8271a8b3',
    'secret':'4a1bd0764cd29d8517f19b95a13650fe608dd95224b7adaf9cd387a0540ad5fb',
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
exchange.set_sandbox_mode(True) 


def get_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=300):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
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
