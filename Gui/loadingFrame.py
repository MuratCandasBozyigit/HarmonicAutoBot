import customtkinter as ctk

class loadingFrame:
    def __init__(self, master):
        self.top = ctk.CTkToplevel(master)
        self.top.title("Yükleniyor...")
        self.top.geometry("400x200")
        self.top.resizable(False, False)
        self.top.grab_set()

        self.label = ctk.CTkLabel(self.top, text="Grafikler Yükleniyor...", font=ctk.CTkFont(size=16))
        self.label.pack(pady=40)

        self.progress = ctk.CTkProgressBar(self.top, mode="indeterminate", width=300)
        self.progress.pack(pady=20)
        self.progress.start()

    def stop_loading(self):
        self.progress.stop()
        self.top.destroy()
