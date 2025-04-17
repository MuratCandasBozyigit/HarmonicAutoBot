import mplfinance as mpf

def ema(df):
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA200"] = df["close"].ewm(span=200, adjust=False).mean()

    apds = [
        mpf.make_addplot(df["EMA50"], color='blue', width=1.2),
        mpf.make_addplot(df["EMA200"], color='red', width=1.2)
    ]
    return apds
