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
