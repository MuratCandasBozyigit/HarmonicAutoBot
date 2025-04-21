import Gui

should_auto_refresh = Gui.tk.BooleanVar(value=True)

def show_chart(event=None):
    global last_candle_time
    Gui.gc.collect()

    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    timeframe = globals.timeframe_var.get()

    if not symbol or not timeframe:
        Gui.messagebox.showwarning("Uyarı", "Lütfen coin ve zaman dilimi seçiniz.")
        return

    df = Gui.Utils.get_ohlcv(symbol, timeframe, limit=Gui.limit_var.get())
    if df is None or df.empty:
        Gui.messagebox.showwarning("Uyarı", "Veri alınamadı veya boş!")
        return

    df = df.dropna()
    df = df.iloc[-Gui.limit_var.get():]
    globals.df = df
    globals.symbol = symbol
    globals.timeframe = timeframe

    for widget in Gui.Gui.chart_frame.winfo_children():
        widget.destroy()

    fig, axlist = Gui.mpf.plot(
        df,
        type='candle',
        style='yahoo',
        title=symbol,
        ylabel='Fiyat',
        volume=False,
        returnfig=True
    )
    ax = axlist[0]

    Gui.detect_and_draw_recent_harmonics(df, ax)

    canvas = Gui.FigureCanvasTkAgg(fig, master=Gui.chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    globals.ax = ax
    globals.canvas = canvas
    last_candle_time = df.index[-1].to_pydatetime().replace(tzinfo=Gui.timezone.utc)
def update_last_candle():
    if globals.df is None or globals.symbol is None:
        return
    try:
        ticker = Gui.exchange.fetch_ticker(globals.symbol)
        last_price = ticker['last']
        high = max(globals.df.iloc[-1]['high'], last_price)
        low = min(globals.df.iloc[-1]['low'], last_price)

        globals.df.loc[globals.df.index[-1], 'close'] = last_price
        globals.df.loc[globals.df.index[-1], 'high'] = high
        globals.df.loc[globals.df.index[-1], 'low'] = low

        globals.ax.clear()
        Gui.mpf.plot(
            globals.df,
            type='candle',
            style='yahoo',
            ax=globals.ax,
            volume=False,
            returnfig=False
        )
        Gui.detect_and_draw_recent_harmonics(globals.df, globals.ax)
        globals.canvas.draw_idle()
        Gui.gc.collect()
    except Exception as e:
        print(f"[update_last_candle] {type(e).__name__}: {e}")
def auto_refresh_chart():
    global last_candle_time
    if not should_auto_refresh.get() or globals.df is None:
        Gui.window.after(1000, auto_refresh_chart)
        return
    try:
        now = Gui.datetime.now(Gui.timezone.utc)
        tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
        tf_seconds = tf_map.get(globals.timeframe, 60)

        if last_candle_time and (now - last_candle_time).total_seconds() >= tf_seconds:
            print("[Refresh] Yeni mum tespit edildi, grafik güncelleniyor.")
            show_chart()
        else:
            update_last_candle()
    except Exception as e:
        print(f"[auto_refresh_chart] {type(e).__name__}: {e}")
    Gui.window.after(1000, auto_refresh_chart)
def pause_refresh(event): should_auto_refresh.set(False)
def resume_refresh(event): should_auto_refresh.set(True)
