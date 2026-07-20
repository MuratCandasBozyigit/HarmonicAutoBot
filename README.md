# Auto Trade-X (HarmonicAutoBot)

A desktop trading assistant for **Binance USD-M Futures**. It charts market candles, detects classic **harmonic XABCD patterns**, and can open **long/short** positions manually or automatically with isolated margin, leverage, take-profit, and stop-loss.

> **This is experimental software for educational and personal use.**  
> Trading cryptocurrencies involves substantial risk of loss. Read the [Disclaimer](#disclaimer--important-legal-notice) before using this project.

---

## Table of Contents

- [What This Project Does](#what-this-project-does)
- [Features](#features)
- [Supported Patterns](#supported-patterns)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Trading Modes](#trading-modes)
- [Risk Controls Built Into the App](#risk-controls-built-into-the-app)
- [Disclaimer & Important Legal Notice](#disclaimer--important-legal-notice)
- [Security Notes](#security-notes)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

## What This Project Does

**Auto Trade-X** is a Python GUI application that connects to your Binance Futures account (testnet or live) and helps you:

1. **Watch** selected USDT-margined futures pairs on candlestick charts  
2. **Detect** harmonic patterns (Gartley, Bat, Butterfly, Crab, Shark, Cypher)  
3. **Trade** either by clicking quick long/short buttons, or by enabling auto-order switches that place market orders when a pattern’s D-point completes near the latest candles  

Position sizing is based on your configured USDT margin amount and leverage. Take-profit and stop-loss percentages are applied after entry.

---

## Features

- Interactive candlestick charts (zoom / pan)
- Auto-refresh chart updates
- Coin watchlist (`coins.json`) — add, switch, remove symbols
- Multiple timeframes: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- Candle history limits: `20`, `50`, `100`, `250`
- Harmonic pattern overlay (bullish = green, bearish = red)
- Auto long / auto short toggles based on completed patterns
- Manual quick long / short with TP + SL
- Settings panel for API keys, leverage, size, TP%, SL%, and theme
- Isolated margin mode before placing orders
- Binance Futures **testnet** or **live** mode via `.env`

---

## Supported Patterns

The detector validates Fibonacci-based XABCD structures, including:

| Pattern   | Typical use in this app      |
|-----------|------------------------------|
| Gartley   | Bullish / bearish setups     |
| Bat       | Bullish / bearish setups     |
| Butterfly | Bullish / bearish setups     |
| Crab      | Bullish / bearish setups     |
| Shark     | Bullish / bearish setups     |
| Cypher    | Bullish / bearish setups     |

Bullish schemas may trigger **long** orders when auto-long is enabled.  
Bearish schemas may trigger **short** orders when auto-short is enabled.

Pattern detection is heuristic. False positives and missed patterns are expected. Do not treat detections as trading advice.

---

## Tech Stack

| Component        | Technology                                      |
|------------------|--------------------------------------------------|
| Language         | Python 3                                         |
| GUI              | CustomTkinter                                    |
| Exchange API     | CCXT (`binance` futures)                         |
| Charts           | mplfinance + matplotlib                          |
| Data             | pandas                                           |
| Config           | python-dotenv (`.env`)                           |
| Direct REST      | requests (isolated margin endpoint)              |

---

## Project Structure

```text
HarmonicAutoBot/
├── main.py                     # Application entry point
├── coins.json                  # Watchlist symbols
├── .env                        # Your local secrets & trading params (do not commit real keys)
├── .env.example                # Template for configuration
├── requirements.txt            # Python dependencies
├── README.md
├── RELEASE_NOTES.md
├── logo/                       # App icons
├── Chart/                      # Chart rendering & refresh
├── DrawPattern/                # Pattern drawing & auto-order triggers
├── Gui/                        # Main window & loading screen
├── Indicators/                 # Harmonic / Fibonacci validation
├── Order/                      # Manual & automatic order execution
└── Utils/                      # Globals, OHLCV fetch, settings, margin helpers
```

---

## Requirements

- Python **3.10+** recommended (developed around Python 3.x)
- A desktop environment with Tk support
- A Binance Futures account (preferably **testnet** first)
- API key permissions suitable for futures trading (enable only what you need)

On Linux you may also need system packages for Tk, for example:

```bash
sudo apt-get install python3-tk
```

---

## Installation

```bash
git clone https://github.com/muratcandasbozyigit/harmonicautobot.git
cd harmonicautobot

python -m venv .venv
# Windows:
# .venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your own API keys and risk settings before launching.

---

## Configuration

Create a `.env` file from `.env.example`:

```env
# Testnet keys (recommended while learning)
TEST_API_KEY=
TEST_API_SECRET=

# Live keys (use only if you accept full financial risk)
REAL_API_KEY=
REAL_API_SECRET=

# Trading parameters
USE_TESTNET=True
LEVERAGE=5
USDT_AMOUNT=15
TP_PERCENT=0.7
SL_PERCENT=1.5
```

### Environment variables

| Variable          | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `USE_TESTNET`     | `True` = Binance Futures testnet; `False` = live trading                    |
| `TEST_API_KEY`    | Testnet API key                                                             |
| `TEST_API_SECRET` | Testnet API secret                                                          |
| `REAL_API_KEY`    | Live API key                                                                |
| `REAL_API_SECRET` | Live API secret                                                             |
| `LEVERAGE`        | Futures leverage                                                            |
| `USDT_AMOUNT`     | Margin amount in USDT used for size calculation                             |
| `TP_PERCENT`      | Take-profit distance from entry (%)                                         |
| `SL_PERCENT`      | Stop-loss distance from entry (%)                                           |

Approximate position size:

```text
size ≈ (USDT_AMOUNT × LEVERAGE) / market_price
```

You can also change many of these values from the in-app settings window. Settings are written back to `.env`.

### Watchlist

Edit `coins.json` as a JSON array of base symbols (USDT pair is implied), for example:

```json
["BTC", "ETH", "SOL"]
```

---

## How to Run

```bash
python main.py
```

A short loading screen appears, then the main **Auto Trade-X** window opens.

---

## How to Use

1. Start with **`USE_TESTNET=True`** and testnet API keys.
2. Enter a coin (for example `BTC`) or click a symbol in the watchlist.
3. Choose timeframe and candle count.
4. Review harmonic patterns drawn on the chart.
5. Optional — enable **Long Emir** / **Short Emir** to allow automatic orders when a pattern completes.
6. Optional — use the quick trade buttons for manual market long/short with TP/SL.
7. Open settings (gear) to adjust API keys, leverage, size, TP%, SL%, and theme.

Auto-refresh updates the chart while enabled. Keep the app running if you want pattern monitoring and auto-orders to continue.

---

## Trading Modes

| Mode            | Behavior                                                                 |
|-----------------|--------------------------------------------------------------------------|
| Chart only      | Auto-order switches off — view patterns without placing trades           |
| Semi-automatic  | Enable long and/or short switches — bot may open positions on patterns   |
| Manual          | Use quick long/short buttons                                             |
| Testnet         | `USE_TESTNET=True` — practice without live funds                         |
| Live            | `USE_TESTNET=False` — real money; full personal risk                     |

---

## Risk Controls Built Into the App

These are **basic tooling helpers only**. They do **not** make trading safe or suitable for anyone.

- Isolated margin mode is set before orders
- Take-profit and stop-loss can be attached after entry
- Auto long / auto short require explicit UI toggles
- Duplicate pattern hashes are tracked in memory for the current session
- CCXT rate limiting is enabled

There is **no** guarantee that TP/SL will fill, that connectivity will remain stable, or that losses will be limited to a specific amount.

---

## Disclaimer & Important Legal Notice

**READ THIS CAREFULLY BEFORE DOWNLOADING, INSTALLING, CONFIGURING, OR RUNNING THIS SOFTWARE.**

### No advice, no agency, no responsibility

- This software is provided **as is**, for **educational**, **research**, and **personal experimentation** purposes only.
- It is **not** financial advice, investment advice, trading advice, a signal service, or a managed trading product.
- The author / developer / publisher of this project **does not trade on your behalf**, **does not manage your funds**, **does not act as your broker, advisor, agent, or fiduciary**, and **does not make any decisions for you**.
- **Every action performed by this application — including charting, pattern detection, order placement, leverage changes, margin mode changes, take-profit, stop-loss, and any automated behavior — is initiated under your control, with your API keys, on your exchange account, and entirely at your own risk.**
- By using this software you confirm that **you alone** are responsible for configuration, enablement of auto-trading features, order size, leverage, API permissions, network connectivity, and all resulting profits or losses.

### No warranty

- There is **no warranty** of any kind: express, implied, merchantability, fitness for a particular purpose, accuracy, reliability, uptime, profitability, or non-infringement.
- Pattern detection can be wrong. Markets can gap. APIs can fail. Orders can reject, partially fill, or behave unexpectedly. Software can contain bugs.
- The author is **not liable** for any direct, indirect, incidental, special, consequential, or exemplary damages — including but not limited to loss of capital, loss of profits, loss of data, account restrictions, exchange fees, liquidations, or emotional distress — arising from use or inability to use this software.

### User assumes all risk

- Cryptocurrency and futures trading are highly volatile and can result in **total loss of funds**, including losses greater than your initial margin when leverage is used.
- You should only use funds you can afford to lose.
- You are solely responsible for complying with the laws and regulations of your jurisdiction, exchange terms of service, tax obligations, and KYC/AML requirements.
- Enabling auto long/short means the bot may place market orders without asking again for each trade. If you do not fully understand that risk, **do not enable those switches** and **do not use live API keys**.

### No binding relationship

- Using, forking, starring, downloading, or modifying this repository **does not create any contract, partnership, employment, agency, or obligation** between you and the author.
- Nothing in this project binds the author to support, maintain, refund, compensate, advise, or intervene in any trading outcome.
- Support, if any, is voluntary and may be discontinued at any time without notice.

### Acceptance

If you do not agree with this disclaimer, **do not use the software**.  
If you use it anyway, you accept that **all risks and consequences are yours alone**.

---

## Security Notes

- Never share your API keys or commit a filled `.env` file to git.
- Prefer API keys with **futures trading only** and **no withdrawal** permission.
- Start on **testnet**.
- Use lower leverage and small `USDT_AMOUNT` until you understand the behavior.
- Keep your machine secure; anyone with access to the running app or `.env` can trade with your keys.

---

## Limitations

- Binance Futures focused (current main branch)
- Session-only duplicate-trade protection (resets when the app restarts)
- No portfolio-level risk limits, daily loss caps, or kill-switch beyond turning off toggles / closing the app
- Requires a graphical desktop session
- UI text is primarily Turkish in the current build

---

## Contributing

Issues and pull requests are welcome for bug fixes, documentation, and careful improvements.  
Do not open requests that ask for guaranteed profit strategies or “set and forget” live money systems.

---

## License

No formal license file is currently included in this repository.  
Unless the author publishes a license later, assume **all rights reserved** by the author, and that you use the code at your own risk under the disclaimer above.

---

## Author

**Murat Candaş Bozyiğit**  
GitHub: [MuratCandasBozyigit](https://github.com/MuratCandasBozyigit)

Questions about markets, personal portfolio management, or guaranteed returns will not be answered as advice. This project is a tool — **you** operate it.
