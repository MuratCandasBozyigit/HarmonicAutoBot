import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicators.emaMurtaza import murtaza  # Sadece bu kaldı

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

def get_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=500):
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

def show_chart(event=None):
    raw_symbol = symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = timeframe_var.get()

    if not symbol or not timeframe:
        messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = get_ohlcv(symbol, timeframe)
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

    def on_scroll(event):
        try:
            if event.state & 0x0004:
                x_min, x_max = ax.get_xlim()
                x_range = x_max - x_min
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
# def execute_trade():
#     raw_symbol = symbol_var.get().strip().upper()
#     symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
#     timeframe = timeframe_var.get()

#     df = get_ohlcv(symbol, timeframe)
#     if df is None or df.empty:
#         messagebox.showwarning("Uyarı", "İşlem için geçerli veri alınamadı!")
#         return

#     try:
#         # EMA stratejisini uygula
#         murtaza(df)

#         # Sinyal sütunları gerçekten eklendi mi kontrol et
#         if "long_signal" not in df.columns or "short_signal" not in df.columns:
#             raise ValueError("Sinyal sütunları df içerisinde bulunamadı. murtaza() fonksiyonu bunları eklemiyor olabilir.")

#         last_row = df.iloc[-1]

#         # Pozisyon parametreleri
#         usdt_amount = 1     # USDT cinsinden işlem büyüklüğü
#         leverage = 20       # 20x kaldıraç

#         trading_exchange.set_leverage(leverage, symbol=symbol)

#         # Güncel fiyat ve miktar hesapla
#         market_price = last_row['close']
#         coin_amount = round((usdt_amount * leverage) / market_price, 3)

#         if last_row.get("long_signal"):
#             side = 'buy'
#             msg = f"[LONG] Sinyal algılandı - {symbol}"
#         elif last_row.get("short_signal"):
#             side = 'sell'
#             msg = f"[SHORT] Sinyal algılandı - {symbol}"
#         else:
#             messagebox.showinfo("Bilgi", "Sinyal tespit edilmedi.")
#             return

#         # Market emri gönder
#         order = trading_exchange.create_market_order(
#             symbol=symbol,
#             side=side,
#             amount=coin_amount
#         )

#         messagebox.showinfo("Başarılı", f"{msg}\nMarket Order Açıldı\nID: {order['id']}")
#         print("[Order Detayları]", order)

#     except ccxt.BaseError as e:
#         print(f"[ccxt error] {type(e).__name__}: {e}")
#         messagebox.showerror("Exchange Hatası", f"ccxt hatası:\n{type(e).__name__}: {e}")

#     except Exception as e:
#         import traceback
#         tb = traceback.format_exc()
#         print(f"[execute_trade] {type(e).__name__}: {e}")
#         print(tb)
#         messagebox.showerror("Hata", f"İşlem sırasında beklenmeyen bir hata oluştu:\n{type(e).__name__}: {e}")


# tk.Button(control_frame, text="Otomatik İşlem Aç", command=execute_trade, bg="green", fg="white").grid(row=0, column=6, padx=5)