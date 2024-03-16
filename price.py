# allows the use of price data across modules

import json

def load(string):
    with open(f"data/{string}.json") as f:
        raw = json.load(f)
    prices = dict()
    no_price = 0
    for c in raw:
        try:
            prices[c["name"]] = float(c["usd"])
        except TypeError:
            prices[c["name"]] = False
            no_price += 1
    if no_price != 0:
        print(f"Warning: {no_price} cards lack price information.")
    return prices

def print_priceless():
    for (name, price) in current.items():
        if price == False:
            print(name)

current = dict()
