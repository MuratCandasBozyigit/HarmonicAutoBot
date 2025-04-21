import numpy as np



class AutoHarmonic:
    def __init__(self, df, length=10, err_percent=10, deviation_threshold=0):
        self.df = df
        self.length = length
        self.err_min = (100 - err_percent) / 100
        self.err_max = (100 + err_percent) / 100
        self.deviation_threshold = deviation_threshold
        self.zigzag_lines = []
        self.zigzag_dirs = []
        self.zigzag_ratios = []
        self.abcd = None
        self.double_top = False
        self.double_bottom = False

    def get_pivot(self, i):
        high_idx = self.df['high'].iloc[i - self.length + 1:i + 1].idxmax()
        low_idx = self.df['low'].iloc[i - self.length + 1:i + 1].idxmin()
        ph = self.df['high'].iloc[high_idx] if high_idx == i else np.nan
        pl = self.df['low'].iloc[low_idx] if low_idx == i else np.nan
        return ph, pl

    def run_zigzag(self):
        last_dir = 0
        for i in range(self.length, len(self.df)):
            ph, pl = self.get_pivot(i)
            dir = 1 if not np.isnan(ph) else -1 if not np.isnan(pl) else last_dir
            if dir != last_dir and (not np.isnan(ph) or not np.isnan(pl)):
                value = ph if dir == 1 else pl
                x2 = i
                y2 = value
                if self.zigzag_lines:
                    x1, y1 = self.zigzag_lines[-1][1]
                    change_percent = abs((y1 - y2) * 100 / y1)
                    if change_percent > self.deviation_threshold:
                        self.zigzag_lines.append(((x1, y1), (x2, y2)))
                        self.zigzag_dirs.append(dir)
                        last_len = abs(y1 - y2)
                        prev_len = abs(self.zigzag_lines[-2][1][1] - self.zigzag_lines[-2][0][1]) if len(self.zigzag_lines) > 1 else last_len
                        ratio = round(last_len / prev_len, 3) if prev_len != 0 else 0
                        self.zigzag_ratios.append(ratio)
                else:
                    self.zigzag_lines.append(((x2, y2), (x2, y2)))
                    self.zigzag_dirs.append(dir)
                    self.zigzag_ratios.append(0)
                last_dir = dir

    def detect_abcd(self):
        if len(self.zigzag_ratios) >= 3 and len(self.zigzag_lines) >= 4:
            abc_ratio = self.zigzag_ratios[-3]
            bcd_ratio = self.zigzag_ratios[-2]
            ab = self.zigzag_lines[-4]
            bc = self.zigzag_lines[-3]
            cd = self.zigzag_lines[-2]
            ab_len = abs(ab[1][1] - ab[0][1])
            cd_len = abs(cd[1][1] - cd[0][1])
            ab_time = abs(ab[1][0] - ab[0][0])
            cd_time = abs(cd[1][0] - cd[0][0])
            price_ratio = cd_len / ab_len if ab_len != 0 else 0
            time_ratio = cd_time / ab_time if ab_time != 0 else 0
            if (0.618 * self.err_min <= abc_ratio <= 0.786 * self.err_max and
                1.272 * self.err_min <= bcd_ratio <= 1.618 * self.err_max):
                self.abcd = [ab, bc, cd]

    def detect_double_top_bottom(self):
        if len(self.zigzag_dirs) >= 4:
            y1 = self.zigzag_lines[-2][1][1]
            y2 = self.zigzag_lines[-3][1][1]
            y3 = self.zigzag_lines[-4][1][1]
            d1 = self.zigzag_dirs[-2]
            d2 = self.zigzag_dirs[-3]
            d3 = self.zigzag_dirs[-4]
            risk = abs(y1 - y3)
            reward = abs(y1 - y2)
            rpr = risk * 100 / (risk + reward) if (risk + reward) != 0 else 0
            if d1 == 1 and d3 == 2 and d2 == -1 and rpr < 40:
                self.double_top = True
            if d1 == -1 and d3 == -2 and d2 == 1 and rpr < 40:
                self.double_bottom = True

    def draw(self, ax):
        for line in self.zigzag_lines:
            (x1, y1), (x2, y2) = line
            ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1)
        if self.abcd:
            for line in self.abcd:
                (x1, y1), (x2, y2) = line
                ax.plot([x1, x2], [y1, y2], color='blue', linewidth=2)
            ax.text(self.abcd[-1][1][0], self.abcd[-1][1][1], 'ABCD', color='blue')
        if self.double_top or self.double_bottom:
            line1 = self.zigzag_lines[-2]
            line2 = self.zigzag_lines[-3]
            x1, y1 = line2[0]
            x2, y2 = line1[1]
            ax.plot([x1, x2], [y1, y2], color='red' if self.double_top else 'green', linewidth=2)
            ax.text(x2, y2, 'DT' if self.double_top else 'DB', color='red' if self.double_top else 'green')

    def run(self):
        self.run_zigzag()
        self.detect_abcd()
        self.detect_double_top_bottom()
