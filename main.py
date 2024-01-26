from adventurelib import *
#from game_gui import *
from game_gui import *
from random import randint
import game_rooms
import game_items
import random
import dialog
#import generate_npc
import characters
import main_missions
# import time
import customtkinter


#game setup
#game_rooms.current_room=game_rooms.forest_main_road
# game_rooms.current_room=game_rooms.rooms_obj[4][9]
# x_coord = 4
# y_coord = 9
x_coord = game_items.x_coord
y_coord = game_items.y_coord
fast_travel_areas = ["Vestenvarth", "Nordvik", "Cathairbhaile", "Hawara", "Capital"]
fast_travel_rooms = {"Vestenvarth": game_rooms.vestanvarth_port, "Nordvik": game_rooms.nordvik_port, "Cathairbhaile": game_rooms.cathairbhaile_port, 
                     "Hawara": game_rooms.hawara_port, "Capital": game_rooms.capital_port}
game_rooms.current_room.visited=False
stealth = 14
#hit_points=20
#in-game currency for player
# floren_balance = 20
# enemy_hit_points=20
# equipped_item = game_items.steel_sword
# game_items.equipped_weapon = game_items.steel_sword
# equipped_armour = game_items.cloak
# game_items.equipped_armour = game_items.cloak
# equipped_item = game_items.equipped_weapon
# equipped_armour = game_items.equipped_armour


#all active quests
# active_missions = []
# completed_missions = []
# inventory=game_items.inventory

#dictionary that contains all terrain scores of the game map
rooms_dict = {}
with open('assets/map_test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        rooms_dict[row['key']] = row['value']


def check_mission_completed():
    for mission in game_rooms.active_missions:
        mission.check_success(game_rooms.current_room, game_items.inventory)
        if mission.type == "Chapter III":
            if game_items.inventory.find(game_items.diary.name):
                mission.completed = True
                print_gui(f"{mission.title} - mission successful.")
                main_missions.current_main_mission = main_missions.chapter4
                game_rooms.active_missions.append(main_missions.chapter4)
                print_gui("\nNew objective: Find the owner of the diary.")
                current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
        else:
            if mission.quest_giver.favour_completed and mission.completed == False:
                print_gui(f"{mission.title} - mission successful.")
                mission.completed = True
                print_gui(f"~You can talk to the quest giver to claim the reward.~")
            elif mission.quest_giver.favour_failed:
                print_gui(f"{mission.title} - mission failed")
        #game_rooms.active_missions.remove(mission)

def set_other_npc_aggr(char):
    for npc in game_rooms.character_obj:
        if char.type == "human":
            if npc.nationality == char.nationality and char.proffession != "bandit":
                npc.aggression = npc.aggression + 15
                npc.kin_killed = True

#update the current location label
def update_current_location(current_room):
    current_location.configure(text="Current Location: "+current_room.title)

def update_hit_points(hit_points):
    player_hit_points.configure(text="HP: "+str(hit_points))

#fast travel when you click on a tile from the map
def fast_travel(event):
    x = game_items.x_coord
    y = game_items.y_coord
    for rect_id, rect_coords in rectangle_coords.items():

        x1, y1, x2, y2 = rect_coords
        if x1 < event.x < x2 and y1 < event.y < y2:
            new_x_coord = rect_id[0]
            new_y_coord = rect_id[1]
            #add a range to the fast travel mechanic
            if game_rooms.current_room == game_rooms.black_lodge or game_rooms.current_room == game_rooms.white_lodge:
                print_gui("You try to use the teleportation Scepter, but it doesn't seem to work here.")
            elif abs(new_x_coord-x)>=5 or abs(new_y_coord-y)>=5:
                print_gui("You try to cast the teleportation spell, but you do not have enough energy to travel that far.\n")
            elif game_rooms.rooms_obj[rect_id[0]][rect_id[1]].type == "0":
                print_gui("You cannot fast travel to the sea, you do not know how to swim.\n")
            else:
                game_rooms.current_room = game_rooms.rooms_obj[rect_id[0]][rect_id[1]]
                game_items.x_coord = new_x_coord
                game_items.y_coord = new_y_coord
                print_gui(random.choice(["You use the teleporting spell to magically travel away from here.\n","You use the warp spell to fast travel.\n",
                                        "You cast the teleportation spell to travel instantly elsewhere.\n"]))
                try:
                    repaint_old_tile(x, y, rooms_dict[f'({x}, {y})'])
                    update_map_position(game_items.x_coord, game_items.y_coord, "red")
                except:
                    print_gui("ERROR")
                update_current_location(game_rooms.current_room)
                look()
                # print(game_items.x_coord)
                # print(game_items.y_coord)


#open a fast travel menu when you try to rent a boat in a port
def open_fast_travel_menu(area_title):
    global fast_travel_menu
    #print(area_title)
    fast_travel_menu = customtkinter.CTkToplevel(root)
    fast_travel_menu.geometry("650x650")
    fast_travel_menu.attributes("-topmost","true")
    fast_travel_menu.title("Fast Travel Menu")
    for area in fast_travel_areas:
        if area != area_title:
            choice_button = customtkinter.CTkButton(fast_travel_menu, width=700, height=50, text=area, command= lambda area=area: go_to_area(area), text_color="black")
            choice_button.pack(padx=5, pady=10)

def go_to_area(area):
    global fast_travel_menu, x_coord, y_coord
    game_rooms.current_room = fast_travel_rooms[area]
    x = game_items.x_coord
    y = game_items.y_coord
    game_items.x_coord = game_rooms.current_room.x
    game_items.y_coord = game_rooms.current_room.y
    x_coord = game_items.x_coord
    y_coord = game_items.y_coord
    try:
        repaint_old_tile(x, y, rooms_dict[f'({x}, {y})'])
        update_map_position(game_items.x_coord, game_items.y_coord, "red")
    except:
        print_gui("ERROR")
    update_current_location(game_rooms.current_room)
    look()
    if main_missions.current_main_mission == main_missions.chapter1 and x_coord == 21 and y_coord == 19:
        characters.captain.favour_completed = True
        check_mission_completed()
        game_rooms.active_missions.append(main_missions.chapter2)
        main_missions.current_main_mission = main_missions.chapter2
        print_gui("\nNew objective: Ask around Cathairbhaile for information.")
        current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
    fast_travel_menu.destroy()


def check_dark_lodge_visit(karma):
    if karma >=50 or game_items.hit_points<=0:
        game_rooms.current_room = game_rooms.black_lodge
        update_current_location(game_rooms.current_room)
        look()


@when("enlightenment")
def white_lodge_visit():
    game_rooms.current_room = game_rooms.white_lodge
    update_current_location(game_rooms.current_room)
    look()

@when("inventory")
@when("inv")
@when("i")
def list_inventory():
    if game_items.inventory:
        print_gui("You have the following items:")
        for item in game_items.inventory:
            print_gui(f"{item.name} - {item.description}\nDamage: {item.damage}\nArmour: {item.bonus}\nWeight: {item.weight}\n")
        print_gui(f"You have {game_items.floren_balance} florens.\n")
    else:
        print_gui("You have nothing in your inventory.\n")

#Item interactions
@when("look at ITEM")
def look_at(item: str):
    """Prints a short description of an item if it is either:
    1. in the current room, or
    2. in our inventory

    Arguments:
        item {str} -- the item to look at
    """

    # Check if the item is in the room
    obj = game_rooms.current_room.items.find(item)
    if not obj:
        # Check if the item is in your inventory
        obj = game_items.inventory.find(item)
        if not obj:
            print_gui(f"I can't find {item} anywhere.")
        else:
            print_gui(f"You have {item}.")
    else:
        print_gui(f"You see {item}.")

@when("describe ITEM")
def describe(item: str):
    """Prints a description of an item if it is either:
    1. in the current room, or
    2. in your inventory

    Arguments:
        item {str} -- the item to look at
    """
    # Check if the item is in the room
    obj = game_rooms.current_room.items.find(item)
    if not obj:
        # Check if the item is in your inventory
        obj = game_items.inventory.find(item)
        if not obj:
            print_gui(f"I can't find {item} anywhere.")
        else:
            print_gui(f"You have {obj.description}.")
    else:
        print_gui(f"You see {obj.description}.")

@when("take ITEM")
@when("get ITEM")
@when("pickup ITEM")
@when("pick up ITEM")
@when("grab ITEM")
@when("collect ITEM")
def take_item(item: str):

    obj = game_rooms.current_room.items.take(item)
    if not obj:
        print_gui(f"I don't see {item} here.")
    else:
        print_gui(f"You now have {obj.description}.")
        game_items.inventory.add(obj)
        check_mission_completed()
        if obj == game_items.diary:
            print_gui("By reading the mage's diary, you acquired knowledge for a new spell.")
            spell = game_items.spells[0]['name']
            game_items.avail_spells.append(spell)


@when("equip ITEM")
def equip_item(item):
    global stealth
    weapon = game_items.inventory.find(item)
    #print("You have equipped:\n",equipped_item)
    if not weapon:
        print_gui(f"You don't have {item} in your inventory.")
    else:
        if not weapon.wearable and not weapon.edible:
            weapon = game_items.inventory.take(item)
            game_items.inventory.add(game_items.equipped_weapon)
            #print(game_items.equipped_weapon)
            # try:
            #     game_items.equipped_items.take(equipped_item)
            # except AttributeError:
            #     print("didn't work")
            game_items.equipped_weapon = weapon
            total_weight = game_items.equipped_armour.weight + game_items.equipped_weapon.weight
            stealth = 24 - total_weight
            print_gui(f"You have equipped: {game_items.equipped_weapon}\n")
            #print("Stealth: ", stealth)
            player_weight.configure(text=f"Total weight: {total_weight}")
            # game_items.equipped_items.add(equipped_item)
            # print(game_items.equipped_items)
        else:
            print_gui("You cannot wield this item.")

@when("wear ITEM")
def wear_item(item):
    armour = game_items.inventory.find(item)
    global stealth
    if not armour:
        print_gui(f"You don't have {armour} in your inventory.")
    else:
        if armour.wearable:
            wearable_armour = game_items.inventory.take(item)
            game_items.inventory.add(game_items.equipped_armour)
            game_items.equipped_armour = wearable_armour
            total_weight = game_items.equipped_armour.weight + game_items.equipped_weapon.weight
            stealth = 24 - total_weight
            game_items.total_hit_points = game_items.hit_points + game_items.equipped_armour.bonus
            player_weight.configure(text=f"Total weight: {total_weight}")
            player_hit_points.configure(text=f"HP: {game_items.total_hit_points}")
            print_gui(f"You wear the {armour}")
        else:
            print_gui("You cannot wear this item.")


@when("equipped")
@when("equipped items")
def show_equipped_items():
    print_gui(f"Weapon: {game_items.equipped_weapon}")
    print_gui(f"Armour: {game_items.equipped_armour}")
    print_gui(f"Total weight: {game_items.equipped_weapon.weight+game_items.equipped_armour.weight}")

##----------------NEEDS REWORK------------------
## COMBAT ##
@when("attack CHARACTER", context=get_context())
@when("fight CHARACTER", context=get_context())
@when("kill CHARACTER", context=get_context())
def fight_enemy(character):
    

    char = game_rooms.current_room.characters.find(character)
    #enemy_hit_points = char.hit_points
    #print("Enemy Hit points: ", char.hit_points)

    # Is the character there?
    if not char:
        print_gui(f"There is no {character} here.")
    elif char in characters.main_mission_characters:
        print_gui("~You can't attack this character~")
    elif char.is_alive==False:
        print_gui(f"{character} is already dead.")
    # It's a character who is there
    else:
        # Set the context, and start the encounter
        #set_context(char.context)
        set_context("combat")
        #sword = inventory.find("sword")
        weapon = game_items.equipped_weapon
        # The player gets a swing
        player_attack = weapon.damage
        if weapon.name == "crossbow":
            print_gui(f"You take a bolt from your quiver and you load it onto the crossbow. You pull the lever that locks the draw, you aim and shoot at {char.name}.")
            print_gui(f"You deal to {char.name} {weapon.damage} damage.\n")
        else:
            print_gui(f"You swing your {weapon} against {char.name}, doing {player_attack} damage!")
        #enemy_hit_points -= player_attack
        
        #different types of monsters/check effectiveness
        dialog.check_player_attack_effectiveness(player_attack, weapon, char)
        #char.hit_points -= player_attack

        # Is the enemy dead?
        if char.hit_points <= 0:
            print_gui(f"{char.name} falls on {char.gen_pronouns} feet, dead.")
            char.is_alive=False
            set_context(None)
            check_mission_completed()
            if char.proffession == "bandit" or char.type == "monster":
                pass
            elif char == characters.mulfeilf:
                main_missions.chapter5.completed = True
                current_main_obj.configure(text="You do not have any other main objectives")
                print_gui("The rogue sorcerer is dead, but you seem to be trapped in the White Lodge.")
                print_gui("\n\n~~~~ΣΕ ΕΥΧΑΡΙΣΤΩ ΠΟΥ ΠΗΡΕΣ ΜΕΡΟΣ ΣΤΗ ΔΟΚΙΜΗ ΤΗΣ BETA~~~~\n~~~~Μπορείς να συνεχίσεις την εξερεύνηση του κόσμου ελεύθερα τώρα που η ιστορία ολοκληρώθηκε~~~~~")

            else:
                set_other_npc_aggr(char)
                game_items.negative_karma += 5
                print_gui(game_items.darkness_progress(game_items.negative_karma))
                check_dark_lodge_visit(game_items.negative_karma)
                karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))
            
        else:
            print_enemy_condition(character)
            print_gui(" ")

            # Then the enemy tries
            # enemy_attack = randint(0, char.attack_dmg)
            # if enemy_attack == 0:
            #     print_gui(f"The {character}'s arm whistles harmlessly over your head!")
            # else:
            #     print_gui(
            #         f"""
            #         The {character} swings his mighty fist,
            #         and does {enemy_attack} damage!
            #         """
            #     )
            #     hit_points -= enemy_attack
            enemy_ambush(character)

            # Is the player dead?
            if game_items.total_hit_points <= 0:
                #end_game(victory=False)
                print_gui("Your journey ends here\n~~~~YOU ARE DEAD~~~~")
                check_dark_lodge_visit(game_items.negative_karma)
                # time.sleep(5)
                #close_game()

            #print_player_condition(character)
            # print_gui(" ")


@when("shoot at CHARACTER")
@when("shoot CHARACTER")
def shoot_character(character):
    char = game_rooms.current_room.characters.find(character)
    #print("Enemy Hit points: ", char.hit_points)
    weapon = game_items.inventory.find("crossbow")
    # Is the character there?
    if not char:
        print_gui(f"There is no {character} here.")
    elif char in characters.main_mission_characters:
        print_gui("~You can't attack this character~")
    elif char.is_alive==False:
        print_gui(f"{character} is already dead.")
    # It's a character who is there
    else:
        if not weapon:
            print_gui("You do not have a crossbow.\n")
        else:
            # Set the context, and start the encounter
            set_context("combat")
            print_gui(f"You take a bolt from your quiver and you load it onto the crossbow. You pull the lever that locks the draw, you aim and shoot at {char.name}.")
            print_gui(f"You deal to {char.name} {weapon.damage} damage.\n")
            dialog.check_player_attack_effectiveness(weapon.damage, weapon, char)
            if char.hit_points <= 0:
                print_gui(f"{char.name} falls on {char.gen_pronouns} feet, dead.")
                char.is_alive=False
                set_context(None)
                check_mission_completed()
                set_other_npc_aggr(char)
                if char.proffession == 'bandit' or char.type == "monster":
                    pass
                elif char == characters.mulfeilf:
                    main_missions.chapter5.completed = True
                    current_main_obj.configure(text="You do not have any other main objectives")
                    print_gui("The rogue sorcerer is dead, but you seem to be trapped in the White Lodge.")
                    print_gui("\n\n~~~~ΣΕ ΕΥΧΑΡΙΣΤΩ ΠΟΥ ΠΗΡΕΣ ΜΕΡΟΣ ΣΤΗ ΔΟΚΙΜΗ ΤΗΣ BETA~~~~\n~~~~Μπορείς να συνεχίσεις την εξερεύνηση του κόσμου ελεύθερα τώρα που η ιστορία ολοκληρώθηκε~~~~~")

                else:
                    game_items.negative_karma += 5
                    print_gui(game_items.darkness_progress(game_items.negative_karma))
                    check_dark_lodge_visit(game_items.negative_karma)
                    karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))
                
            else:
                print_enemy_condition(character)
                print_gui(" ")
                enemy_ambush(character)

                # Is the player dead?
                if game_items.total_hit_points <= 0:
                    print_gui("Your journey ends here\n~~~~YOU ARE DEAD~~~~")
                    check_dark_lodge_visit(game_items.negative_karma)



def print_enemy_condition(character):
    char = game_rooms.current_room.characters.find(character)
    enemy_hit_points = char.hit_points
    if char.type == "human":
        if enemy_hit_points < 20:
            print_gui(f"{char.name} staggers, {char.gen_pronouns} eyes unfocused.")
        elif enemy_hit_points < 15:
            print_gui(f"{char.name}'s steps become more unsteady.")
        elif enemy_hit_points < 10:
            print_gui(f"{char.name} spits and wipes the blood from {char.gen_pronouns} mouth.")
        elif enemy_hit_points < 5:
            print_gui(f"{char.name} snorts and grits {char.gen_pronouns} teeth against the pain.")
        else:
            print_gui(f"{char.name} smiles and readies {char.obj_pronouns}self for the attack.")
    else:
        print_gui(dialog.monster_condition(char))

def print_player_condition(character):

    if game_items.total_hit_points < 4:
        print_gui(f"Your eyes lose focus on {character} as you sway unsteadily.")
    elif game_items.total_hit_points < 8:
        print_gui("""Your footing becomes less steady as you swing your sword sloppily.""")
    elif game_items.total_hit_points < 12:
        print_gui("""Blood mixes with sweat on your face as you wipe it from your eyes.""")
    elif game_items.total_hit_points < 16:
        print_gui("You bite down as the pain begins to make itself felt.")
    else:
        print_gui("You charge into the fray valiantly!")
    print_gui(" ")

@when("assassinate CHARACTER",context=get_context())
@when("stealth kill CHARACTER", context=get_context())
def stealth_kill(character):

    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui(f"There is no {char.name} here.")
    elif char in characters.main_mission_characters:
        print_gui("~You can't attack this character~")
    elif char.is_alive==False:
        print_gui(f"{char.name} is already dead.")
    else:
        if char.type != "human" or char == "mulfeilf":
            say_gui(f"You try to sneak behind the {char.proffession}, but {char.subj_pronouns} hears you.")
            enemy_ambush(char)
        else:

            if stealth>=15:
                say_gui(f"You sneak behind {char.name} and you stab {char.obj_pronouns} in the back, {char.subj_pronouns} instantly dies.")
                char.is_alive=False
                set_context(None)
                check_mission_completed()
                
            else:
                print_gui(f"You try to sneak behind {char.name}, but you are instantly heard and seen.")
                char.aggression = char.aggression + 20
                #if an npc is not inside a town, the npc will attack the player
                if game_rooms.current_room.type!= '7':
                    dialog.open_dialog_window(char, "assassinate")
                    dialog.dialog_window.wait_window()
                    print_gui(f"{char.name}>> "+random.choice(["You will die for this, vagrant!", "What do you think you're doing? See how it's done.", "I'll make sure I won't fail at killing you like you did."]))
                    enemy_ambush(character)
                    
                else:
                    print_gui(f"{char.name}>> Guards! Guards! A murderer is here!")
                    guard = characters.create_guard_npc()
                    game_rooms.current_room.characters.add(guard)
                    print_gui(guard.description)
                    enemy_ambush("guard")
            if char.proffession != 'bandit':
                set_other_npc_aggr(char)
                game_items.negative_karma += 5
                print_gui(game_items.darkness_progress(game_items.negative_karma))
                check_dark_lodge_visit(game_items.negative_karma)
                karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))

@when("steal from CHARACTER", context=get_context())
@when("steal CHARACTER", context=get_context())
def steal(character):
    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui(f"There is no {char.name} here.")
    elif char in characters.main_mission_characters:
        print_gui("~You can't steal from this character~")
    elif char.is_alive==False:
        print_gui(f"You are not proud of this. You search the corpse of {char.name} and you take {char.gen_pronouns} belongings.")
        for obj in char.items:
            game_items.inventory.add(obj)
            print_gui(f"You added {obj} in your inventory.")
        print_gui(f"You successfully steal {char.floren_balance} florens.")
        game_items.floren_balance = game_items.floren_balance + char.floren_balance
        char.floren_balance = 0
        game_items.negative_karma += 3
        print_gui(game_items.darkness_progress(game_items.negative_karma))
        check_dark_lodge_visit(game_items.negative_karma)
        karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))
        
    else:
        if stealth>=15:
            print_gui(f"You sneak behind {char.name}'s back. You succesfully steal {char.obj_pronouns}.")
            for obj in char.items:
                game_items.inventory.add(obj)
                print_gui(f"You added {obj} in your inventory.")
            print_gui(f"You successfully steal {char.floren_balance} florens.")
            game_items.floren_balance = game_items.floren_balance + char.floren_balance
            char.floren_balance = 0
        else:
            print_gui(f"You try to sneak behind the {char.name}'s back unsuccessfully. Now {char.subj_pronouns} is mad at you.")
            if game_rooms.current_room.type != '7':
                print_gui(f"{char.name}>> What are you doing, thief?")
                dialog.open_dialog_window(char, "steal")
                dialog.dialog_window.wait_window()
                enemy_ambush(character)
                
            else:
                print_gui(f"{char.name}>> Guards! Guards! A thief!")
                guard = characters.create_guard_npc()
                game_rooms.current_room.characters.add(guard)
                print_gui(guard.description)
                enemy_ambush("guard")
        if char.proffession != 'bandit':
            #set_other_npc_aggr(char)
            game_items.negative_karma += 3
            print_gui(game_items.darkness_progress(game_items.negative_karma))
            check_dark_lodge_visit(game_items.negative_karma)
            karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))

@when("available spells")
@when("spells")
def show_av_spells():
    print_gui("The spells you have are: \n")
    for spell in game_items.spells:
        print_gui(spell['name'])


@when("consume ITEM")
@when("eat ITEM")
@when("drink ITEM")
def consume_item(item):
    consumable = game_items.inventory.find(item)
    if consumable.edible == False:
        print_gui(f"~You cannot consume {item}~")
    else:
        print_gui(f"~You consume {item}~")
        game_items.hit_points = game_items.hit_points + consumable.bonus
        if game_items.hit_points>20:
            game_items.hit_points = 20
        update_hit_points(game_items.hit_points+game_items.equipped_armour.bonus)

@when("cast SPELL", context=get_context())
def cast_spell(spell):
    if spell not in game_items.avail_spells:
        print_gui(f"~You cannot cast the spell {spell}~")
    else:
        print_gui(f"~You cast {spell}~")
        current_spell = ""
        char = game_rooms.current_room.characters
        for item in game_items.spells:
            if item['name'] == spell:
                current_spell = item
                break
        if current_spell['type'] == "attack":
            if char == []:
                print_gui(f"There is no enemy here to cast {spell}")
            else:
                num_of_chars = 0
                for character in game_rooms.current_room.characters:
                    num_of_chars +=1
                print_gui(current_spell['description'])
                for character in game_rooms.current_room.characters:
                    #if multiple characters are in scene, spell damage splits
                    
                    if character.hit_points<=0:
                        #print_gui(current_spell['description'])
                        #print_enemy_condition(character)
                        print_gui("~You can't cast a spell towards a dead man.~")
                    character.hit_points = character.hit_points - current_spell['damage']/num_of_chars
                    if character.hit_points<=0:
                        character.is_alive = False
                        if character == characters.mulfeilf:
                            main_missions.chapter5.completed = True
                            current_main_obj.configure(text="You do not have any other main objectives")
                            print_gui("The rogue sorcerer is dead, but you seem to be trapped in the White Lodge.")
                            print_gui("\n\n~~~~ΣΕ ΕΥΧΑΡΙΣΤΩ ΠΟΥ ΠΗΡΕΣ ΜΕΡΟΣ ΣΤΗ ΔΟΚΙΜΗ ΤΗΣ BETA~~~~\n~~~~Μπορείς να συνεχίσεις την εξερεύνηση του κόσμου ελεύθερα τώρα που η ιστορία ολοκληρώθηκε~~~~~")

                        # if character.proffession != 'bandit':
                        #     set_other_npc_aggr(character)
                        #     game_items.negative_karma += 5
                        #     print_gui(game_items.darkness_progress(game_items.negative_karma))
                        #     check_dark_lodge_visit(game_items.negative_karma)
                        #     karma.configure("Darkness growth: "+ str(game_items.negative_karma))
                check_mission_completed()
        elif current_spell['type'] == "healing":
            print_gui(current_spell['description'])
            game_items.hit_points = game_items.hit_points + current_spell['bonus']
            if game_items.hit_points > 20:
                game_items.hit_points = 20
            update_hit_points(game_items.hit_points+game_items.equipped_armour.bonus)
                
                



@when("look")
def look():
    """Print the description of the current room.
    If you've already visited it, print a short description.
    """

    if not game_rooms.current_room.visited:
        #say_gui(game_rooms.current_room.description)
        game_rooms.current_room.visited = True
    say_gui(game_rooms.current_room.description)
    print_gui("\n")
    # print("x: ", game_rooms.current_room.x)
    # print("y: ", game_rooms.current_room.y)
    # Are there any items here?
    for item in game_rooms.current_room.items:
        print_gui(f"There is a {item.name} here.")

    #Check if bandits or monsters are in the same room with npc
    list_of_enemy_characters = []
    for char in game_rooms.current_room.characters:
        #print_gui(f"Here is {char}, the {char.proffession}")
        if char.type == "monster" or char.proffession == "bandit":
            list_of_enemy_characters.append(char)
    #non aggressive npcs have a 50-50 chance of survival if in room with bandits or monsters
    for char in game_rooms.current_room.characters:
        if char not in list_of_enemy_characters:
            if len(list_of_enemy_characters)>=1:
                rand = random.randint(0,1)
                if rand == 0:
                    char.is_alive = False
                else:
                    print_gui(f"{char.name}>>"+random.choice(["Please help me!", "You there, please, I'm going to die!", "Someone help me!"]))

    for char in game_rooms.current_room.characters:
        if char.is_alive:
            print_gui(char.description)
            # print(f"{char.name}: aggression- {char.aggression}")
            # print(f"{char.name}: x- {char.x}, y- {char.y}")
            if char.aggression>15:
                if char.kin_killed:
                    #EDW NA MPEI DIALOGOS
                    print_gui(f"{char.name}>> You murderer! You think you can get away with this?")
                enemy_ambush(char.name)
        else:
            print_gui(f"You see the corpse of {char.name}, a {char.proffession}, rotting here.")
    
    if game_rooms.current_room.enter:
        if game_rooms.current_room.enter.title == "Elven ruins":
            print_gui("You stand before some ancient Elven ruins.\n")
        else:
            print_gui(f"There is a {game_rooms.current_room.enter.title} here.\n")
    print_gui("--------------------------------------------------------------------------------------------------------------------")


#Enemy attacks player
def enemy_ambush(character):
    #enemy_attack = randint(0, 10)
    char = game_rooms.current_room.characters.find(character)
    enemy_attack = randint(0,char.attack_dmg+5)
    #enemy_attack = 30
    if char.type == "human":
        if enemy_attack == 0:
            print_gui(random.choice([f"The {char.name}'s weapon whistles harmlessly over your head!",f"{char.name} completely misses you.", 
                                    f"""{char.name} swings {char.gen_pronouns} weapon, 
                                    but {char.gen_pronouns} swing is weak, 
                                    and easily parried by you.""",
                                    f"{char.name} attacks you with all {char.gen_pronouns} might, but you easily block {char.gen_pronouns} attack."]))
        elif enemy_attack <=5:
            print_gui(f"""{char.name} swings {char.gen_pronouns} steel sword, barely piercing your armour, creating you a flesh wound.""")
            #print(f"{char.name} does {enemy_attack} damage")
            game_items.hit_points -= enemy_attack
            #game_items.total_hit_points -= enemy_attack
            print_player_condition(character)
            update_hit_points(game_items.hit_points+game_items.equipped_armour.bonus)
        else:
            print_gui(
                f"""{char.name} attacks you with all {char.gen_pronouns} might,
                and {char.subj_pronouns} lands a powerful blow."""
            )
            game_items.hit_points -= enemy_attack
            #game_items.total_hit_points -= enemy_attack
            #print(f"{char.name} does {enemy_attack} damage")
            print_player_condition(character)
            update_hit_points(game_items.hit_points+game_items.equipped_armour.bonus)
    else:
        print_gui(dialog.monster_attacks(char, enemy_attack))
        print_gui(f"The {char.name} deals {enemy_attack} damage\n")
        game_items.hit_points -= enemy_attack
        #game_items.total_hit_points -= enemy_attack
        print_player_condition(character)
        update_hit_points(game_items.hit_points+game_items.equipped_armour.bonus)


@when("describe")
def describe_room():
    """Print the full description of the room."""
    say_gui(game_rooms.current_room.description)

    # Are there any items here?
    for item in game_rooms.current_room.items:
        print_gui(f"There is {item.description} here.")


#Dialog with character
@when("talk to CHARACTER", context=get_context())
@when("talk CHARACTER", context=get_context())
@when("hello CHARACTER", context=get_context())
@when("greetings CHARACTER", context=get_context())
def dialog_character(character):
    char = game_rooms.current_room.characters.find(character)
    if char:
        if char.type == "monster":
            print_gui("The monster cannot speak.")
        elif char.is_alive:
            if char.favour:
                char_favour = char.favour
                #print("character side quest: ",char_favour)
                mission = game_rooms.Mission(char_favour[0], char_favour[1], [int(char_favour[2]), int(char_favour[3])], char)
                #print_gui(f"{char.name}>>"+dialog.give_task(mission))
                char.mission = mission
                #active_missions.append(mission)
                #update_map_position(int(char_favour[2]), int(char_favour[3]), "black")
            else:
                pass
            
            if not char.greeting and not char.kin_killed and char.context != "arm":
                print_gui(f"{char.name}>> "+ dialog.character_greeting(char))
            elif not char.kin_killed:
                print_gui(f"{char.name}>> "+ char.greeting)
            elif char.kin_killed and game_rooms.current_room.type != '7':
                print_gui(f"{char.name}>> "+random.choice(["You! Murderer! You won't get away with this!", "Murderer! You killed one of my own!", "You! I know what you are! I will have my vengeance!"]))
                enemy_ambush(char)
            # if char.previously_met == False:
            elif char.kin_killed and game_rooms.current_room.type == '7':
                print_gui(f"{char.name}>> "+random.choice(["Guards! Guards! This one here killed one of my own!", "Everyone listen! This one here is a murderer!"]))
                guard = characters.create_guard_npc()
                game_rooms.current_room.characters.add(guard)
                print_gui(guard.description)
                enemy_ambush("guard")
            #     print_gui(f"{char.name}>> " +dialog.character_introduction(char, game_rooms.current_room.super_area_title))
            

            if char.favour_completed and char.context != "spy":
                print_gui(f"{char.name}>> Thank you so much for helping me, stranger. I'm in your debt.\n"+random.choice(["Here is the reward I promised you.", "Take this, you earned it", "You've earned every single one of these."]))
                char.aggression = char.aggression - 10
                game_items.floren_balance = game_items.floren_balance + char.mission.reward
                print_gui(f"~{char.mission.reward} florens were added to your inventory~\n")
            #--------MANAGE DIALOGUE WITH MAIN CHARACTERS-------------
            if char.proffession != "bandit":
                #prologue dialogue selector
                if char.context == "audafir":
                    dialog.open_dialog_window(char, "audafir")
                    dialog.dialog_window.wait_window()
                    characters.audafir.favour_completed = True
                    check_mission_completed()
                    game_rooms.rooms_obj[6][43].characters.remove(characters.audafir)
                    characters.audafir.previously_met = True
                    game_rooms.active_missions.append(main_missions.chapter1)
                    print_gui("As you step out of the House of the Undying, you pass out. While unconscious, a fragment of your memories unlocks, a young sorcerer with long red hair and a scar on his right eye shouting some enchanted words in elvish before you barely escape using the scepter you don't remember how you acquired. This seemingly happened at the top room of a tower, outside the window, an endless sea of sand. The sorcerer is your first lead at finding how to break your curse, and the landscape from your memories doesn't seem to match the cold island of Nordreyjar. You should head south.")
                    main_missions.current_main_mission = main_missions.chapter1
                    print_gui("\nNew objective: Find a way out of the island.")
                    current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
                elif char.context == "spy":
                    dialog.open_dialog_window(char, "spy")
                    dialog.dialog_window.wait_window()
                    characters.spy.previously_met = True
                    if dialog.chapter2_flag and main_missions.chapter2.completed == False:
                        characters.spy.favour_completed = True
                        check_mission_completed()
                        game_rooms.active_missions.append(main_missions.chapter3)
                        main_missions.current_main_mission = main_missions.chapter3
                        print_gui("\nNew objective: Find the sorcerer's tower.")
                        current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
                elif char.context == "grandmaster":
                    dialog.open_dialog_window(char, "grandmaster")
                    dialog.dialog_window.wait_window()
                    characters.grandmaster.favour_completed = True
                    characters.grandmaster.previously_met = True
                    check_mission_completed()
                    game_rooms.rooms_obj[40][29].characters.remove(characters.grandmaster)
                    game_rooms.active_missions.append(main_missions.chapter5)
                    print_gui("You leave the Citadel with the list of the possible lairs the rogue mage could be hiding.")
                    main_missions.current_main_mission = main_missions.chapter5
                    print_gui("\nNew objective: Find the rogue mage.")
                    current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
                    print_gui("\n\n~~A scroll with the last known hideouts of Mulfeilf has been added to your inventory~~")
                    game_items.inventory.add(game_items.instructions)
                elif char.context == "arm":
                    dialog.open_dialog_window(char, "receptionist")
                    dialog.dialog_window.wait_window()
                    print_gui("The sunlight is blinding you, you seem to be back to the regular world. The rot has been weakened, but it still covers your fingers.")
                    game_rooms.current_room = game_rooms.rooms_obj[game_items.x_coord][game_items.y_coord]
                    game_items.negative_karma = 0
                    karma.configure(text="Darkness growth: "+ str(game_items.negative_karma))
                elif char.context == "mulfeilf":
                    dialog.open_dialog_window(char, "mulfeilf")
                    dialog.dialog_window.wait_window()
                    if char.aggression>=20:
                        enemy_ambush(char)
                    else:
                        game_rooms.current_room = game_rooms.rooms_obj[game_items.x_coord][game_items.y_coord]
                        print_gui("You got back from the White Lodge. The rot is still in your hands, but now you have a new goal, to stop Nesin Nauthuy, the grandmaster of the Citadel from summoning the Dark Lord.")
                        print_gui("\n\n~~~~ΣΕ ΕΥΧΑΡΙΣΤΩ ΠΟΥ ΠΗΡΕΣ ΜΕΡΟΣ ΣΤΗ ΔΟΚΙΜΗ ΤΗΣ BETA~~~~\n~~~~Μπορείς να συνεχίσεις την εξερεύνηση του κόσμου ελεύθερα τώρα που η ιστορία ολοκληρώθηκε~~~~~")
                        main_missions.chapter5.completed = True
                        current_main_obj.configure(text="You do not have any other main objectives")
                else:
                    if char.proffession == 'captain':
                        set_context("captain")
                        char.previously_met = True
                        #change floren balance to 200
                        if game_items.floren_balance >= 200:
                            open_fast_travel_menu(game_rooms.current_room.title)
                        else:
                            print_gui(f"{char.name}>> I'm sorry, you seem to be lacking in coin. You need 200 florens.")
                        #add dialogue for captains
                        #print_gui(f"{char.name}>> Greetings traveller")
                    else:
                        dialog.open_dialog_window(char, "talk")
                        if char.proffession == "merchant" or char.proffession == "innkeep" or char.proffession == "blacksmith":
                            dialog.dialog_window.wait_window()
                            print_gui(f"{char.name}>>" +random.choice(["One more thing. Here is what I have in store, traveler.", "Before you go, take a look at my goods, stranger.", "Please look what I have for you before you leave."]))
                            set_context("merchant")
                            print_gui(f"The {char.proffession} leans behind {char.gen_pronouns} counter and brings before you {char.gen_pronouns} goods")
                            for item in char.items:
                                print_gui(item.name+' - '+str(item.cost)+" florens")
                    #elif char.proffession == "captain":
                        
                #wait for dialog window to close before activating the quest
                
        #-------CHECK BUG WHERE MISSION MAY BE ACTIVATED AGAIN---------
                # dialog.dialog_window.wait_window()
                # if char.mission_accepted:
                #     game_rooms.active_missions.append(mission)
                    #update_map_position(int(char_favour[2]), int(char_favour[3]), "black")

            else:
                dialog.open_dialog_window(char, "bandit")
                dialog.dialog_window.wait_window()
                #print("status: "+dialog.steal_status)
                if dialog.steal_status == "true":
                    print_gui(random.choice(["The bandit decides to leave you alone.\n", f"The bandit seems that {char.subj_pronouns} doesn't want to steal you now.\n",
                                             "The bandit runs away, trying to get out of here as fast as possible."]))
                    game_rooms.current_room.characters.remove(char)
                elif dialog.steal_status == "false":
                    print_gui(random.choice(["You fail to convince the bandit, so now you hand over your belongings.\n", "You tried hard to avoid getting stolen, but you are overwhelmed by the bandit.\n"]))
                    # for item in inventory:
                    #     inventory.remove(item)
                        
                        #char.items.add(item)
                    #bandit steals all the florens from the player and disappears
                    game_rooms.current_room.characters.remove(char)
                    game_items.floren_balance = 0
                elif dialog.steal_status == "false_critical":
                    print_gui(random.choice([f"You failed critically to deescalate the situation and the bandit loses {char.gen_pronouns} patience\n.",
                                             f"The bandit seems to lose {char.gen_pronouns} temper, this is going to end violently.\n",
                                             "The time when this could be resolved peacefully has ended, now it seems that you have to fight the bandit to the death.\n"]))
                    enemy_ambush(character)
                dialog.steal_status = ""
        else:
            print_gui("The dead cannot speak.")
    else:
        print_gui(f"There is no {char} here.")
    print_gui("\n")
    #print_gui(dialog.character_task(char))

#Buy items from merchants, blacksmiths etc
@when("buy ITEM from CHARACTER", context=get_context())
@when("buy ITEM CHARACTER", context=get_context())
def buy_item(item, character):

    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui(f"There is no {character} here.")
    else:
        current_context = get_context()
        if current_context == "merchant":
            
            product = char.items.find(item)
            if game_items.floren_balance>= product.cost:
                print_gui(f"You give the {char.name} {product.cost} florens to buy the {product}")
                game_items.inventory.add(product)
                game_items.floren_balance = game_items.floren_balance - product.cost
            else:
                print_gui(f"You can't afford to buy the {product}.")
        else:
            print_gui(f"You can't buy {item} from {character}")

#sell items to any character in exchange for money
@when("sell ITEM to CHARACTER", context=get_context())
@when("sell ITEM CHARACTER", context=get_context())
def sell_item(item, character):

    product = game_items.inventory.find(item)
    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui(f"There is no {char} here.")
    elif product == game_items.gungnir_spear:
        print_gui(random.choice(["You are not going to give away your most valuable item, are you?", "You cannot give away the Gungnir spear", "You will throw the Gungnir just like that?"]))
    elif not product:
        print_gui(f"You don't have {item} in your inventory.")
    else:
        print_gui(random.choice([f"{char.name} reaches for {char.gen_pronouns} pockets, and gives you {product.cost} florens to buy your {product}.",
                                 f"You manage to sell your {product} to {char.name} for the fair price of {product.cost} florens."]))
        game_items.inventory.remove(product)
        game_items.floren_balance = game_items.floren_balance + product.cost

@when("give ITEM to CHARACTER", context=get_context())
@when("give ITEM CHARACTER", context=get_context())
@when("return ITEM to CHARACTER", context=get_context())
@when("return ITEM CHARACTER", context=get_context())
def give_item(item, character):

    product = game_items.inventory.find(item)
    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui(f"There is no {char} here.")
    elif product == game_items.gungnir_spear:
        print_gui(random.choice(["You are not going to give away your most valuable item, are you?", "You cannot give away the Gungnir spear", "You will throw the Gungnir just like that?"]))
    elif not product:
        print_gui(f"You don't have {item} in your inventory.")
    else:
        if char.is_alive:
            print_gui(f"You reach to your pockets, and give {product} to {char.name}.")
            char.items.add(product)
            game_items.inventory.remove(product)
            check_mission_completed()
        else:
            print_gui(f"You reach to your pockets, and leave {product} to {char.name}'s corpse.")
        
        #game_rooms.test_side_quest.check_success(game_rooms.current_room, inventory)


@when("name", context=get_context())
@when("names", context=get_context())
def intro_character():
    for char in game_rooms.current_room.characters:
        if char.is_alive:
            if char.previously_met == False:
                print_gui(f"{char.name}>> "+dialog.character_introduction(char))
                char.previously_met = True
            else:
                print_gui(f"{char.name}>> "+random.choice(["You already know me.", "Did you forget who I am?", "Are you ok? You don't remember me?"]))
        else:
            pass

@when("job CHARACTER", context=get_context())
@when("jobs CHARACTER", context=get_context())
@when("task CHARACTER", context=get_context())
@when("tasks CHARACTER", context=get_context())
@when("quest CHARACTER", context=get_context())
@when("quests CHARACTER", context=get_context())
@when("mission CHARACTER", context=get_context())
@when("missions CHARACTER", context=get_context())
def take_quest(character):
    char = game_rooms.current_room.characters.find(character)
    if char:
        if char.is_alive:
            if char.favour:
                char_favour = char.favour
                #print("character side quest: ",char_favour)
                mission = game_rooms.Mission(char_favour[0], char_favour[1], [int(char_favour[2]), int(char_favour[3])], char)
                print_gui(f"{char.name}>>"+dialog.give_task(mission))
                char.mission = mission
                game_rooms.active_missions.append(mission)
                update_map_position(int(char_favour[2]), int(char_favour[3]), "black")
            else:
                print_gui(f"{char.name}>> I don't have any jobs for you.")
        else:
            print_gui("A dead man cannot give you a job.")
    else:
        print_gui(f"There is no {character} here.")
    


#rent a ship for fast travel between continents
@when("rent ship", context=get_context())
@when("rent boat", context=get_context())
@when("buy ship", context=get_context())
@when("buy boat", context=get_context())
def rent_ship():
    current_context = get_context()

    try:
        char = game_rooms.current_room.characters.find("captain")
        if game_items.floren_balance>=200:
            print_gui(f"{char.name}>> I will depart tomorrow at dawn for Vestenvarth, this here is my longship, Freya's Grace. Don't be late, or else we'll leave without you.\n")
            print_gui("The next day, you board the longship early in the morning, and Freya's Grace starts sailing across the Northern Sea.\n")
            print_gui("~~Ευχαριστώ για τη δοκιμή της Beta~~")
 
            #close_game()
        else:
            print_gui(f"{char.name}>> You don't have the coin, stranger. For 200 florens you can join.")
    except:
        print_gui("There is no one here that can help you rent a ship.")



@when("where TOPIC CHARACTER", context=get_context())
@when("find TOPIC CHARACTER", context=get_context())
def ask_about_topic(topic, character):
    char = game_rooms.current_room.characters.find(character)
    if not char:
        print_gui("You ask, yet there is no one here to answer.")
    elif char.is_alive:
        if char.type == "monster":
            print_gui(f"You ask the {char.name}, but you don't think that it is capable of actually answering.")
        else:
            print_gui(f"{char.name}>> "+dialog.find_topic(topic, char))
    else:
        print_gui(f"{char.name} is dead.")


# Define your movement commands
@when("go DIRECTION")
@when("north", direction="north")
@when("south", direction="south")
@when("east", direction="east")
@when("west", direction="west")
@when("northeast", direction="northeast")
@when("northwest", direction="northwest")
@when("southeast", direction="southeast")
@when("southwest", direction="southwest")
@when("enter", direction="enter")
@when("leave", direction="leave")
# @when("n", direction="north")
# @when("s", direction="south")
# @when("e", direction="east")
# @when("w", direction="west")
def go(direction: str):
    """Processes your moving direction

    Arguments:
        direction {str} -- which direction does the player want to move
    """



    # Is there an exit in that direction?
    next_room = game_rooms.current_room.exit(direction)
    if next_room:
        # Is the door locked?
        if (
            direction in game_rooms.current_room.locked_exits
            and game_rooms.current_room.locked_exits[direction]):
            if next_room.type == '0':
                print_gui(f"~You stand before the water on your {direction}, but you cannot swim.~")
            else:
                print_gui(f"~You can't go {direction} --- the door is locked.~")
        else:
            # Clear the context if necessary
            current_context = get_context()
            # if current_context == "combat":
            #     say_gui(
            #         """You can't flee the battle, what are you, a coward?"""
            #     )
            # else:
            if current_context:
                # print_gui("Fare thee well, traveler!")
                set_context(None)
            x = game_items.x_coord
            y = game_items.y_coord
            game_rooms.current_room = next_room
            if direction == "enter" or direction == "leave":
                print_gui(f"~You {direction} the {game_rooms.current_room.title}~")
            else:
                print_gui(f"~You go {direction}.~")
            if direction == "north":
                game_items.x_coord -= 1
            elif direction == "south":
                game_items.x_coord += 1
            elif direction == "west":
                game_items.y_coord -= 1
            elif direction == "east":
                game_items.x_coord += 1
            elif direction == "northwest":
                game_items.x_coord -= 1
                game_items.y_coord -= 1
            elif direction == "southwest":
                game_items.x_coord += 1
                game_items.y_coord -= 1
            elif direction == "northeast":
                game_items.x_coord -= 1
                game_items.y_coord += 1
            elif direction == "southeast":
                game_items.x_coord += 1
                game_items.y_coord += 1
            try:
                repaint_old_tile(x, y, rooms_dict[f'({x}, {y})'])
                update_map_position(game_items.x_coord, game_items.y_coord, "red")
            except:
                pass
            update_current_location(game_rooms.current_room)
            look()

    # No exit that way
    else:
        print_gui(f"You can't go {direction}.")



# Define a prompt
def prompt():

    # Get possible exits
    exits_string = get_exits(game_rooms.current_room)

    # Are you in battle?
    if get_context() == "combat":
        prompt_string = f"HP: {game_items.hit_points} > "
    else:
        prompt_string = f"({game_rooms.current_room.title}) > "

    return f"""({exits_string}) {prompt_string}"""


def get_exits(room):
    exits = room.exits()

    exits_string = ""
    for exit in exits:
        exits_string += f"{exit[0].upper()}|"

    return exits_string[:-1]


# Start the game
if __name__ == "__main__":
    # No context is normal
    set_context(None)

    # Set the prompt
    prompt = prompt

    # What happens with unknown commands
    # no_command_matches = no_command_matches
    print_gui("You wake up in the middle of nowhere. You have no recollection of the past few days and your head is spinning. You are holding a golden spear and a strange scepter, two seemingly very expensive items that you could never afford as a simple sell-sword. Your fingertips of your left hand are covered in a black rot and you try desperately with the water from your pouch to wash this away, but with no luck.\n")

    # Look at your starting room
    look()

#bind all rectangles to a click event
canvas.bind("<Button-1>", fast_travel)

game_items.inventory.add(game_items.steel_sword)
game_items.inventory.add(game_items.gungnir_spear)
game_items.inventory.add(game_items.apple)
game_items.inventory.add(game_items.crossbow)
#print_gui("Welcome to "+ game_rooms.current_room.super_area_title)
#dummy_monster = characters.generate_monster("vampire")
dummy_bandit = characters.generate_enemy_npc()
game_rooms.rooms_obj[4][8].characters.add(dummy_bandit)
game_rooms.rooms_obj[6][43].characters.add(characters.audafir)
# print(dummy_bandit.intelligence)
# print(dummy_monster)
#game_rooms.rooms_obj[4][10].characters.add(dummy_monster)
# dummy_monster2 = characters.generate_monster("vampire")
# game_rooms.rooms_obj[4][11].characters.add(dummy_monster2)
game_rooms.active_missions.append(main_missions.prologue)
root.mainloop()