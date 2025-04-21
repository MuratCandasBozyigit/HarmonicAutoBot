import pandas as pd
import numpy as np
from İndicators.AH import typee,DTB,ABCD_Formasyn
class ZigZagDetector:
    def __init__(self, length=10, deviation_threshold=0, show_zz=True, err_percent=10):
        self.length = length
        self.deviation_threshold = deviation_threshold
        self.show_zz = show_zz
        self.err_min = (100 - err_percent) / 100
        self.err_max = (100 + err_percent) / 100

        self.zigzag_lines = []
        self.zigzag_labels = []
        self.zigzag_dirs = []
        self.zigzag_ratios = []
        self.max_array_size = 10

    def get_pivot(self, df, i):
        high_idx = df['high'].iloc[i - self.length + 1:i + 1].idxmax()
        low_idx = df['low'].iloc[i - self.length + 1:i + 1].idxmin()
        ph = df['high'].iloc[high_idx] if high_idx == i else np.nan
        pl = df['low'].iloc[low_idx] if low_idx == i else np.nan
        return ph, pl

    def add_zigzag(self, x1, y1, x2, y2, direction):
        self.zigzag_lines.insert(0, ((x1, y1), (x2, y2)))
        self.zigzag_dirs.insert(0, direction)
        if len(self.zigzag_lines) >= 2:
            last_line = self.zigzag_lines[1]
            last_len = abs(last_line[1][1] - last_line[0][1])
            curr_len = abs(y2 - y1)
            ratio = round(curr_len / last_len if last_len != 0 else 0, 3)
        else:
            ratio = 0
        self.zigzag_ratios.insert(0, ratio)
        self.zigzag_labels.insert(0, {
            'text': f'{"HH" if direction == 2 else "LH" if direction == 1 else "HL" if direction == -1 else "LL"} {ratio}',
            'position': (x2, y2),
            'direction': direction
        })
        if len(self.zigzag_lines) > self.max_array_size:
            self.zigzag_lines.pop()
            self.zigzag_labels.pop()
            self.zigzag_dirs.pop()
            self.zigzag_ratios.pop()

    def run(self, df):
        last_dir = 0
        for i in range(self.length, len(df)):
            ph, pl = self.get_pivot(df, i)
            dir = 1 if not np.isnan(ph) else -1 if not np.isnan(pl) else last_dir
            if dir != last_dir and (not np.isnan(ph) or not np.isnan(pl)):
                value = ph if dir == 1 else pl
                x2, y2 = df.index[i], value
                if self.zigzag_lines:
                    x1, y1 = self.zigzag_lines[0][1]
                    change_percent = abs((y1 - y2) * 100 / y1)
                    if change_percent > self.deviation_threshold:
                        self.add_zigzag(x1, y1, x2, y2, dir)
                else:
                    x1, y1 = x2, y2
                    self.add_zigzag(x1, y1, x2, y2, dir)
                last_dir = dir
        return self.zigzag_lines, self.zigzag_labels, self.zigzag_ratios, self.zigzag_dirs
