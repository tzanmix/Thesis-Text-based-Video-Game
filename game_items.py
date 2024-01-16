#game items
import adventurelib as adv
import random

adv.Item.color = "undistinguished"
adv.Item.description = "a generic thing"
adv.Item.edible = False
adv.Item.wearable = False
adv.Item.damage = 0
adv.Item.bonus = 0
adv.Item.weight = 1
adv.Item.cost = 0

x_coord = 4
y_coord = 9
#player health
hit_points = 20
#sum of hit points + armour protection
total_hit_points = 21
#money available to the player
floren_balance = 20
#a stat thats keep track of the crimes the player commits
negative_karma = 0
#player inventory
inventory = adv.Bag()


#weapon materials
materials = ["steel", "silver", "gold", "bronze"]
#possibilities of material in %
weights = [40, 35, 5, 20]
cost_based_on_condition = {"old": 5, "rusty": 10, "brand new": 1, "used": 2}
damage_based_on_condition = {"old": 3, "rusty": 1, "brand new": 10, "used": 7}
#weapon weights
weapon_weights = {"sword": 5, "dagger": 3, "shield": 10, "axe": 7, "warhammer": 8, "spear": 6}
consumables = ["apple", "chicken", "rabbit", "deer", "stew", "healing potion", "ale", "mead"]
consumables_costs = {"apple": 10, "chicken": 20, "rabbit": 15, "deer": 25, "stew": 30, "healing potion": 50, "ale": 20, "mead": 25}
consumables_bonus = {"apple": 3, "chicken": 5, "rabbit": 4, "deer": 6, "mashed potatoes": 3, "stew": 7, "healing potion": 10, "ale": 5, "mead": 6}
consumables_descriptions = {"apple": "a small apple", "chicken": "a cooked chicken leg", "rabbit": "a cooked rabbit", "deer": "well cooked deer leg", 
                            "stew": "a stew with carrots, potatoes, lamb and bass",
                            "healing potion": "a flask of a cyan liquid, it's a healing potion", "ale": "a cup of beer", "mead": "a cup of alcoholic honey wine"}
#armours
armour_types = ["plate armour", "cuirass", "chainmail", "leather armour", "tunic"]
armour_bonus = {"plate armour": 8, "cuirass": 5, "chainmail": 7, "leather armour": 3, "tunic": 1}
armour_weights = {"plate armour": 10, "cuirass": 8, "chainmail": 6, "leather armour": 4, "tunic": 2}
armour_condition = ["worn", "brand new"]
armour_condition_penalty = {"worn": 2, "brand new": 1}
armour_cost = {"plate armour": 250, "cuirass": 175, "chainmail": 120, "leather armour": 75, "tunic": 50}
armour_description = {"plate armour": "A very heavy armour, that consists of metal plates that are shaped to fit the chest, the shoulders and the thighs and also includes gauntlets and a helmet.", 
                      "cuirass": "A heavy piece of armour that covers the chest and the back.", 
                      "chainmail": "A medium weight armour that is made of interlocking metal rings, it combines a balance between flexibility and protection.", 
                      "leather armour": "Made of hardened leather, this light armour provides some protection, but its wearer gains flexibility.", 
                      "tunic": "A simple cotton tunic, it provides no protection, but is very comfortable."}

def generate_weapon(type, condition):
    material = random.choices(materials, weights=weights, k=1)
    #condition = random.choice(["old", "brand new", "used", "rusty"])
    item = adv.Item(condition+" "+material[0]+" "+type, type)
    item.color = material[0]
    item.edible = False
    item.cost = round(random.randint(25,100)/cost_based_on_condition[condition])
    item.weight = weapon_weights[type]
    if type == "shield":
        item.damage = 0
        item.bonus = damage_based_on_condition[condition]
    else:
        #item.damage = random.randint(0,5)+damage_based_on_condition[condition]
        item.damage = weapon_weights[type] + damage_based_on_condition[condition] - random.randint(0,3)
        item.bonus = 0
    item.description = "a "+material[0]+" "+condition+" "+type
    return item
    
def generate_consumable_items():
    type = random.choice(consumables)
    item = adv.Item(type)
    item.edible = True
    item.cost = consumables_costs[type]
    item.description = consumables_descriptions[type]
    item.bonus = consumables_bonus[type]
    return item

def generate_wearable_items(nationality):
    type = random.choice(armour_types)
    condition = random.choice(armour_condition)
    armour = adv.Item(nationality+" "+condition+" "+type, type)
    armour.wearable = True
    armour.cost = round(armour_cost[type]/armour_condition_penalty[condition]) - round(random.randint(0,20)/armour_condition_penalty[condition])
    armour.bonus = armour_bonus[type]
    armour.description = "A "+condition+" "+type+", made by "+nationality+" armourers. "+armour_description[type]
    return armour

def darkness_progress(karma):
    if karma >=10:
        return "The rot starts expanding towards your forearm."
    elif karma >=25:
        return "You feel that the darkness consumes you bit by bit, as the rot reaches your elbow"
    elif karma >=40:
        return "The black rot keeps growing, and it reaches your shoulders"
    elif karma >=55:
        return "Visions start popping in your head, visions of the Dark Lodge the sorcerer told you about. Darkness has consumed you."
    else:
        return "The rot seems to expand from your fingertips, and cover your palm."

#Spells
avail_spells = ["healing spell", "domain expansion"]
spells = [{"name":"fireball", "type":"attack", "damage":15, "bonus": 0, "description": "You take the Eye of Nidafelyr from your inventory and hold it tightly.\nYou whisper the enchanted words, and a powerful fireball is unleashed from this magic orb."}, 
          {"name":"healing spell", "type":"healing", "damage":0, "bonus": 10, "description": "You reach for the Healer's Scepter from your inventory.\nYou gently tap the Scepter to the ground and all your wounds instantly heal."},
          {"name": "domain expansion", "type":"attack", "damage":200, "bonus":0, "description": "You cross your fingers of your right hand and you whisper the enchanted words to cast the domain expansion. Everyone here is trapped inside the magic barrier, which instantly kills them."}]

# Consumable items
apple = adv.Item("small red apple", "apple")
apple.color = "red"
apple.description = "a small ripe red apple"
apple.edible = True
apple.wearable = False
apple.cost = 5
apple.bonus = 5

stew=adv.Item("A stew with carrots, potatoes, lamb and bass", "stew")
stew.description = "stew made of carrots, potatoes, lamb and bass, from the Red Cardinal Inn"
stew.edible=True
stew.wearable=False
stew.cost = 7


#Wearable items
cloak = adv.Item("wool cloak", "cloak")
cloak.color = "grey tweed"
cloak.description = (
    "a grey tweed cloak, heavy enough to keep the wind and rain at bay"
)
cloak.edible = False
cloak.wearable = True
cloak.cost = 25
cloak.weight = 2
cloak.bonus = 1

#weapons
gungnir_spear=adv.Item("Gungnir", "golden spear", 'spear')
gungnir_spear.color="gold"
gungnir_spear.description = (
    """A legendary spear. The shaft and the head are made of gold, it must have belonged to someone important."""
)
gungnir_spear.edible = False
gungnir_spear.wearable = False
gungnir_spear.damage = 15
gungnir_spear.bonus = 0
gungnir_spear.cost = 200
gungnir_spear.weight = 6

crossbow = adv.Item("crossbow")
crossbow.color = "wooden"
crossbow.description = ("a mechanically assisted bow, suitable for ranged combat.")
crossbow.edible = False
crossbow.wearable = False
crossbow.damage = 10
crossbow.bonus = 0
crossbow.cost = 150
crossbow.weight = 0

steel_sword = adv.Item("steel sword", "sword")
steel_sword.color = "steely grey"
steel_sword.description = (
    "a finely made steel sword, honed to a razor edge."
)
steel_sword.edible = False
steel_sword.wearable = False
steel_sword.damage = 8
steel_sword.bonus = 0
steel_sword.cost = 75
steel_sword.weight = 5

#currency
golden_floren=adv.Item("golfen floren", "floren")
golden_floren.color="golden"
golden_floren.description=(
    """a golden floren, the currency in the Nordaernland"""
)
golden_floren.edible=False
golden_floren.wearable=False

#main mission diary
diary = adv.Item("diary", "sorcerer's diary", "mage's diary")
diary.color = "leather"
diary.description = """an old diary that contains spells. The first page has the signature of Nesin Nauthuy, with the seal of the Grandmaster of the Citadel of Mages."""
diary.edible = False
diary.wearable = False

#instructions for final mission
instructions = adv.Item("scroll with possible hideouts", "scroll", "piece of paper")
instructions.color = "paper"
instructions.description = """a scroll that was given to you by Nesin. The following are the possible hideouts of Mulfeilf:
The Nhudelhid camp
The dungeon south of Vestenvarth
The ancient ruins of Maul"""
instructions.edible = False
instructions.wearable = False

#a scroll in Old Elven tongue
scroll = adv.Item("scroll in an ancient language", "scroll")
scroll.color = "paper"
scroll.description = """a scroll from the bookcase of Mulfeilf's dungeon. You cannot make out what those words mean:
Aulubi aulaulmen posseth ala musau foaya ab nabeis. 
Mafau gisalali pauth ay Aulbas pes duth. 
Num yerulf demaulf Keira yaussom"""

#torn page of an old book in Maul catacombs
page = adv.Item("torn page", "page", "old page")
page.description = """a torn page from the catacombs' secret room. The words written seem like enchanted words of a spell,
'May darkness consume whomever wishes harm to the Enlightened One'
This looks like the full spell from the scrolls you found at Mulfeilf's tower south of Hawara,
it could be the spell that grew the rot on your hand."""

equipped_weapon = steel_sword
equipped_armour = cloak


