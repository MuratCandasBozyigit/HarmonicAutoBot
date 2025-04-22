import ccxt
from Utils import globals 
import Utils
import os

def open_position(entry_price, symbol_input=None):
    if not globals.emir_acik:
        print("Emir modu kapalı, işlem açılmadı.")
        return
    try:
           # Binance bağlantısını oluştur
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'} 
        })

        exchange.set_sandbox_mode(globals.use_testnet)

        # Sembolü al ve formatla
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # İzole modu aktif et (eğer Utils içinde bu işlev varsa)
        Utils.set_isolated_mode(globals.api_key, globals.api_secret, binance_symbol)

        # OHLCV verisini al
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            print("Uyarı", "İşlem için geçerli veri alınamadı!")
            return

        # Parametreleri al
        usdt_amount = globals.usdt_amount
        leverage = globals.leverage

        # Kaldıraç ayarla
        exchange.set_leverage(leverage, symbol=symbol)

        # Miktar hesapla
        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Long pozisyon aç
        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        # Giriş fiyatı, TP ve SL hesapla
        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * (1 + globals.tp_percent / 100), 2)
        stop_loss_price = round(entry_price * (1 - globals.sl_percent / 100), 2)

        # TP emri
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

        # SL emri
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

        print(f"[LONG] {symbol} işlemi açıldı. TP: {take_profit_price}, SL: {stop_loss_price}")
    except Exception as e:
        print(f"[open_position] {type(e).__name__}: {e}")
