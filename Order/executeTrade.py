import threading
import Utils
from Utils import globals as globals

def execute_trade():
    threading.Thread(target=_execute_trade_logic, daemon=True).start()

def _execute_trade_logic():
    try:
        # Sembol ve zaman dilimi
        raw_symbol = globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Exchange nesnesi ve ayarlar globals'tan
        exchange = globals.exchange
        leverage = globals.leverage
        usdt_amount = globals.usdt_amount
        tp_percent = globals.tp_percent
        sl_percent = globals.sl_percent

        # İzole moda geçir
        if not Utils.binance_isolated.set_isolated_mode(binance_symbol):
            return

        # Kaldıraç ayarla
        exchange.set_leverage(leverage, symbol=symbol)

        # Son kapanış fiyatını al
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            return

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)
        if coin_amount <= 0:
            return

        # 🚀 ANINDA MARKET EMRİ GÖNDER
        order = exchange.create_market_order(symbol=symbol, side='buy', amount=coin_amount)

        # Ortalama giriş fiyatı
        entry_price = float(order['average']) if 'average' in order and order['average'] else market_price

        # TP/SL fiyatları
        tp_price = round(entry_price * (1 + tp_percent / 100), 4)
        sl_price = round(entry_price * (1 - sl_percent / 100), 4)

        # TP ve SL emirlerini kur
        exchange.create_order(
            symbol=symbol, type='TAKE_PROFIT_MARKET', side='sell',
            amount=coin_amount, params={'triggerPrice': tp_price, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        exchange.create_order(
            symbol=symbol, type='STOP_MARKET', side='sell',
            amount=coin_amount, params={'triggerPrice': sl_price, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        print(f"✅ İşlem açıldı: {symbol} - {coin_amount} coin @ {entry_price} | TP: {tp_price}, SL: {sl_price}")

    except Exception as e:
        print("❌ execute_trade hatası:", e)
