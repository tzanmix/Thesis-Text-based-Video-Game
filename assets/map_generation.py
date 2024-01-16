import tkinter as tk
import random
import csv

# colors: hill, high mountain, plain, forest, desert, sea/river/lake, ocean
colors = ["#9c741f", "#453411", "#53c90e", "#21420d", "#de9e31", "#12bde3", "#0c17ad"]
# terrain_types = {"#9c741f": "hill", "#453411": "mountain", "#53c90e": "plain", "#21420d": "forest", 
#                 "#de9e31": "desert", "#12bde3": "water", "#0c17ad": "ocean"}
terrain_scores = {"ocean": 0, "water": 1, "desert": 2, "plain": 3, "forest": 4, "hill": 5, "mountain": 6}
terrain_types = {"#0c17ad": 0, "#12bde3": 1, "#de9e31": 2,  "#53c90e": 3, "#21420d": 4, "#9c741f": 5, "#453411": 6}
#add town/city tiles to terrain types
final_terrain_types = {"#0c17ad": 0, "#12bde3": 1, "#de9e31": 2,  "#53c90e": 3, "#21420d": 4, "#9c741f": 5, "#453411": 6, "white": 7}

rectangle_ids = {}
rectangle_coords = {}
#INITIALISE GRID WITH OCEAN AND WATER TILES
def create_tile_grid(canvas, rows, columns, rect_width, rect_height):
    rectangles = {}
    for row in range(rows):
        for column in range(columns):
            #tile_color = random.choices(colors, [1, 1, 1, 1, 1, 1, 94], k=1)[0]
            #tile_color = random.choice(colors)
            tile_color = random.choices(["#0c17ad","#12bde3"],[90,10],k=1)[0]
            x1 = column * rect_width 
            y1 = row * rect_height
            x2 = x1 + rect_width
            y2 = y1 + rect_height
            rectangle_ids[(row, column)] = canvas.create_rectangle(x1, y1, x2, y2, fill=tile_color, tags=f'{row},{column}')
            rectangle_coords[(row, column)] = x1, y1, x2, y2
            
            rectangles[(row, column)] = terrain_types[tile_color]
    return rectangles

def change_tile_color(row, column, new_color):
    rect_id = rectangle_ids.get((row, column))
    if rect_id is not None:
        canvas.itemconfig(rect_id, fill=new_color)

#GAME OF LIFE VARIATION FUNCTIONS

#count alive neighbours
#alive neighbours are the neighbours with higher terrain score
def count_neighbours(x,y):
    s=0
    for j in range(-1,2):
        try:
            if game_rooms[(x-1),(y+j)]==game_rooms[x,y]+1:
                s=s+1
        except KeyError: pass
    for j in range(-1,2):
        try:
            if game_rooms[(x+1),(y+j)]==game_rooms[x,y]+1:
                s=s+1
        except KeyError: pass
    try:
        if game_rooms[(x),(y-1)]==game_rooms[x,y]+1:
            s=s+1
    except KeyError: pass
    try:
        if game_rooms[(x),(y+1)]==game_rooms[x,y]+1:
            s=s+1
    except KeyError: pass
    return s



def game_start():
    for i in range(50):
        for j in range(50):
            #current_game_room_score = terrain_scores[game_rooms[(i),(j)]]
            if count_neighbours(i,j)==3:  #exactly three neighbours: add terrain score
                if game_rooms[(i),(j)]<6:
                    game_rooms[(i),(j)] += 1
                else:
                    game_rooms[(i),(j)] = 0
                #game_rooms[(i),(j)] = list(terrain_scores.values()).index(current_game_room_score)
            elif count_neighbours(i,j)>3: #more than 3 neighbours: subtract terrain score
                if game_rooms[(i),(j)]>0:
                    game_rooms[(i),(j)] -= 1
                else:
                    game_rooms[(i),(j)] = 6
                #game_rooms[(i),(j)] = list(terrain_scores.values()).index(current_game_room_score)
            elif count_neighbours(i,j)<2: #less than 2 neighbours: subtract terrain score
                if game_rooms[(i),(j)]>0:
                    game_rooms[(i),(j)] -= 1
                else:
                    game_rooms[(i),(j)] = 3
                #game_rooms[(i),(j)] = list(terrain_scores.values()).index(current_game_room_score)

#change color of tile on click
def change_click_color(event):
    for rect_id, rect_coords in rectangle_coords.items():
        tile_id = rectangle_ids[rect_id]
        x1, y1, x2, y2 = rect_coords
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            canvas.itemconfig(tile_id, fill=current_color)
            game_rooms[rect_id] = final_terrain_types[current_color]
            

#by pushing one of the buttons, global var current_color changes value
def set_current_color(color):
    global current_color
    current_color = color
    print(current_color)

def save_map(tile_map):
    with open('assets/map_test.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)

        # Write the header (column names)
        csv_writer.writerow(["key", "value"])

        # Write the dictionary data as rows
        for key, value in tile_map.items():
            csv_writer.writerow([key, value])
    

# Create the main application window
root = tk.Tk()
root.title("Rectangle Grid")
root.geometry("900x900")

# Create a Canvas widget
canvas = tk.Canvas(root, width=750, height=750)
canvas.grid(row=0, column=0, columnspan=7)

#bind all canvas tiles to mouse click
canvas.bind("<Button-1>", change_click_color)

# Call the function to create the grid of rectangles
game_rooms = create_tile_grid(canvas, 50, 50, 15, 15)
ocean_color = tk.Button(root, text="Ocean Tile", command = lambda: set_current_color("#0c17ad"))
ocean_color.grid(row=1, column=0)
desert_color = tk.Button(root, text="Desert Tile", command = lambda: set_current_color("#de9e31"))
desert_color.grid(row=1, column=1)
plain_color = tk.Button(root, text="Plain Tile", command = lambda: set_current_color("#53c90e"))
plain_color.grid(row=1, column=2)
forest_color = tk.Button(root, text="Forest Tile", command = lambda: set_current_color("#21420d"))
forest_color.grid(row=1, column=3)
hill_color = tk.Button(root, text="Hill Tile", command = lambda: set_current_color("#9c741f"))
hill_color.grid(row=1, column=4)
mountain_color = tk.Button(root, text="Mountain Tile", command = lambda: set_current_color("#453411"))
mountain_color.grid(row=1, column=5)
town_color = tk.Button(root, text="Town Tile", command = lambda: set_current_color("white"))
town_color.grid(row=1, column=6)
save_button = tk.Button(root, text="Save", command= lambda: save_map(game_rooms))
save_button.grid(row=1, column=7)

print(game_rooms)


for i in range(50):
    game_start()



for i in range(50):
    for j in range(50):
        change_tile_color(i, j, list(terrain_types.keys())[list(terrain_types.values()).index(game_rooms[(i),(j)])])
        

for i in range(50):
    for j in range(50):
        if game_rooms[(i),(j)]==1:
            game_rooms[(i),(j)] = 0
            change_tile_color(i, j, "#0c17ad")


# Start the tkinter main loop
root.mainloop()

