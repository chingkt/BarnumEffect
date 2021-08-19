archer = "射手座"
balance = "天秤座"
bigcrap = "巨蟹座"
doublefish = "雙魚座"
evilscorpion = "魔羯座"
goldcow = "金牛座"
lion = "獅子座"
scorpion = "天蠍座"
twins = "雙子座"
virgin = "處女座"
water = "水瓶座"
whitesheep = "牡羊座"


def analysis(star: str) -> str:
    """generates an analysis text based on 12 constellations"""
    if star == archer:
        with open("data/archer.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == balance:
        with open("data/balance.txt", "r", encoding="utf-8") as f:
            return "".join(f.readlines())
    elif star == bigcrap:
        with open("data/bigcrap.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == doublefish:
        with open("data/doublefish.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == evilscorpion:
        with open("data/evilscorpion.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == goldcow:
        with open("data/goldcow.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == lion:
        with open("data/lion.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == scorpion:
        with open("data/scorpion.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == twins:
        with open("data/twins.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == virgin:
        with open("data/virgin.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == water:
        with open("data/water.txt", encoding="utf8") as f:
            return "".join(f.readlines())
    elif star == whitesheep:
        with open("data/whitesheep.txt", encoding="utf8") as f:
            return "".join(f.readlines())
if __name__ == '__main__':
    with open("data/balance.txt", encoding="utf8") as f:
        text = f.readlines()
        print("".join(text))
