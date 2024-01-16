import csv
import tkinter as tk
import random

terrain_types = {'0': "#0c17ad", '1': "#12bde3", '2': "#de9e31", '3': "#53c90e", '4': "#21420d", '5': "#9c741f", '6': "#453411", '7': "white"}

game_rooms = {}
rectangle_ids = {}


def create_tile_map(canvas, rows, columns, rect_width, rect_height):
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
    return rectangles

with open('assets/map_test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        game_rooms[row['key']] = row['value']


game_map = tk.Tk()
game_map.geometry("700x700")
game_map.title("Game Map")

# Create a Canvas widget
canvas = tk.Canvas(game_map, width=500, height=500)
canvas.pack()

# Call the function to create the grid of rectangles
game_rooms = create_tile_map(canvas, 50, 50, 10, 10)

game_map.mainloop()
