#!/usr/bin/env python3
"""Builds data/sql/manual/world_city_life_dialogues.sql: 800 three-step conversations.

The existing conversation engine uses two nearby residents: the first speaks steps 0 and 2,
the second answers in step 1. Places, goods and levels fit a level 60 realm.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "sql", "manual", "world_city_life_dialogues.sql")
COUNT = 800

ITEMS = ["Copper Ore", "Linen Cloth", "Boar Meat", "Light Leather", "Silverleaf",
         "Malachite", "Rough Stone", "Mageweave Cloth", "Iron Ore", "Heavy Leather",
         "Silk Cloth", "Truesilver Ore", "Small Egg", "Shiny Bauble", "Rusted Sword",
         "Green Hills of Stranglethorn", "Blackmouth Oil", "Soft Banana Bread",
         "Coarse Stone", "Wooden Buckler", "Handmade Leather Bag", "Minor Mana Potion",
         "Simple Flour", "Mild Spices", "Empty Vial", "Bottle of Wine"]
PRICES = ["2 silver", "5 silver", "12 silver", "40 silver", "90 silver", "1 gold",
          "2 gold", "3 gold", "5 gold", "8 gold"]
PLACES = ["the auction house", "the bank", "the inn", "the market", "the forge",
          "the dock", "the plaza", "the mailbox", "the flight master", "the fountain",
          "the bridge", "the north gate", "the south gate", "the tailor", "the alchemist",
          "the stable", "the bakery", "the temple", "the watchtower", "the square"]
CREATURES = ["a wolf", "a boar", "a murloc", "a kobold", "a defias", "an ogre",
             "a spider", "a bear"]
REASONS = ["for my profession", "for a friend", "for the guild bank", "to resell",
           "for an alt", "for a quest"]

# step 0 and step 2: first bot; step 1: second bot.
TEMPLATES = [
    ("Where can I find {item} around {place}?", "Try the vendor near {place}; {price} is a fair price.", "Thanks. I will look before {creature} finds me."),
    ("{item} for {price}? That cannot be right.", "It is {place}. Everything there costs a little extra.", "Then I will wait until the market calms down."),
    ("I lost my {item} somewhere near {place}.", "Ask the guard at {place}; he sees everything.", "Good idea. I owe you a drink if it turns up."),
    ("Did you hear about the guild at {place}?", "Only that they are buying {item} for {price}.", "Then I should pay them a visit."),
    ("Do you have a moment for a duel?", "Only if we keep it away from {place}.", "Agreed. The square is no place for a fight."),
    ("I need {item} {reason}. Any advice?", "Buy it at {place} for {price}, or farm {creature}.", "I will try the market first."),
    ("Is the fishing good near {place}?", "The {creature} scare the fish, but the water is calm.", "Then I will bring a longer pole."),
    ("This weather is ruining my {item}.", "It is always like this around {place}.", "I should have bought a cloak."),
    ("Can you believe {item} goes for {price}?", "At {place}, yes. Everywhere else, no.", "I knew I was being robbed."),
    ("I am new here. What is worth seeing?", "Start at {place}, then follow the road to the {creature}.", "That sounds like a plan."),
    ("The guard at {place} keeps staring at me.", "He does that to everyone with {item} in their bags.", "I will keep it out of sight, then."),
    ("Which inn has the best food?", "The one near {place}. Try the stew, it is only {price}.", "I will. My stomach is making decisions now."),
    ("My {item} is broken. Who repairs it?", "The smith near {place}. Tell him I sent you.", "Thanks. I hope he is gentler with it than I was."),
    ("Have you seen {item} anywhere?", "A trader at {place} had one for {price} this morning.", "I will hurry before it is gone."),
    ("I am heading to {place} after this.", "Mind the {creature} on the road; it has been bold lately.", "I will keep my blade ready."),
    ("Do you remember the old days at {place}?", "I remember when {item} cost {price} and nobody complained.", "We were younger and the world was smaller."),
    ("There is a {creature} near {place} again.", "It took my {item} last week. Be careful.", "I will deal with it before it takes anything else."),
    ("I need to practise before the next fight.", "Use the training dummy near {place}; it does not hit back.", "That is exactly my kind of opponent."),
    ("The market at {place} is busy today.", "Busy enough to sell {item} for {price}, if you are lucky.", "I will try my luck before the crowd thins."),
    ("Well, I should get back to {place}.", "Safe roads. Watch for {creature} after dark.", "You too. Do not let the market cheat you."),
]

def esc(text):
    return text.replace("'", "''")

rows = []
script = 0
per_template = COUNT // len(TEMPLATES)
extra = COUNT % len(TEMPLATES)
for t_index, (a, b, c) in enumerate(TEMPLATES):
    n = per_template + (1 if t_index < extra else 0)
    for i in range(n):
        slots = {
            "item": ITEMS[(t_index * 3 + i) % len(ITEMS)],
            "price": PRICES[(t_index * 5 + i) % len(PRICES)],
            "place": PLACES[(t_index * 2 + i) % len(PLACES)],
            "creature": CREATURES[(t_index + i) % len(CREATURES)],
            "reason": REASONS[(t_index + i) % len(REASONS)],
        }
        script += 1
        for step, frame in enumerate((a, b, c)):
            text = frame.format(**slots)
            rows.append((30000 + script, step, text))

with open(OUT, "w", encoding="utf-8", newline="\n") as out:
    out.write("-- City Life: 800 three-step conversations for two nearby residents. Additive and rerunnable.\n")
    out.write("INSERT IGNORE INTO `city_life_custom_chat`\n")
    out.write("(`id`,`group_name`,`conversation_id`,`step`,`speaker_team`,`channel`,`text`,`weight`,`enabled`) VALUES\n")
    values = []
    for index, (ident, step, text) in enumerate(rows):
        values.append("(%d,'conversation',%d,%d,2,0,'%s',100,1)" % (40000 + index, ident, step, esc(text)))
    out.write(",\n".join(values) + ";\n")
print("%d conversations, %d lines" % (script, len(rows)))
