class DoubleTopBottomDetector:
    def __init__(self, zigzag_lines, zigzag_dirs, max_risk_per_reward=40):
        self.zigzag_lines = zigzag_lines
        self.zigzag_dirs = zigzag_dirs
        self.max_risk_per_reward = max_risk_per_reward

    def calculate(self):
        double_top = double_bottom = False
        if len(self.zigzag_lines) >= 4 and len(self.zigzag_dirs) >= 4:
            value = self.zigzag_lines[1][1][1]
            high_low = self.zigzag_dirs[1]

            lvalue = self.zigzag_lines[2][1][1]
            lhigh_low = self.zigzag_dirs[2]

            llvalue = self.zigzag_lines[3][1][1]
            llhigh_low = self.zigzag_dirs[3]

            risk = abs(value - llvalue)
            reward = abs(value - lvalue)
            risk_per_reward = (risk * 100 / (risk + reward)) if (risk + reward) != 0 else 0

            if high_low == 1 and llhigh_low == 2 and lhigh_low == -1 and risk_per_reward < self.max_risk_per_reward:
                double_top = True
            if high_low == -1 and llhigh_low == -2 and lhigh_low == 1 and risk_per_reward < self.max_risk_per_reward:
                double_bottom = True

        return double_top, double_bottom

    def draw(self, ax=None):
        double_top, double_bottom = self.calculate()
        if double_top or double_bottom:
            line1 = self.zigzag_lines[1]
            line2 = self.zigzag_lines[2]
            x1, y1 = line2[0]
            x2, y2 = line1[1]
            midline = line1[0][1]

            risk = abs(y2 - y1)
            reward = abs(y2 - midline)
            rpr = round(risk * 100 / (risk + reward), 2) if (risk + reward) != 0 else 0

            color = 'red' if double_top else 'green'
            label_text = f"{'DT' if double_top else 'DB'} - {rpr:.2f}"

            if ax:
                ax.plot([x1, x2], [y1, y2], color=color, linewidth=2)
                ax.text(x2, y2, label_text, color=color, fontsize=10,
                        verticalalignment='bottom' if double_top else 'top')
