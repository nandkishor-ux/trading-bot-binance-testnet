# 🤖 Trading Bot – Binance Futures Testnet (USDT-M)

A clean, production-style Python CLI application that places **Market** and **Limit** orders on Binance Futures Testnet using direct REST API calls.

---

## 📁 Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance Futures REST client wrapper
    orders.py          # Order placement logic & result model
    validators.py      # Input validation
    logging_config.py  # Structured file + console logging
  cli.py               # CLI entry point (argparse)
  .env.example         # API key template (never commit real keys)
  requirements.txt
  README.md
```

---

## ⚙️ Setup Steps

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your **Binance Futures Testnet** credentials:
```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> 🔗 Get testnet credentials at: https://testnet.binancefuture.com

---

## 🚀 How to Run

### Test connection
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --ping
```

### Place a MARKET order (BUY)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order (SELL)
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2500
```

### CLI Arguments

| Argument       | Short | Required            | Description                     |
|----------------|-------|---------------------|---------------------------------|
| `--symbol`     | `-s`  | ✅ Yes              | Trading pair e.g. `BTCUSDT`     |
| `--side`       |       | ✅ Yes              | `BUY` or `SELL`                 |
| `--type`       | `-t`  | ✅ Yes              | `MARKET` or `LIMIT`             |
| `--quantity`   | `-q`  | ✅ Yes              | Order quantity e.g. `0.01`      |
| `--price`      | `-p`  | ✅ Required for LIMIT | Limit price e.g. `2500`       |
| `--ping`       |       | ❌ Optional         | Test connectivity only           |

---

## 📋 Sample Output

```
============================================================
📋 ORDER REQUEST SUMMARY
============================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
============================================================
✅ ORDER PLACED SUCCESSFULLY
============================================================
  Order ID   : 8677268077
  Status     : FILLED
  Executed   : 0.01
  Avg Price  : 103245.60
============================================================
```

---

## 📝 Logging

Logs are written to the `logs/` directory automatically:
```
logs/trading_bot_YYYYMMDD_HHMMSS.log
```

Each log file captures:
- Outgoing API request parameters
- Full API response (order ID, status, fills)
- Validation errors and exception tracebacks

---

## 🔧 Assumptions

- **Testnet only** — uses `https://testnet.binancefuture.com` as the base URL
- **Direct REST API** — uses `requests` library (no `python-binance` SDK)
- **`recvWindow` = 10000ms** — allows tolerance for server/client time drift
- **USDT-M perpetual futures** — all orders placed on USDT-margined contracts
- Minimum order quantities follow Binance Testnet rules (e.g. BTC ≥ 0.001)

---

## 📦 Dependencies

See `requirements.txt`. Key packages:
- `requests` – HTTP REST calls
- `python-dotenv` – `.env` file loading
