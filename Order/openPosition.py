import ccxt
from Utils import globals
import Utils
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as msgbox
import Utils.binance_isolated as iso


def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)
def open_position(entry_price, symbol_input=None):
    root = ctk.CTk()
    root.withdraw()

    try:
        if not globals.emir_acik:
            return

        raw_symbol = symbol_input or globals.symbol_var.get().strip().upper()
        symbol = raw_symbol if "/" in raw_symbol else raw_symbol + "/USDT"
        binance_symbol = symbol.replace("/", "")
        timeframe = globals.timeframe_var.get()

        # Binance bağlantısı
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True
            }
        })
        exchange.set_sandbox_mode(globals.use_testnet)

        # Gelişmiş pozisyon kontrolü
        try:
            # Önce sembolün futures'da listelendiğini kontrol et
            markets = exchange.load_markets()
            if binance_symbol not in markets:
                msgbox.showerror("Hata", f"{binance_symbol} futures piyasasında bulunamadı")
                return

            # Pozisyon bilgisi al
            positions = exchange.fetch_positions_risk([binance_symbol])
            
            # Pozisyon bilgisi yoksa yeni bir pozisyon oluşturulabilir
            if not positions:
                print(f"Uyarı: {binance_symbol} için aktif pozisyon bulunamadı, yeni pozisyon açılabilir")
            else:
                position = positions[0]
                if position.get('marginType', '').lower() != 'isolated':
                    if not iso.set_isolated_mode(binance_symbol):
                        msgbox.showerror("Hata", "İzole moda geçilemedi")
                        return

        except ccxt.NetworkError as e:
            msgbox.showerror("Ağ Hatası", f"Sunucuya bağlanılamadı: {str(e)}")
            return
        except ccxt.ExchangeError as e:
            msgbox.showerror("Borsa Hatası", f"Binance API hatası: {str(e)}")
            return
        except Exception as e:
            msgbox.showerror("Kontrol Hatası", f"Pozisyon kontrolü başarısız: {str(e)}")
            return

        # Veri çekme işlemi
        try:
            df = Utils.get_ohlcv(symbol, timeframe)
            if df is None or df.empty:
                raise ValueError("Geçerli veri alınamadı")
        except Exception as e:
            msgbox.showerror("Veri Hatası", str(e))
            return

        # Pozisyon oluşturma
        try:
            usdt_amount = globals.usdt_amount
            leverage = globals.leverage
            
            # Kaldıraç ayarı
            try:
                exchange.set_leverage(leverage, symbol=symbol)
            except ccxt.BaseError as e:
                msgbox.showwarning("Uyarı", f"Kaldıraç ayarlanamadı: {str(e)}")

            market_price = df['close'].iloc[-1]
            coin_amount = round((usdt_amount * leverage) / market_price, 3)

            # Ana emir
            order = exchange.create_market_order(
                symbol=symbol,
                side='buy',
                amount=coin_amount,
                params={'positionSide': 'LONG'}
            )
            
            entry_price = float(order['average']) if 'average' in order else market_price
            tp_price = round(entry_price * (1 + globals.tp_percent / 100), 2)
            sl_price = round(entry_price * (1 - globals.sl_percent / 100), 2)

            # TP/SL emirleri
            exchange.create_order(
                symbol=symbol,
                type='TAKE_PROFIT_MARKET',
                side='sell',
                amount=coin_amount,
                params={
                    'stopPrice': tp_price,
                    'reduceOnly': True,
                    'workingType': 'MARK_PRICE'
                }
            )

            exchange.create_order(
                symbol=symbol,
                type='STOP_MARKET',
                side='sell',
                amount=coin_amount,
                params={
                    'stopPrice': sl_price,
                    'reduceOnly': True,
                    'workingType': 'MARK_PRICE'
                }
            )

            msgbox.showinfo("Başarılı", f"""
            {symbol} long pozisyonu açıldı
            Giriş: {entry_price}
            TP: {tp_price}
            SL: {sl_price}
            """)

        except ccxt.InsufficientFunds:
            msgbox.showerror("Hata", "Yetersiz bakiye")
        except ccxt.InvalidOrder as e:
            msgbox.showerror("Hata", f"Geçersiz emir: {str(e)}")
        except ccxt.NetworkError as e:
            msgbox.showerror("Hata", f"Ağ hatası: {str(e)}")

    except Exception as e:
        msgbox.showerror("Kritik Hata", f"Beklenmeyen hata: {str(e)}")
    finally:
        try:
            root.destroy()
        except:
            pass