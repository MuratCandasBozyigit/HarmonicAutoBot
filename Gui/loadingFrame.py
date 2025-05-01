import customtkinter as ctk

class loadingFrame:
    def __init__(self, master):
        self.top = ctk.CTkToplevel(master)
        self.top.title("Yükleniyor...")
        self.top.geometry("400x200")
        self.top.grab_set()

        self.label = ctk.CTkLabel(self.top, text="Grafikler Yükleniyor...", font=ctk.CTkFont(size=14))
        self.label.pack(pady=40)

        self.progress = ctk.CTkProgressBar(self.top, orientation="horizontal", mode="indeterminate")
        self.progress.pack(pady=20, padx=20, fill="x")
        self.progress.start()

    def stop_loading(self):
        self.progress.stop()
        self.top.destroy()
