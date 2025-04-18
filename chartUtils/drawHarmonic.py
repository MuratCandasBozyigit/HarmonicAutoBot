from matplotlib.lines import Line2D
import gc
from helpers.globals import *
from trade_v01 import open_position,add_log,opened_patterns,pattern,draw_harmonic_pattern
from indicators.harmonic import harmonic_xabcd_validate
def detect_and_draw_recent_harmonics(df, ax):
    try:
        # Clear previous lines and texts from chart
        for artist in ax.lines + ax.texts:
            artist.remove()

        # Optional color-coding by pattern name
        color_map = {
            "Gartley": "green",
            "Bat": "blue",
            "Butterfly": "purple",
            "Crab": "red",
            "Shark": "orange",
            "Cypher": "teal"
        }

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

            result = harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
            is_valid, gart, bat, bfly, crab, shark, cyph = result

            if is_valid:
                pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                pattern_type = [gart, bat, bfly, crab, shark, cyph]
                detected = pattern_name[pattern_type.index(True)]

                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)
                ax.plot(xs, ys, color=color_map.get(detected, "darkgreen"), linewidth=1.4)

                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=8, weight='bold')

                ax.text(dX, dY * 1.002, f"{detected}", color='maroon', fontsize=9, weight='bold')
                add_log(f"[Harmonic] {detected} pattern bulundu @ index {dX}")

                # Check if pattern is fresh and eligible for trade
                if dX >= len(df) - 2 and emir_acik:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))

                    if pattern_id not in opened_patterns:
                        open_position(dY, symbol)
                        opened_patterns.add(pattern_id)
                        add_log(f"[Trade Açıldı] {detected} pattern @ fiyattan {dY}")
                    else:
                        add_log(f"[Zaten Açık] {detected} pattern daha önce açıldı.")
                elif not emir_acik:
                    add_log("[Emir Kontrol] Pattern bulundu ama emir modu kapalıydı.")

        gc.collect()

    except Exception as e:
        add_log(f"[harmonic_draw] {type(e).__name__}: {e}")
