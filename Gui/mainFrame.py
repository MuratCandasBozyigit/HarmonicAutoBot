import ccxt
import pandas as pd
import mplfinance as mpf
import customtkinter as ctk
from tkinter import ttk
import customtkinter as ctk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Dahili modüller
import Indicators
import Utils
import Utils.globals as globals
import Order
import Chart
from Utils.save_settings import open_settings_window  # Ayarlar butonu için import

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "dark" else "dark")

def build_gui(root):
    globals.root = root
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("light")

    exchange = ccxt.binance({
        'apiKey': globals.api_key,
        'secret': globals.api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })
    exchange.set_sandbox_mode(globals.use_testnet)
    globals.exchange = exchange

    root.title("Auto Trade Murtaza")
    root.geometry("1280x720")

    container_frame = ctk.CTkFrame(root)
    container_frame.pack(fill="both", expand=True)

    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.grid(row=0, column=0, sticky="nsew")
    globals.chart_frame = chart_frame

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    control_frame = ctk.CTkFrame(container_frame)
    control_frame.grid(row=1, column=0, pady=8, padx=5)

    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(0, weight=1)

    # SATIR 1
    ctk.CTkLabel(control_frame, text="Coin (BTC vs):").grid(row=0, column=0, padx=5, pady=2)
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(control_frame, textvariable=globals.symbol_var, width=120)
    symbol_entry.grid(row=0, column=1, padx=5)
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    ctk.CTkLabel(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframe_combo = ctk.CTkComboBox(control_frame, variable=globals.timeframe_var,
                                      values=["1m", "5m", "15m", "1h", "4h", "1d"])
    timeframe_combo.grid(row=0, column=3, padx=5)

    ctk.CTkLabel(control_frame, text="Bar Sayısı:").grid(row=0, column=4, padx=5)
    globals.limit_var = ctk.IntVar(value=15)
    ctk.CTkSegmentedButton(control_frame, values=["15","50", "100", "250", "500"],
                           variable=globals.limit_var).grid(row=0, column=5, padx=5)

    ctk.CTkButton(control_frame, text="Veriyi Göster",
                  command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)]).grid(row=0, column=6, padx=5)

    refresh_switch = ctk.CTkSwitch(control_frame, text="🔄 Oto Yenileme", variable=globals.should_auto_refresh)
    refresh_switch.grid(row=0, column=7, padx=5)

    # SATIR 2
    ctk.CTkButton(control_frame, text="🚀 Hızlı Long Aç", command=Order.execute_trade).grid(row=1, column=0, padx=5, pady=4)
    ctk.CTkButton(control_frame, text="🛑 Hızlı Short Aç", command=Order.execute_short_trade).grid(row=1, column=1, padx=5, pady=4)

    emir_btn = ctk.CTkButton(control_frame, text="🟢 Long Emir Ara", fg_color="darkgreen")
    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.configure(text="🔴 Long Emir Arıyor..." if globals.emir_acik else "🟢 Long Emir Ara")
       # print("[Emir Kontrol]", "✅ Long Emir aranıyor..." if globals.emir_acik else "❌ Long Emir modu kapalı.")
    emir_btn.configure(command=toggle_long_emir)
    emir_btn.grid(row=1, column=2, padx=5)

    short_emir_btn = ctk.CTkButton(control_frame, text="🟢 Short Emir Ara", fg_color="darkred")
    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik
        short_emir_btn.configure(text="🔴 Short Emir Arıyor..." if globals.short_emir_acik else "🟢 Short Emir Ara")
        #print("[Emir Kontrol]", "✅ Short Emir aranıyor..." if globals.short_emir_acik else "❌ Short Emir modu kapalı.")
    short_emir_btn.configure(command=toggle_short_emir)
    short_emir_btn.grid(row=1, column=3, padx=5)

    ctk.CTkButton(control_frame, text="⚙️ Ayarlar", command=lambda: open_settings_window(root)).grid(row=1, column=4, padx=5)

    # Grafik otomatik yenileme fonksiyonu başlat
    Chart.auto_refresh_chart()