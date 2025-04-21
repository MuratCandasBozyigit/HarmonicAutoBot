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

# Binance Futures Exchange tanımı
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

# Harmonik desenleri tespit edip çizme

def detect_and_draw_recent_harmonics(df, ax):
    from matplotlib.lines import Line2D
    try:
        for artist in ax.lines + ax.texts:
            artist.remove()

        for i in range(4, len(df)):
            x = df.iloc[i - 4]
            a = df.iloc[i - 3]
            b = df.iloc[i - 2]
            c = df.iloc[i - 1]
            d = df.iloc[i]

            xX, xY = i - 4, x['low']
            aX, aY = i - 3, a['high']
            bX, bY = i - 2, b['low']
            cX, cY = i - 1, c['high']
            dX, dY = i, d['low']

            result = İndicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
            is_valid, gart, bat, bfly, crab, shark, cyph = result

            if is_valid:
                pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                pattern_type = [gart, bat, bfly, crab, shark, cyph]
                detected = pattern_name[pattern_type.index(True)]

                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)
                ax.plot(xs, ys, color='darkgreen', linewidth=1.4)
                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=8, weight='bold')

                Cmd.add_log(f"[Harmonic] {detected} pattern bulundu @ index {dX}")
                 #and globals.emir_acik
                if dX == len(df) - 7:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if pattern_id not in opened_patterns:
                        Order.open_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
                        Cmd.add_log(f"[Trade Açıldı] {detected} pattern @ fiyattan {dY}")
        gc.collect()
    except Exception as e:
        Cmd.add_log(f"[harmonic_draw] {type(e).__name__}: {e}")


def show_chart(event=None):
    global last_candle_time
    gc.collect()

    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = globals.timeframe_var.get()

    if not symbol or not timeframe:
        messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = Utils.get_ohlcv(symbol, timeframe, limit=limit_var.get())
    if df is None or df.empty:
        messagebox.showwarning("Uyarı", "Veri alınamadı veya boş!")
        return

    df = df.dropna()
    df = df.iloc[-limit_var.get():]
    globals.df = df
    globals.symbol = symbol
    globals.timeframe = timeframe

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, axlist = mpf.plot(
        df,
        type='candle',
        style='yahoo',
        title=symbol,
        ylabel='Fiyat',
        volume=False,
        returnfig=True
    )
    ax = axlist[0]

    detect_and_draw_recent_harmonics(df, ax)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    globals.ax = ax
    globals.canvas = canvas
    last_candle_time = df.index[-1].to_pydatetime().replace(tzinfo=timezone.utc)
def update_last_candle():
    if globals.df is None or globals.symbol is None:
        return
    try:
        ticker = exchange.fetch_ticker(globals.symbol)
        last_price = ticker['last']
        high = max(globals.df.iloc[-1]['high'], last_price)
        low = min(globals.df.iloc[-1]['low'], last_price)

        globals.df.loc[globals.df.index[-1], 'close'] = last_price
        globals.df.loc[globals.df.index[-1], 'high'] = high
        globals.df.loc[globals.df.index[-1], 'low'] = low

        globals.ax.clear()
        mpf.plot(
            globals.df,
            type='candle',
            style='yahoo',
            ax=globals.ax,
            volume=False,
            returnfig=False
        )
        detect_and_draw_recent_harmonics(globals.df, globals.ax)
        globals.canvas.draw_idle()
        gc.collect()
    except Exception as e:
        print(f"[update_last_candle] {type(e).__name__}: {e}")
def auto_refresh_chart():
    global last_candle_time
    if not should_auto_refresh.get() or globals.df is None:
        window.after(1000, auto_refresh_chart)
        return
    try:
        now = datetime.now(timezone.utc)
        tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
        tf_seconds = tf_map.get(globals.timeframe, 60)

        if last_candle_time and (now - last_candle_time).total_seconds() >= tf_seconds:
            print("[Refresh] Yeni mum tespit edildi, grafik güncelleniyor.")
            show_chart()
        else:
            update_last_candle()
    except Exception as e:
        print(f"[auto_refresh_chart] {type(e).__name__}: {e}")
    window.after(1000, auto_refresh_chart)
def pause_refresh(event): should_auto_refresh.set(False)
def resume_refresh(event): should_auto_refresh.set(True)

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
symbol_entry.bind("<FocusIn>", pause_refresh)
symbol_entry.bind("<FocusOut>", resume_refresh)
symbol_entry.bind("<Return>", lambda e: [show_chart(), resume_refresh(e)])

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
globals.timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=globals.timeframe_var, values=["1m", "5m", "15m", "1h", "4h", "1d"])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)

tk.Button(control_frame, text="Veriyi Göster", command=lambda: [show_chart(), resume_refresh(None)]).grid(row=0, column=4, padx=5)
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
auto_refresh_chart()
window.mainloop()
