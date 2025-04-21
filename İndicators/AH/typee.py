from İndicators.AH import DTB, zigzag, ABCD_Formasyn
class WMHarmonicDetector:
    def __init__(self, zigzag_lines, zigzag_ratios, err_percent=10, enabled_patterns=None):
        self.zz = zigzag_lines
        self.rr = zigzag_ratios
        self.err_min = (100 - err_percent) / 100
        self.err_max = (100 + err_percent) / 100
        self.enabled_patterns = enabled_patterns or {
            'gartley': True, 'crab': True, 'deepCrab': True, 'bat': True, 'butterfly': True,
            'shark': True, 'cypher': True, 'threeDrives': True, 'fiveZero': True
        }
        self.matched_patterns = []
        self.pattern_lines = []
        self.direction = 0

    def in_range(self, val, low, high):
        return low * self.err_min <= val <= high * self.err_max

    def calculate(self):
        if len(self.zz) < 5 or len(self.rr) < 5:
            return False

        xa, ab, bc, cd = self.zz[4], self.zz[3], self.zz[2], self.zz[1]
        yxa, xab, abc, bcd = self.rr[4], self.rr[3], self.rr[2], self.rr[1]

        x = xa[0][1]
        a = xa[1][1]
        b = ab[1][1]
        c = cd[0][1]
        d = cd[1][1]

        xad = abs(a - d) / abs(x - a) if abs(x - a) != 0 else 0
        self.direction = 1 if a > d else -1

        self.pattern_lines = [xa, ab, bc, cd]
        self.matched_patterns.clear()

        def add_pattern(name, cond):
            if self.enabled_patterns.get(name, False) and cond:
                self.matched_patterns.append(name)

        add_pattern("gartley",
            self.in_range(xab, 0.618, 0.618) and
            self.in_range(abc, 0.382, 0.886) and
            (self.in_range(bcd, 1.272, 1.618) or self.in_range(xad, 0.786, 0.786))
        )

        add_pattern("crab",
            self.in_range(xab, 0.382, 0.618) and
            self.in_range(abc, 0.382, 0.886) and
            (self.in_range(bcd, 2.24, 3.618) or self.in_range(xad, 1.618, 1.618))
        )

        add_pattern("deepCrab",
            self.in_range(xab, 0.886, 0.886) and
            self.in_range(abc, 0.382, 0.886) and
            (self.in_range(bcd, 2.0, 3.618) or self.in_range(xad, 1.618, 1.618))
        )

        add_pattern("bat",
            self.in_range(xab, 0.382, 0.5) and
            self.in_range(abc, 0.382, 0.886) and
            (self.in_range(bcd, 1.618, 2.618) or self.in_range(xad, 0.886, 0.886))
        )

        add_pattern("butterfly",
            self.in_range(xab, 0.786, 0.786) and
            self.in_range(abc, 0.382, 0.886) and
            (self.in_range(bcd, 1.618, 2.618) or self.in_range(xad, 1.272, 1.618))
        )

        add_pattern("shark",
            self.in_range(abc, 1.13, 1.618) and
            self.in_range(bcd, 1.618, 2.24) and
            self.in_range(xad, 0.886, 1.13)
        )

        add_pattern("cypher",
            self.in_range(xab, 0.382, 0.618) and
            self.in_range(abc, 1.13, 1.414) and
            (self.in_range(bcd, 1.272, 2.00) or self.in_range(xad, 0.786, 0.786))
        )

        add_pattern("threeDrives",
            self.in_range(yxa, 0.618, 0.618) and
            self.in_range(xab, 1.27, 1.618) and
            self.in_range(abc, 0.618, 0.618) and
            self.in_range(bcd, 1.27, 1.618)
        )

        add_pattern("fiveZero",
            self.in_range(xab, 1.13, 1.618) and
            self.in_range(abc, 1.618, 2.24) and
            self.in_range(bcd, 0.5, 0.5)
        )

        return bool(self.matched_patterns)

    def draw(self, ax=None):
        if not self.calculate():
            return
        color = 'green' if self.direction > 0 else 'red'
        names = '\n'.join(self.matched_patterns)
        xa, ab, bc, cd = self.pattern_lines

        if ax:
            for line in [xa, ab, bc, cd]:
                ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=color, linewidth=2)
            ax.text(cd[1][0], cd[1][1], names, color=color, fontsize=10,
                    va='bottom' if self.direction < 0 else 'top')
