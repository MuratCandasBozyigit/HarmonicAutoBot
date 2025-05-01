import customtkinter as ctk
import threading
import time

import Gui  # build_gui ve loadingFrame burada
import Utils.globals as globals

def start_app():
    def init():
        # Ağır işlem yapılacaksa burada (örneğin veri çekme)
        time.sleep(2)
        globals.root.after(0, finish_init)

    def finish_init():
        Gui.build_gui(globals.root)
        loading.stop_loading()
        globals.root.deiconify()

    threading.Thread(target=init, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Ana pencereyi oluşturuyoruz (artık CTk)
    root = ctk.CTk()
    root.withdraw()

    globals.root = root
    loading = Gui.loadingFrame(root)  # CTk uyumlu loadingFrame
    start_app()

    root.mainloop()
