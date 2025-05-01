import ccxt
import pandas as pd
import mplfinance as mpf
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Dahili modüller
import Indicators
import Utils
import Utils.globals as globals
import Order
import Chart
from Utils.save_settings import open_settings_window


def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "dark" else "dark")


def build_gui(root):
    globals.root = root
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")

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

    # Sol Panel (kontroller)
    left_panel = ctk.CTkFrame(container_frame, width=200)
    left_panel.grid(row=0, column=0, sticky="ns")
    left_panel.grid_propagate(False)

    # Grafik Alanı
    chart_frame = ctk.CTkFrame(container_frame, fg_color="black")
    chart_frame.grid(row=0, column=1, sticky="nsew")
    globals.chart_frame = chart_frame

    # Otomatik yenileme durumu
    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Grid konfigürasyon
    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(1, weight=1)

    # === Sol Panel İçerikleri (Dikey Sıralı) ===

    ctk.CTkLabel(left_panel, text="Coin:", anchor="w").grid(row=0, column=0, padx=10, pady=(15, 2), sticky="w")
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(left_panel, textvariable=globals.symbol_var, width=120)
    symbol_entry.grid(row=1, column=0, padx=10, pady=2)
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    ctk.CTkLabel(left_panel, text="Zaman Dilimi:", anchor="w").grid(row=2, column=0, padx=10, pady=(15, 2), sticky="w")
    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframe_combo = ctk.CTkComboBox(left_panel, variable=globals.timeframe_var,
                                      values=["1m", "5m", "15m", "1h", "4h", "1d"])
    timeframe_combo.grid(row=3, column=0, padx=10, pady=2)

    ctk.CTkLabel(left_panel, text="Bar Sayısı:", anchor="w").grid(row=4, column=0, padx=10, pady=(15, 2), sticky="w")
    globals.limit_var = ctk.IntVar(value=15)
    ctk.CTkSegmentedButton(left_panel, values=["15", "50", "100", "250", "500"], variable=globals.limit_var).grid(
        row=5, column=0, padx=10, pady=2
    )

    # 🔁 Butonlar (Simgeli)
    ctk.CTkButton(left_panel, text="🚀", command=Order.execute_trade, fg_color="green",
                  font=("Arial", 24), width=60, height=40).grid(row=6, column=0, pady=10)

    ctk.CTkButton(left_panel, text="📉", command=Order.execute_short_trade, fg_color="red",
                  font=("Arial", 24), width=60, height=40).grid(row=7, column=0, pady=10)

    # Long Emir Toggle
    emir_btn = ctk.CTkButton(left_panel, text="🟢", fg_color="darkgreen", font=("Arial", 24), width=60, height=40)
    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.configure(text="🔴" if globals.emir_acik else "🟢")
    emir_btn.configure(command=toggle_long_emir)
    emir_btn.grid(row=8, column=0, pady=10)

    # Short Emir Toggle
    short_emir_btn = ctk.CTkButton(left_panel, text="🟢", fg_color="darkred", font=("Arial", 24), width=60, height=40)
    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik
        short_emir_btn.configure(text="🔴" if globals.short_emir_acik else "🟢")
    short_emir_btn.configure(command=toggle_short_emir)
    short_emir_btn.grid(row=9, column=0, pady=10)

    # 📊 Veriyi Göster Butonu
    ctk.CTkButton(left_panel, text="📊", command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)],
                  font=("Arial", 24), width=60, height=40).grid(row=10, column=0, pady=10)

    # ⚙️ Ayarlar
    ctk.CTkButton(left_panel, text="⚙️", command=lambda: open_settings_window(root),
                  font=("Arial", 26), width=60, height=40).grid(row=11, column=0, pady=10)

    # 🔄 Oto Yenileme Switch
    ctk.CTkSwitch(left_panel, text="🔄 Oto Yenile", variable=globals.should_auto_refresh).grid(row=12, column=0, pady=(20, 5))

    # Grafik otomatik yenileme başlat
    Chart.auto_refresh_chart()
