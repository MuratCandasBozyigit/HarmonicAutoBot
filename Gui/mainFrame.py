import ccxt
import pandas as pd
import mplfinance as mpf
import tkinter as tk
import os
import gc
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta, timezone

import İndicators
import Utils
import Utils.globals as globals
import Cmd
import Order
import Chart


exchange = ccxt.binance({
    'apiKey': globals.api_key,
    'secret': globals.api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
exchange.set_sandbox_mode(globals.use_testnet)

# Ana pencere
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.5")
window.geometry("1280x560")

should_auto_refresh = tk.BooleanVar(value=True)
opened_patterns = set()
last_candle_time = None



# Kontrol paneli
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

limit_var = tk.IntVar(value=100)
tk.Label(control_frame, text="Bar Sayısı:").grid(row=0, column=5, padx=5)
tk.Spinbox(control_frame, from_=50, to=1000, increment=50, textvariable=limit_var, width=5).grid(row=0, column=6, padx=5)

tk.Label(control_frame, text="Coin (örn: BTC veya BTC/USDT):").grid(row=0, column=0, padx=5)
globals.symbol_var = tk.StringVar()
symbol_entry = tk.Entry(control_frame, textvariable=globals.symbol_var, width=20)
symbol_entry.grid(row=0, column=1, padx=5)
symbol_entry.insert(0, "BTC")
symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
globals.timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=globals.timeframe_var, values=["1m", "5m", "15m", "1h", "4h", "1d"])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)

tk.Button(control_frame, text="Veriyi Göster", command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)]).grid(row=0, column=4, padx=5)
tk.Button(control_frame, text="Anlık Long Aç", command=Order.execute_trade).grid(row=0, column=5, padx=5)

emir_btn = tk.Button(control_frame, text="🟢 Emir Aç", bg="lightgreen")
def toggle_emir():
    globals.emir_acik = not globals.emir_acik
    emir_btn.config(text="🔴 Emir Arıyor..." if globals.emir_acik else "🟢 Emir Aç!")
    print("[Emir Kontrol]", "✅ Emir aranıyor..." if globals.emir_acik else "⛔ Emir modu kapalı.")
emir_btn.config(command=toggle_emir)
emir_btn.grid(row=0, column=7, padx=10)

# Grafik alanı
chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=False)

# Başlat
Chart.auto_refresh_chart()
window.mainloop()
