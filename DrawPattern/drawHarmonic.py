import Indicators
import Order
import Utils.globals as globals
import gc

from matplotlib.lines import Line2D

opened_patterns = set()

def draw_bullish_patterns(df, ax):
    try:
        for i in range(4, len(df)):
            candles = df.iloc[i-4:i+1]
            schema = ("low", "high", "low", "high", "low")  # Bullish

            x = candles.iloc[0][schema[0]]
            a = candles.iloc[1][schema[1]]
            b = candles.iloc[2][schema[2]]
            c = candles.iloc[3][schema[3]]
            d = candles.iloc[4][schema[4]]

            xX, aX, bX, cX, dX = i-4, i-3, i-2, i-1, i
            xY, aY, bY, cY, dY = x, a, b, c, d

            result = Indicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
            is_valid, gart, bat, bfly, crab, shark, cyph = result

            if is_valid:
                pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                pattern_type = [gart, bat, bfly, crab, shark, cyph]
                detected = pattern_name[pattern_type.index(True)]

                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)

                ax.plot(xs, ys, color='darkgreen', linewidth=1.4)

                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=8, weight='bold')


                if dX == len(df) - 2 and globals.emir_acik:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if pattern_id not in opened_patterns:
                        Order.open_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
        gc.collect()

    except Exception :
        pass

def draw_bearish_patterns(df, ax):
    try:
        for i in range(4, len(df)):
            candles = df.iloc[i-4:i+1]
            schema = ("high", "low", "high", "low", "high")  # Bearish

            x = candles.iloc[0][schema[0]]
            a = candles.iloc[1][schema[1]]
            b = candles.iloc[2][schema[2]]
            c = candles.iloc[3][schema[3]]
            d = candles.iloc[4][schema[4]]

            xX, aX, bX, cX, dX = i-4, i-3, i-2, i-1, i
            xY, aY, bY, cY, dY = x, a, b, c, d

            result = Indicators.harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY)
            is_valid, gart, bat, bfly, crab, shark, cyph = result

            if is_valid:
                pattern_name = ["Gartley", "Bat", "Butterfly", "Crab", "Shark", "Cypher"]
                pattern_type = [gart, bat, bfly, crab, shark, cyph]
                detected = pattern_name[pattern_type.index(True)]

                points = [(xX, xY), (aX, aY), (bX, bY), (cX, cY), (dX, dY)]
                xs, ys = zip(*points)

                ax.plot(xs, ys, color='darkred', linewidth=1.4)

                for label, (px, py) in zip("XABCD", points):
                    ax.text(px, py, label, color='black', fontsize=8, weight='bold')


                if dX == len(df) - 2 and globals.short_emir_acik:
                    pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                    if pattern_id not in opened_patterns:
                        Order.open_short_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
        gc.collect()

    except Exception:
        pass
