import customtkinter as ctk
import threading
import time

import Gui  # build_gui ve loadingFrame burada
import Utils.globals as globals
from Utils.path_utils import resource_path  # resource_path fonksiyonunu çekiyoruz

def start_app():
    def init():
        # Ağır işlem yapılacaksa burada (örneğin veri çekme)
        time.sleep(3)
        globals.root.after(0, finish_init)

    def finish_init():
        Gui.build_gui(globals.root)
        loading.stop_loading()
        globals.root.deiconify()

    threading.Thread(target=init, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Ana pencereyi oluştur
    root = ctk.CTk()
    root.withdraw()
    globals.root = root

    # Logo ikonunu ayarla (build sonrası uyumlu olacak şekilde)
    ico_path = resource_path("logo/logo.ico")
    try:
        root.iconbitmap(ico_path)
    except Exception as e:
        print("Icon yüklenemedi:", e)

    # Yükleme ekranı göster
    loading = Gui.loadingFrame(root)

    # Uygulamayı başlat
    start_app()
    root.mainloop()
