import tkinter as tk
from tkinter import Toplevel, Label

def show_timed_message(title, message, duration=5000):  # duration = milisaniye
    win = Toplevel()
    win.title(title)
    win.geometry("300x100")
    win.configure(bg="#fefefe")
    win.attributes("-topmost", True)

    label = Label(win, text=message, font=("Arial", 11), wraplength=280, bg="#fefefe")
    label.pack(pady=20)

    # 5 saniye sonra pencereyi otomatik kapat
    win.after(duration, win.destroy)
