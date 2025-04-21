import Utils
from Utils import globals
import ccxt
import Gui
exchange = ccxt.binance({
    'apiKey':'991acee08da1311f39d71c52f7d8a12179e1a551096d7047573ed80d8271a8b3',
    'secret':'4a1bd0764cd29d8517f19b95a13650fe608dd95224b7adaf9cd387a0540ad5fb',
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
exchange.set_sandbox_mode(True) 
raw_symbol = Gui.symbol_var.get().strip().upper()
timeframe = Gui.timeframe_var.get()

def execute_trade():
    raw_symbol = Gui.symbol_var.get().strip().upper()
    symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
    binance_symbol = symbol.replace("/", "")
    timeframe = Gui.timeframe_var.get()
    Utils.set_isolated_mode('991acee08da1311f39d71c52f7d8a12179e1a551096d7047573ed80d8271a8b3', '4a1bd0764cd29d8517f19b95a13650fe608dd95224b7adaf9cd387a0540ad5fb', binance_symbol)

    df = Utils.get_ohlcv(symbol, timeframe)
    if df is None or df.empty:
        print("Uyarı", "İşlem için geçerli veri alınamadı!")
        return

    try:
        usdt_amount = 15  # Pozisyon büyüklüğü USDT
        leverage = 10     # Kaldıraç

        exchange.set_leverage(leverage, symbol=symbol)

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Long pozisyon aç
        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

       

        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * 1.005, 2)  # +0.5%
        stop_loss_price = round(entry_price * 0.99, 2)     # -1%

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


        msg = f"[LONG] İşlem açıldı - {symbol}\nTP: {take_profit_price} | SL: {stop_loss_price}"
        print("Başarılı", f"{msg}\nOrder ID: {order['id']}")
        print(order)

    except Exception as e:
        print(f"[execute_trade] {type(e).__name__}: {e}")
        print("Hata", f"İşlem sırasında hata oluştu:\n{e}")