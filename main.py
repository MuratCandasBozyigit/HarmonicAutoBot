import tkinter as tk
import customtkinter as ctk
import threading
import time

import Gui  # build_gui ve loadingFrame burada
import Utils.globals as globals

def start_app():
    def init():
        # Ağır işlem yapılacaksa burada (sadece hesaplama, GUI değil)
        time.sleep(2)  # Simülasyon (gerçek hayatta veri çekme olabilir)

        # build_gui GUI öğelerine dokunduğu için ana thread'e alınmalı
        globals.root.after(0, finish_init)

    def finish_init():
        Gui.build_gui(globals.root)
        loading.stop_loading()
        globals.root.deiconify()

    threading.Thread(target=init).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = tk.Tk()
    root.withdraw()
    globals.root = root

    loading = Gui.loadingFrame(root)  # Loading ekranını göster
    start_app()  # Arka planda işlem başlasın

    root.mainloop()
