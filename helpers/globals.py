import tkinter as tk

should_auto_refresh = tk.BooleanVar(value=True)
opened_patterns = set()
emir_acik = False
aktif_emir_id = None
last_candle_time = None
df = None
canvas = None
fig = None
ax = None
symbol = None
timeframe = None
