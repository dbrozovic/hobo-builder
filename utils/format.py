"""
Contains utilities for formatting strings.
"""

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
