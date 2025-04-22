import İndicators
import Cmd
import Order
import gc
from matplotlib.lines import Line2D
opened_patterns=set()

def detect_and_draw_recent_harmonics(df, ax):
    try:
      #  ax.clear()  # Önceki çizimleri temizle

        for i in range(4, len(df)):
            candles = df.iloc[i-4:i+1]

            # Hem bullish hem bearish kombinasyonlarını dene
            variations = [
                ("bullish", [("low", "high", "low", "high", "low")]),  # Long
                ("bearish", [("high", "low", "high", "low", "high")])  # Short
            ]

            for direction, schema_list in variations:
                for schema in schema_list:
                    x = candles.iloc[0][schema[0]]
                    a = candles.iloc[1][schema[1]]
                    b = candles.iloc[2][schema[2]]
                    c = candles.iloc[3][schema[3]]
                    d = candles.iloc[4][schema[4]]

                    xX, aX, bX, cX, dX = i-4, i-3, i-2, i-1, i
                    xY, aY, bY, cY, dY = x, a, b, c, d

                    result = İndicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
                    is_valid, gart, bat, bfly, crab, shark, cyph = result

                    if is_valid:
                        pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                        pattern_type = [gart, bat, bfly, crab, shark, cyph]
                        detected = pattern_name[pattern_type.index(True)]

                        points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                        xs, ys = zip(*points)

                        color = 'darkgreen' if direction == "bullish" else 'darkred'
                        ax.plot(xs, ys, color=color, linewidth=1.4)

                        for label, (px, py) in zip("XABCD", points):
                            ax.text(px, py, label, color='black', fontsize=8, weight='bold')

                        Cmd.add_log(f"[Harmonic] {direction.upper()} {detected} pattern bulundu @ index {dX}")

                        if dX == len(df) - 1 and globals.is_order_mode_enabled:
                            pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                            if pattern_id not in opened_patterns:
                                Order.open_position(dY, globals.symbol)
                                opened_patterns.add(pattern_id)
                                Cmd.add_log(f"[Trade Açıldı] {direction.upper()} {detected} pattern @ fiyattan {dY}")

        gc.collect()

    except Exception as e:
        Cmd.add_log(f"[harmonic_draw] {type(e).__name__}: {e}")
