import ccxt
import requests
import json
import logging
import time

# Configure logging
import logging

# Setup Logging
logging.basicConfig(
    filename="aicis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 AICIS Trading Bot Started...")

# Exchange API credentials (from your uploaded keys)
EXCHANGES = {
    "binance": {"apiKey": "Aho8iwgfidmfQYSiFnmBTCsla1xNCnPeggSV1XCtYQxCwEILMUCzg0AgdK02FOSz", 
                "secret": "tLZ5reZ45n70g0BTPkr057YxPwB9j6z8qOzZ8FKdwds0ufsyvph8PfQopfTS8x38"},
    "bybit": {"apiKey": "QDFtrEA6H0SGIEZYuy", "secret": "HQRTnWwicRu7NcyMa3oG0HBJN7Afbz7ItHqi"},
    "okx": {"apiKey": "9bebf275-6a03-4e05-b7c1-7ff121fed06c", "secret": "54777BCABEE0E1E86823AC2BA0BA08F0","password": "$tanleyMay20"},
    "huobi": {"apiKey": "bg5t6ygr6y-dc85a4c8-96a6d7c2-965d8", "secret": "b288dae5-a9f8e895-6d3a3f5f-fd0f5"},
    "bitstamp": {"apiKey": "tIP9I7QTaGHdZtQ8gGSxbMOSrz9A6sM5", "secret": "wcApN09sWcmrrR4BwHe4CR2ngXBnJZcy"},
    "gateio": {"apiKey": "1c133d245917839aa0a406c8420fcae5", "secret": "d2d9dd58434037e11206dc8a49f66de9aa83a3022b78689b5a79e0858da41601"},
    "deribit": {"apiKey": "mD99qSRk", "secret": "hqmAmMghYWRiErmAS_1L6012lBtP8Efli_Ls_HDH1uA"},
    "bitfinex": {"apiKey": "dde99252899b20b3129a8d2e3b630fa95084bd7a4f9", "secret": "6dc1319a3ac46d91432ebd426645cb416afc99cb857"},
}

# Function to initialize exchanges
def initialize_exchanges():
    exchange_instances = {}
    for name, keys in EXCHANGES.items():
        try:
            exchange_class = getattr(ccxt, name)
            exchange = exchange_class({
                "apiKey": keys["apiKey"],
                "secret": keys["secret"],
                "enableRateLimit": True,
            })
            exchange.load_markets()
            exchange_instances[name] = exchange
            logging.info(f"✅ Connected to {name.upper()}")
        except Exception as e:
            logging.error(f"❌ Failed to connect to {name.upper()}: {str(e)}")
    return exchange_instances

# Function to execute trades
def execute_trade(exchange, symbol, side, amount):
    logging.info(f"⚡ Attempting trade on {exchange.id.upper()}: {side} {amount} {symbol}")

    try:
        order = exchange.create_market_order(symbol, side, amount)
        logging.info(f"✅ Trade executed on {exchange.id.upper()}: {order}")
    except Exception as e:
        logging.error(f"❌ Trade failed on {exchange.id.upper()} for {symbol}: {str(e)}")



# Function to check balances
def check_balances(exchange):
    try:
        balance = exchange.fetch_balance()
        logging.info(f"💰 {exchange.id.upper()} Balance: {json.dumps(balance, indent=4)}")
    except Exception as e:
        logging.error(f"⚠️ Failed to fetch balance for {exchange.id.upper()}: {str(e)}")

# Function to find arbitrage opportunities
def find_arbitrage_opportunities(exchanges, pair):
    prices = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(pair)
            prices[name] = ticker["last"]
            logging.info(f"{name.upper()} {pair} price: {ticker['last']}")
        except Exception as e:
            logging.error(f"Could not fetch price for {pair} on {name.upper()}: {str(e)}")

    if len(prices) > 1:
        max_price = max(prices.values())
        min_price = min(prices.values())
        spread = (max_price - min_price) / min_price * 100

        logging.info(f"💹 Max price: {max_price}, Min price: {min_price}, Spread: {spread:.2f}%")

        if spread > 0.15:  # Arbitrage threshold (1.5% profit)
            buy_exchange = min(prices, key=prices.get)
            sell_exchange = max(prices, key=prices.get)
            logging.info(f"🔄 Arbitrage Opportunity: Buy on {buy_exchange.upper()} and Sell on {sell_exchange.upper()}")
            return buy_exchange, sell_exchange
    return None, None

# AICIS Trading Engine
def aicis_trading():
    logging.info("🚀 AICIS Trading Bot Starting...")
    exchanges = initialize_exchanges()

    trading_pairs = ["BTC/USDT", "ETH/USDT"]
    trade_amount = 0.01  # Amount of crypto to trade

    while True:
        for pair in trading_pairs:
            buy_exchange, sell_exchange = find_arbitrage_opportunities(exchanges, pair)

            if buy_exchange and sell_exchange:
                execute_trade(exchanges[buy_exchange], pair, "buy", trade_amount)
                execute_trade(exchanges[sell_exchange], pair, "sell", trade_amount)

        logging.info("⏳ Waiting 60 seconds before next scan...")
        time.sleep(60)

# Start trading
if __name__ == "__main__":
    aicis_trading()
