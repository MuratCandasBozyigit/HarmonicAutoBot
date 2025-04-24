import ccxt
from Utils import globals
import Utils
import customtkinter as ctk
from tkinter import messagebox
import Utils.binance_isolated as iso

def show_message(root, title, message, icon="info"):
    message_box = ctk.CTkToplevel(root)
    message_box.title(title)
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)
    
    button = ctk.CTkButton(message_box, text="Tamam", command=message_box.destroy)
    button.pack(pady=10)

def execute_short_trade():
    try:
        # Pencere yönetimi
        root = ctk.CTk()
        root.withdraw()

        # Sembol işleme
        raw_symbol = globals.symbol_var.get().strip().upper().replace("/", "").replace("USDT", "")  # Tüm '/' ve 'USDT'yi kaldır
        symbol = f"{raw_symbol}/USDT"  # UI gösterimi için
        binance_symbol = f"{raw_symbol}USDT"  # Binance formatı

        # Binance bağlantısı
        exchange = ccxt.binance({
            'apiKey': globals.api_key,
            'secret': globals.api_secret,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True
            }
        })
        exchange.set_sandbox_mode(globals.use_testnet)

        # 1. Sembol kontrolü
        markets = exchange.load_markets()
        if binance_symbol not in markets:
            available_symbols = [s.split(':')[0] for s in markets.keys() if 'USDT' in s and ':' not in s][:5]  # İlk 5 sembol
            messagebox.showerror("Hata", 
                f"{binance_symbol} futures piyasasında bulunamadı!\n"
                f"Örnek Semboller: {', '.join(available_symbols)}")
            return

        # 2. Margin tipi kontrolü
        try:
            positions = exchange.fetch_positions_risk([binance_symbol])
            if positions and positions[0].get('marginType', '').lower() != 'isolated':
                try:
                    iso.set_isolated_mode(binance_symbol)
                except Exception as iso_error:
                    if 'No need to change' not in str(iso_error):
                        raise iso_error
        except Exception as e:
            if 'No need to change' not in str(e):
                messagebox.showerror("Hata", f"Margin kontrol hatası:\n{str(e)}")
                return

        # 3. Veri çekme
        df = Utils.get_ohlcv(symbol, globals.timeframe_var.get())
        if df is None or df.empty:
            messagebox.showerror("Hata", "Veri alınamadı")
            return

        # 4. Pozisyon boyutu hesaplama
        market_price = df['close'].iloc[-1]
        amount = round((globals.usdt_amount * globals.leverage) / market_price, 3)

        # 5. Emir oluşturma
        order = exchange.create_market_order(
            symbol=symbol,
            side='sell',
            amount=amount,
            params={'positionSide': 'SHORT'}
        )
        
        # 6. TP/SL ayarları
        entry_price = float(order['average']) if 'average' in order else market_price
        tp_price = round(entry_price * (1 - globals.tp_percent/100), 2)
        sl_price = round(entry_price * (1 + globals.sl_percent/100), 2)
        
        # 7. TP/SL emirleri
        exchange.create_order(
            symbol=symbol,
            type='TAKE_PROFIT_MARKET',
            side='buy',
            amount=amount,
            params={'stopPrice': tp_price, 'reduceOnly': True}
        )
        
        exchange.create_order(
            symbol=symbol,
            type='STOP_MARKET',
            side='buy',
            amount=amount,
            params={'stopPrice': sl_price, 'reduceOnly': True}
        )
        
        messagebox.showinfo("Başarılı", 
            f"SHORT pozisyon açıldı ✅\n"
            f"Sembol: {symbol}\n"
            f"Miktar: {amount}\n"
            f"Giriş: {entry_price}\n"
            f"TP: {tp_price}\n"
            f"SL: {sl_price}")

    except ccxt.InsufficientFunds:
        messagebox.showerror("Hata", "Yetersiz bakiye! Lütfen bakiyenizi kontrol edin")
    except ccxt.InvalidOrder as e:
        messagebox.showerror("Emir Hatası", f"Geçersiz emir parametreleri: {str(e)}")
    except Exception as e:
        messagebox.showerror("Kritik Hata", f"Beklenmeyen hata: {str(e)}")
    finally:
        try:
            root.destroy()
        except:
            pass