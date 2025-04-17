import tkinter as tk

start_price = None
end_price = None
percent_text = None
percent_mode = None  # Bu GUI'den sonra set edilecek

def init_percent_mode(root):
    global percent_mode
    percent_mode = tk.BooleanVar(master=root, value=False)

def toggle_percent_mode():
    if percent_mode:
        percent_mode.set(not percent_mode.get())
        print("Yüzde ölçüm modu:", "AÇIK" if percent_mode.get() else "KAPALI")

def activate(canvas, ax):
    canvas.mpl_connect("button_press_event", lambda event: on_click_percent_measure(event, ax, canvas))

def on_click_percent_measure(event, ax, canvas):
    global start_price, end_price, percent_text

    if not percent_mode or not percent_mode.get() or event.inaxes != ax:
        return

    y_clicked = event.ydata
    if y_clicked is None:
        return

    if start_price is None:
        start_price = y_clicked
        print(f"Başlangıç fiyatı: {start_price:.2f}")
    else:
        end_price = y_clicked
        change = ((end_price - start_price) / start_price) * 100
        percent_label = f"% Değişim: {change:+.2f}%"

        if percent_text:
            percent_text.remove()

        percent_text = ax.text(
            0.01, 0.98, percent_label,
            transform=ax.transAxes,
            fontsize=12,
            color="blue",
            verticalalignment="top",
            bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3')
        )

        print(percent_label)

        canvas.draw_idle()

        # Reset
        start_price = None
        end_price = None
        percent_mode.set(False)
