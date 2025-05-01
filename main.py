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
        
        # Ağır işlem bittiğinde GUI'yi ana thread üzerinde güncellemek için finish_init'i çağırıyoruz.
        globals.root.after(0, finish_init)  # Ana thread üzerinde GUI işlemi

    def finish_init():
        Gui.build_gui(globals.root)
        loading.stop_loading()  # Yükleniyor ekranını kapat
        globals.root.deiconify()  # Ana pencereyi göster

    # Başka bir thread üzerinde init fonksiyonunu çalıştırıyoruz.
    threading.Thread(target=init, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = tk.Tk()
    root.withdraw()  # Ana pencereyi başta gizle
    globals.root = root

    loading = Gui.loadingFrame(root)  # Yükleniyor ekranını göster
    start_app()  # Arka planda işlem başlasın

    root.mainloop()  # Tkinter ana döngüsü
