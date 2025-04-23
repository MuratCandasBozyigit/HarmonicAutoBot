import customtkinter as ctk
from tkinter import messagebox
import os
from dotenv import load_dotenv, set_key

load_dotenv()

def open_settings_window(root):
    win = ctk.CTkToplevel(root)
    win.title("Ayarlar")
    win.geometry("380x650")
    win.resizable(False, False)

    # Başlık
    ctk.CTkLabel(win, text="Genel Ayarlar", font=("Arial", 18, "bold")).pack(pady=10)

    # Tema Seçimi
    ctk.CTkLabel(win, text="Tema Seçimi:", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    theme_var = ctk.StringVar(value=ctk.get_appearance_mode().capitalize())
    theme_selector = ctk.CTkOptionMenu(win, values=["Light", "Dark", "System"], variable=theme_var)
    theme_selector.pack(padx=20, fill="x")

    def apply_theme():
        selected = theme_var.get().lower()
        ctk.set_appearance_mode(selected)
        messagebox.showinfo("Tema", f"Tema '{selected.capitalize()}' olarak ayarlandı.")

    ctk.CTkButton(win, text="Temayı Uygula", command=apply_theme).pack(padx=20, pady=10, fill="x")

    # API Key
    ctk.CTkLabel(win, text="API Key:", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    api_key_entry = ctk.CTkEntry(win, width=280)
    api_key_entry.insert(0, os.getenv("REAL_API_KEY", ""))
    api_key_entry.pack(padx=20, fill="x")

    # Secret Key
    ctk.CTkLabel(win, text="Secret Key:", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    api_secret_entry = ctk.CTkEntry(win, width=280, show="*")
    api_secret_entry.insert(0, os.getenv("REAL_API_SECRET", ""))
    api_secret_entry.pack(padx=20, fill="x")

    # Leverage
    ctk.CTkLabel(win, text="Kaldıraç (Leverage):", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    leverage_entry = ctk.CTkEntry(win, width=280)
    leverage_entry.insert(0, os.getenv("LEVERAGE", "10"))
    leverage_entry.pack(padx=20, fill="x")

    # USDT Amount
    ctk.CTkLabel(win, text="Pozisyon Miktarı (USDT):", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    usdt_entry = ctk.CTkEntry(win, width=280)
    usdt_entry.insert(0, os.getenv("USDT_AMOUNT", "0.5"))
    usdt_entry.pack(padx=20, fill="x")

    # Testnet Seçimi
    use_testnet_var = ctk.BooleanVar(value=os.getenv("USE_TESTNET", "False") == "True")
    ctk.CTkCheckBox(win, text="Testnet Kullan", variable=use_testnet_var).pack(padx=20, pady=15)

    # Ayarları Kaydet
    def save_settings():
        set_key(".env", "REAL_API_KEY", api_key_entry.get())
        set_key(".env", "REAL_API_SECRET", api_secret_entry.get())
        set_key(".env", "LEVERAGE", leverage_entry.get())
        set_key(".env", "USDT_AMOUNT", usdt_entry.get())
        set_key(".env", "USE_TESTNET", str(use_testnet_var.get()))
        messagebox.showinfo("Başarılı", "✅ Ayarlar başarıyla kaydedildi.")

    ctk.CTkButton(win, text="💾 Kaydet", command=save_settings).pack(padx=20, pady=20, fill="x")
