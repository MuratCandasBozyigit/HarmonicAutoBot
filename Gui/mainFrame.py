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

    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.grid(row=0, column=1, sticky="nsew")
    globals.chart_frame = chart_frame

    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(1, weight=1)

    # Sol Panel
    left_panel = ctk.CTkFrame(container_frame, width=240, fg_color="#1e1e1e")
    left_panel.grid(row=0, column=0, rowspan=2, sticky="ns")
    left_panel.grid_propagate(False)

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Coin Girişi
    ctk.CTkLabel(left_panel, text="Coin (BTC vs):", anchor="w").grid(row=0, column=0, padx=10, pady=(15, 2), sticky="w")
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(left_panel, textvariable=globals.symbol_var)
    symbol_entry.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    # === Zaman Dilimi ve Bar Sayısı Birlikte ===
    ctk.CTkLabel(left_panel, text="Zaman Dilimi:", anchor="w").grid(row=2, column=0, padx=10, pady=(15, 2), sticky="w")

    def update_chart_from_inputs(_=None):
        Chart.pause_refresh(None)
        Chart.show_chart()
        Chart.resume_refresh(None)

    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframe_combo = ctk.CTkSegmentedButton(left_panel, variable=globals.timeframe_var,
                                             values=["1m", "5m", "15m", "1h", "4h", "1d"])
    timeframe_combo.grid(row=3, column=0, padx=10, pady=2)
    timeframe_combo.configure(command=update_chart_from_inputs)

    ctk.CTkLabel(left_panel, text="Mum Sayısı:", anchor="w").grid(row=4, column=0, padx=10, pady=(15, 2), sticky="w")
    globals.limit_var = ctk.IntVar(value=15)
    bar_count_combo = ctk.CTkComboBox(left_panel, variable=globals.limit_var,
                                      values=["15", "50", "100", "250"])
    bar_count_combo.grid(row=5, column=0, padx=10, pady=2)
    bar_count_combo.bind("<<ComboboxSelected>>", update_chart_from_inputs)

    # === Butonlar ===
    icon_long = "🚀"
    icon_short = "🛑"
    icon_settings = "⚙️"
    icon_show = "📊"

    ctk.CTkButton(left_panel, text=icon_long, font=("Arial", 24), height=48,
                  command=Order.execute_trade).grid(row=6, column=0, padx=10, pady=(20, 8), sticky="ew")

    ctk.CTkButton(left_panel, text=icon_short, font=("Arial", 24), height=48,
                  command=Order.execute_short_trade).grid(row=7, column=0, padx=10, pady=8, sticky="ew")

    emir_btn = ctk.CTkButton(left_panel, text="🟢 Long Emir Ara", fg_color="darkgreen")
    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.configure(text="🔴 Long Emir Arıyor..." if globals.emir_acik else "🟢 Long Emir Ara")
    emir_btn.configure(command=toggle_long_emir)
    emir_btn.grid(row=8, column=0, padx=10, pady=8, sticky="ew")

    short_emir_btn = ctk.CTkButton(left_panel, text="🟢 Short Emir Ara", fg_color="darkred")
    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik
        short_emir_btn.configure(text="🔴 Short Emir Arıyor..." if globals.short_emir_acik else "🟢 Short Emir Ara")
    short_emir_btn.configure(command=toggle_short_emir)
    short_emir_btn.grid(row=9, column=0, padx=10, pady=8, sticky="ew")

    ctk.CTkButton(left_panel, text=icon_show + " Veriyi Göster",
                  command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)]).grid(row=10, column=0, padx=10, pady=(10, 8), sticky="ew")

    ctk.CTkSwitch(left_panel, text="🔄 Oto Yenileme", variable=globals.should_auto_refresh).grid(row=11, column=0, padx=10, pady=(10, 8), sticky="ew")

    ctk.CTkButton(left_panel, text=icon_settings, font=("Arial", 26), width=48,
                  command=lambda: open_settings_window(root)).grid(row=12, column=0, padx=10, pady=(15, 10), sticky="ew")

    # Grafik otomatik yenileme başlat
    Chart.auto_refresh_chart()
