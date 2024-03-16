import util
import price

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

def drop():
    main.clear()
    side.clear()

def list():
    main_price = 0
    side_price = 0
    print(f"No.  {util.ellipsis('Name', 20)} {util.ellipsis('Price', 7)} Total")
    for (name, no) in main.items():
        p = price.current[name]
        print(f"{no: 02} x {util.ellipsis(name, 20)} "
              f"({p:02.2f}) ${p * no:02.2f}"
              )
        main_price += p * no
    print(f"Total main deck price: ${main_price:02.2f}\n")
    for (name, no) in side.items():
        p = price.current[name]
        print(f"{no: 02} x {util.ellipsis(name, 20)} "
              f"({p:02.2f}) ${p * no:02.2f}"
              )
        side_price += p * no
    print(f"Total sideboard price: ${side_price:02.2f}\n")
    print(f"Total deck price: ${side_price + main_price:02.2f}")

def save(name):
    with open(f"decks/{name}.txt", "w+") as f:
        for c, n in main.items():
            f.write(f"{n} {c}\n")
        f.write("\n")
        for c, n in side.items():
            f.write(f"{n} {c}\n")

def load(name):
    """
    Loads the deck located at data/name.txt. Overwrites the current deck
    without saving it.
    """
    try:
        with open(f"decks/{name}.txt", "r") as f:
            lines = f.readlines()
            drop()
            reading_sideboard = False
            for l in lines:
                if l == "\n":
                    reading_sideboard = True
                else:
                    cardno = util.parse_initial_int(l)
                    no_width = len(str(cardno)) + 1
                    cardname = l[no_width:-1]
                    if reading_sideboard:
                        side[cardname] = cardno
                    else:
                        main[cardname] = cardno
    except OSError as e:
        print(f"Could not open deck \"{name}\".")

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

def move(no, name, direction=None):
    """
    move no name [direction]

    Moves cards between the main deck and the sideboard. A direction can be
    specified manually as the location to move towards, which can be useful if
    copies of a card are present in both the main deck and the sideboard. In
    this situation, the direction defaults to moving to the sideboard if not
    specified.
    """

    def parse_no(no, name, location):
        try:
            return int(no)
        except ValueError as e:
            match location:
                case "main":
                    return main[name]
                case "side":
                    return side[name]

    is_in_main = name in main.keys()
    is_in_side = name in side.keys()

    if not is_in_main and not is_in_side:
        print("Warning: {name} is not in the current deck.")
        return

    match direction:
        case "main":
            if is_in_side:
                no = parse_no(no, name, "side")
                remove(side, no, name)
                add(main, no, name)
        case "side":
            if is_in_main:
                no = parse_no(no, name, "main")
                remove(main, no, name)
                add(side, no, name)
            elif is_in_side:
                no = parse_no(no, name, "side")
                remove(side, no, name)
                add(main, no, name)
