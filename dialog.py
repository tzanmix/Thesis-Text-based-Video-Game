import adventurelib as adv
import random
import json
import customtkinter
import game_gui
import game_rooms
import game_items
import main_missions
import characters

#nodes from the dialog trees
class DialogNode:
    def __init__(self, text, speaker, condition, insult, accept_mission, end, success, knowledge, choices=None):
        self.text = text
        self.speaker = speaker
        self.choices = choices if choices else []
        self.condition = condition
        self.insult = insult
        self.accept_mission = accept_mission
        self.end = end
        self.knowledge = knowledge
        self.success = success

steal_status = ""

lore_magic_question = {"teleportation_scepter": "What do you know about the teleportation scepter?", "gungnir": "Have you ever seen this golden spear?", "spells": "What do you know about spells?"}
lore_main_mission_question = {"sorcerer":"Have you heard of a red haired sorcerer with a scar?", "audafir": "Do you know the Elven sorcerer Audafir?", "curse": "Do you know how you curses are broken?"}
lore_history_question = {"empire": "What do you know about this Empire?", "war": "What do you know about the War of the Four Kingdoms?", "ancient_ones": "What are the Ancient Ones?"}
info_people_question = {"nhudelhid": "What can you tell me about the Nhudelhid people?", "elf": "What do you know about the elves?", "daoine": "What can you tell me about the Daoine?", "norse": "What do you know about the Norse people?", "alnaas": "What can you tell me about the Alnaasi?"}
info_town_question = {"nordvik": "What can you tell me about Nordvik?", "vestenvarth": "What do you know about Vestenvarth?"}
info_monster_question = {"griffin": "What can you tell me about the griffin?", "vampire": "I am a monster hunter, how can I defeat a vampire?", "wraith": "How can I exorcise a wraith?", "werewolf": "What should I do when I come up against a werewolf?", "draugr": "What exactly is a draugr?"}
lore_question = {"lore_question1": lore_magic_question, "lore_question2": lore_main_mission_question, "lore_question3": lore_history_question, "info_question1": info_people_question,
                 "info_question2": info_town_question, "info_question3": info_monster_question}
lore_answer = {"lore_scepter_answer": ["This is an ancient object of power,\ncenturies old, you can warp everywhere within a certain range once you tap it to the ground.",
                                          "This is the Scepter of the Elven sorceress Aulba, who died during the War of the Four Kingdoms.\nI have no idea how you came up with an object so powerful.\nAulba used it to travel instantly from one corner of the world to the other.",
                                          "You've got here one of the most powerful Objects of Power in the world here.\nI don't want to know how you claimed it,\nbut a strong sorcerer could theoretically travel anywhere in the world with this.\nOf course, a non-sorcerer could use it, but in a certain range."],
                "lore_gungnir_answer": ["This right here is the Gungnir Spear.\nLegends say it was gifted to the All-Father by the First Men and he used it to defeat the Harbinger\nand exile him in the Black Lodge forever.\nThere are some other weapons like this one too around the world, object of immeasurable value",
                            "I see you've somehow acquired the Gungnir, the mythical spear of the All-Father.\nBy snapping your fingers it always warps to your hand, so you can never lose it.\nSo I trully have no idea how you managed to take it by the preivous owner."],
                "lore_spells_answer": ["So any non-magic user like you can cast a spell by simply using some Objects of Power.\nOf course, sorcerers can cast spells without them, but by using one, their magic is much more powerful.",
                           "Sorcerers and magic users can cast spells because of years of training.\nThey chant in the Ancient tongue and they basically can do whatever you can imagine.\nThere are also some Objects of Power that can signifantly strengthen a spell,\nor even help a non magic user cast one.\nEvery spell cast by an Object of Power leaves a mark to its target, a signature in runes."],
                "lore_sorcerer_answer": ["Unfortunately for you, I am not aware of any sorcerer matching this description.", "I have not heard of any magic user like this one.", "I do not know anything about this sorcerer."],
                "lore_audafir_answer": ["Hmm yes, Audafir Nemburul, I've heard of him.\nLegends say he was killed during the War of the Great Kingdoms, he was already a century old by then.\nOther historians have argued that he died years later, of old age.\nI have not heard anything else though.",
                            "He is not one of the most famous sages, I can tell you that.\nNot much is known about him, apart from some questionnable history textbooks citing he died in the Great War.",
                            "I have not heard about him unfortunately."],
                "lore_curse_answer": ["Depends on the curse, usually only a single condition can break it.\nThere are some times though that curses are unbreakable.", "Only very powerful sorcerers can cast them.\nThey can only be broken if a certain condition is met, which depends on the curse.\nSo, to break it, you must find exactly what kind of curse has been cast upon you", "I'm sorry for you, you have to find the one that cursed you,\nit is your only way to find out how it can be broken."],
                "lore_empire_answer": {"Norse": ["Personally, I don't really like being part of the Empire,\nthose pointy eared charlatans have no idea how to rule us.", "\nI think we sholu break out of the Empire, we are proud people,\nwe don't like foreigners ruling us.", "\nIf we didn't have the spineless Jarls those Elves have appointed us,\nwe would definetely rebel. We are ruled by imbeciles."],
                           "Alnaasi": ["Honestly, we've lived far better with the Empire. Our people were just spice merchants,\nnow our families have gotten rich over the last decades, and we can travel the world and do any job we want.",
                                       "I really don't like how we were annexed without a fight.\nThe Sheikh is a traitor to our people to bend the knee to an Elf",
                                       "I'd rather not tell you my personal opinion about this."],
                            "Nhudelhid": ["I'm glad that our people were never defeated by those Elves.\nWe always used to live far away from these lands, so we were never the target.",
                                          "Honestly, I think it would be good for our nation to be annexed by the Empire.\nWe come from the Far East, there is no fertile ground there and we can't develop much.",
                                          "I'm afraid of the safety of my people with an empire this big just next to our border."],
                            "Daoine": ["I don't like this regime. Why shouldn't the other races have a say?\nWe are a huge Empire and always ruled by the Elves.",
                                       "I believe we would be better without the Empire.\nNorthern brutes and those pointy-eared arrogant Elves are free to come to our lands and steal our jobs."],
                            "Elf": ["Our people have strengthened since the Empire formed, and every other race that is part of it as well.\nEvery culture's advancement is shared, everyone benefits and yet we are the bad guys...",
                                    "I really think that the Emperor thinks of the other races too much, in fear that he will be dethroned by them.\nHe is an Elf and he doesn't protect his own people's interest."]},
                "lore_war_answer": {"Norse": ["\nI don't believe that these pointy ears defeated us, the terror of the North", "\nWe still honor the fallen every first week of the summer,\nNorthern warriors that never shamed their family names, unlike these modern Jarls and Clan leaders."], 
                        "Alnaasi": ["\nMy people were the only of the First Men that was successful against the elven tyranny.", "\nWe were proud of our people, that were not defeated by the Elves by using pure genius tactics.\nBut the Elves would not let us be free... and the Seikh sold his soul to them."],
                        "Nhudelhid": ["\nOur people were too far away from these events, but we learnt of this conflict", "\nWe are from the Far East and just arrived here recently,\nbut I'm pretty sure that we would defeat all the Four Kingdoms at once.\nThey are weak farmers and traders, where we are survivors of unhospitable lands for centuries."],
                        "Daoine": ["\nI don't want to talk more about this.\nIt was a painful time for our people."],
                        "Elf": ["\nThe humans first stole the land from us and were continuously threatening us.\nWe acted out of self defence, and we won.","\nThese lands were stolen from us, our forefathers would not let this injustice stand.\nWe were superior in combat and magic, the First Men were just brutes, so we should rule our own lands."]},
                "lore_ancient_ones_answer": ["The Ancient Ones are mythical beasts worshipped by the Ancient Elves centuries ago.\nOnly stories that we tell our kids to make them eat their vegetables remain of them.", "These are some mythical beasts supposedely children of the Dark Lord.\nIn some cultures this Dark Lord is the harbinger that the All-Father defeated.\nAccording to ancient elven scrolls, the Ancient Ones were the first inhabitants of the earth,\nand now, they are trapped in the Black Lodge, if you believe anything like that.",
                                             "In some ancient texts, these are the guardians of the Black Lodge.\nBut all these are creations of ancient barbaric religions, the worshippers of those did some really nasty stuff\nlike human sacrifices and creepy rituals."]}


dialog_tree_alt = {
    #"npc_intro_q": ["Hello stranger, what can I do for you?", "Hey there, adventurer, may I help you?", "Greetings, traveller, how can I help you?"],
    "ask_for_quest": ["Is there a job for me?", "Do you have any jobs for me? I'm a good sellsword", "I can help you with any mission for the right price"],
    #"ask_lore": ["What do you know about the Great Purge?"],
    "ask_lore": ["Can I ask you something? I'm a foreigner and I don't know a lot about these places", "Can you help me with something? I want to find out a bit about these lands"],
    #"ask_info": ["Where can I find a boat?", "Where is Nodrvik?", "Where are we now?"],
    "ask_info": ["Can you help me find something?", "I'm kinda lost, can you help me find my way?", "I could use some help navigating these lands"],
    "ask_id": ["Who are you?", "What is your name?"],
    "end_conv": ["I should go", "I should probably leave", "Time to go"],
    "accept_quest": ["I will help you", "Gladly", "Don't worry, consider the feat done", "I'll look into it"],
    "accept_quest_npc": ["Great, I will reward you accordingly", "Thanks for the help, stranger", "I will always be grateful"],
    "decline_quest": ["Nah, it sounds too dangerous", "No", "This sounds too hard", "I'm sorry, I can't help you"],
    "refused_quest": ["You already refused, what do you want?", "The last time you told me that you didn't want the job", "Ahh, maybe you changed your mind?", "What, nobody is hiring you and you came back to me?"],
    "ask_quest_again": ["Yeah, I changed my mind", "Yes, sorry about that earlier, I can help you this time", "I had my hands full last time, now I can commit to your quest"],
    "decline_again": ["Haha, just kidding, I wouldn't help you ever", "Nah, I was joking around, I don't want to help you"],
    "decline_again_ans": ["You think you're that great, huh?", "Who do you think you are to mess around with stuff like these?", "I had enough of your jests vagrant!"],
    "quest_given": ["So, you want some more info on the job I gave you?", "You need to ask something for the job I told you about?", "I hope you are looking into the job I told you, you need something else?"],
    "quest_completed": ["Thank you so much for helping us stranger, here is your reward.", "We will be in your debt traveller, take this coin for your good work", "Thanks for the help kind stranger"],
    "quest_completed_ans": ["No problem", "Glad to help", "I'm always glad to help"],
    "ask_quest_location": ['Where exactly should I go?', "Point me to the right direction", "Where exactly am I going?"],
    "ask_quest_objective": ["Tell me one more time, what am I looking for?", "What am I supposed to do?", "So, what is the objective?"],
    "ask_quest_reward": ["Yes, I would like to know if it's going to be worth my time", "Yes, I would like to know how much I'm getting paid", "Yes, I want to know how much coin I would earn"],
    # "quest_location_ans": [],
    # "quest_objective_ans": [],
    "quest_reward_ans": ["Well, I can give you about 50 florens", "I am running sort of coin right now, when you come back we'll talk about your reward", "I'll reward you handsomely, don't you worry about that", "You'll have my eternal gratitude, how's that for a reward?"],
    "insult_npc": ["I don't believe this is worth my time", "Sounds too unimportant", "I have more important things to do, peasant"],
    "insult_npc_ans": ["Who do you think you are?", "You coward!", "I ask for your help nicely and this is how you repay me?", "You sound like a coward"],
    "insult_back": ["Watch your tone, peasant", "You don't want to anger me any more"],
    "id_negative_answer": ["Get outta here", "None of your business", "I don't care who you are, so neither should you care who I am"],
    "lore_negative": ["Why would you care for something like that, huh?", "Do you think I would share anything with you, foreigner?", "I don't have to share anything with you."],
    "lore_negative_ans": ["I don't trust you at all", "You seem like trouble, I don't like you", "I don't trust you enough to help you vagrant."],
    "lore_positive": ["Sure, what would you like to know?", "I can help you with that, what do you want?", "Of course, how can I help you?"],
    "info_negative": ["Why would you care for something like that, huh?", "Do you think I would share anything with you, foreigner?", "I don't have to share anything with you."],
    "info_negative_answer": ["Alright then, keep your secrets", "Very well then, I don't need you anyway", "Thanks for the help..."],
    "info_positive": ["Sure, what would you like to know?", "I can help you with that, what do you want?", "Of course, how can I help you?"],
    #bandit dialogue
    "bandit_intro": ["You, right there! Give me everything you have now!", "Greetings, traveller. To pass you must give me all your belongings.", "Hello stranger, you are getting robbed right now.", "Give me everything you have and maybe I'll let you live."],
    "intimidate": ["You don't know who you're messing with, thief!", "Get out of my way and maybe I'll be the one to spare you.", "Out of my sight, or I'll evaporate you.", "You have no idea who you're trying to mess with."],
    "mercy": ["*CRYING* Please don't kill me, I'm just passing by.", "*CRYING* Please don't rob me! I'm just a poor traveller", "*CRYING* Please let me go! I'll do anything!"],
    "accept": ["Fine fine, I'll cooperate, just let me go.", "Alright, I'll give you what you want, just let me pass", "I'll give you anything, now let me through"],
    "refuse": ["No, I don't think I will", "Nah, I'm not giving you anything", "You'll get nothing from me, thief"],
    "intimidate_success": ["Oh I'm sorry, please don't hurt me, I just try to make a living here", "Please don't evaporate me, I clearly had no idea who you were", "Please don't murder me, I promise I won't steal and I won't kill ever again"],
    "intimidate_fail_critical": ["Haha, do you think I'm that dumb?", "Pff, I don't believe you at all, and now you have really angered me", "Hahaha, who do you think you are, vagrant?"],
    "intimidate_fail": ["I don't really care who you are, just give me all your coin", "I'm not easily intimidated by threats, now give me everything you have"],
    "intimidate_success_ans": ["*WHISPERING* Haha, I can't believe this worked", "*WHISPERING* Hehe, you don't mess with me", "Now get out of my sight!", "That's right, now run!"],
    "intimidate_fail_ans": ["Well, I'll guess we'll find out who's the tougher one", "I tried to warn you", "Very well, we'll settle this another way"],
    "intimidate_fail_critical_ans": ["Well, I honestly didn't believe this would work", "Oh crap!", "Damn, I thought this could work"],
    "accept_ans": ["Haha, now all your coin is mine, you're free", "Now all your loot belongs to me, you may pass", "Get out of my sight now", "I'm a bandit of honour, you are free to leave now"],
    "refuse_ans": ["Very well, I guess it will be the hard way", "Well, I'll easily rob your belongings from your corpse", "I guess I'll have to kill you then"],
    "mercy_success": ["Ok ok I'm sorry, I won't kill you, just stop crying", "Oh please stop crying, I won't do anything to you, just leave"],
    "mercy_success_ans": ["*WHISPERING* Haha sucker", "*WHISPERING* I can't believe this actually worked", "*WHISPERING* Oof, I got away unharmed"],
    "mercy_fail": ["Stop crying and give me everything", "I'm not easily moved by tears, I am a murderer you know", "Oh boohoo, just give me all you have!"],
    "mercy_fail_ans": ["*SIGH* I thought this would work", "Oh come on", "This really sucks"],

    #---------------LORE AND INFO QUESTIONS#---------------
    "lore_question1": ["I'd like to know about magic.", "I want to ask you something about sorcery", "I want to know about magic and Objects of Power"],
    "lore_question2": ["I want to ask you about something important for me", "I want your guidance for my quest", "I want to ask about my condition"],
    "lore_question3": ["I want to know about the history of this world", "Can you tell me of the history of these lands?", "I'm from far away, and unfamiliar with the history here"],
    "lore_spells_question": ["What do you know about spells?", "Do you know anything about spells?", "Are you familiar with spells?"],
    "lore_scepter_question": ["What do you know about this Scepter?", "Have you ever heard of this Scepter I have?", "What can you tell me about this Scepter?"],
    "lore_gungnir_question": ["Have you ever heard anything about this golden spear?", "What about this golden spear?", "What's this spear?"],
    "lore_sorcerer_question": ["Have you ever heard of a red haired sorcerer with a scar on his face?", "Do you know if any red haired sorcerers are active in the South?"],
    "lore_audafir_question": ["What do you know about the Elven sage Audafir?", "Have you heard of someone named Audafir Nemburul?", "Do you know anything about Audafir?"],
    "lore_curse_question": ["Do you know how I can get rid of a curse?", "I am cursed, do you know of any ways I can be healed?", "How can I cast away a curse?"],
    "lore_empire_question": ["What is this Empire that rules these lands?", "Tell me about the Empire"],
    "lore_war_question": ["What is this War of Four Kingdoms?", "What happened in the War of the Four Kingdoms?", "Tell me about the War of the Four Kingdoms"],
    "lore_ancientones_question": ["What are these Ancient Ones I've seen people here worship?", "Who are the Ancient Ones?", "What do you know about the Ancient Ones?"],

    "info_question1": ["Tell me about the people of this world", "Can you tell me about the people that live here?"],
    "info_question2": ["Tell me about some of the places here", "Can you tell anything about the towns of this continent?"],
    "info_question3": ["Can you tell me about the monsters that live in these lands?", "Do you know anything about the monsters of this place?"],
    
    "info_griffin_question": ["What can you tell me about the griffins?", "What is a griffin?"],
    "info_draugr_question": ["What is a draugr?", "What do you know about the draugr?", "How can I defeat a draugr?"],
    "info_wraith_question": ["What are the wraiths?", "How can I exorcise a wraith?", "What do you know about wraiths?"],
    "info_werewolf_question": ["What do you know about werewolves?", "Do you know anything about werewolves?"],
    "info_vampire_question": ["What do you know about vampires?", "How can I defeat a vampire?", "Do you know about vampires?"],
    "info_griffin_answer": ["A griffin is a large predator, with the body of a lion, the head and the wings of an eagle.\nIt hunts everything that is human sized.\nTo defeat it, you must have a ranged weapon with you, like a crossbow."],
    "info_draugr_answer": ["The draugr are undead soldiers, with no ability to talk or think.\nThey only live to kill. They used to be Norse soldiers centuries ago, that were cursed by some elven sage.\nThey can be killed the same way as humans, but they are stronger and faster by them, so be careful."],
    "info_wraith_answer": ["A wraith is a ghost of a human whose spirit never rest after death.\nThey are very dangerous as they carry the suffering of their final moments in life.\nYou cannot kill them with regular weapons, as they are immaterial. Only magic can harm them."],
    "info_werewolf_answer": ["The werewolf is a man cursed to look like a giant beast,\nconsume human flesh, and live in the darkness, as sunlight hurts their eyes.\nThey are a very fast and strong predator, capable of cutting through knight armour with a single blow.\nSteel and bronze weapons cannot hurt them, they say that only silver ang gold is their weakness."],
    "info_vampire_answer": ["The vampires that live in these lands are not what you would think.\nThey do not have a human form and they do not wake up only in the night.\nThey are 8 feet tall bat-like creatures with a lust for blood.\nThey can only be hurt with weapons made of silver or gold."]
}

current_question = ""
def ask_lore(text):
    global current_question
    question = random.choice(list(lore_question[text].values()))
    #print("QUESTION: ", question)
    #--------------HERE IS THE PROBLEM#--------------
    current_question = list(lore_question[text].keys())[list(lore_question[text].values()).index(question)]
    #print("QUESTION ASKED: ", current_question)
    return question


#the following two functions generate answer based on character traits
def char_answer_lore(character, text):
    # global current_question
    # lore_answer = {"lore_answer1": lambda: lore_magic_answer(current_question, character), "lore_answer2": lambda: lore_main_mission_answer(current_question, character), 
    #                "lore_answer3": lambda: lore_history_answer(current_question, character), "info_answer1": lambda: info_people_answer(current_question, character), 
    #            "info_answer2": lambda: info_town_answer(current_question, character), "info_answer3": lambda: info_monster_answer(current_question, character)}
    # answer = lore_answer[text]
    # print("answer: ", answer)
    if text == "lore_answer1":
        answer_start = ""
        answer_end = ""
        if character.proffession != "sorcerer":
            answer_start = random.choice(["I don't know much about magic", "I'm not really an expert in this", "I am not familiar with sorcery and witchcraft"])
            if character.intelligence > 10:
                answer_end = random.choice([", but I've read about some of these", ", but I've heard elders talk about it", ", but I've heard some legends"])
        else: 
            answer_start = random.choice(["I can help you with that, stranger.", "I am familiar with these arcane arts.", "I've studied magic for years."])
        return answer_start+answer_end
    else:
        return random.choice(["Sure, ask me about it", "I'm listening", "What do you wan to know?"])

def npc_answer(character, text):
    try:
        return random.choice(lore_answer[text])
    except Exception:
        if text == "lore_empire_answer":
            return random.choice(["The Empire was the result of the War of the Four Kingdoms.\nThe elves conquered the lands of the Daoine and the Northerners,\nbut the conquest in the South was not successful.\nEventually, the South was peacefully annexed due to financial troubles.",
                                  "The Elves were the dominant force two centuries ago,\nmore advanced in the art of war and wielders of powerful magic.\nThey defeated the Daoine and the Norse in the field of battle,\nand they eventually through diplomacy took the South.",
                                  "After the Great War ended, the Elven Empire expanded all over the Nordreyjar, the Juun and the North Cyfandir.\nThe capital city was moved into a very secure mountainous island\nand they turned their eyes south, towards the desert people that were still standing.\nEventually, by issuing a trade embargo, the Alnaasi were forced into the Empire with not a single more drop of blood."])+"\n"+random.choice(lore_answer[text][character.nationality])
        elif text == "lore_war_answer":
            return random.choice(
                ["The War of the Four Kingdoms was a conquest war by the Elves that happened two centuries ago.", "The Great War was the most defining war of these lands.", "This was the biggest armed conflinct in the world,\nthe three kingdoms of the First Men, against the Elves with the superior army and sorcery."]
                ) + random.choice(
                ["\nThe Elves, who were the original inhabitors of these lands were never friendly with the First Men,\nthe humans that colonized this region some centuries ago.\nA lot of distrust among the races led to an organised assault from the Elves.", "\nThe humans, that colonised from the West, were never friendly towards the original inhabitors,\nthe Elves. A lot of bad blood between them led to an eventual campaign where the Elves attacked all the First Men."]
                )+ random.choice(
                ["\nThe humans stood no chance against them, so they were defeated, except from the Alnaasi,\nwho scorched earth back to the deserty South, where the Elves wouldn't try to chase them.", "\nThe Elven sages were too much for the First Men, who were eventually defeated.\nThe ancestors of the Alnaasi managed to slip away from the Elves,\nas the conquest against them was beginning to be more and more costly for the Elves."]
                )+random.choice(lore_answer[text][character.nationality])
        else:
            return random.choice(lore_answer[text][character.nationality])

# def lore_magic_answer(current_question, character):
#     answer_start = ""
#     answer_end = ""
#     print("MADE IT HERE TOO")
#     if character.proffession != 'sorcerer':
#         answer_start = random.choice(["I don't know much about magic", "I'm not really an expert in this", "I am not familiar with sorcery and witchcraft"])
#         if character.intelligence > 10:
#             answer_end = random.choice([", but I've read about some of these", ", but I've heard elders talk about it"]) + random.choice(lore_answer1[current_question])
#     else: 
#         answer_start = random.choice(["I can help you with that, stranger.", "I am familiar with these arcane arts.", "I've studied magic for years."])
#         answer_end = random.choice(lore_answer1[current_question])
#     return "OK THIS SHOULD WORK"

# def lore_main_mission_answer(current_question, character):
#     return random.choice(lore_answer2[current_question])

# def lore_history_answer(current_question, character):
#     try:
#         return random.choice(lore_answer3[current_question][character.nationality])
#     except Exception:
#         return random.choice(lore_answer3[current_question])

def info_people_answer(current_question, character):
    return "info people"

def info_monster_answer(current_question, character):
    return "info monster"

def info_town_answer(current_question, character):
    return "info town"

possible_lore_questions = ["lore_question1", "lore_question2", "lore_question3", "info_question1", "info_question2", "info_question3"]
possible_lore_answers = ["lore_answer1", "lore_answer2", "lore_answer3", "info_answer1", "info_answer2", "info_answer3"]
npc_answers = ["lore_spells_answer", "lore_scepter_answer", "lore_gungnir_answer", "lore_sorcerer_answer", "lore_audafir_answer", "lore_curse_answer", "lore_empire_answer",
               "lore_war_answer", "lore_ancientones_answer", "info_people_answer", "info_town_answer", "info_monster_answer"]
def create_node_text(text, character):
    try:
        if text == "give_quest":
            return give_task(character.mission) #+ " " + random.choice(["Will you help me?", "Do you accept?", "Do you wish to help me?"])
        elif text == "npc_intro_q":
            return character_greeting(character)
        elif text == "id_positive_answer":
            return character_introduction(character)
        # elif text in possible_lore_questions:
        #     return ask_lore(text)
        elif text in possible_lore_answers:
            return char_answer_lore(character, text)
        elif text in npc_answers:
            return npc_answer(character, text)
        else:
            return random.choice(dialog_tree_alt[text])
    except KeyError:
        return text

chapter2_flag = ""
#select npc answer to player choices based on npc aggression or intelligence, or whether their quest was accepted or not
def select_npc_answer(current_node, branch_index, type, character):
    global chapter2_flag
    npc_conditions = []
    for i in range(len(current_node.choices[branch_index].choices)):
        npc_conditions.append(current_node.choices[branch_index].choices[i].condition)
    # print(npc_conditions)
    # print("mission accepted: ",character.mission_accepted)
    # print("mission refused: ",character.mission_refused)
    try:
        if character.aggression > 12:
            npc_answer = npc_conditions.index("aggr>12")
            return current_node.choices[branch_index].choices[npc_answer]
        elif character.aggression <= 12:
            npc_answer = npc_conditions.index("aggr<=12")
            return current_node.choices[branch_index].choices[npc_answer]   
    except ValueError:
        
        try:
            if character.intelligence < 10:
                npc_answer = npc_conditions.index("intelligence<10")
                return current_node.choices[branch_index].choices[npc_answer]
            elif character.intelligence > 15:
                npc_answer = npc_conditions.index("intelligence>15")
                return current_node.choices[branch_index].choices[npc_answer]
            elif character.intelligence >= 10:
                npc_answer = npc_conditions.index("intelligence>=10")
                return current_node.choices[branch_index].choices[npc_answer]
        except ValueError:
            
            try:
                if character.favour_completed:
                    npc_answer = npc_conditions.index("quest_completed")
                    character.aggression = character.aggression - 10
                    game_items.floren_balance = game_items.floren_balance + character.mission.reward
                    return current_node.choices[branch_index].choices[npc_answer]
                elif character.mission_accepted==True:
                    npc_answer = npc_conditions.index("mission_accepted")
                    return current_node.choices[branch_index].choices[npc_answer]
                elif character.mission_refused==True:
                    npc_answer = npc_conditions.index("mission_refused")
                    return current_node.choices[branch_index].choices[npc_answer]
                elif character.mission_refused==False and character.mission_accepted==False:
                    npc_answer = npc_conditions.index("!mission_accepted&!mission_refused")
                    return current_node.choices[branch_index].choices[npc_answer]
                
            except ValueError:
                #npc_answer = current_node.choices[branch_index].choices

                try:
                    if game_items.floren_balance>=100:
                        npc_answer = npc_conditions.index("floren_balance>100")
                        chapter2_flag = "true"
                        return current_node.choices[branch_index].choices[npc_answer]
                    else:
                        npc_answer = npc_conditions.index("floren_balance<100")
                        return current_node.choices[branch_index].choices[npc_answer]
                except ValueError:
                    random_npc_answer = random.randint(0,len(current_node.choices[branch_index].choices))
                    #print(current_node.choices[branch_index].choices[random_npc_answer-1].text)
                    random_npc_answer = random_npc_answer-1
                    return  current_node.choices[branch_index].choices[random_npc_answer]

             
    

#function that traverses the dialog tree when in dialog mode with NPC
def traverse_tree(branch_index, type, character):
    global choice_buttons, current_node, dialog_window, label, steal_status
    #variable that checks on what status a conversation with a bandit ends
    try:
        new_node = select_npc_answer(current_node, branch_index, type, character)
        label.configure(text = create_node_text(new_node.text, character))
        #dynamically create all the new choices for the dialog, based on the nodes of the dialog tree
        for j in range(len(choice_buttons)):
            choice_buttons[j].destroy()
        choice_buttons = []
        for i in range(len(new_node.choices)):
            choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text=create_node_text(new_node.choices[i].text, character), command= lambda i=i: traverse_tree(i, type, character), text_color="black")
            choice_buttons.append(choice_button)
            choice_button.pack(padx=5, pady=10)
        current_node = new_node
        #if a question about monsters is asked, add monster info to bestiary
        if current_node.knowledge != "false":
            #print(current_node.knowledge)
            characters.monster_knowledge[current_node.knowledge] = True
        if current_node.insult == "true":
            character.aggression = character.aggression + 10
            #print("insult")
        if current_node.accept_mission == "true":
            #print("mission accepted")
            character.mission_accepted = True
            game_rooms.active_missions.append(character.mission)
        elif current_node.accept_mission == "false":
            character.mission_refused = True
            #print("mission rejected")
        if current_node.success != "":
            steal_status = current_node.success
            #print(current_node.success)
    #at the bottom of the tree, say farewell and reset the current_node pointer
    except IndexError:
        for j in range(len(choice_buttons)):
            choice_buttons[j].destroy()
        if (type == "talk" or type == "audafir" or type == "spy" or type == "grandmaster") and current_node.end == "true":
            choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text="Leave the conversation", command= lambda: dialog_window.destroy(), text_color="black")
            label.configure(text = f"You leave the {character.proffession}")
        elif (type == "talk" or type == "audafir" or type == "spy" or type == "grandmaster") and current_node.end != "end_conv":
            new_node = dialog_tree
            label.configure(text = random.choice(["Anything else?", "Do you want anything else to ask me?"]))
            #dynamically create all the new choices for the dialog, based on the nodes of the dialog tree
            for j in range(len(choice_buttons)):
                choice_buttons[j].destroy()
            choice_buttons = []
            for i in range(len(new_node.choices)):
                choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text=create_node_text(new_node.choices[i].text, character), command= lambda i=i: traverse_tree(i, type, character), text_color="black")
                choice_buttons.append(choice_button)
                choice_button.pack(padx=5, pady=10)
            current_node = new_node
        elif type == "steal" or type == "assassinate":
            choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text="Oh crap", command= lambda: dialog_window.destroy(), text_color="black")
            label.configure(text = "I had enough of you, you won't get away with this!")
        elif type == "bandit":
            choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text="Leave the conversation", command= lambda: dialog_window.destroy(), text_color="black")
            label.configure(text = "The conversation with the bandit ended")

        choice_button.pack(padx=5, pady=10)
        current_node = dialog_tree


#load dialog tree from json to instances of class DialogNode
def load_json_to_dialog_node(json_data):
    if isinstance(json_data, dict):
        text = json_data.get("text", "")
        speaker = json_data.get("speaker", "")
        choices_data = json_data.get("choices", {})
        #na mpei to condition, insult, accept_mission, end
        condition = json_data.get("condition", "false")
        insult = json_data.get("insult", "false")
        accept_mission = json_data.get("accept_mission", "")
        end = json_data.get("end", "false")
        success = json_data.get("success", "")
        knowledge = json_data.get("knowledge", "false")
        choices = [
            load_json_to_dialog_node(choices_data[key])
            for key in choices_data
        ]

        return DialogNode(text, speaker, condition, insult, accept_mission, end, success, knowledge, choices)

    # If the JSON data is not a dictionary, return a leaf node
    return DialogNode(json_data, "Player")

def open_dialog_window(character, type):
    global dialog_window, label, choice_buttons
    global current_node, dialog_tree
    if type == "talk":
        with open("dialogs/dialog_trees.json","r") as json_file:
            tree = json.load(json_file)
    elif type == "steal":
        with open("dialogs/bad_reaction.json","r") as json_file:
            tree = json.load(json_file)
    elif type == "assassinate":
        with open("dialogs/as_attempt.json","r") as json_file:
            tree = json.load(json_file)
    elif type == "bandit":
        with open("dialogs/bandit.json","r") as json_file:
            tree = json.load(json_file)
    elif type == "audafir":
         with open("dialogs/audafir.json","r") as json_file:
            tree = json.load(json_file)
    elif type == "spy":
        if main_missions.chapter2.completed:
            with open("dialogs/spy_chapter_completed.json", "r") as json_file:
                tree = json.load(json_file)
        else:
            with open("dialogs/spy.json", "r") as json_file:
                tree = json.load(json_file)
    elif type == "grandmaster":
        with open("dialogs/grandmaster.json", "r") as json_file:
                tree = json.load(json_file)
    dialog_tree = load_json_to_dialog_node(tree)
    current_node = dialog_tree
    dialog_window = customtkinter.CTkToplevel(game_gui.root)
    dialog_window.attributes("-topmost","true")
    dialog_window.geometry("700x700")
    dialog_window.title(character.name)
    
    label = customtkinter.CTkLabel(dialog_window, width=100, height=100, text=create_node_text(current_node.text, character))
    label.pack()
    choice_buttons = []
    for i in range(len(current_node.choices)):
        choice_button = customtkinter.CTkButton(dialog_window, width=700, height=50, text=create_node_text(current_node.choices[i].text, character), command= lambda i=i: traverse_tree(i, type, character), text_color="black")
        choice_buttons.append(choice_button)
        choice_button.pack(padx=5, pady=10)


def character_greeting(character):
    if character.aggression <=5:
        return random.choice(["Greetings traveler!", "Hello there stranger.", "Aah, here there is an adventurer!", "Welcome stranger."])
    elif character.aggression <=10:
        return random.choice(["What?", "'Morning", "What do ye want?"])
    else:
        return random.choice(["Get lost vagrant.", "Stay out of my sight.", "Get outta here.", "Out of my way, drifter"])
    
def character_introduction(character):
    if character.aggression <=10 and character.proffession != "bandit" and character.proffession != "captain":
        return random.choice([f"Allow me to introduce myself, I am {character.name}", 
                              f"My name is {character.name}",
                              f"I am {character.name}"])
    elif character.proffession == "bandit":
        return random.choice(["Greetings stranger, be kind to give me all your belongings, and I may let you walk away","Well well, what do we have here? Give me everything you have, and don't be a hero.", "Halt there, give me your money and food."])
    elif character.proffession == "captain":
        return f"I am {character.name}, captain of this longship right there, the Freya's Grace. I will sail soon for Vestenvarth, if you want to join, the price is 200 florens for a place at my ship."
    else:
        # return random.choice(["I'm Nanya, none of your business", "Get lost!", "None of your business vagrant!", "I am not in the mood of getting to know you",
        #                       "I don't care who you are, why should you?"])
        return random.choice([f"Get lost!", "None of your business, vagrant!", "Get out of my sight!", "Are you looking for trouble, stranger?", 
                              "Why? You want to know who'll put you to the ground right now?"])
    
def give_task(mission):
    type = mission.type
    objective = mission.objective
    location = mission.location
    if type == "Fetch":
        return "I could use your help, stranger.\n"+random.choice(["A "+objective+" that has been in my family for generations, has been stolen from me.\nWhen I was at "+location+", I was jumped by bandits and they stole my belongings.",
                                                                   "I have lost my "+objective+" at "+location+". Can you bring it back to me? I will reward you accordingly."])
    elif type == "Escort":
        return "I have a job for you traveller, if you choose to accept it.\nMy "+objective.type+" was lost "+objective.gen_pronouns+" at "+location+".\n I haven't heard from "+objective.obj_pronouns+" in a while and I'm worried,\ncan you help "+objective.obj_pronouns+" return back to safety?"
    elif type == "Hunt":
        return "We have a problem, traveller, I have the coin to repay you if you help us.\n"+random.choice(["A vile beast has been terrorizing this area for weeks, many men have fallen trying to hunt it down.\nPlease find this monster and kill it for us.",
                                                                                                             "A "+objective.name+" has been killing everyone passing through this area. I'm not a fighter myself, and I cannot take on a monster like this, please make this area safe again."])
    elif type == "Eliminate":
        return "We could use your help.\n"+random.choice(["Someone named "+objective.name+" has killed my "+random.choice(["brother", "sister", "father", "cousin", "family"])+"\n. Help me avenge my family's memory by bringing "+objective.obj_pronouns+" to the only justice this murderer understands.\nI will reward you handsomely if you hunt "+objective.obj_pronouns+" down in "+mission.location+" and kill "+objective.obj_pronouns+".",
                                                          "A thief and murderer by the name of "+objective.name+" has rampaged through the area for the past weeks.\nI want this criminal dead, and I can pay you handsomely to do this.\nThe coward is said to be hiding somewhere in "+location+".",
                                                          "I hope you're the type of guy who don't ask many questions.\nI have someone I want you to hunt down and kill, "+objective.gen_pronouns+" name is "+objective.name+",\nand you will probably find "+objective.obj_pronouns+" somewhere in "+location+"."])
    elif type == "Collect":
        return "I have some information for you, stranger.\nAccording to some local legends, a "+objective+" is hidden somewhere in "+location+", inside some ancient ruins.\nI have not the courage for the journey, but you seem like a courageous person."
    else:
        return "Rescue someone from somewhere"
    

def find_topic(topic, char):
    if topic == "ship" or topic == "boat" or topic == "longship":
        if char.proffession == "captain":
            return "You have come to the right place, I am the captain of Freya's Grace, this longship right there."
        else:
            return random.choice(["Go to Nordvik, at the southernmost place of this island. There you can find a port and you can rent a cabin in a ship, but that will cost you.",
                                  "You will find a ship at the south of this island, in the port of Nordvik.",
                                  "There are some ships at the port of Nordvik, which is at the southernmost point of this place." ])
    elif topic == "captain":
        if char.proffession == "captain":
            return "You have found him, I am the captain of Freya's Grace."
        else:
            return random.choice(["There is a guy named Sigurd, he is captain of Freya's Grace. He usually is at the Nordvik port.",
                                  "You can find at the Nordvik port, a tall bearded guy with wolf fur, his name is Sigurd Thorfinnson.",
                                  "There is a tall Northerner with a thick black beard that usually hangs out at the port, he is the captain of a longship."])
        
monster_misses = ["but it completely misses you.","but you manage to dodge.", "but you are quick enough to avoid the attack.", "but you manage to parry the attack"]
#combat text
def monster_condition(monster):
    condition = ""
    if monster.name == "vampire":
        if monster.hit_points >= 20:
            condition = "The hit seems to have not affected the vampire."
        elif monster.hit_points <20:
            condition = "The vampire shrieks, as the metal pierces its skin."
        elif monster.hit_points < 13:
            condition = "The vampire cries in agony, but it still doesn't seem to lose its bloodthirst for you."
        elif monster.hit_points <7:
            condition = "The scream of the vampire pierces your ears, it has been worn out significantly."
    elif monster.name == "wraith": 
        if monster.hit_points >= 20:
            condition = "The hit seems to have not affected the wraith at all."
        elif monster.hit_points <20:
            condition = "The hit lands on the wraith, it seems a bit disoriented."
        elif monster.hit_points < 13:
            condition = "The wraith shrieks, it struggles to keep its footing."
        elif monster.hit_points <7:
            condition = "The scream of the wraith pierces your ears, it has been worn out significantly."
    elif monster.name == "griffin":
        if monster.hit_points >= 20:
            condition = "You try to hit the griffin with your weapon, but it flies over you and you miss it."
        elif monster.hit_points <20:
            condition = "You manage to land a blow on the mighty griffin, wounding it a bit."
        elif monster.hit_points <13:
            condition = "The griffin screams in pain, it's struggling in beating its wings."
        elif monster.hit_points <7:
            condition = "The griffin's shriek pierces your ears, it can barely fly anymore."
    elif monster.name == "draugr":
        if monster.hit_points >= 20:
            condition = "You try to hit the draugr with your weapon, but it parries your attack with its sword."
        elif monster.hit_points <20:
            condition = "The draugr tries to deflect your attack, but you manage to wound it."
        elif monster.hit_points <13:
            condition = "The draugr screams in pain, it's struggling to keep its footing."
        elif monster.hit_points <7:
            condition = "The wounded draugr stuggers, it seems like it's at its limit."
    elif monster.type == "werewolf":
        if monster.hit_points >= 20:
            condition = "You land a blow on the werewolf with your weapon, but it seems that the beast is unaffected by it."
        elif monster.hit_points <20:
            condition = "You manage to land a blow on the werewolf, it growls as the metal pierces its skin."
        elif monster.hit_points <13:
            condition = "The werewolf screams in pain, it is still in frenzy."
        elif monster.hit_points <7:
            condition = "The rabid werewolf growls, it is severely wounded."
    return condition
        
def monster_attacks(monster, attack):
    attack_dialog = ""
    if monster.name == "vampire":
        attack_dialog = random.choice(["The vampire moves swiftly towards you, ", "The nocturnal fiend descends upon you suddenly, ",
                                       "The vampire shrieks, and flies toward you with its fangs gleaming like polished daggers, "])
        if attack == 0:
            attack_dialog = attack_dialog + random.choice(monster_misses)
        else:
            attack_dialog = attack_dialog + random.choice([" and its claws pierce your armour.", " and it sinks its fangs into your flesh."])
    elif monster.name == "wraith":
        attack_dialog = random.choice(["The ethereal form of this wraith materializes and rushes towards you, ",
                                       "The spectral presence materializes, the wraith shrieks and tries to land a blow with its bare hands, "])
        if attack == 0:
            attack_dialog = attack_dialog + random.choice(monster_misses)
        else:
            attack_dialog = attack_dialog + random.choice([" and it lands a blow on you.", " and you feel its ghostly hands piercing your skin."])
    elif monster.name == "griffin":
        attack_dialog = random.choice(["The mighty griffin descends from the sky upon you with its sharp talons outstretched, ",
                                       "The frightening griffin beats its wings thunderously and dives towards you, "])
        if attack == 0:
            attack_dialog = attack_dialog + random.choice(monster_misses)
        else:
            attack_dialog = attack_dialog + random.choice([" and its talons pierce your armour.", " and it completely overwhelms you, wounding you gravely."])
    elif monster.name == "draugr":
        attack_dialog = random.choice(["The undead warrior rises, its skeletal hands hold tight its rusty sword and it lunges at you, ",
                                       "The draugr swiftly closes in on you, its mummified hands outstretched, "])
        if attack == 0:
            attack_dialog = attack_dialog + random.choice(monster_misses)
        else:
            attack_dialog = attack_dialog + random.choice([" and its sword pierces your armour.", " and you cannot block the attack, its rusty sword wounds you."])
    elif monster.name == "werewolf":
        attack_dialog = random.choice(["The werewolf's growls pierce your ears, and the furry beast lunges forward, with its claws and fangs extended, ",
                                       "The lycanthrope's howls haunt the atmosphere, you are caught in its predatory gaze, and it instatly attacks you, "])
        if attack == 0:
            attack_dialog = attack_dialog + random.choice(monster_misses)
        else:
            attack_dialog = attack_dialog + random.choice([" and its claws tear your skin.", " and its fangs pierce your armour, and rip your skin."])
    else:
        attack_dialog = "The monster attacks you with all its might, doing "+str(attack)+ " damage."
    return attack_dialog


def check_player_attack_effectiveness(player_attack, weapon, char):
    #print(weapon.color)
    if char.type == "human":
        char.hit_points -= player_attack
    elif char.name == "vampire" or char.name == "werewolf":
        if weapon.color == "silver" or weapon.color == "gold":
            char.hit_points -= player_attack
        else:
            char.hit_points -= 0
    elif char.name == "griffin":
        if weapon.name != "crossbow":
            char.hit_points -= 0
        else:
            char.hit_points -= player_attack
    elif char.name == "wraith":
        pass
        #na mpei kwdikas gia tis adynamies twn wraiths
    else:
        char.hit_points -= player_attack


