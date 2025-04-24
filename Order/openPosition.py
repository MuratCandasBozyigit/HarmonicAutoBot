import ccxt
from Utils import globals
import Utils
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as msgbox

def open_position(entry_price, symbol_input=None):
    if not globals.emir_acik:
        return

    try:
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
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

        Utils.set_isolated_mode(globals.api_key, globals.api_secret, binance_symbol)

        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            return

        usdt_amount = globals.usdt_amount
        leverage = globals.leverage
        exchange.set_leverage(leverage, symbol=symbol)

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        order = exchange.create_market_order(
            symbol=symbol,
            side='buy',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        take_profit_price = round(entry_price * (1 + globals.tp_percent / 100), 2)
        stop_loss_price = round(entry_price * (1 - globals.sl_percent / 100), 2)

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

        root = ctk.CTk()
        root.withdraw()

        msgbox.showinfo("Short Pozisyon Açıldı", f"""
        {symbol} short işlemi açıldı ✅
        Giriş Fiyatı: {entry_price}
        TP: {take_profit_price}
        SL: {stop_loss_price}
        """)

        root.destroy()


    except ccxt.BaseError:
        pass
    except Exception:
        pass
