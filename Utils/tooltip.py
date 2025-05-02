import tkinter as tk
import customtkinter as ctk

class ToolTip:
    def __init__(self, widget, text="Tooltip", bg="#1a1a1a", fg="white", font=("Arial", 10), delay=300):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.font = font
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        widget.bind("<Enter>", self.schedule_show)
        widget.bind("<Leave>", self.hide_tooltip)

    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 50
        y = self.widget.winfo_rooty() + 10

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(bg=self.bg)

        # Tooltip etiketi
        label = ctk.CTkLabel(tw, text=self.text, text_color=self.fg, font=self.font, fg_color=self.bg, corner_radius=6)
        label.pack(padx=5, pady=3)

    def hide_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
