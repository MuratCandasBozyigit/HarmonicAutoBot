import ccxt
import pandas as pd
import mplfinance as mpf
import tkinter as tk
import random
import gc
import psutil, os
import sys
import time
import threading
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicators.harmonic import harmonic_xabcd_validate
from mods.percentage import toggle_percent_mode
from datetime import datetime, timedelta,timezone
from turtle import clear

exchange = ccxt.binance({
    'apiKey':'irGpxO0nbn4jKHNqddCdaBQS14L9XJ5NxMBgLlg6vBrwMqGAGlqyjqJb6prmAP42',
    'secret':'6ZxTkk6CEeeWWHdSUwgduUbXQ8Jw1IL6GN7NTOt95fgoFktPC0qYM1GfhK8VbAag',
    'options': {'defaultType': 'future'}
})

window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.5")
window.geometry("1920x1080")

should_auto_refresh = tk.BooleanVar(value=True)
opened_patterns = set()  
emir_acik = False
aktif_emir_id = None
last_candle_time = None 
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None


def monitor_ram():
    process = psutil.Process(os.getpid())
    used_ram = process.memory_info().rss / 1024**2

    # Terminalin en üst satırına RAM yaz
    sys.stdout.write("\033[1;1H")  # 1. satır, 1. sütuna git
    sys.stdout.write(f"[RAM Takip] Anlık RAM kullanımı: {used_ram:.2f} MB")
    sys.stdout.flush()

    # Altına çizgi çiz (2. satıra)
    sys.stdout.write("\033[2;1H" + "-" * 80)
    sys.stdout.flush()

    # Pattern loglarını 3. satırdan itibaren bas
    for i, line in enumerate(logs[-20:]):
        sys.stdout.write(f"\033[{3+i};1H{line.ljust(80)}")
    sys.stdout.flush()

    # Her 5 saniyede bir tekrar et
    window.after(5000, monitor_ram)

def get_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=300):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        df = df.dropna()
        if df.empty or len(df) < 100:
            print(f"[get_ohlcv] Veri yetersiz: {len(df)} bar")
            return None
        return df
    except Exception as e:
        messagebox.showerror("Hata", f"Veri çekilirken hata oluştu:\n{str(e)}")
        print(f"[get_ohlcv] {type(e).__name__}: {e}")
        return None

logs = []  
def add_log(msg):
    logs.append(msg)

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

            result = harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
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
                ax.text(dX, dY, f"{detected}", color='maroon', fontsize=10, weight='bold')

                add_log(f"[Harmonic] {detected} pattern bulundu @ index {dX}")

                if dX == len(df) - 2:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if emir_acik:
                        if pattern_id not in opened_patterns:
                            open_position(dY)
                            opened_patterns.add(pattern_id)
                    else:
                        add_log("[Emir Kontrol] Pattern bulundu ama emir modu kapalıydı.")
                        add_log(f"[Trade Açıldı] {detected} pattern @ fiyattan {dY}")

        gc.collect()
    except Exception as e:
        add_log(f"[harmonic_draw] {type(e).__name__}: {e}")

def show_chart(event=None):
    global df, fig, ax, canvas, symbol, timeframe
    def clear_canvas():
        if canvas:
            canvas.get_tk_widget().destroy()
            canvas = None
        if fig:
            fig.clf()
            del fig
            fig = None
    
    def clear_cmd():
          os.system('cls' if os.name == 'nt' else 'clear')

    gc.collect()

    raw_symbol = symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = timeframe_var.get()

    if not symbol or not timeframe:
        messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = get_ohlcv(symbol, timeframe, limit=limit_var.get())
    if df is None or df.empty:
        messagebox.showwarning("Uyarı", "Veri alınamadı veya boş!")
        return

    # Veri temizliği (gerekirse)
    df = df.dropna()
    df = df.iloc[-limit_var.get():]

    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Yeni grafik oluşturuluyor
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

    # Harmonik desenler çiziliyor
    detect_and_draw_recent_harmonics(df, ax)

    # tkinter üzerine grafik yerleştiriliyor
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    gc.collect()

def update_last_candle():
    global df, ax, canvas, symbol
    if df is None or symbol is None:
        return

    try:
        ticker = exchange.fetch_ticker(symbol)
        last_price = ticker['last']
        high = max(df.iloc[-1]['high'], last_price)
        low = min(df.iloc[-1]['low'], last_price)

        df.loc[df.index[-1], 'close'] = last_price
        df.loc[df.index[-1], 'high'] = high
        df.loc[df.index[-1], 'low'] = low


        ax.clear()
        mpf.plot(
            df,
            type='candle',
            style='yahoo',
            ax=ax,
            volume=False,
            returnfig=False
        )

        detect_and_draw_recent_harmonics(df, ax)
        canvas.draw_idle()

        gc.collect()
    except Exception as e:
        print(f"[update_last_candle] {type(e).__name__}: {e}")

def auto_refresh_chart():
    global last_candle_time

    if not should_auto_refresh.get() or df is None:
        window.after(1000, auto_refresh_chart)
        return

    try:
        # Şu anki zaman ve son mumun zamanı
        now = datetime.now(timezone.utc)
        last_time = df.index[-1].to_pydatetime().replace(tzinfo=timezone.utc)


        # Eğer yeni bir mum oluşmuşsa, tüm veriyi güncelle
        if last_candle_time is None:
            last_candle_time = last_time

        # Timeframe'e göre mum süresi
        tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
        tf_seconds = tf_map.get(timeframe, 60)

        if (now - last_candle_time).total_seconds() >= tf_seconds:
            print("[Refresh] Yeni mum tespit edildi, grafik güncelleniyor.")
            show_chart()
            last_candle_time = df.index[-1].to_pydatetime().replace(tzinfo=timezone.utc)
        else:
            update_last_candle()


    except Exception as e:
        print(f"[auto_refresh_chart] {type(e).__name__}: {e}")

    window.after(1000, auto_refresh_chart)

def pause_refresh(event): should_auto_refresh.set(False)
def resume_refresh(event): should_auto_refresh.set(True)

def open_position(entry_price):
    global aktif_emir_id

    try:
        symbol_fut = symbol.replace("/", "").upper()
        miktar = round(0.5 / entry_price, 3)

        # Pozisyon aç
        exchange.set_margin_mode('isolated', symbol=symbol)
        exchange.set_leverage(15, symbol=symbol)
        order = exchange.create_order(
            symbol=symbol,
            type='market',
            side='buy',
            amount=miktar,
            params={'positionSide': 'LONG', 'leverage': 15, 'marginType': 'isolated'}
        )
        aktif_emir_id = order['id']
        add_log(f"[ORDER] {symbol_fut} - LONG pozisyon açıldı: {miktar} adet @ {entry_price}")

        # TP hedefini hesapla
        tp_price = round(entry_price * 1.005, 2)

        # Binance'e TP emri gönder
        exchange.create_order(
            symbol=symbol,
            type='TAKE_PROFIT_MARKET',
            side='sell',
            amount=miktar,
            price=tp_price,
            params={
                'stopPrice': tp_price,
                'reduceOnly': True,
                'positionSide': 'LONG',
                'workingType': 'MARK_PRICE'
            }
        )
        add_log(f"[TP] {symbol_fut} - Binance'e TP emri gönderildi: {tp_price}")
        prinf(f"[TP] {symbol_fut} - Binance'e TP emri gönderildi: {tp_price}")
    except Exception as e:
        add_log(f"[Pozisyon Açma] {type(e).__name__}: {e}")


control_frame = tk.Frame(window)
control_frame.pack(pady=10)

limit_var = tk.IntVar(value=100)
tk.Label(control_frame, text="Bar Sayısı:").grid(row=0, column=5, padx=5)
limit_spinbox = tk.Spinbox(control_frame, from_=50, to=1000, increment=50, textvariable=limit_var, width=5)
limit_spinbox.grid(row=0, column=6, padx=5)

tk.Label(control_frame, text="Coin (örn: BTC veya BTC/USDT):").grid(row=0, column=0, padx=5)
symbol_var = tk.StringVar()
symbol_entry = tk.Entry(control_frame, textvariable=symbol_var, width=20)
symbol_entry.grid(row=0, column=1, padx=5)
symbol_entry.insert(0, "BTC")

symbol_entry.bind("<FocusIn>", pause_refresh)
symbol_entry.bind("<FocusOut>", resume_refresh)
symbol_entry.bind("<Return>", lambda e: [show_chart(), resume_refresh(e)])

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=timeframe_var, values=["1m", "5m", "15m", "1h", "4h", "1d"])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)

tk.Button(control_frame, text="Veriyi Göster", command=lambda: [show_chart(), resume_refresh(None)]).grid(row=0, column=4, padx=5)

chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=False)

def toggle_emir():
    global emir_acik
    emir_acik = not emir_acik
    emir_btn.config(text="🔴 Emir Arıyor..." if emir_acik else "🟢 Emir Aç!")

emir_btn = tk.Button(control_frame, text="🟢 Emir Aç", command=toggle_emir, bg="lightgreen")
emir_btn.grid(row=0, column=7, padx=10)


monitor_ram()
auto_refresh_chart()
window.mainloop()
