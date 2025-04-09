import ccxt

okx = ccxt.okx({
    'apiKey': '21c32895-05b5-4664-aafd-887f61e09c1e"',
    'secret': '92E53B83AA212AECAC49836A36105927',
    'password': '$tanleyMay20'
})

balance = okx.fetch_balance()
print(balance['total'])
