import customtkinter as ctk
from dotenv import set_key
import Utils.globals as globals

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title="Bilgi", message=""):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(self, text=message, font=("Arial", 14), wraplength=260).pack(pady=20)
        ctk.CTkButton(self, text="Tamam", command=self.destroy).pack(pady=10)

def open_settings_window(root):
    win = ctk.CTkToplevel(root)
    win.title("⚙️ Ayarlar")
    win.geometry("400x620")
    win.resizable(False, True)
    win.grab_set()

    # Etiket ve girişler
    ctk.CTkLabel(win, text="Binance API Key:").pack(pady=5)
    api_key_entry = ctk.CTkEntry(win, width=300)
    api_key_entry.insert(0, globals.api_key)
    api_key_entry.pack()

    ctk.CTkLabel(win, text="Binance API Secret:").pack(pady=5)
    api_secret_entry = ctk.CTkEntry(win, width=300)
    api_secret_entry.insert(0, globals.api_secret)
    api_secret_entry.pack()

    ctk.CTkLabel(win, text="Kaldıraç (Örn: 10):").pack(pady=5)
    leverage_entry = ctk.CTkEntry(win, width=100)
    leverage_entry.insert(0, str(globals.leverage))
    leverage_entry.pack()
   
    ctk.CTkLabel(win, text="Take Profit (%)").pack(pady=5)
    tp_entry = ctk.CTkEntry(win, width=100)
    tp_entry.insert(0, str(globals.tp_percent))
    tp_entry.pack()

    ctk.CTkLabel(win, text="Stop Loss (%)").pack(pady=5)
    sl_entry = ctk.CTkEntry(win, width=100)
    sl_entry.insert(0, str(globals.sl_percent))
    sl_entry.pack()

    ctk.CTkLabel(win, text="Pozisyon Tutarı (USDT):").pack(pady=5)
    usdt_entry = ctk.CTkEntry(win, width=100)
    usdt_entry.insert(0, str(globals.usdt_amount))
    usdt_entry.pack()

    ctk.CTkLabel(win, text="Testnet Modu:").pack(pady=5)
    use_testnet_var = ctk.BooleanVar(value=globals.use_testnet)
    ctk.CTkSwitch(win, text="Testnet'i Kullan", variable=use_testnet_var).pack()

    ctk.CTkLabel(win, text="Tema Seç:").pack(pady=5)
    theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
    theme_option = ctk.CTkOptionMenu(win, variable=theme_var, values=["Light", "Dark", "System"])
    theme_option.pack()

    def apply_theme():
        selected = theme_var.get().lower()
        ctk.set_appearance_mode(selected)
        CustomMessageBox(win, title="Tema", message=f"Tema '{selected.capitalize()}' olarak ayarlandı.")

    def save_settings():
        set_key(".env", "REAL_API_KEY", api_key_entry.get())
        set_key(".env", "REAL_API_SECRET", api_secret_entry.get())
        set_key(".env", "LEVERAGE", leverage_entry.get())
        set_key(".env", "USDT_AMOUNT", usdt_entry.get())
        set_key(".env", "USE_TESTNET", str(use_testnet_var.get()))
        set_key(".env", "TP_PERCENT", tp_entry.get())
        set_key(".env", "SL_PERCENT", sl_entry.get())

        globals.update_globals()
        CustomMessageBox(win, title="Başarılı", message="✅ Ayarlar başarıyla kaydedildi.")

    ctk.CTkButton(win, text="Temayı Uygula", command=apply_theme).pack(pady=10)
    ctk.CTkButton(win, text="Kaydet ve Kapat", command=lambda: [save_settings(), win.destroy()]).pack(pady=10)
