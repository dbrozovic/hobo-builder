# hobo-builder initialization module
# keeps the price information in line with the central server

import urllib.request
import price

server = "https://cse-linux-01.unl.edu/~dbrozovic2/mtg/data/"

with urllib.request.urlopen(server + "latest.txt") as f:
    server_latest = f.read().decode("utf-8")

with open("data/latest.txt", "a+", encoding="utf-8") as f:
    local_latest = f.read()

if server_latest != local_latest:
    with urllib.request.urlopen(server + server_latest + ".json") as f, \
         open("data/" + server_latest + ".json", "w") as g:
        g.write(f.read().decode("utf-8"))

    with open("data/latest.txt", "w") as f:
        f.write(server_latest)

price.current = price.load(server_latest)
