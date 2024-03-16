# contains all commands available to the user alongside some helper functions

import sys
import price
import deck

def parse(string):
    tokens = []
    current = ""
    parsing_string = False
    for i in range(len(string)):
        if string[i] == '"':
            if parsing_string:
                tokens.append(current)
                current = ""
            parsing_string = not parsing_string
            continue # don't record double quotes
        if string[i] == " " and not parsing_string:
            tokens.append(current)
            current = ""
            continue
        current += string[i]
        if i == len(string) - 1:
            tokens.append(current)
    return tokens

# TODO: move input validation into dedicated funtions
def execute(tokens):
    match tokens[0]:
        case "quit":
            sys.exit(0)
        case "price":
            if tokens[1] in price.current.keys():
                if price.current[tokens[1]] is not False:
                    print(f"${price.current[tokens[1]]:.2f}")
                else:
                    print(f"{tokens[1]} does not have a recorded price.")
            else:
                print(f"No card named \"{tokens[1]}\" found. "
                      "You may have mistyped its name, "
                      "or legal copies of the card may be so scarce "
                      "that Scryfall does not list a regular price.")
        case "list":
            deck.list()
        case "add":
            if tokens[2] in price.current.keys():
                deck.add(deck.main, tokens[1], tokens[2])
        case "remove":
            if tokens[2] in price.current.keys():
                deck.remove(deck.main, tokens[1], tokens[2])
        case "side":
            if tokens[2] in price.current.keys():
                deck.add(deck.side, tokens[1], tokens[2])
        case "move":
            if tokens[2] in price.current.keys():
                try:
                    if tokens[3] in ("main", "side"):
                        deck.move(tokens[1], tokens[2], direction=tokens[3])
                except IndexError as e:
                    deck.move(tokens[1], tokens[2])
        case "save":
            deck.save(tokens[1])
        case "load":
            deck.load(tokens[1])
        case "print-priceless":
            price.print_priceless()
        case "drop":
            drop()

def get_price(name):
    if name in price.current:
        print(f"$ {price.current[name]:.2f}")
    else:
        print(f"No card named \"{name}\" was found.")

# TODO: remove once deck.remove() is implemented
def remove(deck, name, no):
    if no == "all":
        del deck[name]
    else:
        deck[name] -= no
        if deck[name] <= 0:
            del deck[name]

def drop():
   raw = input("Would you like to delete all items in this deck? [y/N] ")
   if raw == "y":
       deck.drop()
