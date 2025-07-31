import threading
import Utils
from Utils import globals as globals
import tkinter.messagebox as messagebox

def execute_trade():
    threading.Thread(target=_execute_trade_logic, daemon=True).start()


def _execute_trade_logic():
    try:
        raw_symbol = globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        exchange_name = globals.exchange.id.lower()

        # Exchange özel sembol formatı (Örn: MEXC'de BTC/USDT yerine BTC_USDT)
        if exchange_name == "mexc":
            symbol = symbol.replace("/", "_")
        elif exchange_name == "bitget":
            symbol = symbol.replace("/", "") + "_UMCBL"

        leverage = globals.leverage
        usdt_amount = globals.usdt_amount
        tp_percent = globals.tp_percent
        sl_percent = globals.sl_percent

        # Kaldıraç ayarı (exchange'e göre)
        if exchange_name in ["binance", "bybit", "bitget"]:
            globals.exchange.set_leverage(leverage, symbol)

        # Piyasa fiyatını al
        ticker = globals.exchange.fetch_ticker(symbol)
        market_price = ticker['last']
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Long işlem aç
        order = globals.exchange.create_market_order(symbol, 'buy', coin_amount)

        # TP/SL ayarları (exchange'e göre)
        entry_price = order['average'] if 'average' in order else market_price
        tp_price = entry_price * (1 + tp_percent / 100)
        sl_price = entry_price * (1 - sl_percent / 100)

        # Exchange'e özel TP/SL
        if exchange_name == "binance":
            globals.exchange.create_order(
                symbol, 'TAKE_PROFIT_MARKET', 'sell', coin_amount,
                params={'stopPrice': tp_price, 'reduceOnly': True}
            )
            globals.exchange.create_order(
                symbol, 'STOP_MARKET', 'sell', coin_amount,
                params={'stopPrice': sl_price, 'reduceOnly': True}
            )
        elif exchange_name == "bybit":
            globals.exchange.create_order(
                symbol, 'TAKE_PROFIT', 'sell', coin_amount,
                params={'stop_loss': sl_price, 'take_profit': tp_price}
            )
        elif exchange_name == "mexc":
            globals.exchange.create_order(
                symbol, 'TAKE_PROFIT_LIMIT', 'sell', coin_amount,
                params={'stopPrice': tp_price, 'stopLossPrice': sl_price}
            )

        messagebox.showinfo("Başarılı", f"{symbol} işlemi açıldı!")

    except Exception as e:
        messagebox.showerror("Hata", f"İşlem açılamadı: {str(e)}")