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
        return

    df = Utils.get_ohlcv(symbol, timeframe, limit=globals.limit_var.get())
    if df is None or df.empty:
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
    canvas.get_tk_widget().pack(fill="both", expand=True)

    globals.ax = ax
    globals.canvas = canvas
    globals.last_candle_time = df.index[-1].to_pydatetime().replace(tzinfo=timezone.utc)


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
    except Exception :
        pass


def auto_refresh_chart():
    if not globals.should_auto_refresh.get():
        globals.root.after(1000, auto_refresh_chart)
        return
    try:
        now = datetime.now(timezone.utc)
        tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
        tf_seconds = tf_map.get(globals.timeframe, 60)

        if globals.last_candle_time and (now - globals.last_candle_time).total_seconds() >= tf_seconds:
           
            show_chart()
        else:
            update_last_candle()
    except Exception :
        pass
    globals.root.after(1000, auto_refresh_chart)


def pause_refresh(event):
    globals.should_auto_refresh.set(False)


def resume_refresh(event):
    globals.should_auto_refresh.set(True)
