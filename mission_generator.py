import random
import csv
import os

game_rooms = {}
locations = []
demo_locations = []
locations2 = ['4,8']

with open(os.getcwd()+'/assets/map_test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        game_rooms[row['key']] = row['value']



#all game locations in dry lands
for i in range(50):
    for j in range(50):
        if game_rooms[f'({i}, {j})']!= '0':
            locations.append(f'{i},{j}')

for i in range(50):
    for j in range(50):
        if game_rooms[f'({i}, {j})']!= '0' and i<=14:
            demo_locations.append(f'{i},{j}')

#mission location will be in an area around the character
def location_around_character(x, y):
    locations = []
    r = random.randint(3, 10)
    for i in range(-abs(r), r):
        for j in range(-abs(r), r):
            try:
                if i == 0 or j == 0:
                    pass
                elif game_rooms[f'({x+i}, {y+j})']!='0' and game_rooms[f'({x+i}, {y+j})']!='7':
                    locations.append(f'{x+i},{y+j}')
            except KeyError:
                pass
    return locations
            

def generate_objective(symbol, location):
    x_coord = location[0]
    y_coord = location[1]
    grammar = {
    "Start": ["Objective"],
    # "Mission": ["Objective", "Location"],
    "Objective": ["Fetch Item Location", "Escort FriendlyCharacter Location", "Eliminate EnemyCharacter Location", 
                  "Collect Treasure Location", "Hunt Monster Location"],
    "Location": location_around_character(x_coord, y_coord),
    #"Treasure": ["Item", "magic_item"],
    "Treasure": ["Item"],
    "Item": ["sword", "spear", "dagger", "shield", "warhammer", "axe"],
    "FriendlyCharacter": ["brother", "sister", "father", "elder"],
    "EnemyCharacter": ["bandit", "murderer", "thief"],
    "Monster": ["draugr", "wraith", "griffin", "vampire"]
}
    
    if symbol not in grammar:
        return symbol  # Return terminal symbol
    
    expansion = random.choice(grammar[symbol])  # Choose a random production rule
    components = expansion.split()
    generated = [generate_objective(component, location) for component in components]
    return ",".join(generated)

# objective = generate_objective("Start", [7, 9])
# mission = objective.split(",")


# print("Mission: ",mission)