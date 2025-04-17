import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicators.harmonic import harmonic_xabcd_validate
from indicators.ema.emaMurtaza import murtaza 

# Binance bağlantısı (Futures)
exchange = ccxt.binance({
    'options': {
        'defaultType': 'future'
    }
})

# Arayüz
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.4")
window.geometry("1920x1080")

draw_ema = tk.BooleanVar(value=True)

def get_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=300):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
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

def detect_and_draw_harmonics(df, ax):
    from matplotlib.lines import Line2D
    window = 50  # kaç bar geri dönüp pattern bakacağız

    for i in range(len(df) - 5, window, -1):  # geriye doğru tarar
        try:
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

                # Noktaları çiz
                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)
                ax.plot(xs, ys, color='darkgreen', linewidth=2)
                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=9, weight='600')

                # Pattern adını yaz
                ax.text(dX, dY, f"{detected}", color='brown', fontsize=12, weight='bold')

                print(f"Harmonik Pattern: {detected} @ Index {dX}")
               # break  # sadece bir pattern çiz

        except Exception as e:
            print(f"[harmonic_draw] {type(e).__name__}: {e}")

def show_chart(event=None):
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

    for widget in chart_frame.winfo_children():
        widget.destroy()

    apds = []
    if draw_ema.get():
        try:
            apds += murtaza(df)
        except Exception as e:
            print(f"[murtaza] {type(e).__name__}: {e}")

    try:
        fig, axlist = mpf.plot(
            df,
            type='candle',
            style='yahoo',
            title=symbol,
            ylabel='Fiyat',
            volume=False,
            addplot=apds if apds else [],
            returnfig=True
        )
    except Exception as e:
        print(f"[mplfinance.plot] {type(e).__name__}: {e}")
        messagebox.showerror("Hata", f"Grafik çiziminde hata:\n{type(e).__name__}: {e}")
        return

    try:
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
    except Exception as e:
        print(f"[FigureCanvasTkAgg] {type(e).__name__}: {e}")
        return
    
    ax = axlist[0]
    try:
        detect_and_draw_harmonics(df, ax)
        canvas.draw_idle()
    except Exception as e:
        print(f"[harmonic_chart] {type(e).__name__}: {e}")


    def on_scroll(event):
        try:
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            x_range = x_max - x_min
            y_range = y_max - y_min

            # Shift: Mumları inceltip uzat (Yatay zoom)
            if event.state & 0x0001:
                zoom_factor = 0.05 * x_range
                if event.delta > 0:
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

            # Alt: Dikey zoom (fiyat ölçeğiyle oyna)
            elif event.state & 0x0008:
                zoom_factor = 0.1 * y_range
                if event.delta > 0:
                    ax.set_ylim(y_min + zoom_factor, y_max - zoom_factor)
                else:
                    ax.set_ylim(y_min - zoom_factor, y_max + zoom_factor)

            # Ctrl: Normal yatay zoom
            elif event.state & 0x0004:
                zoom_factor = 0.1 * x_range
                if event.delta > 0:
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

            canvas.draw_idle()

        except Exception as e:
            print(f"[on_scroll] {type(e).__name__}: {e}")


    widget.bind("<MouseWheel>", on_scroll)

    is_dragging = False
    last_x = None
    last_y = None

    def on_press(event):
        nonlocal is_dragging, last_x, last_y
        is_dragging = True
        last_x = event.x
        last_y = event.y

    def on_release(event):
        nonlocal is_dragging
        is_dragging = False

    def on_motion(event):
        try:
            nonlocal is_dragging, last_x, last_y
            if is_dragging:
                dx = event.x - last_x
                dy = event.y - last_y
                last_x = event.x
                last_y = event.y

                x_min, x_max = ax.get_xlim()
                y_min, y_max = ax.get_ylim()

                pan_x = dx * (x_max - x_min) / widget.winfo_width()
                pan_y = dy * (y_max - y_min) / widget.winfo_height()

                ax.set_xlim(x_min - pan_x, x_max - pan_x)
                ax.set_ylim(y_min + pan_y, y_max + pan_y)

                canvas.draw_idle()
        except Exception as e:
            print(f"[on_motion] {type(e).__name__}: {e}")

    widget.bind("<ButtonPress-1>", on_press)
    widget.bind("<ButtonRelease-1>", on_release)
    widget.bind("<B1-Motion>", on_motion)
  
# Kontroller
control_frame = tk.Frame(window)
control_frame.pack(pady=10)
tk.Label(control_frame, text="Bar Sayısı:").grid(row=0, column=5, padx=5)
limit_var = tk.IntVar(value=100)
limit_spinbox = tk.Spinbox(control_frame, from_=50, to=1000, increment=50, textvariable=limit_var, width=5)
limit_spinbox.grid(row=0, column=6, padx=5)

tk.Label(control_frame, text="Coin (örn: BTC veya BTC/USDT):").grid(row=0, column=0, padx=5)
symbol_var = tk.StringVar()
symbol_entry = tk.Entry(control_frame, textvariable=symbol_var, width=20)
symbol_entry.grid(row=0, column=1, padx=5)
symbol_entry.insert(0, "BTC")
symbol_entry.bind("<FocusIn>", lambda e: symbol_entry.delete(0, tk.END))
symbol_entry.bind("<Return>", show_chart)

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=timeframe_var, values=["1m", "5m", "15m", "1h", "4h", "1d"])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)

tk.Button(control_frame, text="Veriyi Göster", command=show_chart).grid(row=0, column=4, padx=5)

# Ayarlar sekmesi 
settings_frame = tk.Frame(window)
settings_frame.pack(pady=10)

ema_checkbutton = tk.Checkbutton(settings_frame, text="EMA Çizimini Göster", variable=draw_ema)
ema_checkbutton.pack()

chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=True)

# API anahtarlarını buraya yaz (SABİT ve DİKKATLİ KULLAN!)
api_key = 'AB9ABNvPdaqb1Se7YNBkNU254LYZVCNEpvLHVfvkEsl2N9ySmiDxDfn7KfV0sPtn'
api_secret = 'GCWzeHX1UqFdIfct9pZUkdMIhHXyz1yL2Wo5oCOsWP0ZrmRJJzxMqHLRWghYizka'

trading_exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})



window.mainloop()
