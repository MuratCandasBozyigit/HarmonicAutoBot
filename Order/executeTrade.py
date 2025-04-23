import ccxt
from Utils import globals
import Utils

def execute_trade():
    # Kullanıcıdan alınan sembol ve zaman dilimi
    raw_symbol = globals.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = globals.timeframe_var.get()

    # Binance API bağlantısı (testnet seçeneği)
    try:
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)
    except Exception as e:
        print(f"[HATA] Binance API bağlantısı başarısız: {e}")
        return

    # Kaldıraç ve işlem yapılacak veri
    try:
        exchange.set_leverage(globals.leverage, symbol=symbol)
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            print("Uyarı: İşlem için geçerli veri alınamadı!")
            return
    except Exception as e:
        print(f"[HATA] Veri çekme veya kaldıraç ayarı hatası: {e}")
        return

    # İşlem miktarı ve fiyat hesaplaması
    market_price = df['close'].iloc[-1]
    coin_amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

    try:
        # Piyasa emri oluşturuluyor
        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        tp = round(entry_price * (1 + globals.tp_percent / 100), 2)
        sl = round(entry_price * (1 - globals.sl_percent / 100), 2)

        # Take Profit ve Stop Loss emirleri
        exchange.create_order(
            symbol=symbol,
            type='take_profit_market',
            side='sell',
            amount=coin_amount,
            params={'stopPrice': tp, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        exchange.create_order(
            symbol=symbol,
            type='stop_market',
            side='sell',
            amount=coin_amount,
            params={'stopPrice': sl, 'reduceOnly': True, 'workingType': 'MARK_PRICE'}
        )

        print(f"[LONG] {symbol} işlemi açıldı. TP: {tp}, SL: {sl}")
    except ccxt.BaseError as e:
        print(f"[HATA] Binance API hatası: {e}")
    except Exception as e:
        print(f"[HATA] Beklenmeyen hata: {e}")
