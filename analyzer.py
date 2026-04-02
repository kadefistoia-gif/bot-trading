import json

with open("data.json") as f:
    data = json.load(f)

bots = {}

for d in data:
    if "evento" not in d:
        continue

    bot = d["bot_id"]
    bots.setdefault(bot, {"wins":0, "losses":0, "open":None})

    if d["evento"] == "entry":
        bots[bot]["open"] = d["precio"]

    elif d["evento"] in ["tp", "sl"] and bots[bot]["open"]:
        entry = bots[bot]["open"]
        exit = d["precio"]

        if exit > entry:
            bots[bot]["wins"] += 1
        else:
            bots[bot]["losses"] += 1

        bots[bot]["open"] = None

print(bots)
