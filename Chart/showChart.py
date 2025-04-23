# Chart.py
import gc
from datetime import datetime, timezone
import Utils
import DrawPattern
import Utils.globals as globals
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_chart(event=None):
    gc.collect()

    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = globals.timeframe_var.get()

    if not symbol or not timeframe:
        print("Uyarı: Coin ve zaman dilimi girilmedi.")
        return

    df = Utils.get_ohlcv(symbol, timeframe, limit=globals.limit_var.get())
    if df is None or df.empty:
        print("Uyarı: Veri alınamadı.")
        return

    df = df.dropna().iloc[-globals.limit_var.get():]
    globals.df = df
    globals.symbol = symbol
    globals.timeframe = timeframe

    for widget in globals.chart_frame.winfo_children():
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

    canvas = FigureCanvasTkAgg(fig, master=globals.chart_frame)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True)

    globals.ax = ax
    globals.canvas = canvas
    globals.last_candle_time = df.index[-1].to_pydatetime().replace(tzinfo=timezone.utc)

    # 🔍 Zoom eventleri
    def on_scroll(event):
        try:
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            x_range = x_max - x_min
            y_range = y_max - y_min

            if event.state & 0x0001:  # Shift: Yatay zoom
                zoom_factor = 0.05 * x_range
                if event.delta > 0:
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

            elif event.state & 0x0008:  # Alt: Dikey zoom
                zoom_factor = 0.1 * y_range
                if event.delta > 0:
                    ax.set_ylim(y_min + zoom_factor, y_max - zoom_factor)
                else:
                    ax.set_ylim(y_min - zoom_factor, y_max + zoom_factor)

            elif event.state & 0x0004:  # Ctrl: Alternatif yatay zoom
                zoom_factor = 0.1 * x_range
                if event.delta > 0:
                    ax.set_xlim(x_min + zoom_factor, x_max - zoom_factor)
                else:
                    ax.set_xlim(x_min - zoom_factor, x_max + zoom_factor)

            canvas.draw_idle()
        except Exception as e:
            print(f"[on_scroll] {type(e).__name__}: {e}")

    widget.bind("<MouseWheel>", on_scroll)


def update_last_candle():
    if globals.df is None or globals.symbol is None:
        return
    try:
        ticker = globals.exchange.fetch_ticker(globals.symbol)
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
        DrawPattern.draw_bullish_patterns(globals.df, globals.ax)
        DrawPattern.draw_bearish_patterns(globals.df, globals.ax)
        globals.canvas.draw_idle()
        gc.collect()
    except Exception as e:
        print(f"[update_last_candle] {type(e).__name__}: {e}")


def auto_refresh_chart():
    if not globals.should_auto_refresh.get():
        globals.root.after(1000, auto_refresh_chart)
        return
    try:
        now = datetime.now(timezone.utc)
        tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
        tf_seconds = tf_map.get(globals.timeframe, 60)

        if globals.last_candle_time and (now - globals.last_candle_time).total_seconds() >= tf_seconds:
            print("[Refresh] Yeni mum tespit edildi, grafik güncelleniyor.")
            show_chart()
        else:
            update_last_candle()
    except Exception as e:
        print(f"[auto_refresh_chart] {type(e).__name__}: {e}")
    globals.root.after(1000, auto_refresh_chart)


def pause_refresh(event):
    globals.should_auto_refresh.set(False)


def resume_refresh(event):
    globals.should_auto_refresh.set(True)
