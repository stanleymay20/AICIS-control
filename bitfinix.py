import ccxt

exchange = ccxt.bitfinex({
    'apiKey': 'dde99252899b20b3129a8d2e3b630fa95084bd7a4f9',
    'secret': '6dc1319a3ac46d91432ebd426645cb416afc99cb857'
})

balance = exchange.fetch_balance()
print(balance)
