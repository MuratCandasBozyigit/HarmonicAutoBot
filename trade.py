import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Binance bağlantısı
exchange = ccxt.binance({
    'options': {
        'defaultType': 'future'  # Perpetual market verilerini almak için
    }
})

# Sadece .P ile biten perpetual coin çiftlerini al
def get_perpetual_symbols():
    markets = exchange.load_markets()
    perpetual_symbols = [symbol for symbol in markets if symbol.endswith(":USDT")]
    return perpetual_symbols

# OHLCV verisini çek
def get_ohlcv(symbol="BTC/USDT", timeframe="1h", limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        messagebox.showerror("Hata", f"Veri çekilirken hata oluştu:\n{str(e)}")
        return None

# Grafik çiz
def draw_chart(data):
    fig, axlist = mpf.plot(
        data,
        type='candle',
        style='yahoo',
        ylabel='Fiyat',
        volume=False,
        returnfig=True,
    )
    return fig, axlist

# Grafik göster
def show_chart():
    raw_symbol = symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = timeframe_var.get()

    if not symbol or not timeframe:
        messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = get_ohlcv(symbol, timeframe)
    if df is not None:
        # Önceki içeriği temizle
        for widget in chart_frame.winfo_children():
            widget.destroy()

        fig, axlist = draw_chart(df)
        ax = axlist[0]

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=False, padx=(0, 0), anchor="w")

        # Zoom (scroll + Ctrl)
        def on_scroll(event):
            if event.state & 0x0004:
                x_min, x_max = ax.get_xlim()
                x_range = x_max - x_min
                zoom_factor = 0.1 * x_range

                if event.delta > 0:
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

                canvas.draw_idle()

        widget.bind("<MouseWheel>", on_scroll)

        # Sürükleme (sol tık)
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

        widget.bind("<ButtonPress-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)
        widget.bind("<B1-Motion>", on_motion)

        canvas.draw_idle()


# Arayüz
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.2")
window.geometry("1920x1080")

# Coin listesi çek
perpetual_list = get_perpetual_symbols()

# Kontroller
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Hesap Bakiyesi:").grid(row=0, column=4, padx=5)

tk.Label(control_frame, text="Coin (örn: BTC, ETH veya BTC/USDT):").grid(row=0, column=0, padx=5)
symbol_var = tk.StringVar()
symbol_entry = ttk.Combobox(control_frame, textvariable=symbol_var, values=perpetual_list, state="normal")
symbol_entry.grid(row=0, column=1, padx=5)
symbol_entry.set("BTC/USDT")

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=timeframe_var, values=[
    "1m", "5m", "15m", "1h", "4h", "1d"
])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)

# Göster butonu
button = tk.Button(window, text="Veriyi Göster", command=show_chart)
button.pack(pady=5)

# Grafik alanı
chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=True)

window.mainloop()
