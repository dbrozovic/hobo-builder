# hobo-builder initialization module
# keeps the price information in line with the central server

import urllib.request
import price

server = "https://cse-linux-01.unl.edu/~dbrozovic2/mtg/data/"

try:
    with urllib.request.urlopen(server + "latest.txt", timeout=10) as f:
        server_latest = f.read().decode("utf-8")
except urllib.error.URLError as e:
    server_latest = None
    print("Error: Cannot reach price database. Loading latest local prices.")

try:
    with open("data/latest.txt", "r", encoding="utf-8") as f:
        local_latest = f.read()
except FileNotFoundError as e:
    local_latest = None

if server_latest != local_latest and server_latest != None:
    with urllib.request.urlopen(server + server_latest + ".json") as f, \
         open("data/" + server_latest + ".json", "w") as g:
        g.write(f.read().decode("utf-8"))

    with open("data/latest.txt", "w") as f:
        f.write(server_latest)
    price.current = price.load(server_latest)
else:
    price.current = price.load(local_latest)
