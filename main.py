import tkinter as tk
import customtkinter as ctk
import threading
import time

import Gui  # loadingFrame burada
import Utils.globals as globals

def start_app():
    # Build GUI işlemini ayrı bir thread ile yap
    def init():
        Gui.build_gui(globals.root)  # Ağır işlemler burada
        loading.stop_loading()       # Her şey hazırsa yükleniyor ekranı kapat
        globals.root.deiconify()     # Ana pencereyi göster

    threading.Thread(target=init).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = tk.Tk()
    root.withdraw()  # Ana pencereyi başta gizle
    globals.root = root

    loading = Gui.loadingFrame(root)  # Yükleniyor ekranı göster
    start_app()  # Uygulama başlatma işlemi başlasın

    root.mainloop()
