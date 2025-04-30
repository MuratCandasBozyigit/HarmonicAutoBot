import ccxt
from Utils import globals
import Utils
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as msgbox
from Utils.binance_isolated import set_isolated_mode


def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)


def open_position(entry_price=None, symbol_input=None):
    if not globals.emir_acik:
        return

    root = ctk.CTk()
    root.withdraw()

    try:
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Pozisyon zaten açık mı kontrolü
        if symbol in globals.open_positions:
            return

        # İzole moda geç
        iso_result = set_isolated_mode(binance_symbol)
        if not iso_result:
            return

        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            return

        market_price = df['close'].iloc[-1]
        coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

        # Kaldıraç ayarla
        globals.exchange.set_leverage(globals.leverage, symbol=symbol)

        # ✅ Market long emri
        order = globals.exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        # Giriş fiyatı
        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * (1 + globals.tp_percent / 100), 4)
        stop_loss_price = round(entry_price * (1 - globals.sl_percent / 100), 4)

        # ✅ TP emri
        globals.exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='sell',
            amount=coin_amount,
            params={
                'stopPrice': take_profit_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # ✅ SL emri
        globals.exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='sell',
            amount=coin_amount,
            params={
                'stopPrice': stop_loss_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # ✅ Pozisyonu işaretle
        globals.open_positions.add(symbol)

        # 🟢 Bilgi mesajı
        msgbox.showinfo("Pozisyon Açıldı",
            f"{symbol} işlemi açıldı ✅\n"
            f"Giriş: {entry_price:.4f}\n"
            f"TP: {take_profit_price:.4f}\n"
            f"SL: {stop_loss_price:.4f}"
        )

    except ccxt.BaseError as e:
        msgbox.showerror("Binance Hatası", str(e))
    except Exception as e:
        msgbox.showerror("Hata", str(e))
    finally:
        root.destroy()
