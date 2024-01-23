# allows the use of price data across modules

import json

def load(string):
    with open(f"data/{string}.json") as f:
        prices = json.load(f)
    return prices

current = 0 # placeholder
