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

def test_symmetry(xax, abx, bcx, cdx, pAsym) -> bool:
    legs = [xax, abx, bcx, cdx]
    valid_legs = [l for l in legs if l is not None]
    avg = sum(valid_legs) / len(valid_legs)
    for l in valid_legs:
        if l > avg * (1 + pAsym / 100) or l < avg * (1 - pAsym / 100):
            return False
    return True

def test_ab(ab, xa, pErr, p_types: List[bool]) -> List[bool]:
    rat = ab / xa
    t = [False] * 6
    if p_types[0]:  # Gartley
        t[0] = abs(rat - FIB["f618"]) <= FIB["f618"] * pErr / 100
    if p_types[1]:  # Bat
        t[1] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], 0.5])
    if p_types[2]:  # Butterfly
        t[2] = abs(rat - FIB["f786"]) <= FIB["f786"] * pErr / 100
    if p_types[3]:  # Crab
        t[3] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], FIB["f618"]])
    if p_types[4]:  # Shark
        t[4] = rat < 1  # No strict validation
    if p_types[5]:  # Cypher
        t[5] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], FIB["f618"]])
    return t

def test_bc(bc, ab, pErr, p_types: List[bool]) -> List[bool]:
    rat = bc / ab
    t = [False] * 6
    base_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f382"], FIB["f886"]])
    for i in range(4):
        if p_types[i]:
            t[i] = base_test
    if p_types[4]:  # Shark
        t[4] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["shark_mid"], FIB["f1618"]])
    if p_types[5]:  # Cypher
        t[5] = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1414"]])
    return t

def test_cd(cd, bc, xa, xc, ad, pErr, p_types: List[bool]) -> List[bool]:
    rat = cd / bc
    rat2 = ad / xa
    rat3 = cd / xc
    t = [False] * 6
    if p_types[0]:  # Gartley
        bc_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1618"]])
        xa_test = abs(rat2 - FIB["f786"]) <= FIB["f786"] * pErr / 100
        t[0] = bc_test and xa_test
    if p_types[1]:  # Bat
        bc_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f2618"]])
        xa_test = abs(rat2 - FIB["f886"]) <= FIB["f886"] * pErr / 100
        t[1] = bc_test and xa_test
    if p_types[2]:  # Butterfly
        bc_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f2618"]])
        xa_test = any(abs(rat2 - v) <= v * pErr / 100 for v in [FIB["f1272"], FIB["f1618"]])
        t[2] = bc_test and xa_test
    if p_types[3]:  # Crab
        bc_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f224"], FIB["f3618"]])
        xa_test = abs(rat2 - FIB["f1618"]) <= FIB["f1618"] * pErr / 100
        t[3] = bc_test and xa_test
    if p_types[4]:  # Shark
        bc_test = any(abs(rat - v) <= v * pErr / 100 for v in [FIB["f1618"], FIB["f224"]])
        xa_test = any(abs(rat2 - v) <= v * pErr / 100 for v in [FIB["f886"], FIB["shark_mid"]])
        t[4] = bc_test and xa_test
    if p_types[5]:  # Cypher
        t[5] = abs(rat3 - FIB["f786"]) <= FIB["f786"] * pErr / 100
    return t

def harmonic_xabcd_validate(
    xX, xY, aX, aY, bX, bY, cX, cY, dX, dY,
    pErr=20, pAsym=250,
    gart=True, bat=True, bfly=True, crab=True, shark=True, cyph=True
) -> Tuple[bool, bool, bool, bool, bool, bool, bool]:

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

    ab_flags = test_ab(ab, xa, pErr, p_types)
    bc_flags = test_bc(bc, ab, pErr, ab_flags)
    cd_flags = test_cd(cd, bc, xa, xc, ad, pErr, bc_flags)

    valid = any(cd_flags)
    return (valid, *cd_flags)
