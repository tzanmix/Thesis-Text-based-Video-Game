import random
import customtkinter
import json
# grammar = {
#     "Start": ["Root"],
#     # "Mission": ["Objective", "Location"],
#     "Root": ["NPCQ1 PlayerA1 NPCA1", "NPCQ1 PlayerA2 NPCA2", "NPCQ1 PlayerA3 NPCA3"],
#     "NPCQ1": ["What can I do for you, stranger?", "Is there anything I can do for you traveller?", "What do you want?"],
#     "PlayerA1": ["Where can I find the captain?", "Where can I find a ship?", "Where are the ancient elven ruins?"],
#     "PlayerA2": ["Do you have any jobs for me?", "Do you have a quest for me?", "Any jobs for me?"],
#     "PlayerA3": ["Who are you?", "What's your name, stranger?"],
#     "NPCA1": ["You can find it south of here.", "North of here."],
#     "NPCA2": ["As a matter of fact, I do, last week a monster attacked this region.", "I can reward you handsomely if you track down and kill the bandit."],
#     "NPCA3": ["I am the NPC of NPCtopia.", "My name is none of your business."]
# }

# dialog_tree = []

# def generate_dialog(grammar, symbol):
#     if symbol not in grammar:
#         return symbol  # Return terminal symbol
    
#     expansion = random.choice(grammar[symbol])  # Choose a random production rule
#     print("expansion: ", expansion)
#     dialog_tree.append(expansion)
#     components = expansion.split()
#     generated = [generate_dialog(grammar, component) for component in components]
#     return " ".join(generated)

# objective = generate_dialog(grammar, "Start")
# dialog = objective.split(",")


# print("Mission: ", dialog_tree)

class DialogNode:
    def __init__(self, text, speaker, choices=None):
        self.text = text
        self.speaker = speaker
        self.choices = choices if choices else []

node1 = DialogNode("Hello, adventurer!", "NPC")
node2 = DialogNode("What can I do for you?", "NPC")
node3 = DialogNode("Tell me about the quest.", "Player")
node4 = DialogNode("The quest is dangerous. Are you sure you want to proceed?", "NPC")
node5 = DialogNode("Yes, I'm ready.", "Player")
node6 = DialogNode("No, I changed my mind.", "Player")
node7 = DialogNode("Mpla mpla", "Player")

node8 = DialogNode("Great, fetch item", "NPC")
node9 = DialogNode("Goodbye", "Player")
node10 = DialogNode("Bye", "Player")

node1.choices.append(node2)
node2.choices.append(node3)
node3.choices.append(node4)
node4.choices.extend([node5, node6, node7])

node5.choices.append(node8)
node8.choices.extend([node9, node10])

class DialogManager:
    def __init__(self, start_node):
        self.current_node = start_node

    def get_current_node(self):
        return self.current_node

    def choose_option(self, choice_index):
        if choice_index < len(self.current_node.choices):
            self.current_node = self.current_node.choices[choice_index]

def traverse_tree(branch_index):
    global choice_buttons, current_node
    # current_node = current_node.choices[branch_index]
    # print(current_node.text)
    # print(current_node.choices[0].text)
    try:
        print("You clicked: ", current_node.choices[branch_index].text)
        print("length: ", len(current_node.choices[branch_index].choices))
        random_npc_answer = random.randint(0,len(current_node.choices[branch_index].choices))
        print(random_npc_answer)
        random_npc_answer = random_npc_answer-1
        new_node = current_node.choices[branch_index].choices[random_npc_answer]
        label.configure(text = new_node.text)
        for j in range(len(choice_buttons)):
            choice_buttons[j].destroy()
        choice_buttons = []
        for i in range(len(new_node.choices)):
            choice_button = customtkinter.CTkButton(root, width=700, height=50, text=new_node.choices[i].text, command= lambda i=i: traverse_tree(i))
            choice_buttons.append(choice_button)
            choice_button.pack(padx=5, pady=10)
        current_node = new_node
    except IndexError:
        for j in range(len(choice_buttons)):
            choice_buttons[j].destroy()
        choice_button = customtkinter.CTkButton(root, width=700, height=50, text="Goodbye", command= lambda: root.destroy())
        label.configure(text = "Ok then, goodbye traveller.")
        choice_button.pack(padx=5, pady=10)
    


#random dialog tree generator
def generate_dialog_tree(depth, max_depth):
    if depth >= max_depth:
        return DialogNode("This is the end of the dialog.", "System")

    text = f"This is dialog node at depth {depth}."
    speaker = "NPC"

    choices = []
    num_choices = random.randint(1, 3)  # Randomly determine the number of choices

    for _ in range(num_choices):
        child_node = generate_dialog_tree(depth + 1, max_depth)
        choices.append(child_node)

    return DialogNode(text, speaker, choices)

def traverse_dialog_tree(node, indent=0):
    print("  " * indent + f"{node.speaker}: {node.text}")
    for choice in node.choices:
        traverse_dialog_tree(choice, indent + 1)


#load dialog tree from json to instances of class DialogNode
def load_json_to_dialog_node(json_data):
    if isinstance(json_data, dict):
        text = json_data.get("text", "")
        speaker = json_data.get("speaker", "")
        choices_data = json_data.get("choices", {})

        choices = [
            load_json_to_dialog_node(choices_data[key])
            for key in choices_data
        ]

        return DialogNode(text, speaker, choices)

    # If the JSON data is not a dictionary, return a leaf node
    return DialogNode(json_data, "Player")



# dialog_tree = generate_dialog_tree(0, 3)
# traverse_dialog_tree(dialog_tree)

with open("dialog_trees.json","r") as json_file:
    tree = json.load(json_file)

dialog_tree = load_json_to_dialog_node(tree)

root = customtkinter.CTk()
root.geometry("700x700")
root.title("Leif Erikson")
current_node = dialog_tree
label = customtkinter.CTkLabel(root, width=100, height=100, text=current_node.text)
label.pack()
choice_buttons = []
for i in range(len(current_node.choices)):
    choice_button = customtkinter.CTkButton(root, width=700, height=50, text=current_node.choices[i].text, command= lambda i=i: traverse_tree(i))
    choice_buttons.append(choice_button)
    choice_button.pack(padx=5, pady=10)

root.mainloop()