import ccxt

exchange = ccxt.binance({
    'apiKey': 'AB9ABNvPdaqb1Se7YNBkNU254LYZVCNEpvLHVfvkEsl2N9ySmiDxDfn7KfV0sPtn',
    'secret': 'GCWzeHX1UqFdIfct9pZUkdMIhHXyz1yL2Wo5oCOsWP0ZrmRJJzxMqHLRWghYizka',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

try:
    balance = exchange.fetch_balance()
    print("Bağlantı başarılı ✅ USDT:", balance['total'].get('USDT', 'Yok'))
except Exception as e:
    print("❌ Bağlantı hatası:", type(e).__name__, e)

