import math
from typing import Tuple, List

# Fibonacci constants
FIB = {
    "f382": 0.382,
    "f618": 0.618,
    "f786": 0.786,
    "f886": 0.886,
    "f1272": 1.272,
    "f1414": 1.414,
    "f1618": 1.618,
    "f224": 2.24,
    "f2618": 2.618,
    "f3618": 3.618,
    "shark_mid": 1.13
}

def test_symmetry(xax, abx, bcx, cdx=None, pAsym=250.0) -> bool:
    legs = [xax, abx, bcx] if cdx is None else [xax, abx, bcx, cdx]
    avg = sum(legs) / len(legs)
    for leg in legs:
        if leg > avg * (1 + pAsym / 100) or leg < avg * (1 - pAsym / 100):
            return False
    return True

def test_ab(ab, xa, pErr, p_types):
    rat = ab / xa
    t = [False]*6
    if p_types[0]: t[0] = abs(rat - FIB["f618"]) <= FIB["f618"] * pErr / 100
    if p_types[1]: t[1] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], 0.5])
    if p_types[2]: t[2] = abs(rat - FIB["f786"]) <= FIB["f786"] * pErr / 100
    if p_types[3]: t[3] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], FIB["f618"]])
    if p_types[4]: t[4] = rat < 1
    if p_types[5]: t[5] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], FIB["f618"]])
    return t

def test_bc(bc, ab, pErr, p_types):
    rat = bc / ab
    t = [False]*6
    base = [FIB["f382"], FIB["f886"]]
    if p_types[0]: t[0] = any(abs(rat - v) <= v * pErr / 100 for v in base)
    if p_types[1]: t[1] = any(abs(rat - v) <= v * pErr / 100 for v in base)
    if p_types[2]: t[2] = any(abs(rat - v) <= v * pErr / 100 for v in base)
    if p_types[3]: t[3] = any(abs(rat - v) <= v * pErr / 100 for v in base)
    if p_types[4]: t[4] = any(abs(rat - v) <= v * pErr / 100 for v in [1.13, FIB["f1618"]])
    if p_types[5]: t[5] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1414"]])
    return t

def test_cd(cd, bc, xa, xc, ad, pErr, p_types):
    rat = cd / bc
    rat2 = ad / xa
    rat3 = cd / xc
    t = [False]*6
    if p_types[0]:
        bc_ok = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1618"]])
        xa_ok = abs(rat2 - FIB["f786"]) <= FIB["f786"] * pErr / 100
        t[0] = bc_ok and xa_ok
    if p_types[1]:
        bc_ok = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f2618"]])
        xa_ok = abs(rat2 - FIB["f886"]) <= FIB["f886"] * pErr / 100
        t[1] = bc_ok and xa_ok
    if p_types[2]:
        bc_ok = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f2618"]])
        xa_ok = any(abs(rat2 - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1618"]])
        t[2] = bc_ok and xa_ok
    if p_types[3]:
        bc_ok = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f224"], FIB["f3618"]])
        xa_ok = abs(rat2 - FIB["f1618"]) <= FIB["f1618"] * pErr / 100
        t[3] = bc_ok and xa_ok
    if p_types[4]:
        bc_ok = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f224"]])
        xa_ok = any(abs(rat2 - v) <= v * pErr / 100 for v in [FIB["f886"], 1.13])
        t[4] = bc_ok and xa_ok
    if p_types[5]:
        t[5] = abs(rat3 - FIB["f786"]) <= FIB["f786"] * pErr / 100
    return t

def harmonic_xabcd_validate(xX, xY, aX, aY, bX, bY, cX, cY, dX, dY,
                             pErr=20, pAsym=250,
                             gart=True, bat=True, bfly=True, crab=True, shark=True, cyph=True):
    p_types = [gart, bat, bfly, crab, shark, cyph]
    xa = abs(xY - aY)
    xax = abs(xX - aX)
    ab = abs(aY - bY)
    abx = abs(aX - bX)
    bc = abs(bY - cY)
    bcx = abs(bX - cX)
    cd = abs(cY - dY)
    ad = abs(aY - dY)
    xc = abs(xY - cY)
    cdx = abs(cX - dX)

    if not test_symmetry(xax, abx, bcx, cdx, pAsym):
        return (False, False, False, False, False, False, False)

    ab_valid = test_ab(ab, xa, pErr, p_types)
    bc_valid = test_bc(bc, ab, pErr, ab_valid)
    cd_valid = test_cd(cd, bc, xa, xc, ad, pErr, bc_valid)

    return (any(cd_valid), *cd_valid)

# PRZ calculation
def get_prz_levels(pattern_type: int, xY: float, aY: float, bY: float, cY: float):
    bc = cY - bY
    xa = aY - xY
    xc = cY - xY
    bc_u = bc_l = xa_u = xa_l = None
    if pattern_type == 1:  # Gartley
        bc_u = cY - (FIB["f1272"] * bc)
        bc_l = cY - (FIB["f1618"] * bc)
        xa_u = aY - (FIB["f786"] * xa)
    elif pattern_type == 2:  # Bat
        bc_u = cY - (FIB["f1618"] * bc)
        bc_l = cY - (FIB["f2618"] * bc)
        xa_u = aY - (FIB["f886"] * xa)
    elif pattern_type == 3:  # Butterfly
        bc_u = cY - (FIB["f1618"] * bc)
        bc_l = cY - (FIB["f2618"] * bc)
        xa_u = aY - (FIB["f1272"] * xa)
        xa_l = aY - (FIB["f1618"] * xa)
    elif pattern_type == 4:  # Crab
        bc_u = cY - (FIB["f224"] * bc)
        bc_l = cY - (FIB["f3618"] * bc)
        xa_u = aY - (FIB["f1618"] * xa)
    elif pattern_type == 5:  # Shark
        bc_u = cY - (FIB["f1618"] * bc)
        bc_l = cY - (FIB["f224"] * bc)
        xa_u = aY - (FIB["f886"] * xa)
        xa_l = aY - (1.13 * xa)
    elif pattern_type == 6:  # Cypher
        xa_u = cY - (FIB["f786"] * xc)
    return bc_u, bc_l, xa_u, xa_l

# PRZ score
def prz_score(xY, aY, *levels):
    h = abs(aY - xY)
    valid_levels = [l for l in levels if l is not None]
    if len(valid_levels) < 2:
        return 0, None, None
    sorted_lvls = sorted(valid_levels)
    min_diff = float('inf')
    best_pair = (None, None)
    for i in range(len(sorted_lvls)-1):
        diff = sorted_lvls[i+1] - sorted_lvls[i]
        if diff < min_diff:
            min_diff = diff
            best_pair = (sorted_lvls[i], sorted_lvls[i+1])
    score = 1 - (min_diff / h)
    return score, best_pair[0], best_pair[1]

# Harmonic score
def harmonic_score(tp, xX, xY, aX, aY, bX, bY, cX, cY, dX=None, dY=None):
    xa = abs(xY - aY)
    ab = abs(aY - bY)
    bc = abs(bY - cY)
    ad = abs(aY - dY) if dY is not None else None
    cd = abs(cY - dY) if dY is not None else None
    xc = abs(xY - cY)

    def err_ratio(ratio, target):
        return abs(1 - (ratio / target))

    xbre = err_ratio(ab / xa, FIB["f618"]) if xa else 0
    acre = err_ratio(bc / ab, FIB["f886"]) if ab else 0
    bdre = err_ratio(cd / bc, FIB["f1618"]) if bc and cd else 0
    xdre = err_ratio(ad / xa, FIB["f786"]) if ad and xa else 0
    przs = get_prz_levels(tp, xY, aY, bY, cY)
    przscore, cpl1, cpl2 = prz_score(xY, aY, *przs)
    eavg = sum(filter(None, [xbre, acre, bdre, xdre])) / len(list(filter(None, [xbre, acre, bdre, xdre])))
    asym = sum([
        abs(1 - ((aX - xX) / ((bX - aX + cX - bX) / 2))),
        abs(1 - ((bX - aX) / ((aX - xX + cX - bX) / 2))),
        abs(1 - ((cX - bX) / ((aX - xX + bX - aX) / 2))),
        abs(1 - ((dX - cX) / ((aX - xX + bX - aX + cX - bX) / 3))) if dX is not None else 0
    ]) / (4 if dX is not None else 3)
    eD = min(abs(cpl1 - dY), abs(cpl2 - dY)) / xa if dY and cpl1 and cpl2 else 0
    dev = 1 - (0)  # Placeholder for average deviation computation

    return {
        "eavg": eavg,
        "asym": asym,
        "eD": eD,
        "przscore": przscore,
        "cpl1": cpl1,
        "cpl2": cpl2,
        "total_score": ((1 - asym) + (1 - eavg) + przscore + (1 - eD)) / 4
    }
