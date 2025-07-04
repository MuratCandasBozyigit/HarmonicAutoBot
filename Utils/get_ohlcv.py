import time
import pandas as pd
import Utils.globals as globals
import customtkinter as ctk

_last_fetch_time = 0

def show_error(title, message):
    error_window = ctk.CTkToplevel()
    error_window.title(title)
    error_window.geometry("400x200")
    error_window.resizable(False, False)
    error_window.grab_set()

    label = ctk.CTkLabel(error_window, text=message, wraplength=350, justify="left", font=ctk.CTkFont(size=14))
    label.pack(padx=20, pady=40)

    button = ctk.CTkButton(error_window, text="Tamam", command=error_window.destroy)
    button.pack(pady=10)

def get_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=300, cooldown=1.0):
    global _last_fetch_time
    now = time.time()
    if now - _last_fetch_time < cooldown:
        return None
    _last_fetch_time = now

    try:
        ohlcv = globals.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df.dropna(inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        return df if not df.empty else None
    except Exception as e:
        show_error("Hata", f"Veri alınamadı:\n{str(e)}")
        return None
