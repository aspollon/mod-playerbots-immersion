#!/usr/bin/env python3
"""Builds data/sql/manual/world_city_life_chat_catalog.sql: 6,000 ambient lines.

Every line comes from a complete sentence frame whose slots are compatible with that
frame. Openers are not freely mixed with unrelated subjects, which produced nonsense
such as "between us darker skies, so I keep my knife close".
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "sql", "manual", "world_city_life_chat_catalog.sql")
PER_ROLE = 1500

# Each entry: (frame, slots, endings). Every frame uses its own compatible slots.
LEGENDARY = [
    ("I have seen {subject}, {ending}",
     ["worse wars", "better kings", "stranger nights", "quieter markets", "braver recruits",
      "cheaper steel", "longer sieges", "worse harvests", "finer horses", "darker skies",
      "richer guilds", "emptier roads", "stronger storms", "colder winters", "truer friends"],
     ["and I am still standing here.", "but that is another story.", "and I would do it again.",
      "though nobody asked.", "and I have the scars to prove it.", "and this square has not changed.",
      "and I remember every name.", "and I do not miss it.", "and I keep my own counsel.",
      "and I am in no hurry to see it again."]),
    ("In my day, {subject}, {ending}",
     ["we walked to the dungeon", "a copper bought a meal", "guards knew your name",
      "the roads were patrols", "a sword lasted a lifetime", "we had no flying mounts",
      "the innkeeper remembered you", "a duel meant something", "the guild paid its debts",
      "we carried our own arrows", "the market closed at dusk", "the watch was unpaid",
      "the bridge was wooden", "the winters were longer", "the songs were shorter"],
     ["and we liked it.", "and nobody complained.", "and the young ones should be grateful.",
      "though memory is a kind liar.", "and I still do it that way.", "and the world was smaller.",
      "and the evenings were longer.", "and we were still late.", "and it built character.",
      "and I would not trade it."]),
    ("You would not believe {subject}, {ending}",
     ["what I paid for this armour", "how long I waited for this mount", "what the ogres did to my boots",
      "how many wolves I killed", "who I drank with last night", "what the auctioneer told me",
      "how close that duel was", "what lives in the old mine", "how fast the years go",
      "what the guard said to me", "how I lost the shield", "where I buried the chest",
      "why the miller will not speak to me", "how much the repair cost", "who stole my horse"],
     ["and I am not exaggerating.", "but every word is true.", "and I have witnesses.",
      "so do not ask.", "and I keep the receipt.", "and the bard is still working on it.",
      "and I will tell it again later.", "but the ale helps.", "and I am proud of it.",
      "and that is all I will say."]),
    ("Between us, {subject}, {ending}",
     ["the roads are less safe", "the prices are climbing", "the guilds are arguing",
      "the watch is stretched thin", "the docks are quiet", "the north gate is unguarded",
      "the tax collector is due", "the well water tastes odd", "the rats are getting bold",
      "the inn is full of strangers", "the mine is haunted", "the bridge needs repairs",
      "the caravan is late", "the guards are hiring", "the temple is collecting donations"],
     ["and I am not surprised.", "and I watch my step.", "but I have said too much.",
      "and the guards know it too.", "so watch your purse.", "and the market feels it.",
      "and I sleep with one eye open.", "but that is city life.", "and nobody official will admit it.",
      "so stay near the lights."]),
    ("I remember {subject}, {ending}",
     ["the old market", "the first siege", "the night the gate burned", "the winter without bread",
      "the day the guild split", "the bard who never returned", "the well before they covered it",
      "the road before the patrols", "the inn before the new owner", "the square before the statues",
      "the old captain", "the year the river froze", "the festival of lanterns",
      "the house on the corner", "the bell before it cracked"],
     ["and I was younger then.", "but not fondly.", "and the square was full.",
      "though the names are gone.", "and the ale was warm.", "and it rained for a week.",
      "and nobody believed me.", "and I still have the scar.", "but the city has changed.",
      "and I try not to."]),
    ("The old ones say {subject}, {ending}",
     ["the mine is haunted", "the north road is cursed", "the well grants no wishes",
      "the crows bring bad luck", "the old bridge will fall", "a storm follows a broken oath",
      "the dead do not rest under the chapel", "the forest keeps its promises",
      "the river remembers every name", "the statues turn at midnight", "the miller owes a debt",
      "the bell must not ring twice", "the east gate has no shadow", "the lake has no bottom",
      "the first stone was a grave"],
     ["and they are usually right.", "but I have my doubts.", "and the young ones ignore it.",
      "so I mind my own business.", "and the walls remember.", "though nobody listens.",
      "and the market proves it.", "and I have seen it once.", "so I do not go out after dark.",
      "and I would not test it."]),
    ("I once knew {subject}, {ending}",
     ["a guard with one hand", "a mage who feared fire", "a rogue with a kind word",
      "a priest who drank too much", "a captain who never retreated", "a smith who forged the gate",
      "a bard with no voice", "a hunter who knew the woods", "a sailor who hated water",
      "a noble who paid his debts", "a cook who fed the poor", "a scout who never slept",
      "a healer with steady hands", "a farmer with a long memory", "a child who saw the future"],
     ["and they never came back.", "and they owed me money.", "and I still miss them.",
      "but that was another life.", "and they were right about the war.", "and the guild never forgave them.",
      "and the city forgot them.", "but I did not.", "and their sword hangs in my hall.",
      "and I will not speak of it."]),
    ("There was a time when {subject}, {ending}",
     ["a copper bought a meal", "the guards knew your name", "the market closed at dusk",
      "the bridge was the only way north", "the guilds shared a table", "the inn had a bard every night",
      "the watch was unpaid", "the well was the center of town", "the temple fed the poor",
      "the roads were safe after dark", "the gate stood open", "the square held a market every day",
      "the ferry ran at dawn", "the mill belonged to the town", "the bell called the workers"],
     ["and I was there.", "but that is over.", "and we thought it would last.",
      "and the young ones do not believe it.", "and I still keep the habit.", "and the ale was worth drinking.",
      "and the roads were empty.", "but the city grew.", "and nobody locked their door.",
      "and I was happier."]),
    ("Everyone forgets that {subject}, {ending}",
     ["the guards are paid with our taxes", "the roads are repaired in summer", "the well is older than the wall",
      "the guilds owe the city", "the temple shelters the poor", "the market feeds the realm",
      "the dead outnumber the living", "the north gate has no key", "the river floods every spring",
      "the statues were once people", "the taxes are collected twice", "the watch buys its own arrows",
      "the ferry is a private business", "the walls need stones, not speeches", "the poor pay first"],
     ["and it shows.", "but I remember.", "so I keep a candle lit.", "and the market suffers for it.",
      "and the guards do not care.", "which is why we are here.", "and the young ones least of all.",
      "but the old ones know.", "and I have the receipts.", "so I say it again."]),
    ("They tell me {subject}, {ending}",
     ["the market is quiet", "the roads are safe", "the young ones are restless", "the guards are asleep",
      "the guilds are feuding", "the ore is running thin", "the fishing is good", "the inn has new wine",
      "the auction prices are mad", "a storm is coming", "the north road is closed", "the king is visiting",
      "the well has run dry", "the militia is drilling", "the festival is cancelled"],
     ["I have my doubts.", "we will see.", "they are usually wrong.", "and I believe none of it.",
      "but I have heard worse.", "and I intend to find out.", "so I stay where the walls are thick.",
      "and the square is the best place to watch it.", "and I make my own judgment.",
      "so I trust my own eyes."]),
]

BEGGAR = [
    ("Spare a copper for {need}.", ["a warm meal", "a new cloak", "a repair bill", "a bed tonight",
                                     "a loaf of bread", "a healing potion", "a pair of boots",
                                     "a tankard of ale", "a fishing hook", "a letter home",
                                     "a few silver", "an old bag", "a dry corner", "a second chance",
                                     "a kind word"],
     ["Every coin helps.", "I will pay it back. Eventually.", "The guards do not feed me.",
      "I have had a very long week.", "The auction house took the rest.", "I am not proud, only hungry.",
      "A kind word would do too.", "The innkeeper is watching me.", "I will remember you.",
      "Just one, friend."]),
    ("Can you help a fellow with {need}?", ["a few silver", "an old bag", "a spare shirt",
                                            "a little food", "a cheap dagger", "a ride to the inn",
                                            "a message to the guard", "a place by the fire",
                                            "a dry corner", "a second chance", "a warm meal",
                                            "a pair of gloves", "a candle", "a blanket", "a kind word"],
     ["I will not waste it.", "It is colder than it looks.", "I used to have a trade.",
      "The war took the rest.", "I only need a little.", "You look like a generous sort.",
      "I will tell the others.", "It is for a friend, honestly.", "One day I will return it.",
      "The square is not kind to the poor."]),
    ("If you have {need}, I would be grateful.", ["a spare copper", "a crust of bread", "an old cloak",
                                                  "a moment to listen", "a coin for the well", "a kind word",
                                                  "a place at your table", "a frayed rope", "a candle end",
                                                  "a pair of gloves", "a blanket", "a little water",
                                                  "a dry match", "an old boot", "a fish"],
     ["I will make it count.", "I am not asking for much.", "The night is long.",
      "I will share it.", "The others will be glad.", "It is more than I had.",
      "I will say a prayer for you.", "You are too kind.", "I will not forget.",
      "The city could use more like you."]),
    ("A kind soul might offer {need}.", ["a warm meal", "a few silver", "a dry corner", "a blanket",
                                         "a pair of boots", "a healing potion", "a letter home",
                                         "a moment of time", "a kind word", "a second chance",
                                         "a place by the fire", "an old bag", "a candle", "a fish",
                                         "a crust of bread"],
     ["I would not ask twice.", "The night is cold.", "I have nothing left to sell.",
      "The guards walked past me.", "It is for a friend.", "I will repay the kindness.",
      "A little is enough.", "I am not choosy.", "The city has forgotten us.",
      "You are the first to stop."]),
    ("I am asking for {need}.", ["a warm meal", "a few silver", "a dry corner", "a blanket",
                                  "a pair of boots", "a healing potion", "a letter home", "a kind word",
                                  "a second chance", "a place by the fire", "an old bag", "a candle",
                                  "a fish", "a crust of bread", "a little water"],
     ["That is all.", "I will not beg twice.", "The guards will not help.",
      "The auction house took the rest.", "It is colder than it looks.", "I used to have a trade.",
      "The war took the rest.", "I only need a little.", "You look like a generous sort.",
      "I will tell the others."]),
    ("The guards will not give me {need}.", ["a warm meal", "a few silver", "a dry corner", "a blanket",
                                             "a pair of boots", "a healing potion", "a letter home",
                                             "a kind word", "a second chance", "a place by the fire",
                                             "an old bag", "a candle", "a fish", "a crust of bread",
                                             "a little water"],
     ["They never do.", "I asked three times.", "They only see the rags.",
      "The captain has no time.", "I am not worth the paperwork.", "So I ask the square instead.",
      "A kind soul is worth more than a guard.", "The city could do better.",
      "I will not trouble them again.", "You stopped, at least."]),
    ("One small thing: {need}.", ["a warm meal", "a few silver", "a dry corner", "a blanket",
                                   "a pair of boots", "a healing potion", "a letter home", "a kind word",
                                   "a second chance", "a place by the fire", "an old bag", "a candle",
                                   "a fish", "a crust of bread", "a little water"],
     ["That is all I ask.", "It would mean a lot.", "The night is long.",
      "I have had a very long week.", "The auction house took the rest.", "I am not proud, only hungry.",
      "A kind word would do too.", "The innkeeper is watching me.", "I will remember you.",
      "Just one, friend."]),
    ("All I want is {need}.", ["a warm meal", "a few silver", "a dry corner", "a blanket",
                                "a pair of boots", "a healing potion", "a letter home", "a kind word",
                                "a second chance", "a place by the fire", "an old bag", "a candle",
                                "a fish", "a crust of bread", "a little water"],
     ["Nothing more.", "The guards do not feed me.", "I have had a very long week.",
      "The auction house took the rest.", "I am not proud, only hungry.", "A kind word would do too.",
      "The innkeeper is watching me.", "I will remember you.", "Just one, friend.",
      "Every coin helps."]),
    ("Do not have {need}? A kind word helps.", ["a spare copper", "a crust of bread", "an old cloak",
                                                "a moment to listen", "a coin for the well", "a kind word",
                                                "a place at your table", "a frayed rope", "a candle end",
                                                "a pair of gloves", "a blanket", "a little water",
                                                "a dry match", "an old boot", "a fish"],
     ["I will make it count.", "I am not asking for much.", "The night is long.", "I will share it.",
      "The others will be glad.", "It is more than I had.", "I will say a prayer for you.",
      "You are too kind.", "I will not forget.", "The city could use more like you."]),
    ("I used to {past}.", ["own a shop in this city", "guard the north gate",
                            "sail with the fleet", "work the forge", "keep a horse",
                            "sing at the inn", "have a name here", "sell swords to heroes",
                            "know the auctioneer", "sleep under a roof", "feed my family",
                            "pay my taxes", "wear a clean shirt", "own a pair of boots",
                            "have a trade"],
     ["Now I beg for soup.", "Then the war came.", "I miss it every day.",
      "Nobody remembers.", "The guild took everything.", "I am still here.",
      "The city moved on.", "I learned to be invisible.", "That is how it goes.",
      "I would go back."]),
]

BEGGAR_PRESENT = ["beg for soup", "sleep under the bridge", "carry crates at the dock",
                  "sell old iron", "walk everywhere", "sing for coppers", "answer to nobody",
                  "sharpen knives for bread", "wait outside the auction house", "sleep in the alley",
                  "stand in the soup line", "owe the tax collector", "wear these rags",
                  "wrap my feet in cloth", "take whatever work I find"]

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
    "The {fish} are {mood} today.", "I have been watching {fish} for an hour.",
    "{mood} water, {fish} everywhere, and still nothing.", "They say {fish} bite when the {weather}.",
    "A {fish} just laughed at my bait.", "My line is {state}. The {fish} are winning.",
    "I came for {fish} and found {weather}.", "The {fish} here are {mood}, like the weather.",
    "One more cast. The {fish} owe me that much.", "I have caught {fish}, boots and a cold.",
    "The water is {mood}; the {fish} are not.", "If the {fish} are not biting, the {weather} is to blame.",
    "I named a {fish} once. It got away.", "A quiet {place} and a pole. That is enough.",
    "The {fish} are {mood} and my patience is not.", "I could be fighting {creature}. I am watching water instead.",
    "The {fish} know my name by now.", "This {place} is the best spot for {fish}.",
    "The {weather} is perfect. The {fish} disagree.", "I have {state} my line three times. The {fish} are {mood}.",
    "A {fish} would make this whole day worthwhile.", "The {fish} are {mood}; so is the innkeeper.",
    "I saw a {fish} jump. It was showing off.", "The {place} is quiet, the {fish} are not.",
    "My bait is {state}. So is my patience.", "The {fish} are {mood} and I am still here.",
    "I will catch a {fish} if it takes all {weather}.", "The {fish} in this {place} have expensive taste.",
    "I brought {item} instead of bait. The {fish} noticed.", "The {weather} changed and the {fish} stopped caring.",
]
FISH = ["trout", "salmon", "catfish", "perch", "bass", "eels", "sunfish", "mudfish",
        "river fish", "lake fish", "old boots", "murlocs", "turtles"]
MOOD = ["hungry", "sleepy", "suspicious", "playful", "stubborn", "quiet", "rude",
        "generous", "moody", "fast", "slow", "distant", "curious"]
WEATHER = ["rain", "sun", "wind", "fog", "clouds", "cold", "heat", "storm"]
STATE = ["repaired", "lost", "tangled", "replaced", "cleaned", "bent", "ready"]
PLACE = ["lake", "river", "harbour", "dock", "shore", "pond", "creek", "bay"]
ITEM = ["a shiny spoon", "an old boot", "a copper coin", "a flower", "a small rock"]


def esc(text):
    return text.replace("'", "''")


def add(rows, seen, group, text, limit):
    if len(rows) >= limit or text in seen:
        return False
    seen.add(text)
    rows.append((group, text))
    return True


def main():
    rows = []
    legendary = []
    seen = set()
    for frame, subjects, endings in LEGENDARY:
        for subject in subjects:
            for ending in endings:
                add(legendary, seen, "legendary", frame.format(subject=subject, ending=ending), PER_ROLE)
    beggar = []
    seen = set()
    for frame, slots, endings in BEGGAR:
        for slot_index, slot in enumerate(slots):
            for ending in endings:
                text = frame.format(need=slot, past=slot)
                add(beggar, seen, "beggar", text + " " + ending if ending else text, PER_ROLE)
    buyer = []
    seen = set()
    for frame, closer in BUYER:
        for item in ITEMS:
            for price in PRICES:
                text = frame.format(item=item, price=price)
                if closer:
                    text += " " + closer
                add(buyer, seen, "buyer", text, PER_ROLE)
    fishing = []
    seen = set()
    for frame in FISHING:
        for fish in FISH:
            for mood in MOOD:
                for weather in WEATHER:
                    for state in STATE:
                        for place in PLACE:
                            for item in ITEM:
                                text = frame.format(fish=fish, mood=mood, weather=weather,
                                                    state=state, place=place, item=item, creature="a wolf")
                                add(fishing, seen, "fishing", text, PER_ROLE)
    rows = legendary + beggar + buyer + fishing
    with open(OUT, "w", encoding="utf-8", newline="\n") as out:
        out.write("-- City Life: 6,000 ambient lines for the level 60 realm. Additive and rerunnable.\n")
        out.write("-- Groups used by the module: legendary, beggar, buyer, fishing.\n")
        out.write("DELETE FROM `city_life_custom_chat` WHERE `id` BETWEEN 20000 AND 25999;\n")
        out.write("INSERT INTO `city_life_custom_chat`\n")
        out.write("(`id`,`group_name`,`speaker_team`,`channel`,`text`,`weight`,`enabled`) VALUES\n")
        values = []
        for index, (group, text) in enumerate(rows):
            values.append("(%d,'%s',2,0,'%s',100,1)" % (20000 + index, group, esc(text)))
        out.write(",\n".join(values) + ";\n")
    print("%d lines -> %s" % (len(rows), OUT))


if __name__ == "__main__":
    main()
