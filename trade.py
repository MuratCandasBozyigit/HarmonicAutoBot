import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Binance bağlantısı (Futures)
exchange = ccxt.binance({
    'options': {
        'defaultType': 'future'
    }
})

# EMA ayarları
ema_settings = {
    "show_ema50": True,
    "ema50_val": 50,
    "show_ema200": True,
    "ema200_val": 200
}

# Veri çekme fonksiyonu
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

# Grafik çizme fonksiyonu
def show_chart(event=None):
    raw_symbol = symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = timeframe_var.get()

    if not symbol or not timeframe:
        messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = get_ohlcv(symbol, timeframe)
    if df is not None:
        # Önceki grafiği temizle
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # EMA'ları hesapla ve çiz
        apds = []
        if ema_settings["show_ema50"]:
            df["EMA50"] = df["close"].ewm(span=ema_settings["ema50_val"], adjust=False).mean()
            apds.append(mpf.make_addplot(df["EMA50"], color='blue', width=1.2))
        if ema_settings["show_ema200"]:
            df["EMA200"] = df["close"].ewm(span=ema_settings["ema200_val"], adjust=False).mean()
            apds.append(mpf.make_addplot(df["EMA200"], color='red', width=1.2))

        # Grafik oluştur
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

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

        ax = axlist[0]

        # Zoom işlemi (Ctrl + scroll)
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

# EMA Ayar Paneli
def open_ema_settings():
    settings_win = tk.Toplevel(window)
    settings_win.title("EMA Ayarları")
    settings_win.geometry("300x200")

    # EMA 50
    show_50 = tk.BooleanVar(value=ema_settings["show_ema50"])
    tk.Checkbutton(settings_win, text="EMA 50 Göster", variable=show_50).pack(anchor="w", pady=2)

    tk.Label(settings_win, text="EMA 50 Değeri:").pack()
    ema50_entry = tk.Entry(settings_win)
    ema50_entry.insert(0, str(ema_settings["ema50_val"]))
    ema50_entry.pack()

    # EMA 200
    show_200 = tk.BooleanVar(value=ema_settings["show_ema200"])
    tk.Checkbutton(settings_win, text="EMA 200 Göster", variable=show_200).pack(anchor="w", pady=2)

    tk.Label(settings_win, text="EMA 200 Değeri:").pack()
    ema200_entry = tk.Entry(settings_win)
    ema200_entry.insert(0, str(ema_settings["ema200_val"]))
    ema200_entry.pack()

    def save_settings():
        try:
            ema_settings["show_ema50"] = show_50.get()
            ema_settings["ema50_val"] = int(ema50_entry.get())
            ema_settings["show_ema200"] = show_200.get()
            ema_settings["ema200_val"] = int(ema200_entry.get())
            settings_win.destroy()
            show_chart()  # Güncellenmiş ayarlarla yeniden çiz
        except ValueError:
            messagebox.showerror("Hata", "EMA değerleri sayısal olmalıdır.")

    tk.Button(settings_win, text="Kaydet", command=save_settings).pack(pady=10)

# Arayüz
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.4")
window.geometry("1920x1080")

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

# Göster ve Ayarlar butonları
tk.Button(control_frame, text="Veriyi Göster", command=show_chart).grid(row=0, column=4, padx=5)
tk.Button(control_frame, text="EMA Ayarları ⚙️", command=open_ema_settings).grid(row=0, column=5, padx=5)

# Grafik alanı
chart_frame = tk.Frame(window)
chart_frame.pack(fill="both", expand=True)

window.mainloop()
