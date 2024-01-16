import game_rooms
import game_items
import json
import adventurelib as adv
import characters
import main_missions

#takes dictionary from json and returns an object of class Item
def create_item(item):
    equipped_item = adv.Item(item['name'], item['name'].split()[-1])
    equipped_item.color = item['color']
    equipped_item.edible = item['edible']
    equipped_item.cost = item['cost']
    equipped_item.wearable = item['wearable']
    equipped_item.description = item['description']
    equipped_item.weight = item['weight']
    equipped_item.damage = item['damage']
    equipped_item.bonus = item['bonus']
    return equipped_item

def save():
    #save current game characters
    characters_json = []
    for i in range(len(game_rooms.list_of_characters)):
        #bug with double name in saved files
        characters_json.append({"name": game_rooms.list_of_characters[i].name, "family_name": game_rooms.list_of_characters[i].family_name, "title": game_rooms.list_of_characters[i].title, "age": game_rooms.list_of_characters[i].age,
            "proffession": game_rooms.list_of_characters[i].proffession, "nationality": game_rooms.list_of_characters[i].nationality, "gender": game_rooms.list_of_characters[i].gender, "obj_pronouns": game_rooms.list_of_characters[i].obj_pronouns, "subj_pronouns": game_rooms.list_of_characters[i].subj_pronouns, "gen_pronouns": game_rooms.list_of_characters[i].gen_pronouns,
            "aggression": game_rooms.list_of_characters[i].aggression, "previously_met": game_rooms.list_of_characters[i].previously_met, "description": game_rooms.list_of_characters[i].description,
            "favour_completed": game_rooms.list_of_characters[i].favour_completed, "intelligence": game_rooms.list_of_characters[i].intelligence, "x": game_rooms.list_of_characters[i].x, "y": game_rooms.list_of_characters[i].y,
            "is_alive": game_rooms.list_of_characters[i].is_alive, "hit_points": game_rooms.list_of_characters[i].hit_points, "floren_balance": game_rooms.list_of_characters[i].floren_balance, "favour": game_rooms.list_of_characters[i].favour,
            "mission_accepted": game_rooms.list_of_characters[i].mission_accepted, "mission_refused": game_rooms.list_of_characters[i].mission_refused})
    with open('save files/characters.json','w') as json_file:
        json.dump(characters_json, json_file)
    
    #save current player location, condition, inventory
    print(game_items.inventory)
    items_json = []
    for item in game_items.inventory:
        items_json.append({"name": item.name, "color": item.color, "edible": item.edible, "cost": item.cost, "wearable": item.wearable, "description": item.description,
                           "weight": item.weight, "damage": item.damage, "bonus": item.bonus})
    with open('save files/inventory.json','w') as json_inv:
        json.dump(items_json, json_inv)
    weapon = game_items.equipped_weapon
    with open('save files/equipped_weapon.json', 'w') as json_weapon:
        json.dump({"name": weapon.name, "color": weapon.color, "edible": weapon.edible, "cost": weapon.cost, "wearable": weapon.wearable, "description": weapon.description,
                           "weight": weapon.weight, "damage": weapon.damage, "bonus": weapon.bonus}, json_weapon)
    armour = game_items.equipped_armour
    with open('save files/equipped_armour.json', 'w') as json_armour:
        json.dump({"name": armour.name, "color": armour.color, "edible": armour.edible, "cost": armour.cost, "wearable": armour.wearable, "description": armour.description,
                           "weight": armour.weight, "damage": armour.damage, "bonus": armour.bonus}, json_armour)
    
    #save player condition and current main objective
    with open('save files/player_condition.json', 'w') as json_player:
        json.dump({"x_coord": game_items.x_coord, "y_coord": game_items.y_coord, "hit_points": game_items.hit_points, "avail_spells": game_items.avail_spells, 
                   "floren_balance": game_items.floren_balance, "darkness": game_items.negative_karma, 
                   "main_mission": list(main_missions.main_missions.keys())[list(main_missions.main_missions.values()).index(main_missions.current_main_mission)]}, json_player)

    #keep track of the player's visited main locations
    locations_visited = []
    for location in game_rooms.towns:
        for area in location:
            locations_visited.append({f"{area.title}": area.visited})
    with open('save files/visited_locations.json', 'w') as json_locations:
        json.dump(locations_visited, json_locations)
    #save missions and mission progress
    #save rooms and subrooms
    
#BRING BACK THE MAIN MISSION NPCs
def load():
    #characters_list = []
    player_condition = []
    game_rooms.active_missions = []
    game_rooms.list_of_characters = []
    locations_visited = []
    #clear all content from game rooms
    #print(len(game_rooms.rooms_obj[4][9].characters))
    for i in range(50):
        for j in range(50):
            for character in game_rooms.rooms_obj[i][j].characters.copy():
                game_rooms.rooms_obj[i][j].characters.remove(character)
    try:
        # with open('save files/characters.json','r') as json_file:
        #     characters_list = json.load(json_file)
        #load player condition and equipped items
        with open('save files/player_condition.json','r') as json_player:
            player_condition = json.load(json_player)
        #print(player_condition)
        game_items.x_coord = player_condition['x_coord']
        game_items.y_coord = player_condition['y_coord']
        game_rooms.current_room = game_rooms.rooms_obj[game_items.x_coord][game_items.y_coord]
        game_items.hit_points = player_condition['hit_points']
        game_items.avail_spells = player_condition['avail_spells']
        game_items.floren_balance = player_condition['floren_balance']
        game_items.negative_karma = player_condition['darkness']
        main_missions.current_main_mission = main_missions.main_missions[player_condition['main_mission']]
        #append active missions with previous completed main missions too
        game_rooms.active_missions.append(main_missions.current_main_mission)
        with open('save files/equipped_weapon.json','r') as json_weapon:
            weapon = json.load(json_weapon)
        game_items.equipped_weapon = create_item(weapon)
        with open('save files/equipped_armour.json','r') as json_armour:
            armour = json.load(json_armour)
        game_items.equipped_armour = create_item(armour)
        
        #load inventory
        game_items.inventory = adv.Bag()
        with open('save files/inventory.json','r') as json_inv:
            inv = json.load(json_inv)
        #print(inv)
        for item in inv:
            game_items.inventory.add(create_item(item))

        with open('save files/characters.json', 'r') as json_char:
            char = json.load(json_char)
        for character in char:
            new_npc = characters.NonPlayableCharacter(character['name'], character['name'].split()[0], character['proffession'])
            new_npc.context = new_npc.name
            new_npc.age = character['age']
            new_npc.title = character['title']
            new_npc.gender = character['gender']
            new_npc.family_name = character['family_name']
            new_npc.proffession = character['proffession']
            new_npc.aggression = character['aggression']
            new_npc.previously_met = character['previously_met']
            new_npc.is_alive = character['is_alive']
            new_npc.subj_pronouns = character['subj_pronouns']
            new_npc.gen_pronouns = character['gen_pronouns']
            new_npc.obj_pronouns = character['obj_pronouns']
            new_npc.hit_points = character['hit_points']
            new_npc.description = character['description']
            inventory = characters.generate_npc_inventory(new_npc.proffession)
            new_npc.items = adv.Bag(inventory)
            #new_npc.items=adv.Bag([game_items.apple, game_items.golden_floren])
            new_npc.floren_balance = character['floren_balance']
            new_npc.nationality = character['nationality']
            # objective = mission_generator.generate_objective(mission_generator.grammar, "Start")
            # new_npc.favour = objective.split(",")
            new_npc.favour_completed = character['favour_completed']
            new_npc.intelligence = character['intelligence']
            new_npc.favour = character['favour']
            new_npc.mission_accepted = character['mission_accepted']
            new_npc.mission_refused = character['mission_refused']
            new_npc.x = character['x']
            new_npc.y = character['y']
            game_rooms.list_of_characters.append(new_npc)
            #print("x: "+ str(new_npc.x)+", y: "+str(new_npc.y))

        for char in game_rooms.list_of_characters:
            game_rooms.rooms_obj[char.x][char.y].characters.add(char)
            #add a tavern or inn if the character is an innkeeper/tavern owner
            if char.proffession == "innkeeper":
                game_rooms.rooms_obj[char.x][char.y].enter = game_rooms.create_inns(game_rooms.rooms_obj[char.x][char.y].super_area_title)
                game_rooms.rooms_obj[char.x][char.y].enter.x = game_rooms.rooms_obj[char.x][char.y].x
                game_rooms.rooms_obj[char.x][char.y].enter.y = game_rooms.rooms_obj[char.x][char.y].y
            if char.mission_accepted:
                char_favour = char.favour
                mission = game_rooms.Mission(char_favour[0], char_favour[1], [int(char_favour[2]), int(char_favour[3])], char)
                game_rooms.active_missions.append(mission)
        
        #load other information such as main locations visited by the player
        with open('save files/visited_locations.json') as json_locations:
            locations_visited = json.load(json_locations)
        for i in range(len(locations_visited)):
            game_rooms.list_of_main_locations[i].visited = locations_visited[i].keys()

        #add back some main characters
        game_rooms.vestanvarth_port.characters.add(characters.alnaasi_captain)
        game_rooms.cathairbhaile_port.characters.add(characters.alnaasi_captain)
        game_rooms.capital_port.characters.add(characters.alnaasi_captain)
        game_rooms.nordvik_port.characters.add(characters.captain)
    except FileNotFoundError:
        print("Save files corrupted")