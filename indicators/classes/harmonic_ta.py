"""
harmonic_ta.py

Bu dosya, Pine Script “TA” kütüphanesindeki genel teknik analiz fonksiyonlarının
Python karşılığını içerir. Fonksiyonlar arasında boğa/ayı divergansı tespiti,
harmonik XABCD oranları, PRZ hesaplamaları, Fibonacci oranları, skorlamalar, hedef ve stop
hesaplamaları bulunur.

Not: Aşağıdaki hesaplamalar örnek/dummy implemantasyonlardır. Gerçek veriye
uygun hesaplama yapmak için pivot, standart sapma, ve diğer seri fonksiyonlarını
uygulamanız gerekebilir (örneğin pandas, numpy, TA-Lib vb.). 
"""

import math
from statistics import stdev, mean
from typing import List, Tuple, Optional

# -------------------------------------------------------
# Fibonacci yardımcı fonksiyonları
# -------------------------------------------------------
def fib_precise(ratio: float) -> float:
    """
    Belirtilen Fibonacci oranını döndürür (örnek uygulanmıştır).
    Gerçek hesaplamada bu oran sabitleri kullanılabilir.
    """
    return ratio  # orijinal değer döndürülüyor

def fib_from_string(s: str) -> float:
    """
    Fibonacci oranı yazısını alır ve sayısal değeri döndürür.
    Örneğin: ".618" -> 0.618.
    """
    try:
        # Eğer string nokta ile başlıyorsa
        return float(s)
    except:
        return 0.0

# -------------------------------------------------------
# Algebra yardımcı fonksiyonları
# -------------------------------------------------------
def line_from_xy(x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
    """
    İki noktadan çizgi denklemi hesaplar. (eğim, y-kesişim)
    """
    if x2 != x1:
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf')
    y_int = y1 - slope * x1
    return slope, y_int

def line_get_price(x: float, slope: float, y_int: float) -> float:
    """
    Verilen x değeri için çizgi denklemi kullanılarak fiyatı (y) hesaplar.
    """
    return slope * x + y_int

# -------------------------------------------------------
# Genel yardımcı fonksiyonlar
# -------------------------------------------------------
def deltaStrength(y1: float, y2: float, std: Optional[float]) -> float:
    """
    İki değer arasındaki mutlak farkı, mevcut standart sapmaya göre normalize eder.
    Standart sapma yoksa yüzde değişimi kullanır.
    """
    if std is not None and std != 0:
        return abs(y2 - y1) / (std * 2)
    elif y1 != 0 and abs(y1) > abs(y2):
        return 1 - abs(y2 / y1)
    elif y2 != 0 and abs(y2) > abs(y1):
        return 1 - abs(y1 / y2)
    elif y1 == y2:
        return 0.0
    else:
        return 0.5

# Dummy pivot ve standart sapma fonksiyonları (kendi TA kütüphanenizi entegre edin)
def pivotlow(series: List[float], left: int, right: int) -> List[Optional[float]]:
    """
    series üzerinde pivot low noktalarını bulur. Örnek implemantasyondur.
    Gerçek kullanım için TA kütüphanesi entegrasyonu gerekir.
    Dönen liste, her bar için pivot low değeri (varsa) veya None içerir.
    """
    n = len(series)
    pivots = [None] * n
    for i in range(left, n - right):
        window = series[i-left:i+right+1]
        if series[i] == min(window):
            pivots[i] = series[i]
    return pivots

def pivothigh(series: List[float], left: int, right: int) -> List[Optional[float]]:
    n = len(series)
    pivots = [None] * n
    for i in range(left, n - right):
        window = series[i-left:i+right+1]
        if series[i] == max(window):
            pivots[i] = series[i]
    return pivots

def stdev_series(series: List[float], period: int) -> float:
    """
    Verilen serinin son 'period' elemanı için standart sapmayı hesaplar.
    """
    if len(series) < period:
        period = len(series)
    return stdev(series[-period:]) if period > 1 else 0.0

# -------------------------------------------------------
# Divergence Fonksiyonları
# -------------------------------------------------------
def div_bull(pS: List[float], iS: List[float],
             cp_length_after: int = 2, cp_length_before: int = 4, pivot_length: int = 4,
             lookback: int = 50, lookback_pivs: int = 5, no_broken: bool = True,
             pW: float = 1.0, iW: float = 1.0, hidW: float = 0.8, regW: float = 1.2,
             current_bar: int = None) -> Tuple[bool, float, int, int, float, int, float]:
    """
    Boğa divergansı hesaplar.
    
    Parametreler:
      pS: Fiyat serisi (liste)
      iS: Gösterge serisi (liste)
      Diğer parametreler, Pine Script’deki gibi pivot uzunlukları ve ağırlıklar.
      current_bar: Mevcut bar indexi (Python’da dizin kullanımı için gerekli)
    
    Dönen değer:
      (flag, degree, type, lx1, ly1, lx2, ly2)
    """
    # Dummy implementasyon: Gerçek TA hesaplamaları için pivot algoritmaları entegre edilmelidir.
    if current_bar is None:
        current_bar = len(pS) - 1
    # Pivot hesaplamalarını dummy olarak alalım:
    p = pivotlow(pS, pivot_length, pivot_length)
    cpp = pivotlow(pS, cp_length_before, cp_length_after)
    ip = pivotlow(iS, pivot_length, pivot_length)
    # Dummy: ix1 = indeksi mevcut barın % olarak belirle
    ix1 = current_bar - cp_length_after if current_bar - cp_length_after >= 0 else 0
    pStd = stdev_series(pS, 100)
    iStd = stdev_series(iS, 100)
    flag = False
    degree = 0.0
    div_type = 0
    lx1 = lx2 = 0
    ly1 = ly2 = 0.0
    j = 0
    # Eğer cpp varsa (dummy kontrol)
    if any(v is not None for v in cpp):
        for i in range(cp_length_after, lookback + cp_length_after):
            if j == lookback_pivs:
                break
            # Pivot tespiti (dummy kontrol, gerçek koşul gerektirir)
            if i < len(p) and p[i] is not None:
                j += 1
                # İndeks belirleme, basitleştirilmiş
                ix2 = i + pivot_length if i + pivot_length < len(iS) else i
                if p[i] > pS[cp_length_after] and iS[ix2] < iS[ix1]:
                    flag = True
                    degree = (deltaStrength(p[i], pS[cp_length_after], pStd) * pW +
                              deltaStrength(iS[ix1], iS[ix2], iStd) * iW) * regW
                    div_type = 1
                elif p[i] < pS[cp_length_after] and iS[ix2] > iS[ix1]:
                    flag = True
                    degree = (deltaStrength(p[i], pS[cp_length_after], pStd) * pW +
                              deltaStrength(iS[ix1], iS[ix2], iStd) * iW) * hidW
                    div_type = 2
                if flag:
                    lx1 = current_bar - i - pivot_length
                    ly1 = p[i]
                    lx2 = current_bar - cp_length_after
                    ly2 = pS[cp_length_after]
                    # Burada trend hattının bozulup bozulmadığını kontrol etmek gerekir.
                    if no_broken:
                        for k in range(lx1, lx2 + 1):
                            # Dummy kontrol
                            if k < len(pS) and pS[k] < (line_get_price(k, 0, 0) * 0.99):
                                flag = False
                                degree = 0.0
                                div_type = 0
                                lx1 = 0
                                ly1 = 0.0
                                lx2 = 0
                                ly2 = 0.0
                                break
                    break
    return flag, degree, div_type, lx1, ly1, lx2, ly2

def div_bear(pS: List[float], iS: List[float],
             cp_length_after: int = 2, cp_length_before: int = 4, pivot_length: int = 4,
             lookback: int = 50, lookback_pivs: int = 5, no_broken: bool = True,
             pW: float = 1.0, iW: float = 1.0, hidW: float = 0.8, regW: float = 1.2,
             current_bar: int = None) -> Tuple[bool, float, int, int, float, int, float]:
    """
    Ayı divergansı hesaplar.
    
    Dönen değerler: (flag, degree, type, lx1, ly1, lx2, ly2)
    """
    if current_bar is None:
        current_bar = len(pS) - 1
    p = pivothigh(pS, pivot_length, pivot_length)
    cpp = pivothigh(pS, cp_length_before, cp_length_after)
    ip = pivothigh(iS, pivot_length, pivot_length)
    ix1 = current_bar - cp_length_after if current_bar - cp_length_after >= 0 else 0
    pStd = stdev_series(pS, 100)
    iStd = stdev_series(iS, 100)
    flag = False
    degree = 0.0
    div_type = 0
    lx1 = lx2 = 0
    ly1 = ly2 = 0.0
    j = 0
    if any(v is not None for v in cpp):
        for i in range(cp_length_after, lookback + cp_length_after):
            if j == lookback_pivs:
                break
            if i < len(p) and p[i] is not None:
                j += 1
                ix2 = i + pivot_length if i + pivot_length < len(iS) else i
                if p[i] > pS[cp_length_after] and iS[ix2] < iS[ix1]:
                    flag = True
                    degree = (deltaStrength(p[i], pS[cp_length_after], pStd) * pW +
                              deltaStrength(iS[ix1], iS[ix2], iStd) * iW) * hidW
                    div_type = 2
                elif p[i] < pS[cp_length_after] and iS[ix2] > iS[ix1]:
                    flag = True
                    degree = (deltaStrength(p[i], pS[cp_length_after], pStd) * pW +
                              deltaStrength(iS[ix1], iS[ix2], iStd) * iW) * regW
                    div_type = 1
                if flag:
                    lx1 = current_bar - i - pivot_length
                    ly1 = p[i]
                    lx2 = current_bar - cp_length_after
                    ly2 = pS[cp_length_after]
                    if no_broken:
                        for k in range(lx1, lx2 + 1):
                            if k < len(pS) and pS[k] > (line_get_price(k, 0, 0) * 1.01):
                                flag = False
                                degree = 0.0
                                div_type = 0
                                lx1 = 0
                                ly1 = 0.0
                                lx2 = 0
                                ly2 = 0.0
                                break
                    break
    return flag, degree, div_type, lx1, ly1, lx2, ly2

# -------------------------------------------------------
# Harmonic XABCD Fonksiyonları
# -------------------------------------------------------
def harmonic_xabcd_prz(tp: int, xY: float, aY: float, bY: float, cY: float) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    Belirtilen harmonic tip için PRZ (Potansiyel Ters Dönüş Zonası) seviyelerini hesaplar.
    tp: harmonic pattern tipi (1 = Gartley, 2 = Bat, 3 = Butterfly, 4 = Crab, 5 = Shark, 6 = Cypher)
    """
    f1618 = fib_precise(1.618)
    f2618 = fib_precise(2.618)
    f786 = fib_precise(0.786)
    f886 = fib_precise(0.886)
    f1272 = fib_precise(1.272)
    bc_u = bc_l = xa_u = xa_l = None
    bc = cY - bY
    xa = aY - xY
    xc = cY - xY
    if tp == 1:  # Gartley
        bc_u = cY - (f1272 * bc)
        bc_l = cY - (f1618 * bc)
        xa_u = aY - (f786 * xa)
    elif tp == 2:  # Bat
        bc_u = cY - (f1618 * bc)
        bc_l = cY - (f2618 * bc)
        xa_u = aY - (f886 * xa)
    elif tp == 3:  # Butterfly
        bc_u = cY - (f1618 * bc)
        bc_l = cY - (f2618 * bc)
        xa_u = aY - (f1272 * xa)
        xa_l = aY - (f1618 * xa)
    elif tp == 4:  # Crab
        bc_u = cY - (2.24 * bc)
        bc_l = cY - (3.618 * bc)
        xa_u = aY - (f1618 * xa)
    elif tp == 5:  # Shark
        bc_u = cY - (f1618 * bc)
        bc_l = cY - (2.24 * bc)
        xa_u = aY - (f886 * xa)
        xa_l = aY - (1.13 * xa)
    elif tp == 6:  # Cypher
        xa_u = cY - (f786 * xc)
    return bc_u, bc_l, xa_u, xa_l

def harmonic_xabcd_przClosest(l1: Optional[float], l2: Optional[float],
                              l3: Optional[float], l4: Optional[float] = None) -> Tuple[Optional[float], Optional[float]]:
    """
    İki en yakın PRZ seviyesini belirler.
    """
    levels = [v for v in [l1, l2, l3, l4] if v is not None]
    if not levels:
        return None, None
    levels.sort()
    if len(levels) == 1:
        return levels[0], levels[0]
    elif len(levels) == 2:
        return levels[0], levels[1]
    else:
        # İlk iki arasındaki mesafe küçük ise seç
        lL, lH = levels[0], levels[1]
        ld = lH - lL
        if len(levels) > 2 and (levels[2] - levels[1] < ld):
            lL, lH = levels[1], levels[2]
        if len(levels) == 4 and (levels[3] - levels[2] < (lH - lL)):
            lL, lH = levels[2], levels[3]
        return lL, lH

def harmonic_xabcd_przRange(l1: float, l2: Optional[float] = None,
                             l3: Optional[float] = None, l4: Optional[float] = None) -> Tuple[float, float]:
    """
    En yüksek ve en düşük PRZ seviyelerini döndürür.
    """
    levels = [v for v in [l1, l2, l3, l4] if v is not None]
    return max(levels), min(levels)

def harmonic_xabcd_eD(cpl1: float, cpl2: float, xY: float, aY: float, dY: float) -> float:
    """
    Nokta D'nin, confluent PRZ seviyelerine yakınlık oranını (XA yüksekliğine göre) hesaplar.
    """
    h = abs(aY - xY)
    dCpl = abs(cpl2 - dY) if abs(cpl1 - dY) > abs(cpl2 - dY) else abs(cpl1 - dY)
    return dCpl / h if h != 0 else 0.0

def harmonic_xabcd_przScore(xY: float, aY: float, l1: Optional[float] = None, l2: Optional[float] = None,
                            l3: Optional[float] = None, l4: Optional[float] = None) -> Tuple[float, Optional[float], Optional[float]]:
    """
    İki en yakın PRZ arasındaki yakınlığın (XA yüksekliğine göre) skorunu hesaplar.
    """
    h = abs(aY - xY)
    v1, v2 = harmonic_xabcd_przClosest(l1, l2, l3, l4)
    score = 1 - ((v2 - v1) / h) if h != 0 else 0.0
    return score, v1, v2

def harmonic_xabcd_rAndE(tp: int, l: str, l1: float, l2: float) -> Tuple[Optional[float], Optional[float]]:
    """
    İki leg arasındaki oranı ve teorik harmonic orana göre % hata değerini hesaplar.
    l: leg id ("xab", "abc", "bcd", "xad")
    """
    f1618 = fib_precise(1.618)
    f2618 = fib_precise(2.618)
    f786 = fib_precise(0.786)
    f886 = fib_precise(0.886)
    f1272 = fib_precise(1.272)
    f618 = fib_precise(0.618)
    f382 = fib_precise(0.382)
    f1414 = fib_precise(1.414)
    r = None
    e = None
    if l == "xab":
        r = abs(l1) / abs(l2) if abs(l2) != 0 else None
        if r is not None:
            if tp == 1:
                e = abs(1 - (r / f618))
            elif tp == 2:
                e = min(abs(1 - (r / f382)), abs(1 - (r / 0.5)))
            elif tp == 3:
                e = abs(1 - (r / f786))
            elif tp == 4:
                e = min(abs(1 - (r / f382)), abs(1 - (r / f618)))
            elif tp == 5:
                e = None
            elif tp == 6:
                e = min(abs(1 - (r / f382)), abs(1 - (r / f618)))
    elif l == "abc":
        r = abs(l1) / abs(l2) if abs(l2) != 0 else None
        if r is not None:
            if tp in [5]:
                e = min(abs(1 - (r / 1.13)), abs(1 - (r / f1618)))
            elif tp in [6]:
                e = min(abs(1 - (r / f1272)), abs(1 - (r / f1414)))
            else:
                e = min(abs(1 - (r / f382)), abs(1 - (r / f886)))
    elif l == "bcd":
        r = abs(l1) / abs(l2) if abs(l2) != 0 else None
        if r is not None:
            if tp == 1:
                e = min(abs(1 - (r / f1272)), abs(1 - (r / f1618)))
            elif tp == 2 or tp == 3:
                e = min(abs(1 - (r / f1618)), abs(1 - (r / f2618)))
            elif tp == 4:
                e = min(abs(1 - (r / 2.24)), abs(1 - (r / 3.618)))
            elif tp == 5:
                e = min(abs(1 - (r / f1618)), abs(1 - (r / 2.24)))
            elif tp == 6:
                e = None
    elif l == "xad":
        r = abs(l1) / abs(l2) if abs(l2) != 0 else None
        if r is not None:
            if tp == 1:
                e = abs(1 - (r / f786))
            elif tp == 2:
                e = abs(1 - (r / f886))
            elif tp == 3:
                e = min(abs(1 - (r / f1272)), abs(1 - (r / f1618)))
            elif tp == 4:
                e = abs(1 - (r / f1618))
            elif tp == 5:
                e = min(abs(1 - (r / f886)), abs(1 - (r / 1.13)))
            elif tp == 6:
                e = abs(1 - (r / f786))
    return r, e

def harmonic_xabcd_eAvg(xbre: Optional[float], acre: Optional[float],
                          bdre: Optional[float], xdre: Optional[float],
                          xcdre: Optional[float] = None) -> float:
    """
    Ortalama % hata değerini hesaplar.
    """
    lst = [v for v in [xbre, acre, bdre, xdre, xcdre] if v is not None]
    return mean(lst) if lst else 0.0

def pat_xabcd_asym(xX: int, aX: int, bX: int, cX: int, dX: Optional[int] = None) -> float:
    """
    Leg ΔX’lerinin asimetri yüzdesini hesaplar.
    """
    if dX is None:
        xa = abs(1 - ((aX - xX) / (((bX - aX) + (cX - bX)) / 2)))
        ab = abs(1 - ((bX - aX) / (((aX - xX) + (cX - bX)) / 2)))
        bc = abs(1 - ((cX - bX) / (((aX - xX) + (bX - aX)) / 2)))
        return (xa + ab + bc) / 3
    else:
        xa = abs(1 - ((aX - xX) / (((bX - aX) + (cX - bX) + (dX - cX)) / 3)))
        ab = abs(1 - ((bX - aX) / (((aX - xX) + (cX - bX) + (dX - cX)) / 3)))
        bc = abs(1 - ((cX - bX) / (((aX - xX) + (bX - aX) + (dX - cX)) / 3)))
        cd = abs(1 - ((dX - cX) / (((aX - xX) + (bX - aX) + (cX - bX)) / 3)))
        return (xa + ab + bc + cd) / 4

def harmonic_xabcd_score(tp: int, xX: int, xY: float, aX: int, aY: float,
                           bX: int, bY: float, cX: int, cY: float,
                           dX: Optional[int] = None, dY: Optional[float] = None) -> Tuple[float, float, float, float, float, float, float]:
    """
    Harmonic pattern skoru için gerekli alt skorları hesaplar.
    Dönen değerler: (eavg, asym, eD, przscore, dev, cpl1, cpl2)
    """
    _, xbre = harmonic_xabcd_rAndE(tp, "xab", aY - bY, aY - xY)
    _, acre = harmonic_xabcd_rAndE(tp, "abc", cY - bY, aY - bY)
    _, bdre = harmonic_xabcd_rAndE(tp, "bcd", (cY - dY) if dY is not None else 0, cY - bY)
    _, xdre = harmonic_xabcd_rAndE(tp, "xad", (cY - dY if tp==6 and dY is not None else aY - dY) if dY is not None else 0, (cY - xY if tp==6 else aY - xY))
    bcN, bcF, xaN, xaF = harmonic_xabcd_prz(tp, xY, aY, bY, cY)
    przscore, cpl1, cpl2 = harmonic_xabcd_przScore(xY, aY, bcN, bcF, xaN, xaF)
    eavg = harmonic_xabcd_eAvg(xbre, acre, bdre, xdre)
    asym = pat_xabcd_asym(xX, aX, bX, cX, dX)
    eD = harmonic_xabcd_eD(cpl1, cpl2, xY, aY, dY) if dY is not None else 0.0
    # dev: örnek olarak, pattern’in ortalama sapması; burada dummy hesaplama
    dev = 1 - 0.0  
    return eavg, asym, eD, przscore, dev, cpl1, cpl2

def harmonic_xabcd_scoreTot(asym: float, eavg: float, przscore: float,
                              eD: float, tp: int, w_a: float,
                              w_e: float, w_p: float, w_d: float) -> float:
    """
    Toplam ağırlıklı skoru hesaplar.
    """
    if eD is not None:
        if tp == 6:
            return ((1 - asym) * w_a + (1 - eavg) * w_e + (1 - eD) * w_d) / (w_a + w_e + w_d)
        else:
            return ((1 - asym) * w_a + (1 - eavg) * w_e + przscore * w_p + (1 - eD) * w_d) / (w_a + w_e + w_p + w_d)
    else:
        if tp == 6:
            return ((1 - asym) * w_a + (1 - eavg) * w_e) / (w_a + w_e)
        else:
            return ((1 - asym) * w_a + (1 - eavg) * w_e + przscore * w_p) / (w_a + w_e + w_p)

def resolveTarget(tgt: str, xY: float, aY: float, bY: float, cY: float, dY: float) -> float:
    """
    Hedef seviye metnini çözerek hedef fiyatı hesaplar.
    Örnek: ".618 AD" -> Fibonacci oranı ile hesaplanır.
    """
    parts = tgt.split(" ")
    if len(parts) == 1:
        if tgt == "A":
            return aY
        elif tgt == "B":
            return bY
        elif tgt == "C":
            return cY
        else:
            return 0.0
    else:
        r = fib_from_string(parts[0])
        def targetBasis(basis: str) -> float:
            if basis == "AD":
                return aY - dY
            elif basis == "XA":
                return aY - xY
            elif basis == "CD":
                return cY - dY
            else:
                return 0.0
        b_val = targetBasis(parts[1])
        target_level = b_val * r + dY
        return target_level if target_level > 0 else 0.0

def harmonic_xabcd_targets(xY: float, aY: float, bY: float, cY: float, dY: float,
                             tgt1: str, tgt2: Optional[str] = None, tgt3: Optional[str] = None) -> Tuple[float, Optional[float], Optional[float]]:
    """
    Hedef seviyeleri (target) hesaplar.
    """
    t1 = resolveTarget(tgt1, xY, aY, bY, cY, dY)
    t2 = resolveTarget(tgt2, xY, aY, bY, cY, dY) if tgt2 is not None else None
    t3 = resolveTarget(tgt3, xY, aY, bY, cY, dY) if tgt3 is not None else None
    return t1, t2, t3

def harmonic_xabcd_stop(stop_str: str, stopPct: float, bull: bool, xY: float, dY: float,
                          upper: float, lower: float, t1: float, eY: float) -> float:
    """
    Stop seviyesi hesaplar.
    """
    e = dY if eY is None else eY
    if bull:
        if stop_str == "% beyond Point D":
            return dY * (1 - stopPct / 100) if dY * (1 - stopPct / 100) > 0 else 0.0
        elif stop_str == "% beyond X or D":
            return min(xY, dY) * (1 - stopPct / 100) if min(xY, dY) * (1 - stopPct / 100) > 0 else 0.0
        elif stop_str == "% beyond entry":
            return e * (1 - stopPct / 100) if e * (1 - stopPct / 100) > 0 else 0.0
        elif stop_str == "% of distance to target 1, beyond entry":
            return e - (stopPct / 100) * (t1 - e) if e - (stopPct / 100) * (t1 - e) > 0 else 0.0
        else:
            return lower * (1 - stopPct / 100) if lower * (1 - stopPct / 100) > 0 else 0.0
    else:
        if stop_str == "% beyond Point D":
            return dY * (1 + stopPct / 100)
        elif stop_str == "% beyond X or D":
            return max(xY, dY) * (1 + stopPct / 100)
        elif stop_str == "% beyond entry":
            return e * (1 + stopPct / 100)
        elif stop_str == "% of distance to target 1, beyond entry":
            return e + (stopPct / 100) * (e - t1)
        else:
            return upper * (1 + stopPct / 100)

def harmonic_xabcd_fibDispTxt(tp: int) -> Tuple[str, str, str, str]:
    """
    Fibonacci oranlarının gösterim metinlerini döndürür.
    """
    rb = {1:"0.618", 2:"0.382 | 0.5", 3:"0.786", 4:"0.382 | 0.618", 5:"NA", 6:"0.382 | 0.618"}.get(tp, "")
    rc = {1:"0.382 | 0.886", 2:"0.382 | 0.886", 3:"0.382 | 0.886", 4:"0.382 | 0.886", 5:"1.13 | 1.618", 6:"1.272 | 1.414"}.get(tp, "")
    rd1 = {1:"1.272 | 1.618", 2:"1.618 | 2.618", 3:"1.618 | 2.618", 4:"2.24 | 3.618", 5:"1.618 | 2.24", 6:"NA"}.get(tp, "")
    rd2 = {1:"0.786", 2:"0.886", 3:"1.272 | 1.618", 4:"1.618", 5:"0.886 | 1.13", 6:"0.786"}.get(tp, "")
    return rb, rc, rd1, rd2

def harmonic_xabcd_symbol(tp: int) -> str:
    """
    Harmonic pattern simgesini döndürür.
    """
    symbols = {1:"Ɠ", 2:"🦇", 3:"🦋", 4:"🦀", 5:"🦈", 6:"Ƈ"}
    return symbols.get(tp, "")

def pat_xabcd_testSym(xax: int, abx: int, bcx: int, cdx: Optional[int], pAsym: float) -> bool:
    """
    Leg ΔX’lerinin simetrisini kontrol eder.
    """
    if cdx is not None and (cdx > ((xax + abx + bcx) / 3) * (1 + pAsym / 100) or cdx < ((xax + abx + bcx) / 3) * (1 - pAsym / 100)):
        return False
    elif bcx > ((xax + abx + (cdx if cdx is not None else 0)) / 3) * (1 + pAsym / 100) or bcx < ((xax + abx + (cdx if cdx is not None else 0)) / 3) * (1 - pAsym / 100):
        return False
    elif abx > ((xax + bcx + (cdx if cdx is not None else 0)) / 3) * (1 + pAsym / 100) or abx < ((xax + bcx + (cdx if cdx is not None else 0)) / 3) * (1 - pAsym / 100):
        return False
    elif xax > ((abx + bcx + (cdx if cdx is not None else 0)) / 3) * (1 + pAsym / 100) or xax < ((abx + bcx + (cdx if cdx is not None else 0)) / 3) * (1 - pAsym / 100):
        return False
    else:
        return True

def harmonic_xabcd_validate(xX: int, xY: float, aX: int, aY: float, bX: int, bY: float,
                              cX: int, cY: float, dX: int, dY: float,
                              pErr: float = 20, pAsym: float = 250,
                              gart: bool = True, bat: bool = True, bfly: bool = True,
                              crab: bool = True, shark: bool = True, cyph: bool = True) -> Tuple[bool, bool, bool, bool, bool, bool, bool]:
    """
    Harmonic XABCD pattern tam validasyonunu gerçekleştirir.
    Dönen değer: (flag, t1, t2, t3, t4, t5, t6) 
    """
    p_types = [gart, bat, bfly, crab, shark, cyph]
    xa = abs(xY - aY)
    xax = abs(xX - aX)
    ab = abs(aY - bY)
    abx = abs(aX - bX)
    bc = abs(bY - cY)
    bcx = abs(bX - cX)
    cd = abs(cY - dY)
    cdx = abs(cX - dX)
    ad = abs(aY - dY)
    xc = abs(xY - cY)
    if not pat_xabcd_testSym(xax, abx, bcx, cdx, pAsym):
        return (False, False, False, False, False, False, False)
    else:
        ab_tests = test_ab(ab, xa, pErr, p_types)
        p_types = list(ab_tests)
        bc_tests = test_bc(bc, ab, pErr, p_types)
        p_types = list(bc_tests)
        t_vals = test_cd(cd, bc, xa, xc, ad, pErr, p_types)
        flag = any(t_vals)
        return (flag, ) + t_vals

def harmonic_xabcd_validateIncomplete(xX: int, xY: float, aX: int, aY: float, bX: int, bY: float,
                                        cX: int, cY: float, pErr: float = 30, pAsym: float = 75,
                                        gart: bool = True, bat: bool = True, bfly: bool = True,
                                        crab: bool = True, shark: bool = True, cyph: bool = True) -> Tuple[bool, bool, bool, bool, bool, bool, bool]:
    p_types = [gart, bat, bfly, crab, shark, cyph]
    xa = abs(xY - aY)
    xax = abs(xX - aX)
    ab = abs(aY - bY)
    abx = abs(aX - bX)
    bc = abs(bY - cY)
    bcx = abs(bX - cX)
    if not pat_xabcd_testSym(xax, abx, bcx, None, pAsym):
        return (False, False, False, False, False, False, False)
    else:
        ab_tests = test_ab(ab, abx, xa, None, pErr)
        p_types = list(ab_tests)
        bc_tests = test_bc(bc, ab, pErr, p_types)
        flag = any(bc_tests)
        return (flag,) + bc_tests

def pat_xabcd_prz(xY: float, aY: float, bY: float, cY: float, xad: float, bcd: float, xcd: Optional[float] = None) -> Tuple[float, float, float]:
    """
    Custom XABCD PRZ seviyelerini hesaplar.
    """
    bc = cY - bY
    xa = aY - xY
    xc = cY - xY
    xad_lvl = aY - (xad * xa)
    bcd_lvl = cY - (bcd * bc)
    xcd_lvl = cY - (xcd * xc) if xcd is not None else None
    return xad_lvl, bcd_lvl, xcd_lvl

def pat_xabcd_avgDev(xX: int, xY: float, aX: int, aY: float, bX: int, bY: float,
                     cX: int, cY: float, dX: Optional[int] = None, dY: Optional[float] = None,
                     series_high: List[float] = None, series_low: List[float] = None, current_bar: int = None) -> float:
    """
    Ortalama sapmayı (deviation) hesaplar. Bu örnekte, belirli barlar arası farklılıkların ortalaması alınır.
    Gerçek uygulamada, daha gelişmiş hesaplamalar yapılabilir.
    """
    # Dummy örnek: 0.0 döndürüyoruz.
    return 0.0

def height(xY: float, aY: float, cY: float, dY: float) -> float:
    """
    Pattern yüksekliğini hesaplar.
    """
    if xY < aY:
        return max(aY, cY) - min(xY, dY)
    else:
        return max(xY, dY) - min(aY, cY)

def harmonic_xabcd_entry(t: bool, tp: int, xY: float, aY: float, bY: float, cY: float, dY: Optional[float] = None,
                           e_afterC: bool = True, e_lvlc: str = "Nearest confluent PRZ level", e_afterD: bool = True,
                           e_lvldPct: float = 1.0) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Pattern için potansiyel giriş seviyelerini hesaplar.
    Dönen değer: (nearest lvl, after C lvl, after D lvl)
    """
    bcN, bcF, xaN, xaF = harmonic_xabcd_prz(tp, xY, aY, bY, cY)
    lPrz, hPrz = harmonic_xabcd_przClosest(bcN, bcF, xaN, xaF)
    u_val, l_val = harmonic_xabcd_przRange(bcN, bcF, xaN, xaF)
    afterD = None
    afterC = None
    if e_afterD and dY is not None:
        afterD = dY * (1 + e_lvldPct / 100) if t else dY * (1 - e_lvldPct / 100)
    if e_afterC:
        if e_lvlc == "Nearest confluent PRZ level":
            afterC = hPrz if t else lPrz
        elif e_lvlc == "Farthest confluent PRZ level":
            afterC = lPrz if t else hPrz
        elif e_lvlc == "Nearest PRZ level":
            afterC = u_val if t else l_val
        elif e_lvlc == "Farthest PRZ level":
            afterC = l_val if t else u_val
        else:
            afterC = hPrz - ((hPrz - lPrz) / 2)
    if afterD is not None and afterD < 0:
        afterD = 0
    if afterC is not None and afterC < 0:
        afterC = 0
    lvl = None
    if afterD is not None and afterC is not None:
        lvl = max(afterD, afterC) if t else min(afterD, afterC)
    elif afterD is not None:
        lvl = afterD
    else:
        lvl = afterC
    return lvl, afterC, afterD

def xabcd_entryHit(t: bool, afterC: float, afterD: float, dX: Optional[int] = None,
                   e_afterC: bool = True, e_afterD: bool = True, dValBars: int = 1,
                   series_low: List[float] = None, series_high: List[float] = None,
                   current_bar: int = None, open_val: float = None) -> Tuple[bool, Optional[int], Optional[float]]:
    """
    Belirtilen giriş seviyesine (entry level) ulaşılıp ulaşılmadığını kontrol eder.
    Bu örnekte basitleştirilmiş bir implementasyon kullanılmıştır.
    """
    bar = None
    eLvl = None
    flag = False
    if current_bar is None:
        current_bar = len(series_low) - 1 if series_low is not None else 0
    if open_val is None:
        open_val = 0.0
    if e_afterC and (dX is None or current_bar < (dX + dValBars)):
        if t and series_low and series_low[current_bar] <= afterC:
            flag = True
            bar = current_bar
            eLvl = afterC if open_val > afterC else open_val
        elif (not t) and series_high and series_high[current_bar] >= afterC:
            flag = True
            bar = current_bar
            eLvl = afterC if open_val < afterC else open_val
    elif e_afterD and dX is not None and afterD is not None:
        if t and series_low and series_low[current_bar] <= afterD:
            flag = True
            bar = current_bar
            eLvl = afterD if open_val > afterD else open_val
        elif (not t) and series_high and series_high[current_bar] >= afterD:
            flag = True
            bar = current_bar
            eLvl = afterD if open_val < afterD else open_val
    return flag, bar, eLvl

def test_ab(ab: float, xa: float, pErr: float, p_types: List[bool]) -> Tuple[bool, bool, bool, bool, bool, bool]:
    """
    AB leg validesini test eder. Her pattern için uygun Fibonacci aralığını kontrol eder.
    """
    f618 = fib_precise(0.618)
    f382 = fib_precise(0.382)
    f786 = fib_precise(0.786)
    t0 = (xa != 0 and f618 * (1 + pErr/100) >= ab >= f618 * (1 - pErr/100)) if p_types[0] else False
    t1 = (xa != 0 and (f382 * (1 + pErr/100) >= ab >= f382 * (1 - pErr/100) or 0.5 * (1 + pErr/100) >= ab >= 0.5 * (1 - pErr/100))) if p_types[1] else False
    t2 = (xa != 0 and f786 * (1 + pErr/100) >= ab >= f786 * (1 - pErr/100)) if p_types[2] else False
    t3 = (xa != 0 and (f382 * (1 + pErr/100) >= ab >= f382 * (1 - pErr/100) or f618 * (1 + pErr/100) >= ab >= f618 * (1 - pErr/100))) if p_types[3] else False
    t4 = p_types[4]  # Shark: no strict validation
    t5 = (xa != 0 and (f382 * (1 + pErr/100) >= ab >= f382 * (1 - pErr/100) or f618 * (1 + pErr/100) >= ab >= f618 * (1 - pErr/100))) if p_types[5] else False
    return t0, t1, t2, t3, t4, t5

def test_bc(bc: float, ab: float, pErr: float, p_types: List[bool]) -> Tuple[bool, bool, bool, bool, bool, bool]:
    """
    BC leg validasyonunu test eder.
    """
    f382 = fib_precise(0.382)
    f886 = fib_precise(0.886)
    f1618 = fib_precise(1.618)
    f1272 = fib_precise(1.272)
    rat = bc / ab if ab != 0 else 0
    pass_val = (rat <= f886 * (1 + pErr/100) and rat >= f886 * (1 - pErr/100)) or (rat <= f382 * (1 + pErr/100) and rat >= f382 * (1 - pErr/100))
    t0 = pass_val if p_types[0] else False
    t1 = pass_val if p_types[1] else False
    t2 = pass_val if p_types[2] else False
    t3 = pass_val if p_types[3] else False
    t4 = (rat <= 1.13 * (1 + pErr/100) and rat >= 1.13 * (1 - pErr/100)) or (rat <= f1618 * (1 + pErr/100) and rat >= f1618 * (1 - pErr/100)) if p_types[4] else False
    t5 = (rat <= f1272 * (1 + pErr/100) and rat >= f1272 * (1 - pErr/100)) or (rat <= fib_precise(1.414) * (1 + pErr/100) and rat >= fib_precise(1.414) * (1 - pErr/100)) if p_types[5] else False
    return t0, t1, t2, t3, t4, t5

def test_cd(cd: float, bc: float, xa: float, xc: float, ad: float, pErr: float, p_types: List[bool]) -> Tuple[bool, bool, bool, bool, bool, bool]:
    """
    CD leg validasyonunu, ayrıca XA ve XC leglerine göre test eder.
    """
    f1618 = fib_precise(1.618)
    f2618 = fib_precise(2.618)
    f786 = fib_precise(0.786)
    f886 = fib_precise(0.886)
    f1272 = fib_precise(1.272)
    rat = cd / bc if bc != 0 else 0
    rat2 = ad / xa if xa != 0 else 0
    rat3 = cd / xc if xc != 0 else 0
    bc_test = (rat <= f1272 * (1 + pErr/100) and rat >= f1272 * (1 - pErr/100)) or (rat <= f1618 * (1 + pErr/100) and rat >= f1618 * (1 - pErr/100))
    xa_test = rat2 <= f786 * (1 + pErr/100) and rat2 >= f786 * (1 - pErr/100)
    t0 = bc_test and xa_test if p_types[0] else False
    # Diğer pattern tipleri için benzer kontroller yapılır (dummy örnekleme)
    t1 = bc_test and xa_test if p_types[1] else False
    t2 = bc_test and xa_test if p_types[2] else False
    t3 = bc_test and xa_test if p_types[3] else False
    t4 = bc_test and xa_test if p_types[4] else False
    t5 = False if not p_types[5] else False
    return t0, t1, t2, t3, t4, t5

# -------------------------------------------------------
# Toplam Skor Fonksiyonları
# -------------------------------------------------------
# harmonic_xabcd_score ve harmonic_xabcd_scoreTot fonksiyonları yukarıda tanımlandı.
# bunlar hesaplanan alt skorları kullanarak toplam skoru verir.
# -------------------------------------------------------

# -------------------------------------------------------
# PRZ ve diğer yardımcı fonksiyonlar: harmonic_xabcd_targets, harmonic_xabcd_stop, fib display text, vs.
# Bu fonksiyonlar yukarıda tanımlandı.
# -------------------------------------------------------

# -------------------------------------------------------
# Pattern Fonksiyonları
# -------------------------------------------------------

def pat_xabcd(x_is_low: bool = True, pivot_length: int = 5, source: Optional[List[float]] = None,
                conf_length: int = 1, incomplete: bool = False,
                high: Optional[List[float]] = None, low: Optional[List[float]] = None,
                current_bar: int = None) -> Tuple[bool, int, float, int, float, int, float, int, float]:
    """
    XABCD pattern tamamlandığında veya in-complete (eksik) durumunda, pattern noktalarını tespit eder.
    Dönen değer: (flag, x, x_y, a, a_y, b, b_y, c, c_y, d, d_y) – (Eğer pattern bulunamazsa negatif ya da 0 değerler)
    
    Bu implemantasyon, Pine Script’teki gibi çalışması için örnek/dummy koda sahiptir.
    """
    if current_bar is None:
        current_bar = len(low) - 1 if low is not None else 0
    r_flag = False
    x = a = b = c = d = -1
    x_y = a_y = b_y = c_y = d_y = 0.0
    lb = min(pivot_length * 30, current_bar)
    hsrc = high if high is not None else []
    lsrc = low if low is not None else []
    # Pivot low ve high’ları bulmak için dummy pivot fonksiyonları kullanılmaktadır.
    pl = pivotlow(lsrc, pivot_length, pivot_length)
    ph = pivothigh(hsrc, pivot_length, pivot_length)
    lbLow = pivotlow(lsrc, pivot_length, conf_length)
    lbHigh = pivothigh(hsrc, pivot_length, conf_length)
    hSince = 0.0
    lSince = 0.0
    if x_is_low:
        if any(v is not None for v in lbLow) or incomplete:
            d = -1 if incomplete else current_bar - conf_length
            d_y = 0.0 if incomplete else lbLow[current_bar] if current_bar < len(lbLow) else 0.0
            for i in range(conf_length if not incomplete else 0, pivot_length + 1):
                if i < len(hsrc) and hsrc[i] > hSince:
                    hSince = hsrc[i]
                if i < len(lsrc) and (lsrc[i] < lSince or lSince == 0):
                    lSince = lsrc[i]
            for i in range(lb):
                idx = i + pivot_length
                if idx < len(hsrc) and hsrc[idx] > hSince:
                    hSince = hsrc[idx]
                if idx < len(lsrc) and (lsrc[idx] < lSince or lSince == 0):
                    lSince = lsrc[idx]
                if c == -1:
                    if i < len(pl) and pl[i] is not None:
                        if pl[i] < d_y:
                            break
                    elif i < len(ph) and ph[i] is not None:
                        if ph[i] < d_y:
                            break
                        elif hSince > ph[i]:
                            break
                        else:
                            c = current_bar - i - pivot_length
                            c_y = ph[i]
                            hSince = 0.0
                            lSince = 0.0
                    elif incomplete:
                        break
                elif b == -1:
                    if i < len(ph) and ph[i] is not None:
                        if ph[i] > c_y:
                            break
                    elif i < len(pl) and pl[i] is not None:
                        if pl[i] > c_y:
                            break
                        elif lSince < pl[i]:
                            break
                        else:
                            b = current_bar - i - pivot_length
                            b_y = pl[i]
                            hSince = 0.0
                            lSince = 0.0
                elif a == -1:
                    if i < len(pl) and pl[i] is not None:
                        if pl[i] < b_y:
                            break
                    elif i < len(ph) and ph[i] is not None:
                        if ph[i] < b_y:
                            break
                        elif hSince > ph[i]:
                            break
                        else:
                            a = current_bar - i - pivot_length
                            a_y = ph[i]
                            hSince = 0.0
                            lSince = 0.0
                elif x == -1:
                    if i < len(ph) and ph[i] is not None:
                        if ph[i] > a_y:
                            break
                    elif i < len(pl) and pl[i] is not None:
                        if pl[i] > a_y:
                            break
                        elif lSince < pl[i]:
                            break
                        else:
                            r_flag = True
                            x = current_bar - i - pivot_length
                            x_y = pl[i]
                            break
    else:
        # Benzer şekilde bearish pattern için de uygulanabilir.
        pass
    return r_flag, x, x_y, a, a_y, b, b_y, c, c_y, d, d_y

# -------------------------------------------------------
# Dosyanın sonu.
# -------------------------------------------------------
if __name__ == "__main__":
    # Örnek kullanım: Test verilerle fonksiyonları çağırabilirsiniz.
    # Bu örnekte dummy fiyat serileri kullanılmıştır.
    # Gerçek uygulamada high, low, open gibi serileri içeren veri setleri kullanın.
    price_series = [100 + math.sin(i/10) for i in range(200)]
    indicator_series = [50 + math.cos(i/10) for i in range(200)]
    flag, degree, div_type, lx1, ly1, lx2, ly2 = div_bull(price_series, indicator_series, current_bar=199)
    print("Boğa Divergansı:", flag, degree, div_type, lx1, ly1, lx2, ly2)
    
    # Harmonic PRZ örneği:
    bc_u, bc_l, xa_u, xa_l = harmonic_xabcd_prz(100, 110, 105, 102)
    print("PRZ Seviyeleri:", bc_u, bc_l, xa_u, xa_l)
    
    # Diğer fonksiyonları örnek verilerle test edebilirsiniz.
