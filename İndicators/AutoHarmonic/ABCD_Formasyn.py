class HarmonicPatterns:
    def __init__(self, zigzag_lines, zigzag_ratios, err_percent=10, abcd_types_enabled=(True, True, True)):
        self.zigzag_lines = zigzag_lines
        self.zigzag_ratios = zigzag_ratios
        self.err_min = (100 - err_percent) / 100
        self.err_max = (100 + err_percent) / 100
        self.abcd_types_enabled = abcd_types_enabled  # (classic, ab=cd, ext)

        self.abcd_lines = []
        self.abcd_type = None
        self.abcd_direction = None

    def calculate_abcd(self):
        if len(self.zigzag_ratios) >= 3 and len(self.zigzag_lines) >= 4:
            abc_ratio = self.zigzag_ratios[2]
            bcd_ratio = self.zigzag_ratios[1]

            ab = self.zigzag_lines[3]
            bc = self.zigzag_lines[2]
            cd = self.zigzag_lines[1]

            ab_time = abs(ab[1][0] - ab[0][0])
            ab_price = abs(ab[1][1] - ab[0][1])
            cd_time = abs(cd[1][0] - cd[0][0])
            cd_price = abs(cd[1][1] - cd[0][1])

            a, b_ = ab[0][1], ab[1][1]
            c, d = cd[0][1], cd[1][1]

            direction = 0
            is_bullish = a < b_ < d and a < c < d
            is_bearish = a > b_ > d and a > c > d
            direction = 1 if is_bullish else -1 if is_bearish else 0

            time_ratio = cd_time / ab_time if ab_time != 0 else 0
            price_ratio = cd_price / ab_price if ab_price != 0 else 0

            match_type = None
            if self.abcd_types_enabled[0] and 0.618 * self.err_min <= abc_ratio <= 0.786 * self.err_max and \
               1.272 * self.err_min <= bcd_ratio <= 1.618 * self.err_max and direction != 0:
                match_type = "Classic ABCD"
            elif self.abcd_types_enabled[1] and self.err_min <= time_ratio <= self.err_max and \
                 self.err_min <= price_ratio <= self.err_max and direction != 0:
                match_type = "AB=CD"
            elif self.abcd_types_enabled[2] and price_ratio >= 1.272 * self.err_min and price_ratio <= 1.618 * self.err_max and \
                 0.618 * self.err_min <= abc_ratio <= 0.786 * self.err_max and direction != 0:
                match_type = "ABCD Extension"

            if match_type:
                self.abcd_lines = [ab, bc, cd]
                self.abcd_type = match_type
                self.abcd_direction = direction
                return True
        return False

    def draw_abcd(self, ax=None):
        if self.calculate_abcd():
            color = 'red' if self.abcd_direction > 0 else 'green'
            for line in self.abcd_lines:
                (x1, y1), (x2, y2) = line
                if ax:
                    ax.plot([x1, x2], [y1, y2], color=color, linewidth=2)
            label_text = self.abcd_type
            (x_end, y_end) = self.abcd_lines[-1][1]
            if ax:
                ax.text(x_end, y_end, label_text, color=color, fontsize=10, ha='center', va='bottom' if self.abcd_direction > 0 else 'top')
