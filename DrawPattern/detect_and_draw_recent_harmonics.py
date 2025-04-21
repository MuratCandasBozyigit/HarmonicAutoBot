from matplotlib.lines import Line2D
import gc
import İndicators
import Cmd
import Order
import Utils
opened_patterns = set()

def detect_and_draw_recent_harmonics_1(df, ax):
    try:
        # Önce önceki çizimleri sil
        for artist in ax.lines + ax.texts:
            artist.remove()

        # Zigzag çıkarımı
        zz = İndicators.zigzag(length=10, deviation_threshold=0)
        zz.run(df)

        # Harmonik Pattern çizimleri
        abcd = İndicators.ABCD_Formasyn(zz.zigzag_lines, zz.zigzag_ratios)
        abcd.draw_abcd(ax=ax)

        dtb = İndicators.DTB(zz.zigzag_lines, zz.zigzag_dirs)
        dtb.draw(ax=ax)

        wm = İndicators.WMFormasyon(zz.zigzag_lines, zz.zigzag_ratios)
        wm.draw(ax=ax)

        # Trade & log kontrolü — en son point D'ye göre
        if len(zz.zigzag_lines) >= 5:
            last_line = zz.zigzag_lines[1]
            dX, dY = last_line[1]
            dX = int(dX)
            x, a, b, c = zz.zigzag_lines[4], zz.zigzag_lines[3], zz.zigzag_lines[2], zz.zigzag_lines[1]
            xY, aY, bY, cY = x[0][1], a[1][1], b[1][1], c[0][1]

            if dX == len(df) - 7 and globals.emir_acik:
                pattern_id = hash((round(xY, 2), round(aY, 2), round(bY, 2), round(cY, 2), round(dY, 2)))
                if globals.emir_acik:
                    if pattern_id not in opened_patterns:
                        Order.open_position(dY, globals.symbol)
                        opened_patterns.add(pattern_id)
                    Cmd.add_log(f"[Trade Açıldı] Harmonik pattern @ fiyattan {dY}")
                else:
                    Cmd.add_log("[Emir Kontrol] Pattern bulundu ama emir modu kapalıydı.")

        gc.collect()

    except Exception as e:
        globals.add_log(f"[harmonic_draw] {type(e).__name__}: {e}")
