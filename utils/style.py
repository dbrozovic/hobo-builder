"""
    Contains utilities for using ANSI SGR parameters for simple text styling.
    Three escape constants represent common styles, and the warning() and
    error() functions return a string surrounded by the correct escape
    sequences.
"""

CLEAR = "\033[0m"
WARNING = "\033[33;1m"
ERROR = "\033[31;1m"

def warning(message):
    return WARNING + message + CLEAR

def error(message):
    return ERROR + message + CLEAR

class Custom:
    """
        Allows for the creation of custom ANSI SGR sequences.
        self.escape contains the full sequence.
    """
    def __init__(self, effects = "0"):
        self.escape = "\033[" + effects + "m"
    def format(self, message):
        """
            Formats `message` using the SGR sequence previously defined.
        """
        return self.escape + message + CLEAR
