import gc
from matplotlib.lines import Line2D
import İndicators
import Utils.globals as globals
import Cmd
import Order

opened_patterns = set()

def detect_and_draw_recent_harmonics(df, ax):
    try:
        # Önceki çizimleri temizle
        for artist in ax.lines + ax.texts:
            artist.remove()

        for i in range(12, len(df)):
            x = df.iloc[i - 12]
            a = df.iloc[i - 8]
            b = df.iloc[i - 6]
            c = df.iloc[i - 1]
            d = df.iloc[i]
            #10 8 6 4
            xX, xY = i - 12, x['low']
            aX, aY = i - 8, a['high']
            bX, bY = i - 6, b['low']
            cX, cY = i - 1, c['high']
            dX, dY = i, d['low']

            # xY = df['low'].iloc[i - 36 : i - 32].min()
            # aY = df['high'].iloc[i - 24 : i - 20].max()
            # bY = df['low'].iloc[i - 20 : i - 16].min()
            # cY = df['high'].iloc[i - 8  : i - 4].max()
            # dY = df['low'].iloc[i      : i + 1].min()


            result = İndicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)

            is_valid, gart, bat, bfly, crab, shark, cyph = result

            if is_valid:
                pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                pattern_type = [gart, bat, bfly, crab, shark, cyph]
                detected = pattern_name[pattern_type.index(True)]

                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)
                ax.plot(xs, ys, color='darkblue', linewidth=1.5,linestyle="--")
                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=8, weight='bold')

                Cmd.add_log(f"[Harmonic] {detected} pattern bulundu @ index {dX}")

                # Bu noktada en güncel mumdaysak ve emir modu açıksa
                if dX == len(df) - 2 and globals.is_order_mode_enabled:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if pattern_id not in opened_patterns:
                        Order.open_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
                        Cmd.add_log(f"[Trade Açıldı] {detected} pattern @ fiyattan {dY}")

        gc.collect()

    except Exception as e:
        Cmd.add_log(f"[harmonic_draw] {type(e).__name__}: {e}")
