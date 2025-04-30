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
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        exchange = globals.exchange
        leverage = globals.leverage
        usdt_amount = globals.usdt_amount
        tp_percent = globals.tp_percent
        sl_percent = globals.sl_percent

        if not Utils.binance_isolated.set_isolated_mode(binance_symbol):
            return

        exchange.set_leverage(leverage, symbol=symbol)

        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            return

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)
        if coin_amount <= 0:
            return

        order = exchange.create_market_order(symbol=symbol, side='buy', amount=coin_amount)

        entry_price = float(order['average']) if 'average' in order and order['average'] else market_price

        tp_price = round(entry_price * (1 + tp_percent / 100), 4)
        sl_price = round(entry_price * (1 - sl_percent / 100), 4)

        exchange.create_order(
            symbol=symbol, type='TAKE_PROFIT_MARKET', side='sell',
            amount=coin_amount, params={'triggerPrice': tp_price, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        exchange.create_order(
            symbol=symbol, type='STOP_MARKET', side='sell',
            amount=coin_amount, params={'triggerPrice': sl_price, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        messagebox.showinfo("İşlem Başarılı", f"{symbol} için işlem açıldı.\n"
                                              f"Miktar: {coin_amount} coin\n"
                                              f"Giriş: {entry_price}\nTP: {tp_price}\nSL: {sl_price}")

    except Exception as e:
        messagebox.showerror("İşlem Hatası", f"Hata: {e}")
