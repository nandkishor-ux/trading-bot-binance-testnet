from typing import Optional

from bot.client import BinanceFuturesClient, BinanceClientError
from bot.validators import validate_all, ValidationError
from bot.logging_config import setup_logger

logger = setup_logger("orders")


class OrderResult:
    def __init__(self, success: bool, data: dict = None, error: str = ""):
        self.success = success
        self.data    = data or {}
        self.error   = error

    def print_summary(self):
        if self.success:
            d = self.data
            print("\n" + "=" * 50)
            print("✅  ORDER PLACED SUCCESSFULLY")
            print("=" * 50)
            print(f"  Order ID     : {d.get('orderId', 'N/A')}")
            print(f"  Symbol       : {d.get('symbol', 'N/A')}")
            print(f"  Side         : {d.get('side', 'N/A')}")
            print(f"  Type         : {d.get('type', 'N/A')}")
            print(f"  Status       : {d.get('status', 'N/A')}")
            print(f"  Orig Qty     : {d.get('origQty', 'N/A')}")
            print(f"  Executed Qty : {d.get('executedQty', 'N/A')}")
            avg_price = d.get('avgPrice') or d.get('price', 'N/A')
            print(f"  Avg Price    : {avg_price}")
            print("=" * 50 + "\n")
        else:
            print("\n" + "=" * 50)
            print("❌  ORDER FAILED")
            print("=" * 50)
            print(f"  Reason: {self.error}")
            print("=" * 50 + "\n")


def place_order(client: BinanceFuturesClient, symbol, side, order_type, quantity, price=None) -> OrderResult:
    try:
        params = validate_all(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return OrderResult(success=False, error=str(e))

    logger.info(
        f"Order request | symbol={params['symbol']} side={params['side']} "
        f"type={params['order_type']} qty={params['quantity']} price={params['price']}"
    )

    print("\n📋 Order Request Summary")
    print(f"   Symbol    : {params['symbol']}")
    print(f"   Side      : {params['side']}")
    print(f"   Type      : {params['order_type']}")
    print(f"   Quantity  : {params['quantity']}")
    if params['price']:
        print(f"   Price     : {params['price']}")

    try:
        response = client.place_order(
            symbol     = params["symbol"],
            side       = params["side"],
            order_type = params["order_type"],
            quantity   = params["quantity"],
            price      = params["price"],
        )
        return OrderResult(success=True, data=response)

    except BinanceClientError as e:
        logger.error(f"API error: {e}")
        return OrderResult(success=False, error=str(e))

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return OrderResult(success=False, error=f"Unexpected error: {e}")