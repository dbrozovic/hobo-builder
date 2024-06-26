"""
    Contains utilites for parsing user input.
"""

def tokens(string):
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

def initial_int(string):
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
