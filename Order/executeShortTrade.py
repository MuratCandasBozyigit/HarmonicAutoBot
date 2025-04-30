from Utils import globals
from Utils.binance_isolated import set_isolated_mode
import ccxt
import Utils
import customtkinter as ctk

def show_message(title, message, icon="info"):
    message_box = ctk.CTkToplevel()
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)

def execute_short_trade():
    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = globals.timeframe_var.get()
    exchange = globals.exchange

    # İzolasyon Modu
    if not set_isolated_mode(binance_symbol):
        show_message("İzolasyon Hatası", f"{symbol} için izolasyon moduna geçilemedi.", icon="warning")
        return

    try:
        # Kaldıraç Ayarı
        exchange.set_leverage(globals.leverage, symbol=symbol)

        # Fiyat ve Miktar Hesaplama
        ticker = exchange.fetch_ticker(symbol)
        market_price = ticker['last']
        coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

        if coin_amount <= 0:
            show_message("Hatalı Miktar", "İşlem miktarı sıfır!", icon="warning")
            return

        # SHORT Pozisyon Aç
        order = exchange.create_market_order(symbol=symbol, side='sell', amount=coin_amount)

        if not order or order.get('status') not in ['open', 'closed', 'filled']:
            show_message("İşlem Hatası", "Short işlemi açılamadı!", icon="cancel")
            return

        entry_price = float(order['average']) if order.get('average') else market_price
        tp_price = round(entry_price * (1 - globals.tp_percent / 100), 4)
        sl_price = round(entry_price * (1 + globals.sl_percent / 100), 4)

        # Pozisyon takibi için işaretleme
        globals.open_positions.add(symbol + "_short")

        # TP & SL emirleri
        exchange.create_order(
            symbol=symbol,
            type='TAKE_PROFIT_MARKET',
            side='buy',
            amount=coin_amount,
            params={
                'triggerPrice': tp_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        exchange.create_order(
            symbol=symbol,
            type='STOP_MARKET',
            side='buy',
            amount=coin_amount,
            params={
                'triggerPrice': sl_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # Başarılı mesaj
        show_message(
            "SHORT Açıldı",
            f"{symbol} SHORT açıldı\nGiriş: {entry_price}\nTP: {tp_price}\nSL: {sl_price}",
            icon="check"
        )

    except ccxt.BaseError as e:
        show_message("API Hatası", str(e), icon="cancel")
    except Exception as e:
        show_message("Hata", str(e), icon="cancel")
