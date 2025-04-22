import ccxt
import pandas as pd
import mplfinance as mpf
import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Dahili modüller
import İndicators
import Utils
import Utils.globals as globals
import Cmd
import Order
import Chart
from Utils.save_settings import open_settings_window  # Ayarlar butonu için import

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("dark" if current == "light" else "light")
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

    root.title("Harmonic Gözlem Paneli - v0.5")
    root.geometry("1280x720")

    container_frame = ctk.CTkFrame(root)
    container_frame.pack(fill="both", expand=True)

    chart_frame = ctk.CTkFrame(container_frame, fg_color="black")
    chart_frame.grid(row=0, column=0, sticky="nsew")
    globals.chart_frame = chart_frame

    # Otomatik yenileme kontrol değişkeni
    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    control_frame = ctk.CTkFrame(container_frame)
    control_frame.grid(row=1, column=0, pady=8, padx=5)

    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(0, weight=1)

        # SATIR 1: Coin, Zaman Dilimi, Bar Sayısı, Göster Butonu, Oto Yenileme
    ctk.CTkLabel(control_frame, text="Coin (BTC vs):").grid(row=0, column=0, padx=5, pady=2)
    globals.symbol_var = ctk.StringVar(value="BTC")
    symbol_entry = ctk.CTkEntry(control_frame, textvariable=globals.symbol_var, width=120)
    symbol_entry.grid(row=0, column=1, padx=5)
    symbol_entry.bind("<FocusIn>", Chart.pause_refresh)
    symbol_entry.bind("<FocusOut>", Chart.resume_refresh)
    symbol_entry.bind("<Return>", lambda e: [Chart.show_chart(), Chart.resume_refresh(e)])

    ctk.CTkLabel(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
    globals.timeframe_var = ctk.StringVar(value="1h")
    timeframe_combo = ctk.CTkComboBox(control_frame, variable=globals.timeframe_var,
                                      values=["1m", "5m", "15m", "1h", "4h", "1d"])
    timeframe_combo.grid(row=0, column=3, padx=5)

    ctk.CTkLabel(control_frame, text="Bar Sayısı:").grid(row=0, column=4, padx=5)
    globals.limit_var = ctk.IntVar(value=100)
    ctk.CTkSegmentedButton(control_frame, values=["50", "100", "250", "500", "1000"],
                           variable=globals.limit_var).grid(row=0, column=5, padx=5)

    ctk.CTkButton(control_frame, text="Veriyi Göster",
                  command=lambda: [Chart.show_chart(), Chart.resume_refresh(None)]).grid(row=0, column=6, padx=5)

    refresh_switch = ctk.CTkSwitch(control_frame, text="🔄 Oto Yenileme", variable=globals.should_auto_refresh)
    refresh_switch.grid(row=0, column=7, padx=5)

    # SATIR 2: Long Aç, Emir Modu, Ayarlar, Tema, vs
    ctk.CTkButton(control_frame, text="Anlık Long Aç", command=Order.execute_trade).grid(row=1, column=0, padx=5, pady=4)

    emir_btn = ctk.CTkButton(control_frame, text="🟢Long Emir Aç", fg_color="darkgreen")
    def toggle_emir():
        globals.emir_acik = not globals.emir_acik
        emir_btn.configure(text="🔴Long Emir Arıyor..." if globals.emir_acik else "🟢Long Emir Aç!")
        print("[Emir Kontrol]", "✅Long Emir aranıyor..." if globals.emir_acik else "⛔Long Emir modu kapalı.")
    emir_btn.configure(command=toggle_emir)
    emir_btn.grid(row=1, column=1, padx=5)

    ctk.CTkButton(control_frame, text="⚙️ Ayarlar", command=lambda: open_settings_window(root)).grid(row=1, column=2, padx=5)
    ctk.CTkButton(control_frame, text="☼/☾ Tema Değiştir", command=toggle_theme).grid(row=1, column=3, padx=5)

   

    # Şimdi fonksiyonu başlatmak güvenli
    Chart.auto_refresh_chart()

