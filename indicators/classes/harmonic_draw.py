
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt

def pat_colors(bull: bool, buLn=None, beLn=None, ltxt=None) -> List[str]:
    red = "#ff000080"
    grn = "#00ff0080"
    return [
        "#8080804d",
        red,
        grn,
        "#ffffff",
        "#ffffff4d" if ltxt is None else ltxt,
        "#0000ff",
        grn if bull else red if (buLn is None or beLn is None) else buLn if bull else beLn,
        grn if bull else red,
        "#ff0000cc",
        "#00ff00cc",
    ]

def size_map(size: str) -> str:
    mapping = {
        "tiny": "xx-small",
        "small": "x-small",
        "normal": "medium",
        "large": "large",
        "huge": "x-large"
    }
    return mapping.get(size, "medium")

def label_style(style: str) -> str:
    return "up" if style == "bottom" else "down"

def line_style(style: str) -> str:
    mapping = {
        "dotted": ":",
        "dashed": "--",
        "arrowleft": "<-",
        "arrowright": "->"
    }
    return mapping.get(style, "-")

def draw_line(ax, start: Tuple[float, float], end: Tuple[float, float], color: str = 'black', style: str = '-', width: int = 1):
    ax.plot([start[0], end[0]], [start[1], end[1]], linestyle=style, color=color, linewidth=width)

def draw_label(ax, text: str, x: float, y: float, fontsize: int = 9, color: str = 'black'):
    ax.text(x, y, text, fontsize=fontsize, ha='center', color=color)

def draw_xabcd_pattern(ax, points: List[Tuple[float, float]], bull: bool, color_bull="#00ff00", color_bear="#ff0000"):
    color = color_bull if bull else color_bear
    x_vals, y_vals = zip(*points)
    for i in range(len(points) - 1):
        draw_line(ax, points[i], points[i + 1], color=color, style='-', width=2)
    for label, (x, y) in zip(['X', 'A', 'B', 'C', 'D'][:len(points)], points):
        draw_label(ax, label, x, y, fontsize=9, color=color)

def draw_prz_zone(ax, prz_levels: List[float], x_start: int, t_limit: int, color_fill: str = "#cccccc55"):
    for level in prz_levels:
        draw_line(ax, (x_start, level), (x_start + t_limit, level), color="red", style='--', width=2)
        draw_label(ax, f"PRZ {level:.2f}", x_start + t_limit / 2, level, fontsize=8, color="red")

def draw_targets(ax, targets: List[float], x_start: int, t_limit: int, color="green"):
    for i, t in enumerate(targets, 1):
        draw_line(ax, (x_start, t), (x_start + t_limit, t), color=color, style='-', width=3)
        draw_label(ax, f"T{i}: {t:.2f}", x_start + t_limit / 2, t, fontsize=8, color=color)

def draw_entry_stop(ax, entry: float, stop: float, x_start: int, t_limit: int):
    draw_line(ax, (x_start, entry), (x_start + t_limit, entry), color="green", style=':', width=2)
    draw_label(ax, f"Entry: {entry:.2f}", x_start + t_limit / 2, entry, fontsize=8, color="green")
    draw_line(ax, (x_start, stop), (x_start + t_limit, stop), color="red", style='-', width=2)
    draw_label(ax, f"Stop: {stop:.2f}", x_start + t_limit / 2, stop, fontsize=8, color="red")

def main():
    fig, ax = plt.subplots(figsize=(10, 6))
    pattern_points = [(0, 100), (1, 120), (2, 90), (3, 110), (4, 95)]
    draw_xabcd_pattern(ax, pattern_points, bull=True)

    draw_prz_zone(ax, prz_levels=[96, 98, 100], x_start=4, t_limit=3)
    draw_targets(ax, targets=[105, 110], x_start=4, t_limit=3)
    draw_entry_stop(ax, entry=98, stop=93, x_start=4, t_limit=3)

    ax.set_title("XABCD Harmonic Pattern - Python Visualization")
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
