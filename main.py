import init
import command
import deck

while True:
    raw = input(">>> ")
    tokens = command.parse(raw)
    command.execute(tokens)
    # do something to see what command is being called - tokens[0]
    # if price is neccessary feed it to the command module
