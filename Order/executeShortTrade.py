import ccxt
from Utils import globals
import Utils
import customtkinter as ctk
from Utils.binance_isolated import set_isolated_mode

def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)

def execute_short_trade(entry_price, symbol_input=None):
    if not globals.emir_acik:
        return

    # Local değişken olarak open_positions kümesini başlatıyoruz
    open_positions = set()

    # Tek bir root penceresi oluşturuluyor
    root = ctk.CTk()
    root.withdraw()  # Mesaj kutularında gösterilmeden önce pencere gizleniyor.

    try:
        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Eğer pozisyon zaten açıksa işlem açma
        if symbol in open_positions:
            show_message(root, "İşlem Zaten Açık", f"{symbol} için pozisyon zaten açık.", icon="warning")
            return

        # Binance API bağlantısı
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        exchange.set_sandbox_mode(globals.use_testnet)
        
        # İzole moda geçiş
        iso_result = set_isolated_mode(binance_symbol)
        if not iso_result:
            show_message(root, "İzolasyon Hatası", f"{symbol} için izolasyon moduna geçilemedi. İşlem iptal edildi.", icon="warning")
            return
     
        # Verilerin alınması
        df = Utils.get_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            raise ValueError("İşlem için geçerli veri alınamadı!")

        usdt_amount = globals.usdt_amount
        leverage = globals.leverage
        exchange.set_leverage(leverage, symbol=symbol)

        market_price = df['close'].iloc[-1]
        coin_amount = round((usdt_amount * leverage) / market_price, 3)

        # Short işlemi açma
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=coin_amount
        )

        entry_price = float(order['average']) if 'average' in order else market_price
        tp_price = round(entry_price * (1 - globals.tp_percent / 100), 2)
        sl_price = round(entry_price * (1 + globals.sl_percent / 100), 2)

        # TP ve SL emirleri
        exchange.create_order(
            symbol=symbol,
            type='TAKE_PROFIT_MARKET',
            side='buy',
            amount=coin_amount,
            params={
                'triggerPrice': tp_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        exchange.create_order(
            symbol=symbol,
            type='STOP_MARKET',
            side='buy',
            amount=coin_amount,
            params={
                'triggerPrice': sl_price,
                'reduceOnly': True,
                'workingType': 'MARK_PRICE'
            }
        )

        # Local küme içinde pozisyonu ekliyoruz
        open_positions.add(symbol)

        # Başarılı işlem mesajı
        show_message(
            root,
            "SHORT İşlem Açıldı",
            f"{symbol} için SHORT açıldı.\n\n"
            f"Giriş Fiyatı: {entry_price}\n"
            f"TP Fiyatı: {tp_price}\n"
            f"SL Fiyatı: {sl_price}\n\n"
            f"İzole Mod: ✅",
            icon="check"
        )

    except ccxt.BaseError as e:
        show_message(root, "API Hatası", f"Binance API hatası:\n{e}", icon="cancel")
    except Exception as e:
        show_message(root, "Beklenmeyen Hata", f"Hata:\n{e}", icon="cancel")
