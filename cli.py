import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceClientError
from bot.orders import place_order
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger("cli")


def get_credentials():
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print("❌ Error: .env file mein API keys daalo!")
        logger.error("Missing API credentials.")
        sys.exit(1)
    return api_key, api_secret


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot"
    )
    parser.add_argument("--symbol", "-s", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", "-t", dest="order_type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", "-q", required=True)
    parser.add_argument("--price", "-p", default=None)
    parser.add_argument("--ping", action="store_true", help="Connection test")
    return parser


def main():
    parser = build_parser()
    args   = parser.parse_args()

    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)

    if args.ping:
        try:
            server_time = client.get_server_time()
            print(f"✅ Connected to Binance Testnet! Server time: {server_time}")
        except BinanceClientError as e:
            print(f"❌ Connection failed: {e}")
            sys.exit(1)
        sys.exit(0)

    result = place_order(
        client     = client,
        symbol     = args.symbol,
        side       = args.side,
        order_type = args.order_type,
        quantity   = args.quantity,
        price      = args.price,
    )
    result.print_summary()
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()