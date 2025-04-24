import ccxt
from Utils import globals
import Utils
import os
import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox as msgbox
import Utils.binance_isolated as iso
def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)


def open_short_position(entry_price=None, symbol_input=None):
    root = ctk.CTk()  # Ana pencere oluşturuldu
    root.withdraw()  # Pencereyi gizle
    
    try:
        # Sembol bilgilerini al
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Binance bağlantısını kur
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)

        # 1. İzole mod kontrolü
        try:
            position_info = exchange.fetch_positions_risk([binance_symbol])
            if not position_info:
                show_message(root, "Pozisyon Hatası", "Pozisyon bilgisi alınamadı", icon="cancel")
                return
            
            if position_info[0]['marginType'].lower() != 'isolated':  # Düzeltme: 'isolated' olacak
                show_message(root, "Margin Tipi Hatası", 
                           f"{binance_symbol} izole modda değil!\nLütfen önce izole moda geçin.", 
                           icon="cancel")
                return
        except Exception as e:
            show_message(root, "Sistem Hatası", 
                       f"Margin tipi kontrolü başarısız:\n{str(e)}", 
                       icon="cancel")
            return

        # 2. Verileri al ve kontrol et
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            raise ValueError("İşlem için yeterli veri alınamadı.")

        # 3. Kaldıraç ayarla ve miktarı hesapla
        usdt_amount = globals.usdt_amount
        leverage = globals.leverage
        exchange.set_leverage(leverage, symbol=symbol)

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # 4. Short pozisyon aç
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=coin_amount
        )

        # 5. TP/SL ayarları
        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * (1 - globals.tp_percent / 100), 2)
        stop_loss_price = round(entry_price * (1 + globals.sl_percent / 100), 2)

        # 6. TP emri oluştur
        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='buy',
            amount=coin_amount,
            params={
                'stopPrice': take_profit_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # 7. SL emri oluştur
        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='buy',
            amount=coin_amount,
            params={
                'stopPrice': stop_loss_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # 8. Başarılı mesajı göster
        msgbox.showinfo("Short Pozisyon Açıldı", f"""
        {symbol} short işlemi açıldı ✅
        Giriş Fiyatı: {entry_price}
        TP: {take_profit_price}
        SL: {stop_loss_price}
        """)

    except ccxt.InsufficientFunds as e:
        msgbox.showerror("Yetersiz Bakiye", "USDT bakiyeniz işlem açmak için yetersiz!")

    except ccxt.InvalidOrder as e:
        msgbox.showerror("Geçersiz Emir", f"Emir oluşturulamadı. Detay: {str(e)}")

    except ccxt.BaseError as e:
        msgbox.showerror("Borsa Hatası", f"Binance tarafında bir hata oluştu.\n{str(e)}")

    except ValueError as e:
        msgbox.showwarning("Veri Hatası", str(e))

    except Exception as e:
        msgbox.showerror("Bilinmeyen Hata", f"Bir hata oluştu: {str(e)}")

    finally:
        root.destroy()  # Pencereyi kapat