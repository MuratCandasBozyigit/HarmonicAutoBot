import customtkinter as ctk
from tkinter import messagebox
import os
from dotenv import load_dotenv, set_key

load_dotenv()

# Ana pencere referansı (dışarıdan root geçirilmeli)
def open_settings_window(root):
    win = ctk.CTkToplevel(root)
    win.title("API Ayarları")
    win.geometry("350x400")

    # API Key
    ctk.CTkLabel(win, text="API Key:").pack(pady=(15, 5))
    api_key_entry = ctk.CTkEntry(win, width=280)
    api_key_entry.insert(0, os.getenv("REAL_API_KEY", ""))
    api_key_entry.pack()

    # Secret Key
    ctk.CTkLabel(win, text="Secret Key:").pack(pady=(15, 5))
    api_secret_entry = ctk.CTkEntry(win, width=280, show="*")
    api_secret_entry.insert(0, os.getenv("REAL_API_SECRET", ""))
    api_secret_entry.pack()

    # Leverage
    ctk.CTkLabel(win, text="Kaldıraç (Leverage):").pack(pady=(15, 5))
    leverage_entry = ctk.CTkEntry(win, width=280)
    leverage_entry.insert(0, os.getenv("LEVERAGE", "10"))
    leverage_entry.pack()

    # USDT Amount
    ctk.CTkLabel(win, text="Pozisyon Miktarı (USDT):").pack(pady=(15, 5))
    usdt_entry = ctk.CTkEntry(win, width=280)
    usdt_entry.insert(0, os.getenv("USDT_AMOUNT", "0.5"))
    usdt_entry.pack()

    # Testnet Seçeneği
    use_testnet_var = ctk.BooleanVar(value=os.getenv("USE_TESTNET", "False") == "True")
    ctk.CTkCheckBox(win, text="Testnet Kullan", variable=use_testnet_var).pack(pady=15)

    # Kaydet Butonu
    def save_settings():
        set_key(".env", "REAL_API_KEY", api_key_entry.get())
        set_key(".env", "REAL_API_SECRET", api_secret_entry.get())
        set_key(".env", "LEVERAGE", leverage_entry.get())
        set_key(".env", "USDT_AMOUNT", usdt_entry.get())
        set_key(".env", "USE_TESTNET", str(use_testnet_var.get()))
        messagebox.showinfo("Başarılı", "✅ Ayarlar kaydedildi.")

    ctk.CTkButton(win, text="Kaydet", command=save_settings).pack(pady=10)
