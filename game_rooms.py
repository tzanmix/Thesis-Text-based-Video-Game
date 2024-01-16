#Game rooms for demo

import adventurelib as adv
import characters
import game_items
import json
import random
import csv
import mission_generator
import generate_npc
import room_creator

adv.Room.add_direction("enter", "leave")
adv.Room.add_direction("northeast", "southwest")
adv.Room.add_direction("southeast", "northwest")

active_missions = []


#superclass of game area, a grater region with game rooms
class Region(adv.Room):
    def __init__(self, description: str):
        super().__init__(description)
        self.short_desc = ""
        self.description = description
        self.title = ""

# Create a subclass of Rooms to track some custom properties
class GameArea(Region):
    def __init__(self, super_area_title, description: str):
        self.super_area_title=super_area_title
        super().__init__(description)

        # All areas can have locked exits
        self.locked_exits = {
            "north": False,
            "south": False,
            "east": False,
            "west": False,
            "northeast": False,
            "northwest": False,
            "southeast": False,
            "southwest": False
        }
        # All areas can have items in them
        self.items = adv.Bag()

        # All areas can have characters in them
        self.characters = adv.Bag()

        # All areas can have rooms or sub-areas inside them
        # self.rooms = adv.Bag()

        # All areas may have been visited already
        # If so, you can print a shorter description
        self.visited = False

        # Which means each area needs a shorter description
        #self.short_desc = ""

        # Each area also has a very short title for the prompt
        #self.title = ""


locations_journal_entries = {
    "Nordvik": "The former capital of the island-kingdom of Nordreyjar, lard of the fierce Norse people. Since the formation of the Empire this city is in decline, but it still remains an important port for the country. It is located at the southernmost point of the island of Nordreyjar, a cold and mountainous region in the north of the continent.",
    "Vestenvarth": "One of the first colonies of the Norse people away from Nordreyjar, now houses the seat of the Jarl, the highest position for the Norse, a position appointed by the Emperor himself nowadays. It is located at the northernmost point of Juun, a fertile land which the Norse tried to make the most of it before they were annexed by the Empire.",
    "Cathairbhaile": "A large city that used to be the capital of the Daoine people, but now is the most important port of the Empire. The metropolis in northern Juun has become a multicultural center of trade and commerce, as well as a strategic position for hosting half the Imperial Fleet.",
    "Hawara": "Former capital of Al'Naas, Hawara is a metropolis in the biggest desert in the world. Despite its disadvantages due to the infertility of the lands, the city has always been growing in wealth and power, due to the various goods the Alnaasi have been exporting from its port.",
    "Capital": "The newest large city in the known world, it was built in the most unapproachable rocky island of the south to be the most secure seat for the Emperor. The Imperial Fleet patrols around the island have not discouraged the commerce in this city, which is the wealthiest in these lands.",
    "Army of the Naumeir Khanate": "A military camp of the nomadic Nhudelhid people from the east. Their actual intentions are unknown.",
    "Ancient Maul": "The ruins of an ancient Elven city. Not much is known about it.",
    "Aulba": "A small Elven village in the island of Aulba, not much is of worth here."
}

inn_names_start = ["The Jousting", "The Enchanted", "The Royal", "The Lively", "The Red", "The Crimson", "The Black", "The Silent", "The Sable"]
inn_names_fin = ["Cardinal", "Dragon", "Knight", "Bard", "Jug", "Stallion", "Stag", "Tankard", "Flagon"]
def generate_inn_title():
    return random.choice(inn_names_start)+" "+random.choice(inn_names_fin)+" "+random.choice(["Inn", "Tavern"])

def generate_cave_description():
    descr_intro = random.choice(["As you step into the cave, the damp air envelops you, ", 
                                 "The cave widens into a vast cavern, and a gentle breeze carries the distant murmur of subterranean rivers, ", 
                                 "Within this cavern, translucent crystals jut from the walls, casting prismatic reflections across the rocky floor, ",
                                 "The cave twists and turns, revealing a labyrinth of winding passages, ",
                                 "The cavern floor is littered with ember-like stones that emit a warm, comforting glow, "])
    descr_mid = random.choice(["and the walls glisten with a carpet of luminous moss. ", 
                               "stalagmites rise like silent sentinels, and the air is thick with the scent of damp earth and the echoes of unseen depths. ",
                               "the air is dry and carries a faint scent of minerals. ",
                               "the walls seem to weep with iron-rich droplets, creating an eerie yet captivating ambiance. "])
    descr_end = random.choice(["The soft glow casts eerie shadows, revealing a subterranean world where stalactites hang like crystalline chandeliers.",
                               "The cave's walls are adorned with ancient petroglyphs, hinting at the untold stories of those who came before.",
                               "The ground is dusted with frost, and the air bites with the cold, painting the cave in an otherworldly frosty palette.",
                               "The air is cool and crisp, and the occasional drip of mineral-laden water echoes in the silence, creating an otherworldly atmosphere."])
    return descr_intro+descr_mid+descr_end

def generate_dungeon_description():
    pass

def generate_ruins_description():
    descr_intro = random.choice(["The ancient elven ruins exude an ethereal glow, with crumbling spires that seem to channel the fading magic of a bygone era. ",
                                 "High amidst the treetops, these elven ruins stand as a testament to the elves' harmonious coexistence with nature. ",
                                 "In the heart of the ancient elven city lies a celestial nexus, its central fountain once flowing with the purest magic. ",
                                 "Nestled within the embrace of a colossal, ancient tree, the elven ruins weave seamlessly into the natural splendor. "])
    descr_mid = random.choice(["The halls echo with the footsteps of a long-gone elven civilization, and the walls are etched with images of beings ethereal and majestic, capturing the essence of their timeless existence. ",
                               "The remnants of ancient manuscripts and enchanted tomes lay scattered, revealing the intellectual pursuits that once flourished within these hallowed elven walls. ",
                               "Vines and moss intertwine with delicate elven script, telling tales of forgotten enchantments that once graced this sacred sanctum. "])
    descr_end = random.choice(["Elaborate murals on the walls depict scenes of celestial battles, while the air resonates with the haunting echoes of a forgotten elven hymn.",
                               "The murals depict the Eldertree Nexus, its roots entwined with elven glyphs, that emanates an aura of wisdom and tranquility that once connected the elves with the heart of the forest.",
                               "The remnants of telescopes and star maps hint at the elves' profound connection to the cosmos."])
    return descr_intro+descr_mid+descr_end

def generate_inn_description():
    descr_intro = random.choice(["A warm and bustling inn with wooden beams overhead, patrons clinking tankards together. ",
                                 "A cozy tavern with a large stone hearth at its center. ",
                                 "The clatter of tankards and the murmur of conversation fill this lively inn. ",
                                 "A favorite haunt for knights and adventurers, this tavern boasts suits of armor standing guard by the entrance. "])
    descr_mid = random.choice(["Wooden beams support a thatched roof, and the air is perfumed with the scent of pine. ",
                               "Soft candlelight illuminates the dark wood interior, and the gentle melody of a harp accompanies hushed conversations. ",
                               "Wooden benches surround sturdy tables, and the hearth crackles with the warmth of a well-tended fire. ",
                               "Worn tapestries depicting epic battles adorn the walls, and the air is thick with the aroma of spiced ales and savory pies. "])
    descr_end = random.choice(["The scent of hearty stews and roasted meats fills the air as a crackling fireplace casts a flickering glow across the room.",
                               "A mix of laughter and music creates an atmosphere of lively camaraderie.",
                               "The bar is adorned with silver tankards, and patrons indulge in fine wines and delicacies fit for kings.",
                               "The air carries a hint of enchantment, making it a haven for those seeking the extraordinary."])
    return descr_intro+descr_mid+descr_end

def create_caves(super_area_title):
    cave = GameArea("Cave in "+super_area_title, generate_cave_description())
    cave.title = "cave"
    return cave

def create_dungeon(super_area_title):
    dungeon = GameArea("Dungeon in "+super_area_title, generate_dungeon_description())
    dungeon.title = "dungeon"
    return dungeon

def create_elven_ruins(super_area_title):
    ruins = GameArea("Ancient Elven ruins in "+super_area_title, generate_ruins_description())
    ruins.title = "Elven ruins"
    return ruins

def create_inns(super_area_title):
    inn_title = generate_inn_title()
    inn = GameArea(inn_title + " in "+super_area_title, generate_inn_description())
    inn.title = inn_title
    return inn

test_area = Region("""Welcome to test area""")
test_area.title="Demo area"
test_area.short_desc="An area for testing"
test_area.description="test area"
test_area.type="village"

forest_main_road=GameArea("test area","""You are at the public road of the Nidafellyr Forest,
    birds are chirping, the wind is howling, which doesn't really make
    much sense, since the birds would not be chirping if the weather in this
    forest was this bad.""")
forest_main_road.title="Main road of Nidafellyr Forest"
forest_main_road.short_desc="You arrive at the area of Nordlings"



small_village = GameArea("test area",
    """
    This is a Nordling village. All the houses are made
    of cobblestone. Everyone is locked inside their houses, which
    is weird, considering what you've heard of the Nordlings.
    I wonder why...
    
    You distinguish one slighlty larger structure on the south, must be the
    tavern
    
    As you approach, you here an elderly and weak voice on your north
    """)
small_village.title = "Nordling village"
small_village.short_desc = "A small village you encounter on your way"


eolderman_house = GameArea("test area","""This is the house from which the voice originates.
    You see an elder gentleman wearing a brown worn robe sitting
    on a bench, beside the house's wooden door""")
eolderman_house.title = "Eorlderman's house"
eolderman_house.short_desc = "The house of the eolderman of this village, curious, it looks exactly like every other house here"


tavern=GameArea("test area",
    """
    Welcome to the tavern of the village. No one is here, except
    the inkeeper. The oven doesn't scorch, the inkeeper's apron is clean,
    he has not cooked for today.
    """)
tavern.title = ("The Red Cardinal Innkeep")
tavern.short_desc = "You arrive at the tavern of the village."


fork = GameArea("test area",
    """
    As you leave the village, you think about how unprepared you
    really are. Your lack of experience and pitiful equipment
    are certainly no match for whatever has been stealing
    the villages livestock.

    As you travel, you come across a fork in the path. The path of
    the livestock thief continues east. However, you know
    the village of Dunhaven lies to the west, where you may
    get some additional help.
    """)
fork.title = "Fork in road"
fork.short_desc = "You are at a fork in the road."


abandoned_hamlet = GameArea("test area",
    """
    Another Nordling village. This one is completely abandoned. No signs
    of fighting, no broken down doors, or burnt down houses. Just an empty
    village. Perhaps the villages of the previous one on your road would
    know what happened and they are hiding now""")
abandoned_hamlet.title = "An abandoned village"
abandoned_hamlet.short_desc = "The village you heard about, completely abandoned, but you see some footprints going east, through the forest."

cave=GameArea("Cave", """As you step into the cave, the damp air envelops you, and the walls glisten with a carpet of luminous moss. 
              The soft glow casts eerie shadows, revealing a subterranean world where stalactites hang like crystalline chandeliers."""
)
cave.title="cave"
cave.short_desc="You see a dead soldier inside the cave."

witch_hut=GameArea("test area",
    """
    A wooden hut, in the middle of nowhere.
    """
)
witch_hut.title="Witch's hut"
witch_hut.short_desc="You spot a small wooden hut."

forest_main_road.east=small_village
small_village.north=eolderman_house
small_village.south=tavern
small_village.east=fork
fork.north=abandoned_hamlet
abandoned_hamlet.east=cave

rooms = [forest_main_road, small_village, fork, abandoned_hamlet, cave]

with open('assets/characters.json', 'r') as json_file:
    characters_list = json.load(json_file)




# home.items.add(adventurelib_game_items.apple)
fork.items.add(game_items.cloak)
# cave_mouth.items.add(adventurelib_game_items.slug)

eolderman_house.characters.add(characters.eolderman)
tavern.characters.add(characters.innkeep)
#cave.characters.add(characters.draugr)
cave.characters.add(characters.generate_monster(random.choice(["vampire","wraith","draugr"])))
# small_village.characters.add(new_npc)
fork.enter=witch_hut
#abandoned_hamlet.characters.add(characters.draugr)
# giant_cave.characters.add(adventurelib_game_characters.giant)

game_rooms = {}

with open('assets/game_rooms.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        game_rooms[row['key']] = eval(row['value'])


rooms_obj = []
for i in range(50):
    row = []
    for j in range(50):
        dict_room = game_rooms[f'({i}, {j})']
        new_room = GameArea(dict_room['super area title'], dict_room['description'])
        new_room.title = dict_room['title']
        new_room.short_desc = dict_room['description']
        new_room.continent = dict_room['continent']
        new_room.type = dict_room['type']
        new_room.x = i
        new_room.y = j
        row.append(new_room)
    rooms_obj.append(row)

#add directions to all world tiles, lock the exits at the edges of the world
for i in range(50):
    for j in range(50):
        cur_room = rooms_obj[i][j]
        if j-1>=0:
            cur_room.west = rooms_obj[i][j-1]
        else:
            cur_room.locked_exits['west'] = True
        try:
            cur_room.east = rooms_obj[i][j+1]
        except IndexError:
            cur_room.locked_exits['east'] = True
        if i-1>=0:
            cur_room.north = rooms_obj[i-1][j]
        else:
            cur_room.locked_exits['north'] = True
        try:
            cur_room.south = rooms_obj[i+1][j]
        except IndexError:
            cur_room.locked_exits['south'] = True
        if i+1<=49 and j+1<=49:
            cur_room.southeast = rooms_obj[i+1][j+1]
        else:
            cur_room.locked_exits['southeast'] = True
        if i+1<=49 and j-1>=0:
            cur_room.southwest = rooms_obj[i+1][j-1]
        else:
            cur_room.locked_exits['southwest'] = True
        if i-1>=0 and j+1<=49:
            cur_room.northeast = rooms_obj[i-1][j+1]
        else:
            cur_room.locked_exits['northeast'] = True
        if i-1>=0 and j-1>=0:
            cur_room.northwest = rooms_obj[i-1][j-1]
        else:
            cur_room.locked_exits['northwest'] = True


#lock all the exits that get to the sea
for i in range(1,49):
    for j in range(1,49):
        cur_room = rooms_obj[i][j]
        if cur_room.type !='0':
            if cur_room.north.type == '0':
                cur_room.locked_exits['north'] = True
            if cur_room.south.type == '0':
                cur_room.locked_exits['south'] = True
            if cur_room.west.type == '0':
                cur_room.locked_exits['west'] = True
            if cur_room.east.type == '0':
                cur_room.locked_exits['east'] = True
            if cur_room.northwest.type == '0':
                cur_room.locked_exits['northwest'] = True
            if cur_room.northeast.type == '0':
                cur_room.locked_exits['northeast'] = True
            if cur_room.southwest.type == '0':
                cur_room.locked_exits['southwest'] = True
            if cur_room.southeast.type == '0':
                cur_room.locked_exits['southeast'] = True

#print(rooms_obj[4][7].locked_exits)

#creating the town/city rooms
#-------VESTENVARTH#-------
vestanvarth_suburbs_west = rooms_obj[13][7]
vestanvarth_suburbs_west.title = "West Vestanvarth suburbs"
vestanvarth_suburbs_west.description = """This is the border of a large Northerner settlement in the Continent, Vestenvarth. 
    Small cottages with thatched roofs and timber walls surround you, exactly like the ones seen in Nordreyjar."""
vestanvarth_suburbs_west.super_area_title = "Vestenvarth"

vestanvarth_port = rooms_obj[13][5]
vestanvarth_port.title = "Vestenvarth Port"
vestanvarth_port.description = """Vestenvarth is nestled along the rugged coastline, 
    flanked by imposing cliffs and rocky shores that shield it from the tempestuous Northaenvagr, the North Sea. 
    The port's strategic location allows easy access to the open ocean while providing natural protection against storms and invaders."""
vestanvarth_port.super_area_title = "Vestenvarth"

vestenvarth_fort = rooms_obj[13][6]
vestenvarth_fort.title = "The Storrborg Fort"
vestenvarth_fort.description = """The most spectacular building on the Continent, the Storrborg Fort, the heart of the Northern culture, 
    a fortress cut out of the mountain overlooking the bay and serving as home seat to the powerful clan Drummond, rulers of the Northerners. 
    According to legend, Grymmdjarr, mythical hero and founder of the kingdom of Nordreyjar, carved the fortress with his bare hands after the successful invasion of the Continent."""
vestenvarth_fort.super_area_title = "Vestenvarth"

vestenvarth_pit = rooms_obj[14][6]
vestenvarth_pit.title = "The Pit"
vestenvarth_pit.description = """A former quarry, now this is a fighting arena, carved into the rugged terrain. 
    The Northerners love the brutal contest that happens every spring here, with warriors from all over the world competing,
    hoping to gain fame and glory. At the center of the arena lies the pit itself, 
    a circular area marked by a perimeter of wooden stakes and a bed of sand mixed with gravel. 
    In the pit's center, a massive, fire-blackened oak log stands upright, its gnarled branches forming a grotesque canopy. 
    This "Yggdrasil Stump" is a symbol of the world tree, a reminder of the connection between the mortal realm and the gods."""
vestenvarth_pit.super_area_title = "Vestenvarth"

vestanvarth = [vestanvarth_port, vestanvarth_suburbs_west, vestenvarth_fort, vestenvarth_pit]

dungeon = GameArea("North Cyfandir", """Within the heart of the dungeon lies a dimly lit room with a reflective pool in the center. You stand over the pool and look to the water to see your reflection, but shadows reveal themselves in the water's surface. You can't make out exactly what these fleeting images mean. It looks like a battle, but is it from the past, or a possible future? 
\nA big bookcase is covering the northern stone wall of the dungeon. It is filled with history books and ancient scrolls in the Old Elven tongue.""")
dungeon.title = "Sorcerer's dungeon"
dungeon.x = 16
dungeon.y = 7
rooms_obj[16][7].enter = dungeon
dungeon.items.add(game_items.scroll)

#-------NORDVIK#-------
nordvik_suburbs = rooms_obj[13][24]
nordvik_suburbs.title = "West Nordvik suburbs"
nordvik_suburbs.short_desc = ""
nordvik_suburbs.description = """The suburbs of Nordvik, the capital of Nordreyjar, boast elevated settlements, 
    perched on the cliffs, overlooking the sparkling azure waters of the fjord. 
    Small cottages with thatched roofs and timber walls provide breathtaking panoramic views of the surrounding landscapes. 
    Despite the boisterous and noisy nature of the Northerners, residents here enjoy the serenity of the fjord and the soothing sounds of lapping waves."""
nordvik_suburbs.super_area_title = "Nordvik"

nordvik_port = rooms_obj[14][24]
nordvik_port.title = "Nordvik Port"
nordvik_port.description = """ The heart of Nordvik is its expansive natural harbor, framed by imposing stone piers and wooden docks. 
    Northerners' longships, sleek and ornately carved, are moored along the quays, their dragon figureheads glistening in the sunlight. 
    These ships bear the banners and shields of various clans, testament to the unity of all Northerners in this island-kingdom."""
nordvik_port.super_area_title = "Nordvik"
nordvik_port.characters.add(characters.captain)

nordvik_center = rooms_obj[13][25]
nordvik_center.title = "Nordvik market"
nordvik_center.description = """As you walk to the center of Nordvik, the rhythmic clang of hammers on anvils can be heard echoing through the market as 
    blacksmiths and armorers work diligently to craft weapons and armor,
    as well as the shouts of Northern fishermen and merchants, trying to sell their products.
    Finely made swords, shields, and intricate jewelry are displayed alongside the bustling smithies, fresh herring, salmon, trout are seen on the counters of the fishermen, 
    while the merchants haggle over exotic goods, spices from Eythiria, silk from the Far East, and old maps that lead to great treasures all over the world."""
nordvik_center.super_area_title = "Nordvik"

nordvik_suburbs_east = rooms_obj[13][26]
nordvik_suburbs_east.title = "East Nordvik suburbs"
nordvik_suburbs_east.description = """Just beyond the town's borders lie fertile meadows, where Northern families cultivate crops and tend to their livestock, a patchwork of cultivated fields and grazing pastures. 
    The thatched farmsteads blend seamlessly into the lush greenery, and hearty vegetables and herbs grow in well-tended gardens."""
nordvik_suburbs_east.super_area_title = "Nordvik"

nordvik = [nordvik_center, nordvik_port, nordvik_suburbs, nordvik_suburbs_east]

#-------NHUDELHID CAMP#-------
nomad_camp_west = rooms_obj[19][44]
nomad_camp_west.title = "Military encampment of the Nomads"
nomad_camp_west.description = """You arrive at the encampment of a grand Nomad army. 
    Hundreds of tents made of goat hide are spread in this rocky terrain, an uncomfortable place for a military encampment,
    but the Nomads from the Far East are not people that enjoy comfort. Troops are being trained, blacksmiths and armorers are practicing their craft right here."""
nomad_camp_west.super_area_title = "Army of the Naumeir Khanate"

nomad_camp_east = rooms_obj[19][45]
nomad_camp_east.title = "Khan's tent"
nomad_camp_east.description = """Here is the tent of the mighty Khan. Even though he is king of the Nomads, he enjoys few amenities.
    The royal tent is no bigger than the tents that surround it, and is guarded by no one. The Khan doesn't need protection, nor comfort."""
nomad_camp_east.super_area_title = "Army of the Naumeir Khanate"

nhudelhid_camp = [nomad_camp_east, nomad_camp_west]

#-------AULBA#-------
eythir_village_west = rooms_obj[41][14]
eythir_village_west.title = "Aulba port"
eythir_village_west.description = """A village of the Eythir, the mysterious people of the two isles in the south. 
    Aulba, hugs the shoreline, its thatched-roof cottages and timber-built structures huddled close to the water's edge. 
    The village's layout is organic, with winding cobblestone pathways that meander between homes and gardens."""
eythir_village_west.super_area_title = "Aulba"

eythir_village = rooms_obj[41][15]
eythir_village.title = "Aulba's plaza"
eythir_village.description = """A central plaza, adorned with a magnificent, centuries-old oak tree, serves as the Aulba's heart.
    Skilled Eythir fishermen, sailors and blacksmiths live here, as well as elder storetellers, who share tales from the main island of Eythiria,
    tales of monsters, treasures and ancient magical ruins."""
eythir_village.super_area_title = "Aulba"
aulba = [eythir_village, eythir_village_west]


#-------CATHAIRBHAILE#-------
cathairbhaile_wall = rooms_obj[21][17]
cathairbhaile_wall.title = "Walls of Cathairbhaile"
cathairbhaile_wall.description = """You stand before the gates of the large stone walls of the city of Cathairbhaile. 
The gate is manned by Daoine soldiers that check the identification of everyone entering or leaving the town."""
cathairbhaile_wall.super_area_title = "Cathairbhaile"

cathairbhaile_center = rooms_obj[21][18]
cathairbhaile_center.title = "Cathairbhaile Market Square"
cathairbhaile_center.description = """The heart of the town is the market square, where merchants, traders, blacksmiths and armourers have set up counters, or have their own shop around the plaza.
A prominent church is served as a focal point in this square."""
cathairbhaile_center.super_area_title = "Cathairbhaile"

cathairbhaile_port = rooms_obj[21][19]
cathairbhaile_port.title = "Cathairbhaile Port"
cathairbhaile_port.description = """The very narrow streets of Cathairbhaile lead to the port of this city. Norse longships and Elven galleys are anchored in the large docks.
Tradehouses and guildhalls line the cobbled streets of the port."""
cathairbhaile_port.super_area_title = "Cathairbhaile"

cathairbhaile_suburbs = rooms_obj[22][17]
cathairbhaile_suburbs.title = "Cathairbhaile Suburbs"
cathairbhaile_suburbs.description = """Timber buildings with overhanging upper stories are placed very closed to each other, leaving as little space for the cobbled streets as possible.
Residents of the suburbs have gathered around the well, to draw fresh water."""
cathairbhaile_suburbs.super_area_title = "Cathairbhaile"

cathairbhaile = [cathairbhaile_center, cathairbhaile_port, cathairbhaile_suburbs, cathairbhaile_wall]

detective_agency = GameArea("Cathairbhaile", """You enter the small building with the label 'Fenn Detective Agency'. The narrow interior is illuminated by the soft glow of candles, the walls are decorated by Alnaasi tapestries, and in the middle of the room, the main face of the agency sits on her desk, buried in scrolls and old books.""")
detective_agency.title = "Fenn Detective Agency"
cathairbhaile_center.enter = detective_agency
detective_agency.x = 21
detective_agency.y = 18
detective_agency.characters.add(characters.spy)

#-------HAWARA#-------
hawara_walls_west = rooms_obj[47][11]
hawara_walls_west.title = "Western Hawara Walls"
hawara_walls_west.description = """You arrive at the gate of Shifa in Hawara. The walls of the sand metropolis are heavily guarded by the Empirial Guard. Outside the walls lie an endless sea of sand, while inside the walls a vibrant city expands."""
hawara_walls_west.super_area_title = "Hawara"

hawara_walls_east = rooms_obj[47][14]
hawara_walls_east.title = "Eastern Hawara Walls"
hawara_walls_east.description = """You stand before the gate of Zun in Hawara, the eastern end of the metropolis. This gate is smaller than the western main gate, but still an impressive feat of Alnaasi architecture. Outside this gate, a tall stone monument for the fallen of the War of the Four Kingdoms stands."""
hawara_walls_east.super_area_title = "Hawara"

hawara_port = rooms_obj[47][12]
hawara_port.title = "Hawara Port"
hawara_port.description = """The gravel-covered streets of Hawara, the very short stone buildings that do not cast a shadow from the scorching hot sun makes the climate in this city unbearable, until you reach the port, where northwest wind from the sea makes the temperature a little cooler. Boats and galleys from all corners of the Empire are stationed in the docks of Hawara."""
hawara_port.super_area_title = "Hawara"
hawara_port.characters.add(characters.alnaasi_captain)

hawara_center = rooms_obj[47][13]
hawara_center.title = "Hawara Grand Bazaar"
hawara_center.description = """You walk through countless counters of merchants all over the world, that sell spices, jewelry and even weapons in the interior of the vibrant bazaar. The Grand Bazaar is the largest covered market in the world, with its walls decorated with mosaics in the Alnaasi style, depicting older Sheikhs, historic battles and the sphinx, the former coat of arms of free Al'Naas."""
hawara_center.super_area_title = "Hawara"

hawara = [hawara_center, hawara_port, hawara_walls_east, hawara_walls_west]

tower = GameArea("Kathban Albahr Desert", "The inside of the tower is a mess. Most of the bookshelves lie on the floor, filling the place with destroyed books, tomes and scrolls, the wooden workbench of the laboratory is broken in half, shattered glass flasks are everywhere. One half burnt scroll stands out, it has a depiction of a half rotten hand, like yours. You can make out the words 'May ... consume ...'")
tower.title = "Sorcerer's tower"
rooms_obj[49][12].enter = tower
tower.x = 49
tower.y = 12
#tower.items.add(game_items.diary)

citadel = rooms_obj[40][29]
citadel.title = "The Citadel"
citadel.description = """You enter the large castle at the top of the hills of the cape, the school of the sorcerers, or the Citadel as they call it. 
You hear the waves smashing the hill on which the castle is located as you enter the main hall, whose floor is made of a polished marble,
its walls are decorated in tapestries depicting dragons, legendary sorcerers and older battles."""
citadel.super_area_title = "Capital"
citadel.characters.add(characters.grandmaster)

capital_port = rooms_obj[43][30]
capital_port.title = "The Capital Port"
capital_port.description = """The port is illuminated by the soft glow of magical lanterns, galleys of the elven fleet are stationed there, crafted from enchanted wood, bearing the flag of the Empire, the Golden Tree in a teal background."""
capital_port.super_area_title = "Capital"

capital_center = rooms_obj[41][29]
capital_center.title = "The Capital Marketplace"
capital_center.description = """You pass through the vibrant marketplace, where merchants from all the known corners of the world have set up their shops. 
The countless counters and the hordes of buyers makes an almost suffocating atmosphere as you navigate through the cobbled streets of the city."""
capital_center.super_area_title = "Capital"

capital_square = rooms_obj[42][29]
capital_square.title = "The Capital Central Square"
capital_square.description = """The Godlen Tree stands proud in the middle of the Central Square. Tall, slender towers adorned with intricate carvings of leaves surround the square."""
capital_square.super_area_title = "Capital"

capital_gardens = rooms_obj[43][29]
capital_gardens.title = "The Capital Gardens"
capital_gardens.description = """At the edge of the city, the Eternal Gardens expand. Flowers of every hue and shape flourish year-round. Magical fountains, adorned with sparkling gems, release a symphony of gentle melodies that harmonize with the rustling leaves and the distant sound of cascading waterfalls."""
capital_gardens.super_area_title = "Capital"

capital = [citadel, capital_center, capital_gardens, capital_port, capital_square]
# capital_island = [[41, 26], [42, 26], [43, 25], [43, 26], [44, 26], [41, 27], [42, 27], [43, 27], [44, 27], [45, 27], [41, 28], [42, 28], [43, 28], [44, 28]
#                   [40, 29], [41, 29], [42, 29], [43, 29], [43, 30]]

maul_square = rooms_obj[36][2]
maul_square.title = "Maul's main square"
maul_square.description = """You arrive at the ruins of the Main Square of Maul, now a desolate expanse with cracked cobblestone streets and dilapidated structures. Once vibrant with elven craftsmanship, the square is now littered with fallen statues, their ethereal features worn away by the hands of time."""
maul_square.super_area_title = "Ancient City of Maul"

maul_temple = rooms_obj[37][2]
maul_temple.title = "Maul's Holy City"
maul_temple.description = """Maul's Holy City, the sacred place of worship, now lies in ruins. The Temple at the center of the district has collapsed, its roof has caved in, the broken column hint at the grandeur that once graced the holy site. As you're looking around the inside of the temple, you see an entrance to the catacombs."""
maul_temple.super_area_title = "Ancient City of Maul"

catacombs = GameArea("Ancient City of Maul", """You descend to the shadowy depth of these ancient catacombs, a network of old tunnels and crypts hidden beneath the surface. As you venture deeper into the crypt, you reach an empty room with a desk and a chair, too modern to be part of the original ancient catacombs. You see absolutely nothing of value here, except of some torn pages below the desk.""")
catacombs.title = "an entrance to the catacombs"
maul_temple.enter = catacombs
catacombs.x = 37
catacombs.y = 2
catacombs.items.add(game_items.page)

demo_locations = []
for i in range(50):
    for j in range(50):
        if i == 6 and j == 43:
            pass
        else:
            if rooms_obj[i][j].type != '0' and rooms_obj[i][j].type != '7':
                demo_locations.append(rooms_obj[i][j])


character_obj = []
list_of_characters = []
character_rooms = [rooms_obj[13][24], rooms_obj[14][24], rooms_obj[13][25], rooms_obj[13][26]]
towns = [capital, nordvik, vestanvarth, aulba, cathairbhaile, hawara, nhudelhid_camp]
list_of_main_locations = [citadel, capital_center, capital_gardens, capital_port, capital_square,
                          nordvik_center, nordvik_port, nordvik_suburbs, nordvik_suburbs_east,
                          vestanvarth_port, vestanvarth_suburbs_west, vestenvarth_fort, vestenvarth_pit,
                          eythir_village, eythir_village_west,
                          cathairbhaile_center, cathairbhaile_port, cathairbhaile_suburbs, cathairbhaile_wall,
                          hawara_center, hawara_port, hawara_walls_east, hawara_walls_west, 
                          nomad_camp_east, nomad_camp_west]
# for i in range(20):
#     room = random.choices([character_rooms, demo_locations], [60, 40], k=1)
#     print(room)
#print(random.choice(demo_locations, character_rooms))

#add all characters in a list
for i in range(len(characters_list)):
    #add a quest_given attribute
    new_char = characters_list[i]
    new_npc = characters.NonPlayableCharacter(new_char['name']+' '+new_char['family_name'], new_char['name'], new_char['proffession'])
    new_npc.context = new_npc.name
    new_npc.age = new_char['age']
    new_npc.title = new_char['title']
    new_npc.gender = new_char['gender']
    new_npc.family_name = new_char['family_name']
    new_npc.proffession = new_char['proffession']
    new_npc.aggression = new_char['aggression']
    new_npc.previously_met = new_char['previously met']
    new_npc.is_alive=True
    new_npc.subj_pronouns = new_char['subj_pronouns']
    new_npc.gen_pronouns = new_char['gen_pronouns']
    new_npc.obj_pronouns = new_char['obj_pronouns']
    new_npc.hit_points=20
    new_npc.description = new_char['description']
    inventory = characters.generate_npc_inventory(new_npc.proffession)
    new_npc.items = adv.Bag(inventory)
    #new_npc.items=adv.Bag([game_items.apple, game_items.golden_floren])
    new_npc.floren_balance = random.randint(5,250)
    new_npc.nationality = new_char['nationality']
    objective = mission_generator.generate_objective("Start", [5, 7])
    new_npc.favour = objective.split(",")
    new_npc.favour_completed = new_char['favour_completed']
    new_npc.intelligence = new_char['intelligence']
    character_obj.append(new_npc)


def add_character_attributes(nationality, profession, location):
    char = characters.create_random_NPC(nationality, profession)
    #add character in list
    location.characters.add(char)
    list_of_characters.append(char)
    #add character x and y coordinate in game world
    char.x = location.x
    char.y = location.y
    objective = mission_generator.generate_objective("Start", [char.x, char.y])
    char.favour = objective.split(",")
    char.favour_completed = False

#add characters in town tiles
def fill_towns():
    professions = ["blacksmith", "merchant", "soldier"]
    for area in nordvik:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("","", area)
            
    for area in vestanvarth:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("Norse", random.choice(professions), area)
    for area in cathairbhaile:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("","", area)
    for area in capital:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("Elf", random.choice(professions), area)
    for area in aulba:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("Elf", random.choice(professions), area)
    for area in hawara:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("Alnaasi", random.choice(professions), area)
    for area in nhudelhid_camp:
        rnd = random.randint(2,4)
        for i in range(rnd):
            add_character_attributes("Nhudelhid", random.choice(["soldier", "blacksmith"]), area)

#add characters or enemies every second or third tile
def add_characters():
    for i in range(len(demo_locations)):
        choice = random.choices(["npc", "monster", "bandit"], [50,25,25], k=1)
        try:
            if choice == "monster":
                room_index = i+random.randint(0,3)
                demo_locations[room_index].characters.add(characters.generate_monster())
            elif choice == "bandit":
                room_index = i+random.randint(0,3)
                demo_locations[room_index].characters.add(characters.generate_enemy_npc())
            else:
                room_index = i+random.randint(0,3)
                char = characters.create_random_NPC("","")
                demo_locations[room_index].characters.add(char)
                #add character in list
                list_of_characters.append(char)
                #add character x and y coordinate in game world
                char.x = demo_locations[room_index].x
                char.y = demo_locations[room_index].y
                objective = mission_generator.generate_objective("Start", [char.x, char.y])
                char.favour = objective.split(",")
                char.favour_completed = False
                # char_index = random.randint(len(character_rooms),len(character_obj))
                # if character_obj[char_index].x == -2:
                #     demo_locations[room_index].characters.add(character_obj[char_index])
                #     #add character x and y coordinate
                #     character_obj[char_index].x = demo_locations[room_index].x
                #     character_obj[char_index].y = demo_locations[room_index].y
                #add a tavern or inn if the character is an innkeeper/tavern owner
                if char.proffession == "innkeeper":
                    demo_locations[room_index].enter = create_inns(demo_locations[room_index].super_area_title)
                    demo_locations[room_index].enter.x = demo_locations[room_index].x
                    demo_locations[room_index].enter.y = demo_locations[room_index].y
                # else:
                #     pass
        except IndexError:
            pass

def add_caves():
    for i in range(len(demo_locations)):
        #add caves randomly in hill or mountain type terrain
        if demo_locations[i].type == "5" or demo_locations[i].type == "6":
            random_seed = random.randint(0,10)
            if random_seed == 0:
                demo_locations[i].enter = create_caves(demo_locations[i].super_area_title)
                demo_locations[i].enter.x = demo_locations[i].x
                demo_locations[i].enter.y = demo_locations[i].y
                #monsters that can exist in caves
                demo_locations[i].enter.characters.add(characters.generate_monster(random.choice(["vampire", "wraith", "werewolf", "draugr"])))
        #add elven ruins in forest type terrain
        elif demo_locations[i].type == "4":
            random_seed = random.randint(0,10)
            if random_seed == 0:
                demo_locations[i].enter = create_elven_ruins(demo_locations[i].super_area_title)
                demo_locations[i].enter.characters.add(characters.generate_monster(random.choice(["wraith", "draugr"])))
                demo_locations[i].enter.x = demo_locations[i].x
                demo_locations[i].enter.y = demo_locations[i].y
                #add some scrolls/book items for lore
        #add some taverns/inns in plains or towns
        # elif demo_locations[i].type == "3" or demo_locations[i].type == "7":
        #     random_seed = random.randint(0,20)
        #     if random_seed == 0:
        #         demo_locations[i].enter = create_inns(demo_locations[i].super_area_title)
        #         demo_locations[i].enter.x = demo_locations[i].x
        #         demo_locations[i].enter.y = demo_locations[i].y
                # demo_locations[i].enter.characters.add(characters.)

def complete_mission(mission):
    # mission.completed = True
    mission.successful = True
    #print_gui(f"{mission.title} - mission successful.")

def generate_mission_description(type, objective, location, quest_giver):
    descr_start = random.choice(["As you were passing through "+rooms_obj[quest_giver.x][quest_giver.y].super_area_title+",", "While in "+location+",", "Along your journey,"])
    descr_middle = random.choice(["you met a "+quest_giver.proffession+" by the name of "+quest_giver.name+", who asked for your help.",
                                  "a "+quest_giver.proffession+" named "+quest_giver.name+" needed you for a job.",
                                  "the "+quest_giver.nationality+" "+quest_giver.proffession+" "+quest_giver.name+" hired you for a mission."])
    #descr_end = random.choice(["The "+quest_giver.nationality+" wants you to find the "+objective])
    if type == "Fetch":
        descr_end = "The "+quest_giver.nationality+" wants you to find "+quest_giver.gen_pronouns+" "+objective+". The object was lost somewhere in "+location+"."
    elif type == "Eliminate":
        descr_end = "A criminal has been rampaging through "+location+", and you were hired by "+quest_giver.name+" to hunt down and eliminate him."
    elif type == "Collect":
        descr_end = quest_giver.name+" has told you about a treasure hidden somewhere in "+location+". Perhaps you could check this out."
    elif type == "Hunt":
        descr_end = "A monster has been rampaging through "+location+". You were hired by "+quest_giver.name+" to get rid of the "+objective+" so that the region is safe again."
    elif type == "Escort":
        descr_end = "The "+quest_giver.proffession+" has lost "+quest_giver.gen_pronouns+" "+objective+" somewhere in "+location+". "+quest_giver.subj_pronouns+" hired you to find and escort to safety the "+objective+"."
    else:
        descr_end = "The "+quest_giver.nationality+" wants you to find the "+objective
    return descr_start+" "+descr_middle+" "+descr_end

main_mission_type = ["Prologue", "Chapter I", "Chapter II", "Chapter III", "Chapter IV", "Chapter V"]
main_mission_descriptions = {"Prologue": """You woke up in the middle of nowhere with no memories of the last days. You were holding a golden spear, and a strange scepter, and in your pockets you found a pouch with 50 florens inside. A strange marking on your face and a black rot on your fingertips of your left hand indicate that you were a victim of black magic. A sorcerer might know how you will break the spell.""",
                             "Chapter I": """A fraction of your memories unlocked. You were seemingly in a middle of a battle with a red haired sorcerer with a scar when you barely escaped using the scepter. You remember that a window was there, and outside you saw an endless desert. So you decide that you must leave the island and pursue your lead south.""",
                             "Chapter II": """You arrived at Cathairbhaile, the biggest port in the world. People from all the corners of the Earth gather here, traders, merchants, spies, who could give you the information you seeked.""",
                             "Chapter III": """The detective gave you the location of a tower that belonged to a sorcerer that might match your description, so you decided to travel there to investigate.""",
                             "Chapter IV": """The tower was a mess, broken flasks everywhere, bookcases and shelves broken, large tomes and scrolls in the ground everywhere. You picked up a diary that contained spells signed by someone named Nesin Nauthuy, the grandmaster of the Citadel.""",
                             "Chapter V": """Memories started to come back to you after you talked to the grandmaster. You were hired by him to assassinate Mulfeilf Deim, a red haired sorcerer, formerly an apprentice of Nesin in the Citadel that had gone rogue. You still couldn't remember how the fight between you two ended, so you assumed he was still alive. The grandmaster sent you to chase his trail again, but this time, you both wanted him alive to break your curse."""}
class Mission():
    def __init__(self, type, objective, location, quest_giver):
        self.type = type
        self.objective = objective
        if location == []:
            self.location = location
        else:
            self.location = rooms_obj[location[0]][location[1]].super_area_title
            self.x = location[0]
            self.y = location[1]
        #self.location = location
        #self.target_object = target_object
        self.quest_giver = quest_giver
        self.completed = False
        self.successful = ""
        self.enemy_npc = False
        
        self.reward = random.randint(100,200)
        if self.type in main_mission_type:
            self.description = main_mission_descriptions[self.type]
        else:
            self.description = "Along your journey, you have met "+ quest_giver.name + ", a "+quest_giver.proffession+ " who has asked for your help.\n"
            self.description = generate_mission_description(type, objective, self.location, quest_giver)
        if self.type == "Fetch" or self.type == "Collect":
            condition = random.choice(["old", "brand new", "used", "rusty"])
            self.target_object = game_items.generate_weapon(self.objective, condition)
            rooms_obj[location[0]][location[1]].items.add(self.target_object)
            
            #self.description = self.description+"The "+quest_giver.nationality+" "+quest_giver.proffession+" has lost "+quest_giver.gen_pronouns+" "+self.target_object+" and has tasked you with returning it to "+quest_giver.obj_pronouns+".\nYou will find it in "+self.location
            if self.type == "Fetch":
                self.title = "Favours: Return " + self.objective + " to " + self.quest_giver.name 
            else:
                self.title = "Treasure Hunt: Find "+self.objective

        elif self.type == "Escort":
            self.objective = characters.generate_objective_npc(self.objective, self.quest_giver)
            enemy_npc = characters.generate_enemy_npc()
            self.enemy_npc = enemy_npc
            rooms_obj[location[0]][location[1]].characters.add(self.objective)
            rooms_obj[location[0]][location[1]].characters.add(enemy_npc)
            self.title = "Favours: Escort "+self.objective.name + " back to "+self.location

        elif self.type == "Eliminate":
            self.objective = characters.generate_enemy_npc()
            rooms_obj[location[0]][location[1]].characters.add(self.objective)
            self.title = "Bounty: Eliminate "+self.objective.name

        elif self.type == "Hunt":
            self.objective = characters.generate_monster(objective)
            rooms_obj[location[0]][location[1]].characters.add(self.objective)
            self.title = "Monster Hunt: Find and eliminate "+self.objective.name

    def check_success(self, current_room, inventory):
        #quest_giver = current_room.characters.find(self.quest_giver)
        if self.type == "Fetch":            
            for obj in self.quest_giver.items:
                if self.target_object == obj:
                    complete_mission(self)
                    self.quest_giver.favour_completed = True
                    break
                
        elif self.type == "Eliminate" or self.type == "Hunt":
            char = self.objective
            if char.is_alive == False:
                complete_mission(self)
                self.quest_giver.favour_completed = True
        
        elif self.type == "Collect":
            obj = self.objective
            for item in inventory:
                if obj == item:
                    complete_mission(self)
                    self.quest_giver.favour_completed = True
                    break
        
        elif self.type == "Escort":
            char = self.objective
            if char.is_alive == False:
                self.quest_giver.favour_failed = True
            elif char.is_alive == True and self.enemy_npc.is_alive == False:
                complete_mission(self)
                self.quest_giver.favour_completed = True
        #check when a main mission ended
        elif self.type in main_mission_type:
            objective = self.objective
            if objective.favour_completed:
                complete_mission(self)
        

vestanvarth_port.characters.add(characters.alnaasi_captain)
cathairbhaile_port.characters.add(characters.alnaasi_captain)
capital_port.characters.add(characters.alnaasi_captain)

# objective = mission_generator.generate_objective("Start", [5, 9])
# mission = objective.split(",")
# print(mission)
add_characters()
add_caves()
fill_towns()
current_room = rooms_obj[4][9]
#test_side_quest = Mission("Fetch", "sword", [4, 8], character_obj[0])
