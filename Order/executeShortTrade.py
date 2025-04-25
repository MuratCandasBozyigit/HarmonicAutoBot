import ccxt
from Utils import globals
import Utils
import time
import hmac
import hashlib
import requests
import customtkinter as ctk
from Utils.binance_isolated import set_isolated_mode

def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)


def execute_short_trade():
    root = ctk.CTk()  # Message box için kök pencere

    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = globals.timeframe_var.get()

    # Binance bağlantısı
    try:
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)
    except Exception as e:
        show_message(root, "Bağlantı Hatası", f"Binance API bağlantısı başarısız:\n{e}", icon="cancel")
        return

    iso_result = set_isolated_mode(binance_symbol)
    if not iso_result:
        show_message(root, "Margin Hatası", f"{symbol} için izolasyon moduna geçilemedi. İşlem iptal edildi.", icon="cancel")
        return


    # Kaldıraç ve veri çekimi
    try:
        exchange.set_leverage(globals.leverage, symbol=symbol)
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            show_message(root, "Veri Uyarısı", "İşlem için geçerli veri alınamadı!", icon="warning")
            return
    except Exception as e:
        show_message(root, "Veri/Kaldıraç Hatası", f"Hata oluştu:\n{e}", icon="cancel")
        return

    # Coin miktarı hesaplama
    market_price = df['close'].iloc[-1]
    coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

    # Short işlemi ve TP/SL emirleri
    try:
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        tp = round(entry_price * (1 - globals.tp_percent / 100), 2)
        sl = round(entry_price * (1 + globals.sl_percent / 100), 2)

               # TP Order
        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='buy',
            amount=coin_amount,
            params={
                'stopPrice': tp,
                'price': tp,               # <-- Bunu da ekliyoruz, kritik!
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # SL Order
        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='buy',
            amount=coin_amount,
            params={
                'stopPrice': sl,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )


        show_message(root, "SHORT İşlem Açıldı", f"{symbol} SHORT açıldı.\nTP: {tp}, SL: {sl}\nİzole Mod: ✅", icon="check")
    except ccxt.BaseError as e:
        show_message(root, "API Hatası", f"Binance API hatası:\n{e}", icon="cancel")
    except Exception as e:
        show_message(root, "Beklenmeyen Hata", f"Hata:\n{e}", icon="cancel")
