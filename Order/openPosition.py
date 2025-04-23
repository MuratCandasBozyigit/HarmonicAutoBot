import ccxt
from Utils import globals
import Utils
import os

def open_position(entry_price, symbol_input=None):
    try:
        # Sembol ve zaman dilimi
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Binance bağlantısı
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)

        # İzole mod
        Utils.set_isolated_mode(globals.api_key, globals.api_secret, binance_symbol)

        # OHLCV veri kontrolü
        df = Utils.get_ohlcv(symbol, timeframe)
       

        usdt_amount = globals.usdt_amount
        leverage = globals.leverage

        try:
            exchange.set_leverage(leverage, symbol=symbol)
        except Exception:
            pass

        # Miktar hesapla
        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Long işlemi
        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        # Fiyatlar
        entry_price = float(order.get('average', market_price))
        tp = round(entry_price * (1 + globals.tp_percent / 100), 2)
        sl = round(entry_price * (1 - globals.sl_percent / 100), 2)

        # TP
        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='sell',
            amount=coin_amount,
            params={'stopPrice': tp, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        # SL
        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='sell',
            amount=coin_amount,
            params={'stopPrice': sl, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )


    except Exception :
        pass
