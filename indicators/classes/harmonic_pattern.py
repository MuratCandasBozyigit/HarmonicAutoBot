from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt

# Algebra yardımcı fonksiyonları
def line_from_xy(x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
    slope = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
    yint = y1 - slope * x1
    return slope, yint

def line_get_price(x: float, slope: float, yint: float) -> float:
    return slope * x + yint

# Draw yardımcı fonksiyonları
def line_style(style: str) -> str:
    mapping = {
        "solid": "-",
        "dotted": ":",
        "dashed": "--",
        "arrowleft": "-<",
        "arrowright": "->"
    }
    return mapping.get(style, "-")

def label_style(position: str) -> dict:
    # Konumlandırmayı basitleştirmek için (örneğin "top" veya "bottom")
    # Matplotlib'te text alignment özellikleri kullanılır.
    if position.lower() == "top":
        return {"va": "bottom"}
    else:
        return {"va": "top"}

def size_map(size: str) -> int:
    # Basit bir font boyutu eşlemesi
    mapping = {
        "tiny": 8,
        "small": 10,
        "normal": 12,
        "large": 14,
        "huge": 16
    }
    return mapping.get(size, 12)

# Pattern kütüphanesi için sınıflar

class Point:
    def __init__(self, x: int, y: float):
        self.x = x
        self.y = y
        self.label_obj = None  # Çizimde oluşturulan text objesi

    def erase_label(self, ax: plt.Axes):
        if self.label_obj is not None:
            try:
                self.label_obj.remove()
            except Exception:
                pass
            self.label_obj = None

    def draw_label(self, ax: plt.Axes, position: str = "bottom", clr: str = "gray", transp: float = 50.0,
                   txt_clr: str = "white", txt: Optional[str] = None, tooltip: Optional[str] = None,
                   size: str = "small"):
        # Önce varsa eski label silinir
        self.erase_label(ax)
        txt_to_display = txt if txt is not None else f"{self.y:.5f}"
        style_params = label_style(position)
        font_size = size_map(size)
        # Matplotlib'te transparency renk koduyla sağlanmadığından basitçe renk ismi kullanıyoruz.
        self.label_obj = ax.text(self.x, self.y, txt_to_display, color=txt_clr, fontsize=font_size,
                                  ha='center', **style_params)
        return self.label_obj

class Leg:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.deltaX = b.x - a.x
        self.deltaY = b.y - a.y
        self.prev: Optional["Leg"] = None
        self.next: Optional["Leg"] = None
        self.retrace: Optional[float] = None
        self.line_obj = None  # matplotlib Line2D

    def erase(self, ax: plt.Axes):
        if self.line_obj is not None:
            try:
                self.line_obj.remove()
            except Exception:
                pass
            self.line_obj = None

    def draw(self, ax: plt.Axes, clr: str = "gray", style: str = "solid", transp: float = 20.0, width: int = 1):
        self.erase(ax)
        lstyle = line_style(style)
        # Basit çizgi çizimi; arrow stili için farklı işlem yapılabilir ama burada düz çizgi kullanıyoruz.
        self.line_obj, = ax.plot([self.a.x, self.b.x], [self.a.y, self.b.y], linestyle=lstyle, color=clr, linewidth=width)
        return self.line_obj

    def get_line_terms(self) -> Tuple[float, float]:
        return line_from_xy(self.a.x, self.a.y, self.b.x, self.b.y)

    def get_price(self, index: int) -> Optional[float]:
        if self.a.x <= index <= self.b.x:
            slope, yint = self.get_line_terms()
            return line_get_price(index, slope, yint)
        return None

def valid_pattern_legs(leg1: Leg, leg2: Leg) -> bool:
    if leg1.b.x != leg2.a.x:
        return False
    if leg1.b.y != leg2.a.y:
        return False
    return True

def leg_init(a: Point, b: Point, prev: Optional[Leg] = None, next_leg: Optional[Leg] = None) -> Leg:
    new_leg = Leg(a, b)
    if prev is not None and valid_pattern_legs(prev, new_leg):
        new_leg.prev = prev
        if prev.deltaY != 0:
            new_leg.retrace = (new_leg.deltaY / prev.deltaY) * -1
        prev.next = new_leg
    if next_leg is not None and valid_pattern_legs(new_leg, next_leg):
        new_leg.next = next_leg
    return new_leg

class Pattern:
    def __init__(self, legs: List[Leg], type_: str = "free", subType: Optional[str] = None,
                 name: Optional[str] = None, pid: Optional[str] = None):
        self.legs = legs
        self.type = type_
        self.subType = subType
        self.name = name
        self.pid = pid

    def erase(self, ax: plt.Axes):
        for leg in self.legs:
            leg.erase(ax)

    def draw(self, ax: plt.Axes, clr: str = "gray", style: str = "solid", transp: float = 20.0, width: int = 1) -> List:
        self.erase(ax)
        line_objs = []
        for leg in self.legs:
            line_obj = leg.draw(ax, clr, style, transp, width)
            line_objs.append(line_obj)
        return line_objs

def valid_for_type(tp: str, legs: List[Leg]) -> bool:
    valid = True
    n = len(legs)
    if n < 2:
        valid = False
    elif tp == "xabcd":
        if n != 3 and n != 4:
            valid = False
    elif tp in ["zigzag", "xabcd"]:
        for i in range(1, n):
            leg_curr = legs[i]
            leg_prev = legs[i - 1]
            if leg_prev.deltaY < 0 and leg_curr.deltaY < 0:
                valid = False
                break
            elif leg_prev.deltaY > 0 and leg_curr.deltaY > 0:
                valid = False
                break
    return valid

def pattern_init_from_legs(legs: List[Leg], tp: str = "free", name: Optional[str] = None,
                             subType: Optional[str] = None, pid: Optional[str] = None) -> Optional[Pattern]:
    if valid_for_type(tp, legs):
        return Pattern(legs, tp, subType, name, pid)
    return None

def pattern_init_from_points(points: List[Point], tp: str = "free", name: Optional[str] = None,
                               subType: Optional[str] = None, pid: Optional[str] = None) -> Optional[Pattern]:
    legs = []
    n = len(points)
    if n >= 3:
        prev_leg = None
        for i in range(1, n):
            leg_i = leg_init(points[i - 1], points[i], prev_leg)
            legs.append(leg_i)
            prev_leg = leg_i
        return pattern_init_from_legs(legs, tp, name, subType, pid)
    return None

# Örnek kullanım
def main():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Hard-coded koordinatlar (örnek: ADAUSD 4h Gartley formasyonu)
    xX, xY = 10681, 0.344
    aX, aY = 10714, 0.296
    bX, bY = 10743, 0.322
    cX, cY = 10752, 0.300
    dX, dY = 10796, 0.329

    # Noktaların oluşturulması
    x_point = Point(xX, xY)
    a_point = Point(aX, aY)
    b_point = Point(bX, bY)
    c_point = Point(cX, cY)
    d_point = Point(dX, dY)

    # Bacakların (legs) oluşturulması
    xa = leg_init(x_point, a_point)
    ab = leg_init(a_point, b_point, xa)
    bc = leg_init(b_point, c_point, ab)
    cd = leg_init(c_point, d_point, bc)
    points = [x_point, a_point, b_point, c_point, d_point]
    legs = [xa, ab, bc, cd]
    pattern_obj = pattern_init_from_points(points, "xabcd")

    # Çizim: Nokta etiketleri
    d_point.draw_label(ax, position="top")
    x_point.draw_label(ax, position="top", txt="X")
    a_point.draw_label(ax, position="bottom", txt="A")
    c_point.draw_label(ax, position="bottom", txt="C")

    # Desenin çizimi
    if pattern_obj is not None:
        pattern_obj.draw(ax, clr="red", style="solid", width=2)
    
    # Bir bacağın çizimi (örnek olarak)
    next_point = Point(d_point.x + 50, d_point.y * 0.8)
    next_leg = leg_init(d_point, next_point)
    next_leg.draw(ax, clr="blue", style="arrowright")

    # Bacağa ilişkin detaylar (örneğin ab bacağı retracement oranı)
    ab_retrace = ab.retrace
    b_point.draw_label(ax, position="top", txt=f"B\nRetracement\nAB/XA = {ab_retrace:.3f}" if ab_retrace is not None else "N/A")
    
    midX = d_point.x + 25
    mid_price = next_leg.get_price(midX)
    if mid_price is not None:
        slope, yint = next_leg.get_line_terms()
        mid_point = Point(midX, mid_price)
        mid_point.draw_label(ax, position="bottom", txt=f"Slope = {slope:.4f}\ny-int = {yint:.4f}")

    ax.set_title("Harmonic Pattern - Python Visualization")
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
