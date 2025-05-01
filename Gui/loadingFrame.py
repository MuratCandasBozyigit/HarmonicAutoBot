import tkinter as tk
from tkinter import ttk

class loadingFrame:
    def __init__(self, master):
        self.top = tk.Toplevel(master)  # Yeni bir pencere oluştur
        self.top.title("Yükleniyor...")
        self.top.geometry("400x200")
        self.top.grab_set()  # Ana pencereyi kilitle

        self.frame = tk.Frame(self.top)
        self.frame.pack(expand=True)

        self.label = tk.Label(self.frame, text="Grafikler Yükleniyor...", font=("Helvetica", 16))
        self.label.pack(pady=50)

        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=20)
        self.progress.start()

    def stop_loading(self):
        self.progress.stop()
        self.top.destroy()  # loading penceresini kapat
