import tkinter as tk
import İndicators
import Utils
import Utils.globals as globals
import Order
import Chart
import Gui

if __name__ == "__main__":
    root = tk.Tk()
    globals.root = root
    Gui.build_gui(root)
    root.mainloop()
