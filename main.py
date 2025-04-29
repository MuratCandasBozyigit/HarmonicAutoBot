import tkinter as tk
import Indicators
import Utils
import Utils.globals as globals
import Order
import Chart
import Gui
import sys

def setup_globals():
    """Global ayarları başlatır."""
    globals.root = None 

if __name__ == "__main__":
    setup_globals()
    root = tk.Tk()
    globals.root = root
    Gui.build_gui(root)
    root.mainloop()
