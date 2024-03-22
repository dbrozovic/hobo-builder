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

    def add(self, num, name, loc="main"):
        """
        Adds `num` copies of `name` to the deck. Defaults to `self._main`,
        but addition to the sideboard instead can be specified with
        `loc="side"`. Does not attempt to ensure `name` is a valid card name.
        """
        if loc not in {"main", "side"}:
            # TODO: throw warning?
            return
        if loc == "main":
            if name not in self._main:
                self._main[name] = 0
            self._main[name] += num
        else:
            if name not in self._side:
                self._side[name] = 0
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

    def number_of(self, name, loc=None):
        """
        Returns the number of times name appears in `self._main` or
        `self._side`. By default, copies both the main deck and the sideboard
        are counted. To specify one in particular, call with `loc="main"` or
        `loc="side"`.
        """
        if loc is None:
            return self.number_of(name, loc="main") \
                 + self.number_of(name, loc="side")
        num = 0
        if loc == "main":
            if name in self._main:
                num += self._main[name]
        elif loc == "side":
            if name in self._side:
                num += self._side[name]
        else:
            # TODO: warn about invalid `loc`
            return 0
        return num

    def iter_main(self):
        for name in self._main:
            yield name

    def iter_side(self):
        for name in self._side:
            yield name

    def __str__(self):
        s = ""
        for c, n in self._main.items():
            s += f"{n} {c}\n"
        s += "\n"
        for c, n in self._side.items():
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

    # let's see if this works
    def iter(self):
        for name in self._contents:
            yield name

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
