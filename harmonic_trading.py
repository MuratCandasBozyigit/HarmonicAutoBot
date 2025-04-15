import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from binance.client import Client

# Binance API anahtarlarını buraya giriyoruz
api_key = 'PKgSzPrw3pWDqu7tH9qFAlrlEJxHqT6JcmXKN01RiQfWTF0NRhZbiGgkXQVwiNEL'
api_secret = 'Kpmrf8DescaLEDtN4OnuUv2XL7PHjfpZv9PHRPoh2pTJgh96Qdu93o1GDRXmjLFT'

client = Client(api_key, api_secret)
# Veri çekme fonksiyonu
def get_live_data():
    klines = client.get_historical_klines("EURUSDT", Client.KLINE_INTERVAL_15MINUTE, "1500 minutes ago UTC")
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df

# Fiyat değişimini hızlıca kontrol etme fonksiyonu
def check_price_change(last_close, current_close):
    price_diff = current_close - last_close
    if price_diff > 0:
        print(f"Fiyat {price_diff} arttı!")
    elif price_diff <= -1:
        print(f"Fiyat {abs(price_diff)} düştü!")

# İlk veriyi al
initial_df = get_live_data()
last_close = initial_df['Close'].iloc[-1]

# İlk çizimi yap
fig, axlist = mpf.plot(
    initial_df,
    type='candle',
    style='charles',
    volume=True,
    returnfig=True
)

# Her yenilemede çağrılacak fonksiyon
def animate(i):
    global last_close
    df = get_live_data()
    current_close = df['Close'].iloc[-1]
    check_price_change(last_close, current_close)  # Fiyat değişimini kontrol et
    last_close = current_close  # Son fiyatı güncelle
    
    axlist[0].clear()
    axlist[2].clear()  # Volume axis
    mpf.plot(
        df,
        type='candle',
        style='charles',
        ax=axlist[0],
        volume=axlist[2],
        datetime_format='%H:%M',
        xrotation=20
    )

# 10 saniyede bir grafik yenilenir
ani = FuncAnimation(fig, animate, interval=100)  # 10 saniyede bir yenile

# Grafiği göster
plt.show()