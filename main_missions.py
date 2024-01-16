import game_rooms
import characters
import game_items

#first main mission-prologue
prologue = game_rooms.Mission("Prologue", characters.audafir, [6, 43], characters.audafir)
prologue.description = """You woke up in the middle of nowhere with no memories of the last days.You were holding a golden spear, and a strange scepter, and in your pockets you found a pouch with 50 florens inside. The black rot on your fingertips of your left hand indicate that you were a recipient of black magic spell. A sorcerer might know how you will break the spell."""
prologue.title = "Prologue - The rot"
prologue.objective = characters.audafir
prologue.short_description = "Find a sorcerer to ask about your condition"

current_main_mission = prologue

chapter1 = game_rooms.Mission("Chapter I", characters.captain, [14, 24], characters.captain)
chapter1.description = """A fraction of your memories unlocked. You were seemingly in a middle of a battle with a red haired sorcerer with a scar when you barely escaped using the scepter. You remember that a window was there, and outside you saw an endless desert. So you decide that you must leave the island and pursue your lead south."""
chapter1.title = "Chapter I - Cyfandir"
chapter1.short_description = "Find a way to leave Nordreyjar"

chapter2 = game_rooms.Mission("Chapter II", characters.spy, [21, 18], characters.spy)
chapter2.description = """You arrived at Cathairbhaile, the biggest port in the world. People from all the corners of the Earth gather here, traders, merchants, spies, who could give you the information you seeked."""
chapter2.title = "Chapter II - The Spy"
chapter2.short_description = "Ask around the city of Cathairbhaile for information"

chapter3 = game_rooms.Mission("Chapter III", characters.spy, [49, 12], game_items.diary)
chapter3.description = """The detective gave you the location of a tower that belonged to a sorcerer that might match your description, so you decided to travel there to investigate."""
chapter3.title = "Chapter III - The Tower"
chapter3.short_description = "Investigate the sorcerer's tower"
game_rooms.tower.items.add(game_items.diary)

chapter4 = game_rooms.Mission("Chapter IV", characters.grandmaster, [40, 29], characters.grandmaster)
chapter4.description = """The tower was a mess, broken flasks everywhere, bookcases and shelves broken, large tomes and scrolls in the ground everywhere. You picked up a diary that contained spells signed by someone named Nesin Nauthuy, the grandmaster of the Citadel."""
chapter4.title = "Chapter IV - The Citadel"
chapter4.short_description = "Ask the Grandmaster in the Citadel for the sorcerer"

chapter5 = game_rooms.Mission("Chapter V", characters.grandmaster, [], characters.mulfeilf)
chapter5.description = """Memories started to come back to you after you talked to the grandmaster. You were hired by him to assassinate Mulfeilf Deim, a red haired sorcerer, formerly an apprentice of Nesin in the Citadel that had gone rogue. You still couldn't remember how the fight between you two ended, so you assumed he was still alive. The grandmaster sent you to chase his trail again, but this time, you both wanted him alive to break your curse."""
chapter5.title = "Chapter V - The Rogue Mage"
chapter5.short_description = "Pursue the Grandmaster's leads to find the rogue mage"



main_missions = {"prologue": prologue, "chapter1": chapter1, "chapter2": chapter2, "chapter3": chapter3, "chapter4": chapter4}
# print(list(main_missions.keys())[list(main_missions.values()).index(current_main_mission)])
