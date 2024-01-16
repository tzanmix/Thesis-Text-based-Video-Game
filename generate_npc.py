import random
import generate_names
import json

nationalities=["Norse","Alnaasi","Nhudelhid","Elf","Daoine"]
genders=["male","female"]
#proffessions=["innkeep","soldier","bandit","merchant","duke","count","king","spy","blacksmith","sorcerer","traveler"]
proffessions = ["innkeeper", "soldier", "merchant", "blacksmith", "traveller", "farmer"]

arabic_male_names=["Muhammad","Ahmed","Ali","Omar","Hassan","Hussein","Khalid","Abdul","Hamza","Salim","Nizar","Farid","Rashid","Tariq","Karim","Jamal","Mustafa","Hisham","Yahya","Rami"]
arabic_female_names=["Aisha","Fatima","Khadija","Zainab","Mariam","Safiya","Hafsa","Sumayyah","Rabi'a","Layla","Noura","Jamila","Zahra","Hind","Saida","Salma","Asma","Maimuna","Firdaus","Zaynab"]

celtic_female_names=["Ceana", "Catriona", "Slaine", "Brid", "Eilish", "Bronach", "Fine", "Bearnas", "Eibhlin", "Eilis", "Cairistiona", "Liadan", "Caitlyn", "Feidhelm", "Mairead", "Ros", "Carlin", "Caitrin", "Beathag", "Mairead", "Sile", "Dearbhail", "Caoimhe", "Doileag", "Mairead", "Eithne", "Eubha", "Mor"]
celtic_male_names=["Cuirealan", "Naomhan", "Aodh", "Eadan", "Eochaidh", "Fionan", "Fionntan", "Fearghas", "Huisdean", "Maoilios", "Caorall", "Camran", "Cailean", "Cathal", "Machar", "Donovan", "Cairbre", "Dughall", "Ninnidh", "Murchadh", "Scotaidh", "Nilidh", "Angaidh", "Brian", "Flannagan", "Neasan", "Dubhshith", "Eacharn", "Taraghlan"]

nomad_male_names=["Altan","Batbayar","Bayarmaa","Bayarjargal","Bolor","Chinggis","Delger","Dulguun","Enkhjin","Erdene","Gantulga","Gerel","Jargal","Khaliun","Khulan","Munkhtuya","Naran","Nergui","Nyamjargal","Oyunbileg","Purev","Sodnom","Tseren","Tuguldur","Uyanga"]
nomad_female_names=["Altanchimeg","Altansarnai","Amarjargal","Ankhtsetseg","Badamlyanhua","Battsetseg","Bayalag","Bolormaa","Chimeg","Delbee","Enebish","Enkhmaa","Erdenetsetseg","Khaltmaa","Kheshigmaa","Mandakh","Margaderdene","Munkh","Munkhbayar","Naimanzuunadintsetseg","Narantuya","Narmandakh","Odval","Orghana","Saikhanbayar","Sarantsatsral","Soyolmaa","Togtuun","Tsogbayar","Tungalag","Üürtsaikh","Yagaan","Yargui","Zolzaya"]

norse_male_names=['Agmundr', 'Arni', 'Austri', 'Bekan', 'Birgir', 'Bjarni', 'Bjolan', 'Bjorn', 'Bragi', 'Bárdr', 'Dufgus', 'Dufbhakr', 'Egill', 'Eileifr', 'Eilaefr', 'Eiliefr', 'Einarr', 'Eiriekr', 'Ella', 'Erlingr', 'Eyfastr', 'Eysteinn', 'Finnr', 'Freyvidr', 'Fridthjofr', 'Frodi', 'Gandalfr', 'Gautstafr', 'Geirmundr', 'Geirr', 'Gizurr', 'Gjaflaugr', 'Grimr', 'Gunnarr', 'Gudbrandr', 'Gudmundr', 'Halldorr', 'Haraldr', 'Helgi', 'Hreidarr', 'Hrobjartr', 'Hrolfr', 'Hakon', 'Hogni', 'Hordr', 'Ingimarr', 'Ingjaldr', 'Jatvarðr', 'Kalman', 'Kinadr', 'Kjaran', 'Knutr', 'Kormakr', 'Leifr', 'Leidulfr', 'Magnus', 'Oddr', 'Ragnarr', 'Rikvidr', 'Runi', 'Sigurdr', 'Sindri', 'Skirnir', 'Steinarr', 'Stigr', 'Sveinn', 'Sverrir', 'Tadkr', 'Tryggvi', 'Vidbjorn', 'Vegardr', 'Vidarr', 'Yngvarr', 'Aki', 'Asbjorn', 'Asgeirr', 'Askell', 'Ivarr', 'Oleifr', 'Olafr', 'Thorbjorn', 'Thorgeirr', 'Thorgnýr', 'Forsteinn', 'Frondr', 'Forfredr', 'Thorir', 'Ogmundr', 'Ozurr']
norse_female_names=['Borghildr', 'Dagny', 'Edna', 'Gerdr', 'Grimhildr', 'Gunnhildr', 'Gunnr', 'Gunnvor', 'Gudrun', 'Helga', 'Hjordis', 'Hreidunn', 'Hrodny', 'Inga', 'Ingibjorg', 'Ingiridr', 'Ingridr', 'Jorunn', 'Ragnfridr', 'Ragnhildr', 'Rannveig', 'Signy', 'Sigridr', 'Asa', 'Ashildr', 'Aslaug', 'Astridr', 'Forny']

all_names_dict={
    "Daoine" : [celtic_female_names, celtic_male_names],
    "Norse" : [norse_female_names, norse_male_names],
    "Nhudelhid" : [nomad_female_names, nomad_male_names],
    "Alnaasi" : [arabic_female_names, arabic_male_names],
    "Elf" : [generate_names.elf_female_names,generate_names.elf_male_names]
}

all_titles={
    #culture : [king, duke, count]
    "Norse" : ["Hilmir", "Jarl", "Hofdingi"],
    "Daoine" : ["Ri", "Diuc", "Taoiseach"],
    "Nhudelhid" : ["Khan", "High Chieftain", "Chieftain"],
    "Alnaasi" : ["Sultan", "Caliph", "Emir"],
    "Elf" : ["Jur", "Deyi", "Noal"]
}

npc_clothes_male = {
    "Norse": ["The Norse is wearing a tunic-like garment made of wool.", "The man is wearing a linen tunic, covered in a cloak, and leather boots.", "The Norse is wearing a wool tunic, covered in a cloak fastened in brooches."],
    "Alnaasi": ["The Alnaasi individual is wearing a flowing white robe.", "The Alnaasi man is wearing a loose robe and he is covering his head with a keffiyeh"],
    "Daoine": ["The man is wearing a simple tunic made of wool.", "The Daoine man wears a cloak made of linen, his pants are carried by his leather belt."],
    "Elf": ["The Elf is wearing a tunic-like long sleeved garment.", "The Elf wears a distinctive silk garment."],
    "Nhudelhid": ["The man is wearing a traditional Nhudelhid garment, a long robe with a high collar.", "The man is wearing a silk bright colored robe with a high collar."]
}
npc_clothes_female = {
    "Norse": ["The Norse woman wears a dress held together in brooches.", "The woman is wearing a linen dress with layers of woolen fabrics for warmth."],
    "Alnaasi": ["The Alnaasi woman is wearing a long dress with a veil."],
    "Daoine": ["The woman is wearing a simple tunic made of wool.", "The Daoine woman wears a cloak made of linen, his pants are carried by his leather belt."],
    "Elf": ["The Elven woman is wearing a long layered dress", "The Elven woman is wearing a long silk bright colored dress."],
    "Nhudelhid": ["The man is wearing a traditional Nhudelhid garment, a long robe with a high collar.", "The man is wearing a silk bright colored robe with a high collar."],
}
def generate_description(proffession, nationality, gender, obj_pronouns, subj_pronouns, gen_pronouns, age, aggression):
    if gender == 1:
        npc_gender = "man"
    else:
        npc_gender = "lady"
    if age <35:
        npc_descr = "young"
    elif age <60:
        npc_descr = "middle-aged"
    else:
        npc_descr = "old"
    if proffession == "merchant":
        descr_start = f"A merchant has set up {gen_pronouns} counter here.\n"
    elif proffession == "innkeeper":
        descr_start = f"Here an innkeeper sits, with {gen_pronouns} apron dirty, outside {gen_pronouns} tavern.\n"
    elif proffession == "traveller":
        descr_start = f"You run into a fellow traveller on {gen_pronouns} horse's back, with a huge bundle.\n"
    elif proffession == "blacksmith":
        #???
        descr_start = f"You've been hearing the rythmic clang of a hammer by afar, now you see a blacksmith working {gen_pronouns} craft.\n"
    elif proffession == "town elder":
        descr_start = f"The old man with the bald head and the sparse white beard stands in front of you. He is wearing a ragged leather robe.\n"
    elif proffession == "soldier":
        descr_start = f"A {npc_gender} stands in front of you, holding a spear, {gen_pronouns} armor is rusty, {gen_pronouns} boots are muddy.\n"
    elif proffession == "bandit":
        descr_start = f"A {npc_gender} draws {gen_pronouns} old rusty sword and points it to you. This is not going well, {subj_pronouns} must be a bandit.\n"
    elif proffession == "spy":
        descr_start = f"A hooded individual runs into you and never makes eye contact. A shady {npc_gender} indeed, it is a spy."
    elif proffession == "farmer":
        descr_start = f"You come across a local farmer, wearing muddy leather boots and a tattered tunic."
    else:
        descr_start = f"The fancy clothing of the individual before you indicate that {subj_pronouns} must be high-born. That is a {proffession}."
        pass
    #???
    descr_middle = f"The {proffession} is a " + random.choice([f"huge, intimidating {npc_gender}","tall and commanding presence", "towering figure", "tiny "+npc_gender, "short "+npc_descr+" "+npc_gender, "giant of a "+npc_gender, "an absolute beast of a "+ npc_gender, npc_gender + " of medium height", npc_gender + " of medium stature", npc_gender + " of lower stature"]) + " , with " + random.choice(["piercing ", "beautiful ", "jarring ", "deep ", ""]) + random.choice(["blue", "chestnut", "green", "brown", "red", "yellow"]) + " eyes.\n"
    #???
    if gender == 1 and proffession != "town elder":
        rnd = random.randint(0,5)
        if rnd == 5:
            descr_middle = descr_middle + f"The {npc_descr} man has a bald head and "+  random.choice(["a sharp beard", "a thick and dense beard", "a slender moustache", "thick sideburns"])+".\n"
        else:
            descr_middle = descr_middle + f"The {npc_descr} man also has "+ random.choice(["long ", "short ", "coarse ", "sparse ", " "])+ random.choice(["curly", "straight"])+ " "+random.choice(["black", "chestnut", "blonde", "white", "platinum", "red", "gold", "silver"])+" hair and "+  random.choice(["a sharp beard", "a thick and dense beard", "a slender moustache", "thick sideburns"])+".\n"
        if proffession != "soldier":
            descr_middle = descr_middle + random.choice(npc_clothes_male[nationality])
    else:
        descr_middle = descr_middle + f"The {npc_descr} woman also has"+ random.choice(["long", "short"])+ " "+ random.choice(["curly", "straight", "coarse"])+ " "+random.choice(["black", "chestnut", "blonde", "white", "platinum", "red", "gold", "silver"])+" hair. " 
        if proffession != "soldier":
            descr_middle = descr_middle + random.choice(npc_clothes_female[nationality])
    
    if aggression <=5:
        descr_end = random.choice([f"This {proffession} looks at you with respect.", f"The {proffession} seems open-hearted.", f"The {proffession} looks welcoming."])
    elif aggression <=10:
        descr_end = random.choice([f"This {proffession} looks at you with indifference", f"The {proffession} seems kinda suspicious of you. You should be careful not to provoke {obj_pronouns} any more.", f"The {proffession} looks at you with contempt.", f"The {proffession} tries not to make eye contact with you."])
    else:
        descr_end = random.choice([f"The {proffession} seems absolutely furious once {subj_pronouns} becomes aware of you. You should be careful with {obj_pronouns}.", f"The {proffession} doesn't seem to like you at all. This could go badly.", f"The {proffession} looks at you with disgust."])
    return descr_start + descr_middle + descr_end + '\n\n'

#function that creates random NPCs
def createRandomNpc():
    gender=random.choice([0,1]) #0 for female, 1 for male
    nationality=random.choice(nationalities)
    proffession = random.choice(proffessions)
    age = random.randint(17,85)
    name = name_based_on_gender(nationality, gender)
    #random_npc=Npc(npc_gender, name_based_on_gender(npc_nationality, npc_gender), random.randint(16,99), random.choice(proffessions), npc_nationality)
    family_name = findFamilyName(nationality, gender)
    title = findTitle(nationality, proffession)
    intelligence = random.randint(5,20)

    if gender==1:
        obj_pronouns="him"
        subj_pronouns="he"
        gen_pronouns="his"
    else:
        obj_pronouns="her"
        subj_pronouns="she"
        gen_pronouns="her"

    #print([name, family_name, title, age, proffession, nationality, obj_pronouns, subj_pronouns])
    aggression = random.randint(0,10)
    return {"name": name, "family_name": family_name, "title": title, "age": age,
    "proffession": proffession, "nationality": nationality, "gender": gender, "obj_pronouns": obj_pronouns, "subj_pronouns": subj_pronouns, "gen_pronouns": gen_pronouns,
    "aggression": aggression, "previously met": False, "description": generate_description(proffession, nationality, gender, obj_pronouns, subj_pronouns, gen_pronouns, age, aggression),
    "favour_completed": False, "intelligence": intelligence}
        


    

#choose npc name based on gender and nationality
def name_based_on_gender(nationality, gender):
    char_name = all_names_dict.get(nationality)[gender]
    return random.choice(char_name)

#choose npc surname based on nationality and proffession
def findFamilyName(nationality, gender):
    if nationality=="Norse":
        if gender==1:
            return random.choice(norse_male_names)+"son"
        else:
            return random.choice(norse_male_names)+"dottir"
    elif nationality=="Daoine":
        return "Ó "+random.choice(celtic_male_names)+"i"
    elif nationality=="Alnaasi":
        return "Al "+random.choice(arabic_male_names)+"yad"
    else:
        return random.choice(generate_names.elf_family_names)

#choose npc title if proffession= king, duke or count
def findTitle(nationality, proffession):
    if proffession=="king":
        return all_titles.get(nationality)[0]
    elif proffession=="duke":
        return all_titles.get(nationality)[1]
    elif proffession=="count":
        return all_titles.get(nationality)[2]
    else:
        return "none"

# characters_json = []

# for i in range(150):
#     characters_json.append(createRandomNpc())


# with open('assets/characters.json', 'w') as json_file:
#     json.dump(characters_json, json_file)

