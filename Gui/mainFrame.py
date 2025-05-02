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

    # Sol Panel
    left_panel = ctk.CTkFrame(container_frame, fg_color="#2A2E3B", width=200)
    left_panel.pack(side="left", fill="y")

    # Grafik Alanı
    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.pack(side="left", fill="both", expand=True)
    globals.chart_frame = chart_frame

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Coin girişi
    ctk.CTkLabel(left_panel, text="Coin (BTC vs):").pack(pady=(10, 0))
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(left_panel, textvariable=globals.symbol_var, width=120)
    symbol_entry.pack(pady=(0, 10))
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    # Zaman Dilimi Seçimi
    ctk.CTkLabel(left_panel, text="Zaman Dilimi:").pack(pady=(10, 5))
    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]
    button_grid_frame = ctk.CTkFrame(left_panel)
    button_grid_frame.pack(pady=(0, 10))

    def select_timeframe(tf):
        globals.timeframe_var.set(tf)
        Chart.show_chart()

    for i, tf in enumerate(timeframes):
        btn = ctk.CTkButton(button_grid_frame, text=tf, width=50, height=30,
                            command=lambda tf=tf: select_timeframe(tf))
        row, col = divmod(i, 3)
        btn.grid(row=row, column=col, padx=6, pady=6)

    # Mum sayısı seçimi
    ctk.CTkLabel(left_panel, text="Mum Sayısı:").pack()
    globals.limit_var = ctk.StringVar(value="20")
    limit_combo = ctk.CTkComboBox(left_panel, variable=globals.limit_var,
                                  values=["20", "50", "100", "250"],
                                  command=lambda _: Chart.show_chart())
    limit_combo.pack(pady=(0, 10))

    # Grafik gösterme butonu
    btn_goster = ctk.CTkButton(left_panel, text="📊", width=40,
                               command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)])
    btn_goster.pack(pady=5)
    ToolTip(btn_goster, "Grafiği Göster")

    # Hızlı İşlem Butonları
    btn_long = ctk.CTkButton(left_panel, text="🚀", width=40, command=Order.execute_trade)
    btn_long.pack(pady=5)
    ToolTip(btn_long, "Hızlı Long Aç")

    btn_short = ctk.CTkButton(left_panel, text="🛑", width=40, command=Order.execute_short_trade)
    btn_short.pack(pady=5)
    ToolTip(btn_short, "Hızlı Short Aç")

    # --- Switch Satırı: Long & Short ---
    emir_switch_row = ctk.CTkFrame(left_panel)
    emir_switch_row.pack(pady=(10, 0))

    globals.emir_acik_var = ctk.BooleanVar(value=False)
    globals.short_emir_acik_var = ctk.BooleanVar(value=False)

    long_switch = ctk.CTkSwitch(emir_switch_row, text="📈 Long", variable=globals.emir_acik_var)
    long_switch.pack(side="left", padx=10)

    short_switch = ctk.CTkSwitch(emir_switch_row, text="📉 Short", variable=globals.short_emir_acik_var)
    short_switch.pack(side="left", padx=10)

    # --- Alt Satır: Oto Yenileme & Ayar Butonu ---
    control_row = ctk.CTkFrame(left_panel)
    control_row.pack(pady=10)

    refresh_switch = ctk.CTkSwitch(control_row, text="🔄 Oto", variable=globals.should_auto_refresh)
    refresh_switch.pack(side="left", padx=10)

    btn_settings = ctk.CTkButton(control_row, text="⚙️", width=40, command=lambda: open_settings_window(root))
    btn_settings.pack(side="left", padx=10)
    ToolTip(btn_settings, "Ayarları Aç")

    # Otomatik grafik yenileme
    Chart.auto_refresh_chart()


