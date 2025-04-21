from İndicators.AH import ABCD_Formasyn, zigzag, typee

class DoubleTopBottomDetector:
    def __init__(self, zigzag_lines, zigzag_dirs, max_risk_per_reward=40):
        self.zigzag_lines = zigzag_lines
        self.zigzag_dirs = zigzag_dirs
        self.max_risk_per_reward = max_risk_per_reward
        self.result = None  # 'double_top' veya 'double_bottom'

    def calculate(self):
        if len(self.zigzag_lines) < 4 or len(self.zigzag_dirs) < 4:
            return False

        # Son 3 zirve/dip noktası
        val1 = self.zigzag_lines[1][1][1]
        dir1 = self.zigzag_dirs[1]

        val2 = self.zigzag_lines[2][1][1]
        dir2 = self.zigzag_dirs[2]

        val3 = self.zigzag_lines[3][1][1]
        dir3 = self.zigzag_dirs[3]

        # Double Top
        if dir1 == 1 and dir3 == 1 and abs(val1 - val3) / val3 < 0.01:  # %1'lik fark toleransı
            self.result = 'double_top'
            return True

        # Double Bottom
        if dir1 == -1 and dir3 == -1 and abs(val1 - val3) / val3 < 0.01:
            self.result = 'double_bottom'
            return True

        return False

    def draw(self, ax=None):
        if not self.result:
            return

        color = 'blue'
        label = 'Double Top' if self.result == 'double_top' else 'Double Bottom'

        # Çizim için son iki tepe/dip noktaları
        p1 = self.zigzag_lines[1][1]
        p2 = self.zigzag_lines[3][1]

        if ax:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linestyle='--', color=color, linewidth=2)
            ax.text(p2[0], p2[1], label, color=color, fontsize=10,
                    va='bottom' if self.result == 'double_bottom' else 'top')
