import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Binance bağlantısı
exchange = ccxt.binance()

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

def show_chart():
    symbol = symbol_var.get()
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
        ax = axlist[0]  # sadece fiyat eksenine zoom yapacağız

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=False,padx=(0, 0),  anchor="w")

        # Mouse scroll eventini bağla
        def on_scroll(event):
            if event.state & 0x0004:  # Ctrl tuşu basılıysa
                # x limiti al
                x_min, x_max = ax.get_xlim()
                x_range = x_max - x_min
                zoom_factor = 0.1 * x_range

                if event.delta > 0:
                    # Yakınlaştır
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    # Uzaklaştır
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

                canvas.draw_idle()

        # Windows için scroll bind (macOS'ta farklı olabilir)
        widget.bind("<MouseWheel>", on_scroll)

# Tkinter arayüzü
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.1")
window.geometry("1920x1080")

# Coin ve Zaman Dilimi Seçimi
control_frame = tk.Frame(window)
control_frame.pack(pady=10)


tk.Label(control_frame, text="Hesap Bakiyesi:").grid(row=0, column=4, padx=5)

tk.Label(control_frame, text="Coin (örnek: BTC/USDT):").grid(row=0, column=0, padx=5)
symbol_var = tk.StringVar()
symbol_entry = ttk.Combobox(control_frame, textvariable=symbol_var, values=[
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"
])
symbol_entry.grid(row=0, column=1, padx=5)
symbol_entry.current(0)

tk.Label(control_frame, text="Zaman Dilimi:").grid(row=0, column=2, padx=5)
timeframe_var = tk.StringVar()
timeframe_combo = ttk.Combobox(control_frame, textvariable=timeframe_var, values=[
    "1m", "5m", "15m", "1h", "4h", "1d"
])
timeframe_combo.grid(row=0, column=3, padx=5)
timeframe_combo.current(3)  # Varsayılan olarak 1h seçili

# Göster Butonu
button = tk.Button(window, text="Veriyi Göster", command=show_chart)
button.pack(pady=5)

# Grafik alanı
chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=True)

window.mainloop()
