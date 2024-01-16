import tkinter as tk
import re
from adventurelib import *
from adventurelib import Pattern, commands, _available_commands
import textwrap
import command_filter
# import map_loader
import csv
import customtkinter
import random
import save_game
import game_rooms
import main_missions
import game_items
import characters

terrain_types = {'0': "#0c17ad", '1': "#12bde3", '2': "#de9e31", '3': "#53c90e", '4': "#21420d", '5': "#9c741f", '6': "#453411", '7': "white"}
# game_rooms = {}
rectangle_ids = {}
rectangle_coords = {}

#active_missions = []
completed_missions = []

text_font = 'cambria'
text_size = 15
num_of_lines = 0 #number of line we are currently in game, in text output

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green") 
#defining the root window
root = customtkinter.CTk()
root.geometry("1250x750")
root.title("Eternal Quest Pre-Alpha")

#defining variables and functionality of input box
user_input = customtkinter.StringVar()

#function to replace print, so that the output goes to gui
def print_gui(str):
    output_text.insert("end", str)
    output_text.insert("end",'\n')
    output_text.see(tk.END)

#function to replace say function of adventurelib (straight from adventurelib sourcecode)
def say_gui(msg):
    """Print a message.

    Unlike print(), this deals with de-denting and wrapping of text to fit
    within the width of the window.

    Paragraphs separated by blank lines in the input will be wrapped
    separately.

    """
    msg = str(msg)
    msg = re.sub(r'^[ \t]*(.*?)[ \t]*$', r'\1', msg, flags=re.M)
    # width = get_terminal_size()[0]
    paragraphs = re.split(r'\n(?:[ \t]*\n)', msg)
    formatted = (textwrap.fill(p.strip(), width=720) for p in paragraphs)
    output_text.insert("end", '\n\n'.join(formatted))
    output_text.insert("end", '\n')
    output_text.see(tk.END)

def _handle_command(cmd):
    #Handle a command typed by the user.
    ws = cmd.lower().split()

    for pattern, func, kwargs in _available_commands():
        args = kwargs.copy()
        matches = pattern.match(ws)
        if matches is not None:
            args.update(matches)
            func(**args)
            break
    else:
        print_gui(f"I don't understand '{cmd}'")
    print()

def submit_command(event):
    #cmd = user_input.get().strip()
    inp = user_input.get()
    cmd = command_filter.filter_command(user_input.get()).strip()
    print("The command is " + cmd)
    _handle_command(cmd)
    user_input.set("")

    #write the user commands in user logs folder
    logs = open("user logs/logs.txt", "a")
    #logs.write(user_input.get()+"\n")
    logs.write(inp)
    logs.write("\n")
    logs.close()

#bind enter key to input box
def enter_bind(event):
    submit_command()

#menu functions
# def donothing():
#     pass

# def save_game():
#     pass

# def load_game():
#     pass

#load game map
def open_map():
    
    game_rooms = {}
    with open('assets/map_test.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            game_rooms[row['key']] = row['value']


    # game_map = customtkinter.CTkToplevel()
    # game_map.geometry("700x700")
    # game_map.title("Game Map")
    global canvas
    # Create a Canvas widget
    # canvas = customtkinter.CTkCanvas(game_map, width=500, height=500)
    # canvas.pack()
    canvas = customtkinter.CTkCanvas(root, width=500, height=500)
    canvas.grid(row=1, column=10, rowspan=2, padx=10, pady=2)

    # Call the function to create the grid of rectangles
    game_rooms = create_tile_map(canvas, 50, 50, 10, 10, game_rooms)
    update_map_position(4, 9, "red")



    
#create tiles based on the values of map.csv
def create_tile_map(canvas, rows, columns, rect_width, rect_height, game_rooms):
    rectangles = {}
    for row in range(rows):
        for column in range(columns):
            
            tile_color = terrain_types[game_rooms[f'({row}, {column})']]
            x1 = column * rect_width 
            y1 = row * rect_height
            x2 = x1 + rect_width
            y2 = y1 + rect_height
            rectangle_ids[(row,column)] = canvas.create_rectangle(x1, y1, x2, y2, fill=tile_color)
            rectangles[(row, column)] = "mpla"
            rectangle_coords[(row, column)] = x1, y1, x2, y2
            
    return rectangles

#paint tail in red to show current player position in map
def update_map_position(x, y, fillcolor):
    rect_id = rectangle_ids.get((x, y))
    if rect_id is not None:
        canvas.itemconfig(rect_id, fill=fillcolor)

def repaint_old_tile(x, y, terrain_score):
    rect_id = rectangle_ids.get((x,y))
    if rect_id is not None:
        canvas.itemconfig(rect_id, fill=terrain_types[terrain_score])

def close_game():
    root.destroy()

def end_game():
    endpopup = customtkinter.CTkToplevel(root)
    endpopup.geometry = "300x300"
    endpopup.title = "End of Demo"
    customtkinter.CTkLabel(endpopup, text="~~Ευχαριστώ που συμμετείχατε στη δοκιμή της Beta~~").pack()
    customtkinter.CTkButton(endpopup, text="Έξοδος", command=close_game).pack()

def save_gui():
    save_game.save()

def load_gui():
    output_text.delete("0.0", "end")
    x = game_items.x_coord
    y = game_items.y_coord
    save_game.load()
    print_gui("Last save file loaded ~~~ Enter 'look' to start")
    player_hit_points.configure(text="HP: "+str(game_items.hit_points))
    karma.configure(text="Darkness growth: "+str(game_items.negative_karma))
    current_main_obj.configure(text="Current objective: "+main_missions.current_main_mission.short_description)
    update_map_position(game_items.x_coord, game_items.y_coord, "red")
    repaint_old_tile(x, y, game_rooms.rooms_obj[x][y].type)
    for mission in main_missions.main_missions.values():
        if mission != main_missions.current_main_mission:
            mission.completed = True
            game_rooms.active_missions.append(mission)
        else:
            break
    if main_missions.current_main_mission.type == "Prologue":
        game_rooms.rooms_obj[6][43].characters.add(characters.audafir)
    elif main_missions.current_main_mission.type == "Chapter I":
        characters.audafir.previously_met = True
        game_rooms.citadel.characters.add(characters.grandmaster)
    elif main_missions.current_main_mission.type == "Chapter II":
        characters.audafir.previously_met = True
        characters.captain.previously_met = True
        game_rooms.citadel.characters.add(characters.grandmaster)
    elif main_missions.current_main_mission.type == "Chapter III" or main_missions.current_main_mission.type == "Chapter IV":
        characters.audafir.previously_met = True
        characters.captain.previously_met = True
        characters.spy.previously_met = True
        game_rooms.citadel.characters.add(characters.grandmaster)
    elif main_missions.current_main_mission.type == "Chapter V":
        characters.audafir.previously_met = True
        characters.captain.previously_met = True
        characters.spy.previously_met = True
        characters.grandmaster.previously_met = True

    #ADD MAIN MISSION CHARACTERS AND CAPTAINS


# Add a Scrollbar(horizontal)
vert_scrollbar=customtkinter.CTkScrollbar(root, orientation='vertical')
#v.pack(side=tk.RIGHT, fill='y')

input_entry = customtkinter.CTkEntry(root, textvariable=user_input, font=(text_font, text_size, 'bold'), width= 570)
input_entry.bind("<Return>", submit_command)
enter_btn = customtkinter.CTkButton(root, text="Enter", command = submit_command, text_color="black", font=(text_font, text_size, 'bold'))
#output_text = tk.Text(root, bg = 'dark grey', yscrollcommand=vert_scrollbar.set, font=(text_font, text_size))
output_text = customtkinter.CTkTextbox(root, font=(text_font, text_size), width=710, height=500, wrap="word")

#not a great way to make output read-only
output_text.bind("<Key>", lambda e: "break")


vert_scrollbar.configure(command=output_text.yview)

#adding a top menu

# menubar = tk.Menu(root, background="blue")
# root.configure(menu=menubar)

# filemenu = tk.Menu(menubar, tearoff=0, background="blue")
# filemenu.add_command(label="Save", command=save_game)
# filemenu.add_command(label="Load", command=load_game)
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=root.quit)
# menubar.add_cascade(label="File", menu=filemenu)

# helpmenu = tk.Menu(menubar, tearoff=0)
# helpmenu.add_command(label="User Command Guide", command=donothing)
# helpmenu.add_command(label="About", command=donothing)
# menubar.add_cascade(label="Help", menu=helpmenu)

# journalmenu = tk.Menu(menubar, tearoff=0)
# journalmenu.add_command(label="Quests", command=donothing)
# journalmenu.add_command(label="Characters", command=donothing)
# journalmenu.add_command(label="Locations", command=donothing)
# journalmenu.add_command(label="Bestiary", command=donothing)
# journalmenu.add_command(label="Map", command=open_map)
# menubar.add_cascade(label="Journal", menu=journalmenu)

question_mark = tk.PhotoImage(file="assets/question.png")

def write_logs(txt):
    global journal_textbox
    journal_textbox.delete("0.0","end")
    if txt == "Locations":
        journal_textbox.insert("0.0", "By travelling to new locations, your journal will be updated.\n\n\n")
        for town in game_rooms.towns:
            cur_visited_status = False
            
            for area in town:
                cur_visited_status = cur_visited_status or area.visited
            #print(f"{town[0].super_area_title}: {cur_visited_status}")
            if cur_visited_status:
                journal_textbox.insert("0.0", town[0].super_area_title+"\n\n"+game_rooms.locations_journal_entries[area.super_area_title]+"\n\n\n")
        #journal_textbox.insert("0.0", game_rooms.towns[0][0].super_area_title)
    #journal_textbox.insert("0.0", txt)
    elif txt == "Characters":
        journal_textbox.insert("0.0", "As you meet new people in your journey, the journal will be updated.\n\n\n")
        for character in characters.main_mission_characters:
            if character.previously_met:
                if not character.journal_entry:
                    pass
                else:
                    journal_textbox.insert("0.0", character.name+":\n\n"+character.journal_entry+"\n\n\n")
    elif txt == "Bestiary":
        journal_textbox.insert("0.0", "You can learn more about monsters by asking the locals.\n\n\n")
        #print(characters.monster_knowledge)
        for monster in characters.all_monster_types:
            if characters.monster_knowledge[monster]:
                journal_textbox.insert("0.0", monster+"\n\n"+characters.bestiary_entries[monster]+"\n\n\n")

#tutorial window
def open_tutorial():
    tutorial = customtkinter.CTkToplevel(root)
    tutorial.geometry("700x700")
    tutorial.attributes("-topmost","true")
    with open('assets/tutorial.txt','r', encoding='utf-8') as tutorial_txt:
        text = tutorial_txt.read()

    tutorial_textbox = customtkinter.CTkTextbox(tutorial, width=680, height=680, wrap="word", font=(text_font, text_size))
    tutorial_textbox.pack()
    tutorial_textbox.insert("1.0", text)

#journal window, info about characters, quests and locations
def open_journal():
    journal = customtkinter.CTkToplevel(root)
    journal.geometry("650x650")
    journal.attributes("-topmost","true")
    journal.title("Journal")
    global journal_textbox, characters_button, quests_button, locations_button, bestiary_button
    journal_textbox = customtkinter.CTkTextbox(journal, width=600, height=600, font=(text_font, text_size), wrap="word")
    journal_textbox.insert("0.0", "Your journal will be updated as you encounter new people, towns and monsters.")
    characters_button = customtkinter.CTkButton(journal, width=45, height=30, border_width=0, corner_radius=8, command=lambda: write_logs("Characters"), text="Characters", text_color="black").grid(row=0, column=0)
    locations_button = customtkinter.CTkButton(journal, width=45, height=30, border_width=0, corner_radius=8, command=lambda: write_logs("Locations"), text="Locations", text_color="black").grid(row=0, column=1)
    bestiary_button = customtkinter.CTkButton(journal, width=45, height=30, border_width=0, corner_radius=8, command=lambda: write_logs("Bestiary"), text="Bestiary", text_color="black").grid(row=0, column=2)
    journal_textbox.grid(row=1, column=0, columnspan=4, padx=2, pady=2)


def quest_select(event):
    # get all selected indices
    global active_quest_listbox, quest_textbox
    selected_index = active_quest_listbox.curselection()
    quest_textbox.delete("0.0","end")
    quest_textbox.insert("0.0",game_rooms.active_missions[selected_index[0]].description)
    try:
        update_map_position(game_rooms.active_missions[selected_index[0]].x, game_rooms.active_missions[selected_index[0]].y, "black")
        update_map_position(game_rooms.active_missions[selected_index[0]].quest_giver.x, game_rooms.active_missions[selected_index[0]].quest_giver.y, "yellow")
    except AttributeError:
        pass

def open_quests():
    global active_quest_listbox, quest_textbox
    quests = customtkinter.CTkToplevel(root)
    quests.geometry("1000x650")
    quests.attributes("-topmost","true")
    quests.title("Quests")
    active_quest_listbox = tk.Listbox(quests, selectmode=tk.SINGLE, background="grey", font=(text_font, 12))
    #completed_quest_listbox = tk.Listbox(quests, selectmode=tk.SINGLE, width=25, height=300, background="red", font=(text_font, 12))
    quest_textbox = customtkinter.CTkTextbox(quests, font=(text_font, text_size), wrap="word")
    quest_textbox.insert("0.0","Quest Information")
    # for i in range(15):
    #     active_quest_listbox.insert(i, random.choice(["mpla", "mpla mpla", "quest", "fetch quest", "escort quest"]))
    #     completed_quest_listbox.insert(i, random.choice(["mpla", "mpla mpla", "quest", "fetch quest", "escort quest"]))
    for i in range(len(game_rooms.active_missions)):
        title = game_rooms.active_missions[i].title
        if game_rooms.active_missions[i].completed:
            title = title + " - Completed"
        active_quest_listbox.insert(i, title)
    active_quest_listbox.bind("<<ListboxSelect>>", quest_select)
    active_quest_listbox.grid(row=0, column=0, sticky="nsew")
    #completed_quest_listbox.grid(row=1, column=0)
    quest_textbox.grid(row=0, column=1, sticky="nsew")
    quests.grid_columnconfigure(0, weight=1)
    quests.grid_columnconfigure(1, weight=1)
    quests.grid_rowconfigure(0, weight=1)



tutorial_button = customtkinter.CTkButton(master=root, width=45, height=30, border_width=0, corner_radius=8, command=open_tutorial, text="Tutorial", text_color="black", font=(text_font, text_size, 'bold'))
journal_button = customtkinter.CTkButton(master=root, width=45, height=30, border_width=0, corner_radius=8, command=open_journal, text="Journal", text_color="black", font=(text_font, text_size, 'bold'))
quests_button = customtkinter.CTkButton(master=root, width=45, height=30, border_width=0, corner_radius=8, command=open_quests, text="Quests", text_color="black", font=(text_font, text_size, 'bold'))
save_button = customtkinter.CTkButton(master=root, width=45, height=30, border_width=0, corner_radius=8, command=save_gui, text="Save", text_color="black", font=(text_font, text_size, 'bold'))
load_button = customtkinter.CTkButton(master=root, width=45, height=30, border_width=0, corner_radius=8, command=load_gui, text="Load", text_color="black", font=(text_font, text_size, 'bold'))
current_location = customtkinter.CTkLabel(master=root, text="West Nordreyjar", font=(text_font, text_size, 'bold'))
player_hit_points = customtkinter.CTkLabel(master=root, text="HP: 20", font=(text_font, text_size, 'bold'))
player_weight = customtkinter.CTkLabel(master=root, text="Total Weight: 7", font=(text_font, text_size, 'bold'))
current_main_obj = customtkinter.CTkLabel(master=root, text="Current objective: "+main_missions.current_main_mission.short_description, font=(text_font, text_size, 'bold'))
karma = customtkinter.CTkLabel(master=root, text="Darkness growth: "+str(game_items.negative_karma), font=(text_font, text_size, 'bold'))

#placing gui elements
tutorial_button.grid(row=0, column=0, padx=2, pady=2)
journal_button.grid(row=0, column=1, padx=2, pady=2)
quests_button.grid(row=0, column=2, padx=2, pady=2)
save_button.grid(row=0, column=3, padx=2, pady=2)
load_button.grid(row=0, column=4, padx=2, pady=2)
output_text.grid(row=1, column=0, columnspan=9, padx=2, pady=2)
input_entry.grid(row=2, column=0, columnspan=8, padx=2, pady=2)
enter_btn.grid(row=2, column=8, padx=2, pady=2)
#vert_scrollbar.grid(row=1, column=9)
current_location.grid(row=3, column=10, padx=2, pady=2)
player_hit_points.grid(row=3, column=0, padx=2, pady=2)
player_weight.grid(row=3, column=1, padx=2, pady=2)
current_main_obj.grid(row=4, column=0, padx=2, pady=2, columnspan=4)
karma.grid(row=5, column=0, padx=2, pady=2)
open_map()

# root.mainloop()