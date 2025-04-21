import ccxt
import pandas as pd
import mplfinance as mpf
import tkinter as tk
import os
import gc
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta, timezone

import İndicators
import Utils
import Utils.globals as globals
import Cmd
import Order
import Chart
# Binance Futures Exchange tanımı
exchange = ccxt.binance({
    'apiKey': globals.api_key,
    'secret': globals.api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
exchange.set_sandbox_mode(globals.use_testnet)

# Ana pencere
window = tk.Tk()
window.title("Harmonic Gözlem Paneli - v0.5")
window.geometry("1280x560")

should_auto_refresh = tk.BooleanVar(value=True)
opened_patterns = set()
last_candle_time = None

# Harmonik desenleri tespit edip çizme

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

            result = İndicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
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

                Cmd.add_log(f"[Harmonic] {detected} pattern bulundu @ index {dX}")
                 #and globals.emir_acik
                if dX == len(df) - 7:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if pattern_id not in opened_patterns:
                        Order.open_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
                        Cmd.add_log(f"[Trade Açıldı] {detected} pattern @ fiyattan {dY}")
        gc.collect()
    except Exception as e:
        Cmd.add_log(f"[harmonic_draw] {type(e).__name__}: {e}")

