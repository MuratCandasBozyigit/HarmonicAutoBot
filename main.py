import customtkinter as ctk
import threading
import time
import Gui  # build_gui ve loadingFrame burada
import Utils.globals as globals

def start_app():
    def init():
        # Ağır işlem yapılacaksa burada (örneğin veri çekme)
        time.sleep(3)  # Örnek olarak 3 saniye bekleyelim
        globals.root.after(0, finish_init)  # finish_init'i ana iş parçacığında çalıştır

    def finish_init():
        Gui.build_gui(globals.root)  # GUI'yi başlat
        loading.stop_loading()  # Yükleniyor ekranını durdur
        globals.root.deiconify()  # Ana pencereyi göster

    threading.Thread(target=init, daemon=True).start()  # Arka planda başlat

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Temayı ayarla
    ctk.set_default_color_theme("blue")  # Tema rengi ayarla

    # Ana pencereyi oluşturuyoruz (CTk uyumlu)
    root = ctk.CTk()
    root.withdraw()  # Pencereyi başlatmadan önce gizle

    globals.root = root  # globals içinde root referansını sakla
    loading = Gui.loadingFrame(root)  # CTk uyumlu loadingFrame başlat
    start_app()  # Uygulama başlat

    root.mainloop()  # Ana döngüyü başlat
