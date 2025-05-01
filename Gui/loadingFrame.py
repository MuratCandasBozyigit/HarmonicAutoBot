import tkinter as tk
from tkinter import ttk

class loadingFrame:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Yükleniyor...")
        self.top.geometry("400x200")
        self.top.grab_set()

        self.label = tk.Label(self.top, text="Grafikler Yükleniyor...", font=("Helvetica", 14))
        self.label.pack(pady=40)

        self.progress = ttk.Progressbar(self.top, mode='indeterminate')
        self.progress.pack(pady=20)
        self.progress.start()

    def stop_loading(self):
        self.progress.stop()
        self.top.destroy()
