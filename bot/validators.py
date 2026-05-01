from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    if not symbol.isalnum():
        raise ValidationError(f"Invalid symbol '{symbol}'. Use alphanumeric only (e.g., BTCUSDT).")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a number.")
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {qty}")
    return qty


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None or str(price).strip() == "":
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid price '{price}'. Must be a number.")
        if p <= 0:
            raise ValidationError(f"Price must be greater than 0. Got: {p}")
        return p
    return None


def validate_all(symbol: str, side: str, order_type: str, quantity: str, price: Optional[str] = None):
    validated_symbol   = validate_symbol(symbol)
    validated_side     = validate_side(side)
    validated_type     = validate_order_type(order_type)
    validated_qty      = validate_quantity(quantity)
    validated_price    = validate_price(price, validated_type)

    return {
        "symbol":     validated_symbol,
        "side":       validated_side,
        "order_type": validated_type,
        "quantity":   validated_qty,
        "price":      validated_price,
    }