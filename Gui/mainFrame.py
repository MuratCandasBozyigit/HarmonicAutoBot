import ccxt
import pandas as pd
import mplfinance as mpf
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import json
import os
import tkinter as tk
from PIL import Image
# Dahili modüller
import Indicators
import Utils
import Utils.globals as globals
import Order
import Chart
from Utils.tooltip import ToolTip
from Utils.save_settings import open_settings_window

path = "coins.json"

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

    image =Image.open("logo/logo.ico")
    image = image.resize((128, 128))
    root.display =ctk.CTkImage(light_image=image,dark_image=image)  # İkonu ayarla
    icon = root.iconbitmap("logo/logo.ico")  # İkonu ayarla

    root.title("Auto Trade-X")
    root.geometry("1280x720")

    container_frame = ctk.CTkFrame(root)
    container_frame.pack(fill="both", expand=True)

    # Sol panel
    left_panel = ctk.CTkFrame(container_frame, fg_color="transparent", width=200)
    left_panel.pack(side="left", fill="y", padx=20, pady=20)

    # Grafik alanı
    chart_frame = ctk.CTkFrame(container_frame, fg_color="gray")
    chart_frame.pack(side="left", fill="both", expand=True)
    globals.chart_frame = chart_frame

    globals.should_auto_refresh = ctk.BooleanVar(value=True)

    # Coin giriş
    ctk.CTkLabel(left_panel, text="Coin (BTC vs):").pack(pady=(10, 0))
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

    btn_ekle = ctk.CTkButton(coin_input_row, text="➕", width=40, command=lambda: add_coin_to_list())
    btn_ekle.pack(side="left", padx=5)
    ToolTip(btn_ekle, "Coini Listeye Ekle")

    def add_coin_to_list():
        coin = globals.symbol_var.get().upper()
        if not coin:
            return
        path = "coins.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                coins = json.load(f)
        else:
            coins = []
        if coin not in coins:
            coins.append(coin)
            with open(path, "w") as f:
                json.dump(coins, f)
            
            # Bildirim ekleme
            show_notification(f"{coin} başarıyla listeye eklendi!")

            # Coin butonlarını yenile
            refresh_coin_buttons()

    # Zaman dilimi
    ctk.CTkLabel(left_panel, text="Zaman Dilimi:").pack(pady=(10, 5))
    globals.timeframe_var = ctk.StringVar(value="15m")
    timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]

    def select_timeframe(tf):
        globals.timeframe_var.set(tf)
        Chart.show_chart()

    for i in range(0, len(timeframes), 3):
        row = ctk.CTkFrame(left_panel, fg_color="transparent")
        row.pack(pady=(0, 10))
        for tf in timeframes[i:i+3]:
            btn = ctk.CTkButton(row, text=tf, width=40, height=30, command=lambda tf=tf: select_timeframe(tf))
            btn.pack(side="left", padx=5)

    # Mum sayısı
    ctk.CTkLabel(left_panel, text="Mum Sayısı:").pack(pady=(15, 5))
    globals.limit_var = ctk.StringVar(value="20")
    limit_combo = ctk.CTkComboBox(left_panel, variable=globals.limit_var,
                                  values=["20", "50", "100", "250"],
                                  command=lambda _: Chart.show_chart())
    limit_combo.pack(pady=(0, 15))

    # Hızlı işlemler
    quick_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    quick_row.pack(pady=(10, 5))
    btn_long = ctk.CTkButton(quick_row, text="🚀", width=70, command=Order.execute_trade)
    btn_long.pack(side="left", padx=10)
    ToolTip(btn_long, "Hızlı Long Aç")
    btn_short = ctk.CTkButton(quick_row, text="🛑", width=70, command=Order.execute_short_trade)
    btn_short.pack(side="left", padx=10)
    ToolTip(btn_short, "Hızlı Short Aç")

    # Long / Short emir anahtarları
    emir_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    emir_row.pack(pady=(15, 5))
    long_switch = ctk.CTkSwitch(emir_row, text="📈 Long Emir", command=lambda: toggle_long_emir())
    long_switch.pack(side="left", padx=10)
    short_switch = ctk.CTkSwitch(emir_row, text="📉 Short Emir", command=lambda: toggle_short_emir())
    short_switch.pack(side="left", padx=10)

    def toggle_long_emir():
        globals.emir_acik = not globals.emir_acik

    def toggle_short_emir():
        globals.short_emir_acik = not globals.short_emir_acik

    # Oto yenileme ve ayar butonu
    bottom_row = ctk.CTkFrame(left_panel, fg_color="transparent")
    bottom_row.pack(pady=(15, 5))
    refresh_switch = ctk.CTkSwitch(bottom_row, text="🔄 Oto Yenile", variable=globals.should_auto_refresh)
    refresh_switch.pack(side="left", padx=10)
    btn_settings = ctk.CTkButton(bottom_row, text="⚙️", width=40, command=lambda: open_settings_window(root))
    btn_settings.pack(side="left", padx=10)
    ToolTip(btn_settings, "Ayarları Aç")

    # Coin butonları (3 sıra x 7 coin)
    coin_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    coin_frame.pack(pady=(15, 10))

    def refresh_coin_buttons():
        # Coin butonlarını yenile
        for widget in coin_frame.winfo_children():
            widget.destroy()  # Önce eski butonları temizle
        
        # Yeniden coin butonları oluştur
        if os.path.exists(path):
            with open(path, "r") as f:
                coins = json.load(f)
        else:
            coins = []

        max_per_row = 5
        for i in range(0, min(len(coins), 20), max_per_row):
            row = ctk.CTkFrame(coin_frame, fg_color="transparent")
            row.pack(pady=2)
            for coin in coins[i:i+max_per_row]:
                #btn = ctk.CTkButton(row, text=coin, width=45, height=30)
                btn = ctk.CTkButton(row, text=coin, width=45, height=30, command=lambda c=coin: coin_button_clicked(c))

                btn.pack(side="left", padx=2)

                # Sağ tıklama menüsü için
                def on_right_click(event, coin=coin):
                    menu = tk.Menu(root, tearoff=False)  # Tkinter'ın standart Menu widget'ını kullanıyoruz
                    menu.add_command(label="Sil", command=lambda: delete_coin(coin))
                    menu.post(event.x_root, event.y_root)

                btn.bind("<Button-3>", on_right_click)

    def coin_button_clicked(coin):
        globals.symbol_var.set(coin.upper())  # Coini büyük harfe dönüştür
        Chart.show_chart()

    def delete_coin(coin):
        # Coin silme işlemi
        path = "coins.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                coins = json.load(f)
            if coin in coins:
                coins.remove(coin)
                with open(path, "w") as f:
                    json.dump(coins, f)
                show_notification(f"{coin} başarıyla silindi!")
                refresh_coin_buttons()  # Butonları yenile

    # Otomatik grafik yenileme başlat
    Chart.auto_refresh_chart()

    def show_notification(message):
        # Ekrana kısa bildirim ekleyelim
        notification_label = ctk.CTkLabel(root, text=message, fg_color="green", width=300, height=30)
        notification_label.place(relx=0.5, rely=0.95, anchor="center")
        root.after(3000, notification_label.destroy)  # 3 saniye sonra kaybolacak

    refresh_coin_buttons()
