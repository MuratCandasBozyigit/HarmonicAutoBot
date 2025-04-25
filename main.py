import tkinter as tk
import Indicators
import Utils
import Utils.globals as globals
import Cmd
import Order
import Chart
import Gui
import sys
if __name__ == "__main__":
    root = tk.Tk()
    #root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    globals.root = root
    Gui.build_gui(root)
    root.mainloop()
