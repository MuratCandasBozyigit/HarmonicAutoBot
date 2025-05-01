import tkinter as tk
import customtkinter as ctk
import time
import Gui
import Utils.globals as globals

def setup_globals():
    globals.root = None 

def show_main_frame():
    Gui.build_gui(globals.root)

if __name__ == "__main__":
    setup_globals()
    root = tk.Tk()
    root.withdraw()  # İlk başta gizle (loading ekranı çıkana kadar)

    globals.root = root
    loading = Gui.loadingFrame(root)

    # loading ekranında işlemler yapabilirsin, örnek olarak bekletiyoruz
    root.after(100, lambda: print("Veri çekiliyor..."))
    root.after(3000, lambda: (
        loading.stop_loading(),
        root.deiconify(),   # Ana pencereyi tekrar göster
        show_main_frame()
    ))

    root.mainloop()
