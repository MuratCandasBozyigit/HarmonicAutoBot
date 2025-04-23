import ccxt
from Utils import globals 
import Utils
import os

def open_position(symbol_input=None):
    if not globals.emir_acik:
        return

    try:
        # Sembolü al ve formatla
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Binance bağlantısını oluştur
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)

        # İzole modu aktif et (eğer Utils içinde bu işlev varsa)
        Utils.set_isolated_mode(globals.api_key, globals.api_secret, binance_symbol)

        # OHLCV verisini al
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            print("Veri alınamadı veya boş veri geldi!")
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
        take_profit_order = exchange.create_order(
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
        stop_loss_order = exchange.create_order(
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

        # Başarıyla işlem yapıldığını bildir
        print(f"Pozisyon açıldı: {symbol} - Giriş Fiyatı: {entry_price}, TP: {take_profit_price}, SL: {stop_loss_price}")

    except ccxt.NetworkError as e:
        print(f"Ağ hatası oluştu: {str(e)}")
    except ccxt.ExchangeError as e:
        print(f"Borsa hatası oluştu: {str(e)}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {str(e)}")
