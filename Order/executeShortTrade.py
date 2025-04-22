import ccxt
from Utils import globals
import Utils

def execute_short_trade():
    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = globals.timeframe_var.get()

    exchange = ccxt.binance({
        'apiKey': globals.api_key,
        'secret': globals.api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })
    exchange.set_sandbox_mode(globals.use_testnet)

    try:
        exchange.set_leverage(globals.leverage, symbol=symbol)
    except Exception as e:
        print(f"Kaldıraç ayarlanamadı: {e}")
        return

    df = Utils.get_ohlcv(symbol, timeframe)
    if df is None or df.empty:
        print("Uyarı", "İşlem için geçerli veri alınamadı!")
        return

    market_price = df['close'].iloc[-1]
    coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

    try:
        # SHORT: Sell order
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price

        # SHORT: TP daha düşük, SL daha yüksek
        tp = round(entry_price * (1 - globals.tp_percent / 100), 2)
        sl = round(entry_price * (1 + globals.sl_percent / 100), 2)

        # TP: Buy (pozisyonu kapatmak için)
        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='buy',
            amount=coin_amount,
            params={'stopPrice': tp, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        # SL: Buy (pozisyonu kapatmak için)
        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='buy',
            amount=coin_amount,
            params={'stopPrice': sl, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        print(f"[SHORT] {symbol} işlemi açıldı. Giriş: {entry_price}, TP: {tp}, SL: {sl}")
    except Exception as e:
        print(f"[HATA] {e}")
