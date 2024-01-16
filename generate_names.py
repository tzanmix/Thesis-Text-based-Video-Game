import random

#generate Sea People names
elf_family_names=[]
elf_male_names=[]
elf_female_names=[]
# Define the context-free grammar rules
grammar = {
    "<name>": ["<nameStart> <nameMiddle0to2> <nameEnd>"],
	"<nameMiddle0to2>": ["","<nameMiddle>", "<nameMiddle> <nameMiddle>"],
	"<nameStart>": ["<nsCons> <nmVowel>", "<nsCons> <nmVowel>", "<nsCons> <nmVowel>", "<nsVowel>"],
	"<nameMiddle>": ["<nmCons> <nmVowel>"],
	"<nameEnd>": ["<neCons> <neVowel>", "<neCons>", "<neCons>"],
	"<nsCons>": ["J", "M", "P", "N", "Y", "D", "F"],
	"<nmCons>": ["l", "m", "lm", "th", "r", "s", "ss", "p", "f", "mb", "b", "lb", "d", "lf"],
	"<neCons>": ["r", "n", "m", "s", "y", "l", "th", "b", "lb", "f", "lf"],
	"<nsVowel>": ["A", "Au", "Ei"],
	"<nmVowel>": ["a", "e", "i", "o", "u", "au", "oa", "ei"],
	"<neVowel>": ["e", "i", "a", "au"]
}

# Function to generate names using the grammar
def generate_name(grammar, symbol):
    if symbol not in grammar:
        return symbol  # Return terminal symbol
    
    expansion = random.choice(grammar[symbol])  # Choose a random production rule
    components = expansion.split()
    generated = [generate_name(grammar, component) for component in components]
    return "".join(generated)

# Generate family names
for i in range(random.randint(23,42)):
    name = generate_name(grammar, "<name>")
    elf_family_names.append(name)
    # print(name)

for j in range(random.randint(25,30)):
    male_name = generate_name(grammar, "<name>")
    elf_male_names.append(male_name)

for k in range(random.randint(25,30)):
    male_name = generate_name(grammar, "<name>")
    elf_female_names.append(male_name)

