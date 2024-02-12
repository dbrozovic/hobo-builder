# allows access to the decklist across multiple modules

main = dict()
side = dict()

# list of card names with no limit on allowed copies
no_max = [
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
        "Snow-Covered Plains",
        "Snow-Covered Island",
        "Snow-Covered Swanp",
        "Snow-Covered Mountain",
        "Snow-Covered Forest",
        "Dragon's Approach",
        "Persistent Petitioners",
        "Rat Colony",
        "Relentless Rats",
        "Shadowborn Apostle",
        "Slime Against Humanity"
]

def list():
    pass
    # 4 x Lightning Bolt      (0.24) $0.96

def save(name):
    with open(f"decks/{name}.txt", "w+") as f:
        for c, n in main.items():
            f.write(f"{n} {c}\n")
        f.write("\n")
        for c, n in side.items():
            f.write(f"{n} {c}\n")

def total(place):
    s = 0
    for c in place:
        s += c
    return s

def add(place, no, name):
    no = int(no)
    if name not in place:
        place[name] = 0
    place[name] += no
    if place[name] > 4 and name not in no_max:
        print(f"Warning: This deck has {place[name]} copies of \"{name}\". "
              "This deck may not be legal.")

def remove(place, no, name):
    if no == "all":
        del place[name]
        return
    no = int(no)
    if name in place:
        place[name] -= no
        if place[name] <= 0:
            del place[name]
