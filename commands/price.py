"""
    `price card_name`

Prints the price of `card_name`, which should be enclosed within double quotes
if it contains a space. Matches names exactly.
"""

import hobo_core

try:
    name = args[0]
except IndexError:
    pass
else:
    p = price_list.get(name)
    match p:
        case -2:
            hobo_core.show_warning(f"No recognized card named {name}.")
        case -1:
            hobo_core.show_warning(f"No price recorded for {name}.")
        case _:
            print(f"$ {p:.2f}")
