# mainFrame.py
import ccxt
import pandas as pd
import mplfinance as mpf
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

import İndicators
import Utils
import Utils.globals as globals
import Cmd
import Order
import Chart

def build_gui(root):
    globals.root = root

    exchange = ccxt.binance({
        'apiKey': globals.api_key,
        'secret': globals.api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })
    exchange.set_sandbox_mode(globals.use_testnet)
    globals.exchange = exchange

    root.title("Harmonic Gözlem Paneli - v0.5")
    root.geometry("1280x720")

    # Yeni bir üst çerçeve tanımla
    container_frame = tk.Frame(root)
    container_frame.pack(fill="both", expand=True)

    # Grafik alanı (üstte olacak)
    chart_frame = tk.Frame(container_frame, bg="black")
    chart_frame.grid(row=0, column=0, sticky="nsew")  # Üst
    globals.chart_frame = chart_frame
    globals.should_auto_refresh = tk.BooleanVar(value=True)

    # Kontrol paneli (altta olacak)
    control_frame = tk.Frame(container_frame)
    control_frame.grid(row=1, column=0, pady=5)

    # Satır/kolon oranları
    container_frame.grid_rowconfigure(0, weight=1)   # grafik alanı genişleyebilir
    container_frame.grid_rowconfigure(1, weight=0)   # kontrol sabit
    container_frame.grid_columnconfigure(0, weight=1)

    # Kontrol bileşenleri (aynı şekilde kalabilir)
    globals.limit_var = tk.IntVar(value=100)
    tk.Label(control_frame, text="Bar Sayısı:").grid(row=0, column=5, padx=5)
    tk.Spinbox(control_frame, from_=50, to=1000, increment=50,
               textvariable=globals.limit_var, width=5).grid(row=0, column=6, padx=5)

    tk.Label(control_frame, text="Coin (örn: BTC):").grid(row=0, column=0, padx=5)
    globals.symbol_var = tk.StringVar()
    symbol_entry = tk.Entry(control_frame, textvariable=globals.symbol_var, width=20)
    symbol_entry.grid(row=0, column=1, padx=5)
    symbol_entry.insert(0, "BTC")
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
    globals.timeframe_var = tk.StringVar()
    timeframe_combo = ttk.Combobox(control_frame, textvariable=globals.timeframe_var,
                                   values=["1m", "5m", "15m", "1h", "4h", "1d"])
    timeframe_combo.grid(row=0, column=3, padx=5)
    timeframe_combo.current(3)

    tk.Button(control_frame, text="Veriyi Göster",
              command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)]).grid(row=0, column=4, padx=5)

    tk.Button(control_frame, text="Anlık Long Aç", command=Order.execute_trade).grid(row=0, column=8, padx=5)

    emir_btn = tk.Button(control_frame, text="🟢Long Emir Aç", bg="lightgreen")

    def toggle_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.config(text="🔴Long Emir Arıyor..." if globals.emir_acik else "🟢Long Emir Aç!")
        print("[Emir Kontrol]", "✅Long Emir aranıyor..." if globals.emir_acik else "⛔Long Emir modu kapalı.")

    emir_btn.config(command=toggle_emir)
    emir_btn.grid(row=0, column=7, padx=10)

    # Otomatik grafik güncellemesi başlat
    Chart.auto_refresh_chart()
