import json
import logging
import os
import time

import ccxt

logging.basicConfig(
    filename="aicis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("AICIS legacy trading bot started")

# SECURITY NOTE
# -------------
# Exchange credentials must be supplied through environment variables or a
# dedicated secret manager. Never commit API keys, secrets, passwords, or
# exchange credentials to this repository.
#
# Any credential that appeared in previous public Git history must be treated
# as exposed and rotated/revoked at the provider. Removing it from the current
# branch tip does not revoke it and does not erase historical copies.

EXCHANGE_ENV = {
    "binance": ("BINANCE_API_KEY", "BINANCE_API_SECRET", None),
    "bybit": ("BYBIT_API_KEY", "BYBIT_API_SECRET", None),
    "okx": ("OKX_API_KEY", "OKX_API_SECRET", "OKX_API_PASSWORD"),
    "huobi": ("HUOBI_API_KEY", "HUOBI_API_SECRET", None),
    "bitstamp": ("BITSTAMP_API_KEY", "BITSTAMP_API_SECRET", None),
    "gateio": ("GATEIO_API_KEY", "GATEIO_API_SECRET", None),
    "deribit": ("DERIBIT_API_KEY", "DERIBIT_API_SECRET", None),
    "bitfinex": ("BITFINEX_API_KEY", "BITFINEX_API_SECRET", None),
}


def load_exchange_credentials():
    credentials = {}
    for exchange_name, (key_var, secret_var, password_var) in EXCHANGE_ENV.items():
        api_key = os.getenv(key_var)
        api_secret = os.getenv(secret_var)
        password = os.getenv(password_var) if password_var else None

        # Fail closed for an exchange when required credentials are absent.
        if not api_key or not api_secret or (password_var and not password):
            logging.warning("Skipping %s: required credentials are not configured", exchange_name)
            continue

        entry = {"apiKey": api_key, "secret": api_secret}
        if password is not None:
            entry["password"] = password
        credentials[exchange_name] = entry

    return credentials


def initialize_exchanges():
    exchange_instances = {}
    for name, keys in load_exchange_credentials().items():
        try:
            exchange_class = getattr(ccxt, name)
            exchange_config = {
                "apiKey": keys["apiKey"],
                "secret": keys["secret"],
                "enableRateLimit": True,
            }
            if "password" in keys:
                exchange_config["password"] = keys["password"]

            exchange = exchange_class(exchange_config)
            exchange.load_markets()
            exchange_instances[name] = exchange
            logging.info("Connected to %s", name.upper())
        except Exception as exc:
            logging.error("Failed to connect to %s: %s", name.upper(), str(exc))
    return exchange_instances


def execute_trade(exchange, symbol, side, amount):
    logging.info("Attempting trade on %s: %s %s %s", exchange.id.upper(), side, amount, symbol)
    try:
        order = exchange.create_market_order(symbol, side, amount)
        logging.info("Trade executed on %s: %s", exchange.id.upper(), json.dumps(order, default=str))
    except Exception as exc:
        logging.error("Trade failed on %s for %s: %s", exchange.id.upper(), symbol, str(exc))


def check_balances(exchange):
    try:
        balance = exchange.fetch_balance()
        logging.info("Balance fetched for %s", exchange.id.upper())
        return balance
    except Exception as exc:
        logging.error("Failed to fetch balance for %s: %s", exchange.id.upper(), str(exc))
        return None


def find_arbitrage_opportunities(exchanges, pair):
    prices = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(pair)
            prices[name] = ticker["last"]
            logging.info("%s %s price: %s", name.upper(), pair, ticker["last"])
        except Exception as exc:
            logging.error("Could not fetch price for %s on %s: %s", pair, name.upper(), str(exc))

    if len(prices) > 1:
        max_price = max(prices.values())
        min_price = min(prices.values())
        spread = (max_price - min_price) / min_price * 100
        logging.info("Max price: %s, Min price: %s, Spread: %.2f%%", max_price, min_price, spread)

        if spread > 0.15:
            buy_exchange = min(prices, key=prices.get)
            sell_exchange = max(prices, key=prices.get)
            logging.info(
                "Arbitrage opportunity: buy on %s and sell on %s",
                buy_exchange.upper(),
                sell_exchange.upper(),
            )
            return buy_exchange, sell_exchange
    return None, None


def aicis_trading():
    exchanges = initialize_exchanges()
    if len(exchanges) < 2:
        raise RuntimeError(
            "At least two fully configured exchanges are required. "
            "Provide credentials through environment variables or a secret manager."
        )

    trading_pairs = ["BTC/USDT", "ETH/USDT"]
    trade_amount = 0.01

    while True:
        for pair in trading_pairs:
            buy_exchange, sell_exchange = find_arbitrage_opportunities(exchanges, pair)
            if buy_exchange and sell_exchange:
                execute_trade(exchanges[buy_exchange], pair, "buy", trade_amount)
                execute_trade(exchanges[sell_exchange], pair, "sell", trade_amount)
        logging.info("Waiting 60 seconds before next scan")
        time.sleep(60)


if __name__ == "__main__":
    aicis_trading()
