#!/usr/bin/env python3
"""Builds data/sql/manual/world_city_life_chat_catalog.sql: 6,000 ambient lines.

Four roles that actually use the City Life chat table: legendary residents, beggars,
buyers and fishers. All places, goods and levels fit a level 60 realm.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "sql", "manual", "world_city_life_chat_catalog.sql")
PER_ROLE = 1500

LEG_OPEN = ["I have seen", "They tell me", "In my day", "You would not believe",
            "I remember", "They say", "I have heard", "Long before you were born",
            "Listen closely", "Between us", "The old ones say", "I once knew a man who",
            "There was a time when", "Do not repeat this", "Everyone forgets that"]
LEG_SUB = ["worse wars", "better kings", "stranger nights", "quieter markets", "braver recruits",
           "cheaper steel", "longer sieges", "worse harvests", "finer horses", "darker skies",
           "richer guilds", "emptier roads", "stronger ale", "colder winters", "truer friends"]
LEG_END = ["and I am still standing here.", "but that is another story.", "and I would do it again.",
           "though nobody asked.", "and I have the scars to prove it.", "so I keep my blade close.",
           "and this square has not changed.", "which is more than I can say for the realm.",
           "and I remember every name.", "but the ale was better then."]
BEG_OPEN = ["Spare a copper for", "Can you help a fellow with", "I used to", "If you have",
            "A kind soul might offer", "I am asking for", "Do you have", "Any chance of",
            "I would not ask, but", "The guards will not give me", "One small thing:",
            "Could you spare", "I need only", "A generous sort might share", "All I want is"]
BEG_NEED = ["a warm meal", "a new cloak", "a repair bill", "a bed tonight", "a loaf of bread",
            "a healing potion", "a pair of boots", "a tankard of ale", "a fishing hook",
            "a letter home", "a few silver", "an old bag", "a dry corner", "a second chance",
            "a kind word"]
BEG_END = ["Every coin helps.", "I will pay it back. Eventually.", "The guards do not feed me.",
           "I have had a very long week.", "The auction house took the rest.",
           "I am not proud, only hungry.", "A kind word would do too.",
           "The innkeeper is watching me.", "I will remember you.", "Just one, friend."]


LEGENDARY = [
    ("I have seen", ["worse wars", "better kings", "stranger nights", "quieter markets",
                     "braver recruits", "cheaper steel", "longer sieges", "worse harvests",
                     "finer horses", "darker skies"],
     ["and I am still standing here.", "but that is another story.", "and I would do it again.",
      "though nobody asked.", "and I have the scars to prove it.", "so I keep my blade close.",
      "and this square has not changed.", "which is more than I can say for the realm.",
      "and I remember every name.", "but the ale was better then."]),
    ("They tell me", ["the market is quiet", "the roads are safe", "the young ones are restless",
                      "the guards are asleep", "the guilds are feuding", "the ore is running thin",
                      "the fishing is good", "the inn has new wine", "the auction prices are mad",
                      "a storm is coming"],
     ["I have my doubts.", "we will see.", "they are usually wrong.", "and I believe none of it.",
      "so I sharpen my sword.", "and I still lock my door.", "but I have heard worse.",
      "and I intend to find out.", "so I stay where the walls are thick.",
      "and the square is the best place to watch it."]),
    ("In my day", ["we walked to the dungeon", "a copper bought a meal", "guards knew your name",
                   "the roads were patrols", "a sword lasted a lifetime", "we had no flying mounts",
                   "the innkeeper remembered you", "a duel meant something", "the guild paid its debts",
                   "we carried our own arrows"],
     ["and we liked it.", "and nobody complained.", "and the young ones should be grateful.",
      "though memory is a kind liar.", "and I still do it that way.", "and the world was smaller.",
      "and the ale was cheaper.", "and we were still late.", "and it built character.",
      "and I would not trade it."]),
    ("You would not believe", ["what I paid for this armour", "how long I waited for this mount",
                               "what the ogres did to my boots", "how many wolves I killed",
                               "who I drank with last night", "what the auctioneer told me",
                               "how close that duel was", "what lives in the old mine",
                               "how fast the years go", "what the guard said to me"],
     ["and I am not exaggerating.", "but every word is true.", "and I have witnesses.",
      "so do not ask.", "and I keep the receipt.", "and the bard is still working on it.",
      "and I will tell it again later.", "but the ale helps.", "and I am proud of it.",
      "and that is all I will say."]),
]

BEGGAR = [
    ("Spare a copper for", ["a warm meal", "a new cloak", "a repair bill", "a bed tonight",
                            "a loaf of bread", "a healing potion", "a pair of boots",
                            "a tankard of ale", "a fishing hook", "a letter home"],
     ["Every coin helps.", "I will pay it back. Eventually.", "The guards do not feed me.",
      "I have had a very long week.", "The auction house took the rest.",
      "I am not proud, only hungry.", "A kind word would do too.",
      "The innkeeper is watching me.", "I will remember you.", "Just one, friend."]),
    ("Can you help a fellow with", ["a few silver", "an old bag", "a spare shirt",
                                    "a little food", "a cheap dagger", "a ride to the inn",
                                    "a message to the guard", "a place by the fire",
                                    "a dry corner", "a second chance"],
     ["I will not waste it.", "It is colder than it looks.", "I used to have a trade.",
      "The war took the rest.", "I only need a little.", "You look like a generous sort.",
      "I will tell the others.", "It is for a friend, honestly.", "One day I will return it.",
      "The square is not kind to the poor."]),
    ("I used to", ["own a shop in this city", "guard the north gate", "sail with the fleet",
                   "work the forge", "keep a horse", "sing at the inn", "have a name here",
                   "sell swords to heroes", "know the auctioneer", "sleep under a roof"],
     ["and now I beg for soup.", "and then the war came.", "and I miss it every day.",
      "and nobody remembers.", "and the guild took everything.", "and I am still here.",
      "and the city moved on.", "and I learned to be invisible.", "and that is how it goes.",
      "and I would go back."]),
    ("If you have", ["a spare copper", "a crust of bread", "an old cloak", "a moment to listen",
                     "a coin for the well", "a kind word", "a place at your table",
                     "a frayed rope", "a candle end", "a pair of gloves"],
     ["I will make it count.", "I am not asking for much.", "The night is long.",
      "I will share it.", "The others will be glad.", "It is more than I had.",
      "I will say a prayer for you.", "You are too kind.", "I will not forget.",
      "The city could use more like you."]),
]

BUYER = [
    ("WTB {item}, paying {price}.", "COD please."),
    ("Buying {item} for {price}.", "Mail it COD."),
    ("WTB {item}. {price} each.", "Send it COD."),
    ("Paying {price} for {item}.", "COD only, please."),
    ("Need {item}, {price}.", "I will pay the postage."),
    ("WTB {item} in bulk. {price} per stack.", "COD to me."),
    ("Looking for {item}. Offering {price}.", "Mail COD."),
    ("{item} wanted. {price}.", "Quick deal, COD."),
    ("WTB {item}, {price} and not a copper more.", "COD or no deal."),
    ("Buying {item} for an alt. {price}.", "Send COD."),
    ("WTB {item} for the guild bank. {price}.", "COD please."),
    ("Need {item} before the raid. {price}.", "Mail it COD."),
    ("WTB {item}, paying well. {price}.", "COD, thanks."),
    ("{item} for {price}? I am buying.", "Send it COD."),
    ("WTB {item}. Will pay {price}.", "COD only."),
    ("Buying {item} at {price}.", "Post it COD."),
    ("WTB {item} for a friend. {price}.", "COD, please."),
    ("Need {item}. {price} is fair.", "Mail COD."),
    ("WTB {item}, {price} per piece.", "COD to the usual name."),
    ("Buying {item} today only. {price}.", "COD, no haggling."),
    ("WTB {item}. {price}.", "Send it COD and I will stop shouting."),
    ("Paying {price} for {item}.", "COD, and a thank you."),
    ("WTB {item}. {price} each, any amount.", "Mail COD."),
    ("Looking for {item} for {price}.", "COD please."),
    ("WTB {item}, {price}.", "Post it COD."),
    ("Buying {item} for {price}.", "COD to the guild bank."),
    ("WTB {item} before the market closes. {price}.", "COD, hurry."),
    ("Need {item}, paying {price}.", "Mail it COD."),
    ("WTB {item}. {price}.", "COD and no questions."),
    ("Buying {item} at {price}.", "Send it COD."),
]
ITEMS = ["level 55-60 green gear", "level 60 cloth", "level 60 leather", "level 60 mail",
         "level 60 plate", "a level 60 chestpiece", "a level 60 weapon", "endgame greens",
         "Mageweave Cloth", "Runecloth", "Truesilver Ore", "Thorium Ore", "Heavy Leather",
         "Rugged Leather", "Silk Cloth", "Iron Ore", "Copper Ore", "Small Radiant Shard",
         "Large Radiant Shard", "Dream Dust", "Golden Sansam", "Mountain Silversage",
         "Black Lotus", "Fused Wiring", "Essence of Water", "Essence of Air",
         "a sturdy shield", "a healer's ring", "a caster cloak", "a tanking trinket"]
PRICES = ["3 gold", "5 gold", "8 gold", "10 gold", "12 gold", "15 gold", "18 gold",
          "20 gold", "25 gold", "30 gold", "40 gold", "50 gold", "2 gold 50",
          "75 silver", "1 gold", "60 silver", "90 silver"]

FISHING = [
    ("The {fish} are {mood} today.", ""),
    ("I have been watching {fish} for an hour.", ""),
    ("{mood} water, {fish} everywhere, and still nothing.", ""),
    ("They say {fish} bite when the {weather}.", ""),
    ("A {fish} just laughed at my bait.", ""),
    ("My line is {state}. The {fish} are winning.", ""),
    ("I came for {fish} and found {weather}.", ""),
    ("The {fish} here are {mood}, like the weather.", ""),
    ("One more cast. The {fish} owe me that much.", ""),
    ("I have caught {fish}, boots and a cold.", ""),
    ("The water is {mood}; the {fish} are not.", ""),
    ("If the {fish} are not biting, the {weather} is to blame.", ""),
    ("I named a {fish} once. It got away.", ""),
    ("A quiet {place} and a pole. That is enough.", ""),
    ("The {fish} are {mood} and my patience is not.", ""),
    ("I could be fighting {creature}. I am watching water instead.", ""),
    ("The {fish} know my name by now.", ""),
    ("This {place} is the best spot for {fish}.", ""),
    ("The {weather} is perfect. The {fish} disagree.", ""),
    ("I have {state} my line three times. The {fish} are {mood}.", ""),
    ("A {fish} would make this whole day worthwhile.", ""),
    ("The {fish} are {mood}; so is the innkeeper.", ""),
    ("I saw a {fish} jump. It was showing off.", ""),
    ("The {place} is quiet, the {fish} are not.", ""),
    ("My bait is {state}. So is my patience.", ""),
    ("The {fish} are {mood} and I am still here.", ""),
    ("I will catch a {fish} if it takes all {weather}.", ""),
    ("The {fish} in this {place} have expensive taste.", ""),
    ("I brought {item} instead of bait. The {fish} noticed.", ""),
    ("The {weather} changed and the {fish} stopped caring.", ""),
]
FISH = ["trout", "salmon", "catfish", "perch", "bass", "eels", "sunfish", "mudfish",
        "river fish", "lake fish", "old boots", "murlocs", "turtles"]
MOOD = ["hungry", "sleepy", "suspicious", "playful", "stubborn", "quiet", "rude",
        "generous", "moody", "fast", "slow", "distant", "curious"]
WEATHER = ["rain", "sun", "wind", "fog", "clouds", "cold", "heat", "storm"]
STATE = ["repaired", "lost", "tangled", "replaced", "cleaned", "bent", "ready"]
PLACE = ["lake", "river", "harbour", "dock", "shore", "pond", "creek", "bay"]
ITEM = ["a shiny spoon", "an old boot", "a copper coin", "a flower", "a small rock"]


def sql_escape(text):
    return text.replace("'", "''")


def build_rows():
    rows = []
    next_id = 20000
    # Legendary
    seen = set()
    count = 0
    for opening in LEG_OPEN:
        for subject in LEG_SUB:
            for closer in LEG_END:
                text = "%s %s, %s" % (opening, subject, closer)
                if text in seen:
                    continue
                seen.add(text)
                rows.append(("legendary", text))
                count += 1
                if count >= PER_ROLE:
                    break
            if count >= PER_ROLE:
                break
        if count >= PER_ROLE:
            break
    # Beggar
    seen = set()
    count = 0
    for opening in BEG_OPEN:
        for need in BEG_NEED:
            for closer in BEG_END:
                text = "%s %s. %s" % (opening, need, closer)
                if text not in seen:
                    seen.add(text)
                    rows.append(("beggar", text))
                    count += 1
                    if count >= PER_ROLE:
                        break
            if count >= PER_ROLE:
                break
        if count >= PER_ROLE:
            break
    # Buyer
    seen = set()
    count = 0
    for frame, closer in BUYER:
        for item in ITEMS:
            for price in PRICES:
                text = frame.format(item=item, price=price)
                if closer:
                    text += " " + closer
                if text not in seen:
                    seen.add(text)
                    rows.append(("buyer", text))
                    count += 1
                    if count >= PER_ROLE:
                        break
            if count >= PER_ROLE:
                break
        if count >= PER_ROLE:
            break
    # Fishing
    seen = set()
    count = 0
    for frame, _ in FISHING:
        for fish in FISH:
            for mood in MOOD:
                for weather in WEATHER:
                    for state in STATE:
                        for place in PLACE:
                            for item in ITEM:
                                text = frame.format(fish=fish, mood=mood, weather=weather, state=state, place=place, item=item, creature="a wolf")
                                if text not in seen:
                                    seen.add(text)
                                    rows.append(("fishing", text))
                                    count += 1
                                    if count >= PER_ROLE:
                                        break
                            if count >= PER_ROLE:
                                break
                        if count >= PER_ROLE:
                            break
                    if count >= PER_ROLE:
                        break
                if count >= PER_ROLE:
                    break
            if count >= PER_ROLE:
                break
        if count >= PER_ROLE:
            break
    return rows, next_id


def main():
    rows, next_id = build_rows()
    with open(OUT, "w", encoding="utf-8", newline="\n") as out:
        out.write("-- City Life: 6,000 ambient lines for the level 60 realm. Additive and rerunnable.\n")
        out.write("-- Groups used by the module: legendary, beggar, buyer, fishing.\n")
        out.write("INSERT IGNORE INTO `city_life_custom_chat`\n")
        out.write("(`id`,`group_name`,`speaker_team`,`channel`,`text`,`weight`,`enabled`) VALUES\n")
        values = []
        for index, (group, text) in enumerate(rows):
            values.append("(%d,'%s',2,0,'%s',100,1)" % (next_id + index, group, sql_escape(text)))
        out.write(",\n".join(values) + ";\n")
    print("%d lines -> %s" % (len(rows), OUT))


if __name__ == "__main__":
    main()
