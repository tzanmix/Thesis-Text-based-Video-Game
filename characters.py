# Import the adventurelib library
import adventurelib as adv
import game_items
import random
import generate_npc
import mission_generator

# All characters have some properties
adv.Item.greeting = ""
adv.Item.context = ""


#all_monster_types = ["giant", "draugr", "wight", "werewolf", "griffin", "basilisk", "dragon", "vampire"]
all_monster_types = ["draugr", "werewolf", "griffin", "vampire", "wraith"]
#all_monster_types = ["vampire"]
nationalities=["Norse","Alnaasi","Nhudelhid","Elf","Daoine"]
genders=["male","female"]
#proffessions=["innkeep","soldier","bandit","merchant","duke","count","king","spy","blacksmith","sorcerer","traveler"]
proffessions = ["innkeeper", "soldier", "merchant", "blacksmith", "traveller", "farmer"]
draugr_knowledge = False
werewolf_knowledge = False
griffin_knowldge = False
vampire_knowledge = False
wraith_knowledge = False
monster_knowledge = {"draugr": False, "werewolf": False, "wraith": False, "vampire": False, "griffin": False}
#add journal entries
bestiary_entries = {
    "draugr": "The draugr or 'Dreygur' as the Norse call it, is an undead creature, a Norse soldier that was cursed into this form centuries ago. The draugr are fast and strong monsters, but can be defeated with all conventional arms.",
    "vampire": "The vampires of these lands are not what someone would expect. These are not humanoids, they have bat-like traits, larger and more monstrous than regular bats. They cannot disguise themselves as humans, despite what the legends say, but they are still one of the most dangerous species on the world. They have an insatiable lust for blood, they are almost invincible to most conventional weapons. They can be killed by silver or gold weapons.",
    "werewolf": "The werewolves are cursed humans that transform into wolf-like creatures. When in form of the wolf, they lose every sense of humanity in them and have an unsaturated hunger. They consume every possible meat, including human. They are very fast creatures, capable of piercing the strongest armour with their claws in a single blow. They are vulnerable to only silver or gold weapons",
    "griffin": "The largest flying predator in the world, the griffin or the 'gryphon' is a half lion half eagle creature that wreaks havoc in these lands. It has the head and the wings of an eagle, the body of a very large lion. It is known to eat its prey alive, piece by piece. It can be defeated with the use of ranged combat weapons, such as a crossbow, as the griffin will not fight on land when it feels threatened.",
    "wraith": "The wraith is a soul of a human that never rested in peace after death. It has no memories of its past life, so it is strictly guided by its hartred towards the living. It is visible to humans, but is immaterial, so no weapon can work against them, making them an impossible opponent against mortals. They can be defeated only with the use of spells."}



class NonPlayableCharacter(adv.Item):
    patience=0
    attack_dmg=5
    type = "human"
    kin_killed = False
    is_alive = True
    previously_met = False
    favour_failed = False
    mission_accepted = False
    mission_refused = False
    favour_completed = False
    intelligence = 0
    x = -2
    y = -2
    journal_entry = False


class MonsterEnm(adv.Item):
    attack_dmg=10
    hit_points = 20
    type = "monster"
    gen_pronouns = "its"
    subj_pronouns = "it"
    obj_pronouns = "it"
    proffession = "monster"
    is_alive = True
    kin_killed = False
    x = -2
    y = -2

def generate_npc_attributes(npc, gender):
    npc.is_alive = True
    npc.hit_points = 20
    if npc.proffession == "bandit":
        npc.aggression = 15
    else:
        npc.aggression = 5
    npc.previously_met = False
    if gender == "male":
        npc.gender = 1
        npc.subj_pronouns = "he"
        npc.gen_pronouns = "his"
        npc.obj_pronouns = "him"
    else:
        npc.gender = 0
        npc.subj_pronouns = "she"
        npc.gen_pronouns = "her"
        npc.obj_pronouns = "her"
    npc.description = generate_npc.generate_description(npc.proffession, npc.nationality, npc.gender, npc.obj_pronouns, npc.subj_pronouns, npc.gen_pronouns, npc.age, npc.aggression)


def generate_npc_inventory(proffession):
    inventory = []
    type = ["sword", "spear", "dagger", "shield", "warhammer", "axe"]
    condition = ["old", "brand new", "used", "rusty"]
    num_of_items = random.randint(5,15)
    if proffession == "blacksmith":
        for i in range(num_of_items):
            inventory.append(game_items.generate_weapon(random.choice(type), random.choice(condition)))
        for j in range(3):
            inventory.append(game_items.generate_wearable_items("Norse"))
    elif proffession == "innkeep":
        for i in range(num_of_items):
            inventory.append(game_items.generate_consumable_items())
    elif proffession == "merchant":
        for i in range(round(num_of_items/2)):
            inventory.append(game_items.generate_weapon(random.choice(type), random.choice(condition)))
            inventory.append(game_items.generate_consumable_items())
    else:
        for i in range(round(num_of_items/4)):
            inventory.append(game_items.generate_weapon(random.choice(type), random.choice(condition)))
            inventory.append(game_items.generate_consumable_items())
    #NA GRAFTEI INVENTORY GIA TERATA, BANDITS KAI GUARDS
    return inventory

def create_random_NPC(nationality, proffession):
    if nationality == "":
        nationality = random.choice(nationalities)
    if proffession == "":
        proffession = random.choice(proffessions)
    gender = random.choice([0,1])
    name = generate_npc.name_based_on_gender(nationality, gender)
    family_name = generate_npc.findFamilyName(nationality, gender)
    new_npc = NonPlayableCharacter(name+" "+family_name, name, proffession)
    new_npc.context = new_npc.name
    new_npc.age = random.randint(18,85)
    new_npc.title = generate_npc.findTitle(nationality, proffession)
    new_npc.gender = gender
    new_npc.family_name = family_name
    new_npc.proffession = proffession
    new_npc.aggression = random.randint(0,10)
    new_npc.previously_met = False
    new_npc.is_alive = True
    if gender == 1:
        new_npc.subj_pronouns = "he"
        new_npc.gen_pronouns = "his"
        new_npc.obj_pronouns = "him"
    else:
        new_npc.subj_pronouns = "she"
        new_npc.gen_pronouns = "her"
        new_npc.obj_pronouns = "her"
    new_npc.hit_points=20
    new_npc.description = generate_npc.generate_description(proffession, nationality, gender, new_npc.obj_pronouns, new_npc.subj_pronouns, new_npc.gen_pronouns, new_npc.age, new_npc.aggression)
    inventory = generate_npc_inventory(new_npc.proffession)
    new_npc.items = adv.Bag(inventory)
    #new_npc.items=adv.Bag([game_items.apple, game_items.golden_floren])
    new_npc.floren_balance = random.randint(5,250)
    new_npc.nationality = nationality
    # objective = mission_generator.generate_objective("Start")
    # new_npc.favour = objective.split(",")
    # new_npc.favour_completed = False
    new_npc.intelligence = random.randint(5, 20)
    #list_of_characters.append(new_npc)
    return new_npc

npc = create_random_NPC("","")
print("TEST TEST: ",npc.name)

#generate non playable characters that are objectives to side quests
def generate_objective_npc(type, quest_giver):
    obj_proffession = random.choice(generate_npc.proffessions)
    if type == "brother":
        obj_name = generate_npc.name_based_on_gender(quest_giver.nationality, 1)
        objective = NonPlayableCharacter(obj_name+' '+quest_giver.family_name, obj_name, obj_proffession)
        objective.proffession = obj_proffession
        objective.nationality = quest_giver.nationality
        objective.age = random.randint(quest_giver.age-2, quest_giver.age+7)
        generate_npc_attributes(objective, "male")
    elif type == "sister":
        obj_name = generate_npc.name_based_on_gender(quest_giver.nationality, 0)
        objective = NonPlayableCharacter(obj_name+' '+quest_giver.family_name, obj_name, obj_proffession)
        objective.proffession = obj_proffession
        objective.nationality = quest_giver.nationality
        objective.age = random.randint(quest_giver.age-2, quest_giver.age+7)
        generate_npc_attributes(objective, "female")
    elif type == "father":
        obj_name = generate_npc.name_based_on_gender(quest_giver.nationality, 1)
        objective = NonPlayableCharacter(obj_name+' '+quest_giver.family_name, obj_name, obj_proffession)
        objective.proffession = obj_proffession
        objective.nationality = quest_giver.nationality
        objective.age = random.randint(quest_giver.age+17, quest_giver.age+37)
        generate_npc_attributes(objective, "male")
    elif type == "elder":
        obj_name = generate_npc.name_based_on_gender(quest_giver.nationality, 1)
        obj_family_name = generate_npc.findFamilyName(quest_giver.nationality, 1)
        objective = NonPlayableCharacter(obj_name+' '+obj_family_name, obj_name, "elder", "eolderman")
        objective.proffession = "town elder"
        objective.nationality = quest_giver.nationality
        objective.age = random.randint(65,99)
        generate_npc_attributes(objective, "male")
    objective.type = type
    return objective

#generate enemy bandits
def generate_enemy_npc():
    nationality = random.choice(generate_npc.nationalities)
    enemy_name = generate_npc.name_based_on_gender(nationality, 1)
    enemy_family_name = generate_npc.findFamilyName(nationality, 1)
    enemy = NonPlayableCharacter(enemy_name+' '+enemy_family_name, enemy_name, "bandit", "criminal")
    enemy.proffession = "bandit"
    enemy.nationality = nationality
    enemy.favour = False
    enemy.age = random.randint(20,50)
    enemy.intelligence = random.randint(5,20)
    generate_npc_attributes(enemy, "male")
    enemy.items = generate_npc_inventory("bandit")
    enemy.floren_balance = random.randint(15,75)
    return enemy

def generate_monster_description(type):
    if type == "vampire":
        return random.choice(["There is the blood-thirsty vampire.\nIt used to be a man, but now a monstrous bat-like creature with long claws stands before you.\nIt decorates its grey fur with shiny jewels from its victims and its shriek pierces your ears.",
                              "You take a look at this beast and you see no human characteristic left in this large monster.\nAt 7 feet tall, this bat-like creature of the night likes to drain the blood from its victims rather than shredding them apart.\nIts large claws and bat-like form give you the chills."])
    elif type == "draugr":
        return "An undead draugr stands before you. A corpse of a Northerner soldier, with its skin rotting, sunken eyes, rusty armour, broken shield.\nA very dangerous monster, fast and strong, despite its grotesque and weak appearance."
    elif type == "wraith":
        return "You see an ethereal transluscent figure, a human form, wrapped with rags.\nThis is a wraith, a deceased human that was wronged before death, a creature that suffers immeasurable pain, and carries immense hatred towards the living."
    elif type == "griffin":
        return "A massive creature flies above your head. The head and wings of an eagle, and the body of a lion indicate that this is a griffin, a formidable combination of leonine power and avian grace."
    elif type == "werewolf":
        return "A monstrous werewolf emerges from the shadows, its fur bristling with feral intensity. Its eyes ablaze with an annatural hunger, its snarl is bloodcurling, its fangs sharp."

def add_monster_trophy(type):
    pass

def generate_monster(type):
    monster_type = type
    monster = MonsterEnm(monster_type)
    monster.description = generate_monster_description(monster_type)
    monster.context = monster_type
    monster.is_alive = True
    #monster.items = adv.Bag(add_monster_trophy(monster_type))
    monster.aggression = 20
    monster.items = generate_npc_inventory("monster")
    return monster



def create_guard_npc():
    enemy_name = generate_npc.name_based_on_gender("Norse", 1)
    enemy_family_name = generate_npc.findFamilyName("Norse", 1)
    enemy = NonPlayableCharacter(enemy_name+' '+enemy_family_name, enemy_name, "guard", "city guard")
    enemy.proffession = "guard"
    enemy.nationality = "Norse"
    enemy.age = random.randint(20,50)
    enemy.description = random.choice([f"""A city guard arrives, he is a large Northerner with a thick black beard, 
                                       wearing plate armour made of the finest steel, covered in a dark red cloak\n
                                       {enemy.name}>> Stay where you are criminal! You are under arrest.""",
                                       f"""A medium built Northerner with a steel plate armour, and a dark red cloak arrives.
                                       He is a member of the city guard.
                                       {enemy.name}>> Surrender criminal, or die by my spear."""])
    generate_npc_attributes(enemy, "male")
    enemy.items = generate_npc_inventory("guard")
    enemy.floren_balance = random.randint(35,55)
    return enemy

eolderman = NonPlayableCharacter("Sygtrygrr Sigurdson", "elder", "eolderman")
eolderman.description = """The eolderman, Sygtrygrr Sigurdson, a tall distinguished member
of the community. His steely grey hair and stiff beard inspire confidence."""
eolderman.greeting = (
    "Greetings traveler. Our village has a problem, you seem like one capable with a sword, can you help us?"
)
eolderman.context = "elder"
eolderman.proffession = "village elder"
eolderman.aggression=0
eolderman.is_alive=True
eolderman.subj_pronouns="he"
eolderman.gen_pronouns="his"
eolderman.obj_pronouns="him"
eolderman.hit_points=20
eolderman.items=adv.Bag([game_items.apple, game_items.golden_floren])


innkeep = NonPlayableCharacter("Uhtred Ivarson", "Uhtred", "tavern owner", "innkeep")
innkeep.description = """Uhtred the inkeep greets you, a bald, short well-built man, 
    with a thick black beard."""
innkeep.greeting = (
    "Welcome to the Red Cardinal, we have ale, wine, and i can make some stew. Would you like to take a look at what we offer?"
)
innkeep.context = "innkeep"
innkeep.proffession = "innkeep"
innkeep.aggression=0
innkeep.is_alive=True
innkeep.subj_pronouns="he"
innkeep.gen_pronouns="his"
innkeep.obj_pronouns="him"
innkeep.hit_points=20
innkeep.items=adv.Bag([game_items.apple, game_items.golden_floren])

draugr = MonsterEnm("Draugr soldier", "draugr")
draugr.description = """You thought it was a dead body of a soldier rotting, but it
    rises and looks directly into your eyes. It's a draugr, an undead soldier with rusty armor and
    a silver sword"""
draugr.greeting=(
    "AAAAUUUUUURGH"
)
draugr.context="draugr"
draugr.proffession="undead soldier"
draugr.hit_points=20
draugr.aggression=20
draugr.is_alive=True
draugr.subj_pronouns="he"
draugr.gen_pronouns="his"
draugr.obj_pronouns="him"
draugr.items=adv.Bag([game_items.apple, game_items.golden_floren])


captain = NonPlayableCharacter("Sigurd Thorfinnson", "Captain Sigurd Thorfinnson", "captain", "Sigurd")
captain.description = """A tall northerner with a thick black beard stands beside the docks where a longship is stationed. He is wearing a tunic, covered in wolf fur, and has an axe and a sword hanging from his belt. He introduces himself to you as the captain of Freya's Grace.\n"""
captain.greeting = "Greetings, traveller, are you here to rent a cabin on my ship?"
captain.proffession = "captain"
captain.context = "captain"
captain.favour = []
captain.previously_met = False
captain.is_alive = True
captain.favour_completed = False
captain.aggression = 7
captain.subj_pronouns = "he"
captain.gen_pronouns = "his"
captain.obj_pronouns = "him"
captain.items = adv.Bag([game_items.cloak])
captain.floren_balance = 180
captain.x = 14
captain.y = 24


audafir = NonPlayableCharacter("Audafir Nemburul", "Audafir", "Elven sorcerer", "sorcerer")
audafir.description = "An enormous tower emerges out of nowhere, this might be the place where the sorcerer lives. You enter through the wooden gates, carved with ancient runes, and the host comes to welcome you. The sorcerer is an old man with a long beard and long white hair that cover his pointy ears. He wears a blue robe with depictions of dragons knitted in gold threads.\n" 
audafir.proffession = "sorcerer"
audafir.context = "audafir"
audafir.aggression = 0
audafir.items = adv.Bag([game_items.cloak])
audafir.floren_balance = 10
audafir.favour = []
audafir.intelligence = 20
audafir.journal_entry = """A sorcerer you encountered in some hills in Western Nordreyjar, the old elven mage offered his hospitality in the House of the Undying and answered your questions about the strange markings and the black sludge on your hand. Once you stepped out of his tower, it completely disappeared.\n"""
audafir.x = 6
audafir.y = 43

spy = NonPlayableCharacter("Ygritte Fenn", "Ygritte", "spy", "detective")
spy.description = """The Daoine elderly lady lifts her head and greets you without standing up. The red haired woman with the round glasses introduces herself as Ygritte Fenn, the detective that owns this agency.\n"""
spy.context = "spy"
spy.proffession = "spy"
spy.aggression = 0
spy.floren_balance = 100
spy.items = adv.Bag([game_items.cloak])
spy.favour = []
spy.intelligence = 20
spy.journal_entry = """The red haired old lady you encountered in Cathairbhaile was the head of a detective agency, and she had some of the information you needed. You reluctantly paid for her services and she revealed to you the possible location of the sorcerer you were looking for.\n"""
spy.x = 21
spy.y = 18

alnaasi_captain = NonPlayableCharacter("Rami Yemau", "Rami", "captain")
alnaasi_captain.description = """A short man with a thick black beard shouts orders to some sailors. The well dressed Alnaasi introduces himself as the captain of the Unskinkable.\n"""
alnaasi_captain.context = "captain"
alnaasi_captain.proffession = "captain"
alnaasi_captain.aggression = 0
alnaasi_captain.floren_balance = 100
alnaasi_captain.items = adv.Bag([game_items.cloak])
alnaasi_captain.favour = []
alnaasi_captain.intelligence = 15
alnaasi_captain.x = 47
alnaasi_captain.y = 12

grandmaster = NonPlayableCharacter("Nesin Nauthuy", "grandmaster", "sorcerer", "sage")
grandmaster.description = """The grandmaster of the school greets you like you know each other. He is a middle aged man - although he might be way older than he looks - of a slender and tall frame, draped in a golden robe, with a hood decorated by knitted runes to conceal his bald head.\n"""
grandmaster.context = "grandmaster"
grandmaster.proffession = "sorcerer"
grandmaster.aggression = 0
grandmaster.floren_balance = 100
grandmaster.items = adv.Bag([game_items.cloak])
grandmaster.favour = []
grandmaster.intelligence = 20
grandmaster.journal_entry = "Your search for the cure lead you to the grandmaster of the Citadel, Nesin Nauthuy. Apparently, he hired you to hunt down and kill a former apprentice of him, Mulfeilf Deim, who started practicing the Dark Arts. With a list of Mulfeilf's possible lairs, you could resume your search.\n"
grandmaster.x = 40
grandmaster.y = 29

mulfeilf = NonPlayableCharacter("Mulfeilf Deim", "sorcerer", "rogue mage", "rogue sorcerer")
mulfeilf.description = """The man you've been looking for finally stands in front of you. His long red fiery hair cover his pointy ears, a leather patch covers his right eye, he removes his golden cloak and his chainmail made from magical gems unveils.\n"""
mulfeilf.context = "mulfeilf"
mulfeilf.proffession = "sorcerer"
mulfeilf.aggression = 0
mulfeilf.floren_balance = 100
mulfeilf.items = adv.Bag([game_items.cloak])
mulfeilf.favour = []
mulfeilf.intelligence = 20
mulfeilf.x = -3
mulfeilf.y = -3


main_mission_characters = [audafir, captain, spy, grandmaster, mulfeilf]