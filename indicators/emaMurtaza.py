from ta.trend import ema_indicator
from ta.momentum import RSIIndicator
import mplfinance as mpf
import pandas as pd

def murtaza(df):
    if len(df) < 200:
        print("[murtaza] Yeterli veri yok (en az 200 bar gerekli)")
        return []

    try:
        df['ema_50'] = ema_indicator(df['close'], window=50)
        df['ema_200'] = ema_indicator(df['close'], window=200)
        df['rsi'] = RSIIndicator(df['close'], window=14).rsi()

        df['bullish'] = df['ema_50'] > df['ema_200']
        df['bearish'] = df['ema_50'] < df['ema_200']

        df['rsi_cross_up'] = (df['rsi'] > 50) & (df['rsi'].shift(1) <= 50)
        df['rsi_cross_down'] = (df['rsi'] < 50) & (df['rsi'].shift(1) >= 50)

        df['long_signal'] = df['bullish'] & df['rsi_cross_up']
        df['short_signal'] = df['bearish'] & df['rsi_cross_down']

        buy_plot = df['close'].where(df['long_signal'])
        sell_plot = df['close'].where(df['short_signal'])

        plots = [
            mpf.make_addplot(df['ema_50'], color='blue', width=1, label='EMA 50'),
            mpf.make_addplot(df['ema_200'], color='red', width=1, label='EMA 200'),
            mpf.make_addplot(buy_plot, type='scatter', marker='^', markersize=100, color='green'),
            mpf.make_addplot(sell_plot, type='scatter', marker='v', markersize=100, color='red')
        ]

        return plots
    except Exception as e:
        print(f"[murtaza] {type(e).__name__}: {e}")
        return []
