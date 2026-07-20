# Release Notes — Auto Trade-X (HarmonicAutoBot)

## Overview

**Auto Trade-X** is a desktop application for Binance USD-M Futures that charts markets, detects harmonic XABCD patterns, and can place long/short futures orders manually or automatically.

This release documents the current mainline capabilities of the project: charting, pattern overlay, settings management, isolated-margin order helpers, and optional auto-trading switches.

---

## Purpose

Help users visually inspect harmonic structures on Binance Futures charts and optionally execute trades from the same desktop client — either with one-click manual orders or by enabling pattern-triggered auto orders.

This software is a **personal tooling / experimental utility**. It is **not** a managed fund, signal service, investment product, or financial advisory relationship.

---

## What’s Included

### Charting & analysis
- Candlestick charts for selected USDT futures symbols
- Timeframes: 1m, 5m, 15m, 1h, 4h, 1d
- Candle count options and auto-refresh
- Watchlist via `coins.json`
- Harmonic pattern drawing for Gartley, Bat, Butterfly, Crab, Shark, and Cypher

### Trading
- Manual quick long / short market orders
- Optional auto long / auto short when a validated pattern completes near the latest candles
- Configurable leverage, USDT margin amount, take-profit %, and stop-loss %
- Isolated margin mode request before orders
- Testnet or live mode controlled by `USE_TESTNET`

### Configuration
- `.env`-based API keys and trading parameters
- In-app settings window that can persist values back to `.env`

---

## How to Use (Quick Start)

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in **testnet** keys first
3. Set `USE_TESTNET=True`
4. Run: `python main.py`
5. Select a symbol, timeframe, and review patterns
6. Keep auto-order switches **off** until you understand the flow
7. Only switch to live keys if you fully accept personal financial risk

Full setup details are in `README.md`.

---

## Important: Risk, Responsibility & Non-Agency Statement

**Please read before installing or running any release build.**

- The author of this project **does not place trades for you**, **does not operate your account**, and **does not act on your behalf in any capacity**.
- All API keys, leverage, order sizes, take-profit / stop-loss values, and auto-trade toggles are **configured and controlled by the user**.
- Any order sent to Binance through this application is an action of **the user’s own software instance**, running on **the user’s machine**, with **the user’s credentials**.
- **All financial risk belongs exclusively to the user.** Losses, liquidations, missed fills, API errors, incorrect pattern detections, bugs, downtime, and exchange-side issues are **not the author’s responsibility**.
- Nothing in this release creates a contract, agency relationship, partnership, or obligation that binds the author to compensate, advise, support, or intervene.
- By downloading, installing, or running this software — especially with live trading enabled — you acknowledge that **you alone accept every outcome**.

If you need a managed trading service or professional advice, **do not use this bot**.

---

## Recommended Safety Practice

- Start on Binance Futures **testnet**
- Use API keys **without withdrawal** permission
- Keep leverage and `USDT_AMOUNT` small
- Leave auto long/short disabled until you have verified behavior
- Never commit real API secrets to git or share them publicly

---

## Known Limitations

- Pattern detection is approximate and can be wrong
- Duplicate auto-trade protection is session-based (in memory)
- No advanced portfolio risk engine or guaranteed stop execution
- Current main focus is Binance Futures

---

## Support

This project may receive voluntary updates. Support is not guaranteed.  
Using the software means you accept the disclaimer in `README.md` and this release note in full.
