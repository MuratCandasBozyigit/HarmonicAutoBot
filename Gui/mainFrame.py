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
from Utils.tooltip import ToolTip
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

    # Sol panel (arka plan kaldırıldı)
    left_panel = ctk.CTkFrame(container_frame, fg_color="transparent", width=200)
    left_panel.pack(side="left", fill="y", padx=20, pady=20)

    # Grafik alanı
    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.pack(side="left", fill="both", expand=True)
    globals.chart_frame = chart_frame

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Coin Label
    ctk.CTkLabel(left_panel, text="Coin (BTC vs):").pack(pady=(10, 0))

    # Coin input + Göster butonu (yan yana)
    coin_input_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    coin_input_row.pack(pady=(10, 5))

    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(coin_input_row, textvariable=globals.symbol_var, width=100)
    symbol_entry.pack(side="left", padx=(0, 5))
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    btn_goster = ctk.CTkButton(coin_input_row, text="📊", width=40,
                               command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)])
    btn_goster.pack(side="left", padx=5)
    ToolTip(btn_goster, "Grafiği Göster")

    # Zaman dilimi başlığı
    ctk.CTkLabel(left_panel, text="Zaman Dilimi:").pack(pady=(10, 5))
    globals.timeframe_var = ctk.StringVar(value="15m")

    # Zaman dilimi butonları 3-3-2
    timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]
    def select_timeframe(tf):
        globals.timeframe_var.set(tf)
        Chart.show_chart()

    for i in range(0, len(timeframes), 3):
        row = ctk.CTkFrame(left_panel, fg_color="transparent")
        row.pack(pady=(0, 10))  # Aradaki boşluğu artırdık
        for tf in timeframes[i:i+3]:
            btn = ctk.CTkButton(row, text=tf, width=40, height=30,
                                command=lambda tf=tf: select_timeframe(tf))
            btn.pack(side="left", padx=5)  # Aradaki boşluğu artırdık

    # Mum sayısı
    ctk.CTkLabel(left_panel, text="Mum Sayısı:").pack(pady=(15, 5))
    globals.limit_var = ctk.StringVar(value="20")
    limit_combo = ctk.CTkComboBox(left_panel, variable=globals.limit_var,
                                  values=["20", "50", "100", "250"],
                                  command=lambda _: Chart.show_chart())
    limit_combo.pack(pady=(0, 15))  # Aradaki boşluğu artırdık

    # Hızlı işlemler (yan yana)
    quick_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    quick_row.pack(pady=(10, 5))
    btn_long = ctk.CTkButton(quick_row, text="🚀", width=70, command=Order.execute_trade)
    btn_long.pack(side="left", padx=10)  # Aradaki boşluğu artırdık
    ToolTip(btn_long, "Hızlı Long Aç")
    btn_short = ctk.CTkButton(quick_row, text="🛑", width=70, command=Order.execute_short_trade)
    btn_short.pack(side="left", padx=10)  # Aradaki boşluğu artırdık
    ToolTip(btn_short, "Hızlı Short Aç")

    # Long / Short Emir Ara Switchleri (aynı satırda)
    emir_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    emir_row.pack(pady=(15, 5))  # Aradaki boşluğu artırdık

    long_switch = ctk.CTkSwitch(emir_row, text="📈 Long Emir", command=lambda: toggle_long_emir())
    long_switch.pack(side="left", padx=10)  # Aradaki boşluğu artırdık
    short_switch = ctk.CTkSwitch(emir_row, text="📉 Short Emir", command=lambda: toggle_short_emir())
    short_switch.pack(side="left", padx=10)  # Aradaki boşluğu artırdık

    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik
         
    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik

    # Oto yenileme + Ayarlar (aynı satırda)
    bottom_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    bottom_row.pack(pady=(15, 5))  # Aradaki boşluğu artırdık

    refresh_switch = ctk.CTkSwitch(bottom_row, text="🔄 Oto Yenile", variable=globals.should_auto_refresh)
    refresh_switch.pack(side="left", padx=10)  # Aradaki boşluğu artırdık

    btn_settings = ctk.CTkButton(bottom_row, text="⚙️", width=40,
                                 command=lambda: open_settings_window(root))
    btn_settings.pack(side="left", padx=10)  # Aradaki boşluğu artırdık
    ToolTip(btn_settings, "Ayarları Aç")

    # Otomatik grafik yenileme başlat
    Chart.auto_refresh_chart()

