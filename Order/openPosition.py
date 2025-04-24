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

def open_position(entry_price, symbol_input=None):
    if not globals.emir_acik:
        return

    # Tek bir root penceresi oluşturuluyor
    root = ctk.CTk()
    root.withdraw()  # Mesaj kutularında gösterilmeden önce pencere gizleniyor.

    try:
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Binance API bağlantısı
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)
        
        # İzole moda geçiş
        iso_result = set_isolated_mode(binance_symbol)
        if not iso_result:
            show_message(root, "İzolasyon Hatası", f"{symbol} için izolasyon moduna geçilemedi. İşlem iptal edildi.", icon="warning")
            return
     
        # Verilerin alınması
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            raise ValueError("İşlem için geçerli veri alınamadı!")

        usdt_amount = globals.usdt_amount
        leverage = globals.leverage
        exchange.set_leverage(leverage, symbol=symbol)

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Market emri ile işlem açma
        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * (1 + globals.tp_percent / 100), 2)
        stop_loss_price = round(entry_price * (1 - globals.sl_percent / 100), 2)

        # TP ve SL emirleri
        exchange.create_order(
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

        exchange.create_order(
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

        # Başarılı işlem mesajı
        msgbox.showinfo("Long Pozisyon Açıldı", f"""
        {symbol} long işlemi açıldı ✅
        Giriş Fiyatı: {entry_price}
        TP: {take_profit_price}
        SL: {stop_loss_price}
        """)

    except ccxt.InsufficientFunds:
        msgbox.showerror("Yetersiz Bakiye", "USDT bakiyeniz bu işlemi açmak için yetersiz.")

    except ccxt.InvalidOrder as e:
        msgbox.showerror("Geçersiz Emir", f"Emir oluşturulamadı. Hata: {str(e)}")

    except ccxt.BaseError as e:
        msgbox.showerror("Borsa Hatası", f"Binance API'den gelen bir hata oluştu.\n{str(e)}")

    except ValueError as e:
        msgbox.showwarning("Veri Hatası", str(e))

    except Exception as e:
        msgbox.showerror("Bilinmeyen Hata", f"Beklenmeyen bir hata oluştu:\n{str(e)}")

    finally:
        root.destroy()  # Pencere kapatılıyor
