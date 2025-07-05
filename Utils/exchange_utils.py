import ccxt
from .config import BORSALAR, DEFAULT_EXCHANGE


def exchange_olustur(borsa_adi=DEFAULT_EXCHANGE):
    try:
        # Borsa bilgilerini al
        config = BORSALAR.get(borsa_adi.lower())
        if not config:
            raise ValueError(f"{borsa_adi} desteklenmiyor")

        # Borsa objesi oluştur
        exchange_class = getattr(ccxt, borsa_adi)
        exchange = exchange_class(config)
        exchange.load_markets()

        print(f"{borsa_adi} başarıyla bağlandı!")
        return exchange

    except Exception as e:
        print(f"Hata: {borsa_adi} bağlantısı başarısız: {str(e)}")
        return None


def sembol_duzelt(sembol, borsa_adi):
    """ Borsalara göre sembol formatını standartlaştır """
    if borsa_adi in ['binance', 'bybit', 'huobi']:
        return f"{sembol.split('/')[0]}/{sembol.split('/')[1]}"
    elif borsa_adi in ['kucoin', 'okx', 'gateio']:
        return f"{sembol.split('/')[0]}-{sembol.split('/')[1]}"
    else:
        return sembol