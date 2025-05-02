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

    # Left panel
    left_panel = ctk.CTkFrame(container_frame, fg_color="#2A2E3B", width=200)
    left_panel.pack(side="left", fill="y")

    # Chart frame
    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.pack(side="left", fill="both", expand=True)
    globals.chart_frame = chart_frame

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Coin entry
    ctk.CTkLabel(left_panel, text="Coin (BTC vs):").pack(pady=(10, 0))
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(left_panel, textvariable=globals.symbol_var, width=120)
    symbol_entry.pack(pady=(0, 10))
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    # Timeframe selection
    ctk.CTkLabel(left_panel, text="Zaman Dilimi:").pack()
    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframe_combo = ctk.CTkComboBox(left_panel, variable=globals.timeframe_var,
                                      values=["1m", "5m", "15m", "1h", "4h", "1d"],
                                      command=lambda _: Chart.show_chart())
    timeframe_combo.pack(pady=(0, 10))

    # Bar count selection
    ctk.CTkLabel(left_panel, text="Mum Sayısı:").pack()
    globals.limit_var = ctk.StringVar(value="20")
    limit_combo = ctk.CTkComboBox(left_panel, variable=globals.limit_var,
                                  values=["20", "50", "100", "250"],
                                  command=lambda _: Chart.show_chart())
    limit_combo.pack(pady=(0, 10))

    # Show chart button
    btn_goster = ctk.CTkButton(left_panel, text="📊", width=40,
                               command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)])
    btn_goster.pack(pady=5)
    ToolTip(btn_goster, "Grafiği Göster")

    # Auto refresh switch
    refresh_switch = ctk.CTkSwitch(left_panel, text="🔄 Oto Yenileme", variable=globals.should_auto_refresh)
    refresh_switch.pack(pady=5)

    # Quick Long button
    btn_long = ctk.CTkButton(left_panel, text="🚀", width=40, command=Order.execute_trade)
    btn_long.pack(pady=5)
    ToolTip(btn_long, "Hızlı Long Aç")

    # Quick Short button
    btn_short = ctk.CTkButton(left_panel, text="🛑", width=40, command=Order.execute_short_trade)
    btn_short.pack(pady=5)
    ToolTip(btn_short, "Hızlı Short Aç")

    # Toggle Long order button
    emir_btn = ctk.CTkButton(left_panel, text="📈", width=40, fg_color="darkgreen")
    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.configure(text="🔴" if globals.emir_acik else "📈")
    emir_btn.configure(command=toggle_long_emir)
    emir_btn.pack(pady=5)
    ToolTip(emir_btn, "Long Emir Ara")

    # Toggle Short order button
    short_emir_btn = ctk.CTkButton(left_panel, text="📉", width=40, fg_color="darkred")
    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik
        short_emir_btn.configure(text="🔴" if globals.short_emir_acik else "📉")
    short_emir_btn.configure(command=toggle_short_emir)
    short_emir_btn.pack(pady=5)
    ToolTip(short_emir_btn, "Short Emir Ara")

    # Settings button
    btn_settings = ctk.CTkButton(left_panel, text="⚙️", width=40, command=lambda: open_settings_window(root))
    btn_settings.pack(pady=5)
    ToolTip(btn_settings, "Ayarları Aç")

    # Start auto-refresh for the chart
    Chart.auto_refresh_chart()
