import ccxt
from Utils import globals
import Utils
import time
import hmac
import hashlib
import requests
import customtkinter as ctk

def set_isolated_mode(api_key, api_secret, symbol, use_testnet=False):
    base_url = "https://testnet.binancefuture.com" if use_testnet else "https://fapi.binance.com"
    endpoint = "/fapi/v1/marginType"
    timestamp = int(time.time() * 1000)

    binance_symbol = symbol.replace("/", "")
    params = f"symbol={binance_symbol}&marginType=ISOLATED&timestamp={timestamp}"
    signature = hmac.new(api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {
        "X-MBX-APIKEY": api_key
    }

    url = f"{base_url}{endpoint}?{params}&signature={signature}"
    response = requests.post(url, headers=headers)

    if response.status_code != 200 and "marginType is already ISOLATED" not in response.text:
        raise Exception(f"İzole moda geçiş başarısız: {response.text}")

def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)

def execute_short_trade():
    root = ctk.CTk()  # Create the root window for message boxes

    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = globals.timeframe_var.get()

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

    # İzole moda geçiş
    try:
        set_isolated_mode(globals.api_key, globals.api_secret, symbol, globals.use_testnet)
    except Exception as e:
        show_message(root, "İzolasyon Hatası", f"İzole moda geçiş başarısız:\n{e}", icon="warning")
        return

    try:
        exchange.set_leverage(globals.leverage, symbol=symbol)
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            show_message(root, "Veri Uyarısı", "İşlem için geçerli veri alınamadı!", icon="warning")
            return
    except Exception as e:
        show_message(root, "Veri/Kaldıraç Hatası", f"Hata oluştu:\n{e}", icon="cancel")
        return

    market_price = df['close'].iloc[-1]
    coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

    try:
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        tp = round(entry_price * (1 - globals.tp_percent / 100), 2)
        sl = round(entry_price * (1 + globals.sl_percent / 100), 2)

        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='buy',
            amount=coin_amount,
            params={'stopPrice': tp, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='buy',
            amount=coin_amount,
            params={'stopPrice': sl, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        show_message(root, "SHORT İşlem Açıldı", f"{symbol} SHORT açıldı.\nTP: {tp}, SL: {sl}", icon="check")
    except ccxt.BaseError as e:
        show_message(root, "API Hatası", f"Binance API hatası:\n{e}", icon="cancel")
    except Exception as e:
        show_message(root, "Beklenmeyen Hata", f"Hata:\n{e}", icon="cancel")
