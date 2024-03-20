import json

class Deck:
    """
    Represents a decklist (not necessarily a legal or valid one) and provides
    some basic methods for interacting with that decklist.
    """

    def __init__(self):
        self._main = dict()
        self._side = dict()

    def clear(self):
        """
        Removes all elements from self.main and self.side.
        """
        self._main.clear()
        self._side.clear()

    def add_main(self, num, name):
        """
        Adds `num` to `self._main[name]`. Does not attempt to ensure `name` is
        a valid card name.
        """
        self._main[name] += num

    def add_side(self, num, name):
        """
        Adds `num` to `self._side[name]`. Does not attempt to ensure `name` is
        a valid card name.
        """
        self._side[name] += num

    def remove_main(self, num, name):
        """
        Subtracts `num` from `self._main[name]`. If the resulting number is
        less than one, `self._main[name]` is deleted.
        """
        if name in self._main:
            self._main[name] -= num
            if self._main[name] < 1:
                del self._main[name]

    def remove_side(self, num, name):
        """
        Subtracts `num` from `self._side[name]`. If the resulting number is
        less than one, `self._side[name]` is deleted.
        """
        if name in self._side:
            self._side[name] -= num
            if self._side[name] < 1:
                del self._side[name]

    def number_of(self, name, in=None):
        """
        Returns the number of times name appears in `self._main` or
        `self._side`. By default, copies both the main deck and the sideboard
        are counted. To specify one in particular, call with `in="main"` or
        `in="side"`.
        """
        if in is None:
            return self.number_of(name, "main") + self.number_of(name, "side")
        num = 0
        if name in self[f"_{in}"]:
            num += self[f"_{in}"][name]
        return num

    def in_main(self, name):
        """
        Returns true if `name` is in `self._main`.
        """
        return name in self._main

    def in_side(self, name):
        """
        Returns true if `name` is in `self._side`.
        """
        return name in self._side

    def __str__(self):
        s = ""
        for c, n in self.main.items():
            s += f"{n} {c}\n"
        s += "\n"
        for c, n in self.side.items():
            s += f"{n} {c}\n"
        return s

class PriceList:
    """
    Represents the legal cards and their prices. When initialized, a date in
    yyyy-mm-dd format may be specified to load prices from that date if
    available locally. If no date is specified, the most recent available
    price data loaded.
    """
    def __init__(self, date=None):
        self._contents = dict()
        if date is None:
            with open("data/latest.txt") as f:
                date = f.read()
        self._load(date)

    def _load(self, string):
        """
        Loads the contents of `data/[string].json` to `self._contents` as a
        dictionary of name:price pairs. Cards without a recorded price are
        given a value of -1.
        """
        self._no_price = 0

        try:
            f = open(f"data/{string}.json")
        except FileNotFoundError:
            # TODO: write some error handling.
            pass
        else:
            with f:
                raw = json.load(f)

        for c in raw:
            try:
                self._contents[c["name"]] = float(c["usd"])
            except TypeError:
                self._no_price += 1
                self._contents[c["name"]] = -1

    def get(self, name):
        """
        Returns the price of `name`. A return value of -1 indicates that there
        is no recorded price for `name`. A return value of -2 indicates that
        `name` is not recognized as a format-legal card.
        """
        if name not in self._contents:
            return -2
        else:
            return self._contents[name]

def parse_tokens(string):
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

# TODO: maybe move to separate file for command utils?
def ellipsis(string, length):
    """
    Returns a string padded or truncated to the given length.
    If the string is longer, it is truncated three characters short and padded
    with "..."
    """
    if len(string) <= length:
        return f"{string:<{length}}"
    else:
        return f"{string[:length - 3]}..."

def parse_initial_int(string):
    """
    If the first sequence of characters are digits, parses and returns those
    characters as an integer. Otherwise returns 0.
    """
    stripped_string = ""
    for c in string:
        if c.isdigit():
            stripped_string += c
        else:
            break
    if stripped_string == "":
        return 0
    else:
        return int(stripped_string)
