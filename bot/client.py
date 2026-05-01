import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"
logger = setup_logger("binance_client")


class BinanceClientError(Exception):
    pass


class BinanceFuturesClient:

    def __init__(self, api_key: str, api_secret: str):
        self.api_key    = api_key
        self.api_secret = api_secret
        self.session    = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: Dict[str, Any]) -> str:
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _timestamp(self) -> int:
        try:
          server_time = self._request("GET", "/fapi/v1/time")
          return server_time["serverTime"]
        except:
             return int(time.time() * 1000)

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Dict:
        params = params or {}

        if signed:
            params["timestamp"] = self._timestamp()
            params["signature"] = self._sign(params)

        url = BASE_URL + endpoint
        logger.debug(f"-> {method} {url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method == "POST":
                response = self.session.post(url, data=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug(f"<- {response.status_code} | {response.text[:300]}")
            data = response.json()

        except requests.exceptions.ConnectionError:
            logger.error("Network error: unable to reach Binance Testnet.")
            raise BinanceClientError("Network error: check your internet connection.")
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise BinanceClientError("Request timed out. Try again.")
        except Exception as e:
            logger.error(f"Unexpected error during request: {e}")
            raise BinanceClientError(f"Unexpected error: {e}")

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            logger.error(f"Binance API error: {data}")
            raise BinanceClientError(f"Binance error {data['code']}: {data.get('msg', 'Unknown error')}")

        return data

    def get_server_time(self) -> Dict:
        return self._request("GET", "/fapi/v1/time")

    def place_order(self, symbol, side, order_type, quantity, price=None, time_in_force="GTC"):
        params: Dict[str, Any] = {
            "symbol":   symbol,
            "side":     side,
            "type":     order_type,
            "quantity": quantity,
             "recvWindow": 10000,
        }
        if order_type == "LIMIT":
            if price is None:
                raise BinanceClientError("Price must be provided for LIMIT orders.")
            params["price"]       = price
            params["timeInForce"] = time_in_force

        logger.info(f"Placing order: {params}")
        response = self._request("POST", "/fapi/v1/order", params=params, signed=True)
        logger.info(f"Order response: {response}")
        return response