#harmonic.py

import matplotlib.pyplot as plt
from indicators.classes.Obj_XABCD_Harmonic import Point, init_params, init_xabcd
from indicators.classes.harmonic_draw import draw_prz_zone, draw_targets, draw_entry_stop

def analyze_and_draw():
    # Örnek veriler (XABCD noktaları)
    x, a, b, c, d = Point(0, 100), Point(1, 120), Point(2, 95), Point(3, 115), Point(4, 105)

    # Parametreleri ayarla
    params = init_params(pct_error=20, pct_asym=200, types=[1])  # sadece Gartley

    # Harmonic objesi oluştur
    pattern = init_xabcd(x, a, b, c, d, params=params)

    # Grafik çizimi
    fig, ax = plt.subplots(figsize=(12, 6))
    if pattern:
        pattern.draw_pattern(ax, clr="green" if pattern.bull else "red")
        pattern.draw_label(ax)

        # PRZ çizimi
        prz_levels = [v for v in [pattern.prz_bN, pattern.prz_bF, pattern.prz_xN, pattern.prz_xF] if v is not None]
        draw_prz_zone(ax, prz_levels, x_start=d.x, t_limit=3)

        # Hedefler ve stop (örnek değerlerle)
        pattern.set_target(1)
        target1 = pattern.t1
        stop = d.y * 0.98 if pattern.bull else d.y * 1.02
        entry = pattern.d.y  # giriş için D noktası kullanılabilir

        draw_targets(ax, targets=[target1], x_start=d.x, t_limit=3)
        draw_entry_stop(ax, entry=entry, stop=stop, x_start=d.x, t_limit=3)

    ax.set_title("Harmonic Pattern Analysis")
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_and_draw()
