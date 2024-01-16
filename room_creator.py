import random
import csv

terrain_types = {'0': 'sea', '2': 'desert', '3': 'plain', '4': 'forest', '5': 'hill', '6': 'mountain', '7': 'town'}


def select_continent(terrain_type_code, i, j):
    if i<=14 and terrain_type_code!='0':
        return "Nordreyjar"
    elif i>=13 and j<=27 and terrain_type_code!='0':
        return "Cyfandir"
    elif i>=8 and j>=21 and terrain_type_code!='0':
        return "Juun"
    

def select_super_area_title(terrain_type_code, i, j):
    if terrain_type_code == '0':
        if i<=11:
            return "Northaenvagr"
        elif i>11 and i<28 and j<=9:
            return "Mhor Gorllewinol"
        elif i>11 and j>9 and j<44:
            return "Farraige Mhor"
        elif i>=41 and j<=7:
            return "Lake Buhayra"
        elif i>41 and j>=44:
            return "Baruun Nuur Lake"
        elif i>=25 and i<=28 and j>=47:
            return "Loch Thiar Lake"
        elif i>28 and i<=31 and j>44:
            return "Abhainn Mhor River"
        else:
            return "water"
    elif terrain_type_code == '2':
        if i>=43 and j<=25: #south desert
            return "Kathban Albahr Desert"
        else:
            return "desert"
    elif terrain_type_code == '4': #forest
        if i>16 and i<28 and j<=13:
            return "Coillte Cogarnach Forest"
        elif i>3 and i<10:
            return "Skogr Forest"
        elif i>=40 and i<=46:
            return "Id-Shidiin Mod Woods"
        elif i>=35 and i<=37:
            return "Coedydd Cyfriniol Woods"
        else:
            return "Nirur Forest"
    # elif terrain_type_code == '6':
    #     return "mountain"
    elif i<=13 and j<=24 and terrain_type_code != '0':
        return "West Nordreyjar"
    elif i<=13 and j>24 and terrain_type_code!='0':
        return "East Nordreyjar"
    elif i>13 and i<=30 and j<=19 and terrain_type_code!='0':
        return "North Cyfandir"
    elif i>30 and j<=27 and terrain_type_code!='0':
        return "South Cyfandir"
    elif i>7 and j>=23 and i<30 and terrain_type_code!='0':
        return "North Juun"
    elif i>=30 and j>=33 and terrain_type_code!='0':
        return "South Juun"
    else:
        return "mpla"
    

def select_description(terrain_type_code, i, j, super_area_title):
    if terrain_type_code == '0':
        if i<=11: #arctic water
            return random.choice(["""As you continue your journey, a vast expanse of icy water stretches before you. """, 
                                  """As far as the eye can see, the water is a vast expanse of glacial blue, its surface punctuated by jagged ice floes. """,
                                  """The northern lights dance across the night sky in a spectacular display of color and light. """,
                                  """While you sail across the Northaenvagr sea, you see that life flourishes in the icy waters. """]) + random.choice(
                                ["""Pods of graceful orcas glide through the waves, their sleek black and white bodies a stark contrast against the blue backdrop.""",
                                 """The frigid air bites at your skin, and the silence is almost overwhelming, 
                                  broken only by the occasional creaking of ice or the distant call of a lone seabird. """,
                                  """Their vibrant hues reflect in the icy waters below, casting an otherworldly glow upon the frozen sea. 
                                  Icebergs float by like silent sentinels, their reflective surfaces catching the shimmering colors of the aurora. 
                                  It's a magical and breathtaking sight that leaves you in awe of the wonders of the Northaenvagr sea.""",
                                  """Seals lounge on ice floes, their whiskered faces turned towards the sun. 
                                  Curious penguins dive beneath the surface, darting through the water with incredible speed."""])

        else:
            return random.choice(["""The gentle lapping of waves creates a soothing rhythm as the first light of dawn breaks across the horizon. """,
                                  """Dark clouds gather overhead as the sea churns with energy. Waves rise and crash against the rugged rocks, sending salty spray into the air. """,
                                  """The moon hangs low in the sky, casting a silvery path across the water's surface. """,
                                  """The tempest rages with unrelenting fury, as waves surge and crash against one another, forming towering walls of water that seem to defy gravity. """,
                                  """Lightning splits the sky in blinding arcs of brilliance, illuminating the tumultuous seascape of """ + super_area_title +""" in stark contrast. """,
                                  """The horizon is a tumultuous blend of dark clouds and roiling waters, blurred together in a disorienting dance. """
                                  ]) + random.choice(
                                ["""A faint mist hovers above the water's surface, adding an ethereal quality to the scene. """,
                                """The wind howls, tugging at your clothes and whipping your hair into a frenzy. 
                                  Lightning streaks across the sky, briefly illuminating the foamy crests of waves. """,
                                """The gentle waves shimmer with each soft ripple, reflecting the moon's glow like a million diamonds. 
                                  A sense of tranquility pervades the air, broken only by the distant call of a night bird. """
                                """The first twinkling lights mirror the constellations above, creating a breathtaking connection between the heavens and the tranquil waters below. """,
                                """Rain pelts down in diagonal sheets, stinging your skin with each drop. 
                                  The wind howls like a vengeful spirit, tearing at your clothes and sending sea spray in every direction. """,
                                """For a brief moment, the entire expanse of the water is laid bare, revealing the churning chaos beneath. """,
                                """The sea and sky meld into a maelstrom of gray and black, the boundary between them all but erased. """
                                ]) + random.choice([
                                """The air is cool and refreshing, carrying the scent of salt and adventure.""",
                                """It's a wild and powerful display of nature's might. """,
                                """This is a place where time seems to stand still, inviting you to immerse yourself in its serene beauty and contemplate the mysteries of the world. """,
                                """Amidst the chaos, the horizon disappears behind a veil of mist and rain, leaving you feeling small and insignificant in the face of nature's power. """,
                                """The jagged bolts paint a surreal tableau of violence and beauty, 
                                  while the accompanying thunder shakes the very ground beneath your feet, a reminder of the immense forces at play. """,
                                """The jagged bolts paint a surreal tableau of violence and beauty, 
                                  while the accompanying thunder shakes the very ground beneath your feet, a reminder of the immense forces at play. """,
                                """It's as if the world is reduced to this single, chaotic plane, where the distinction between air and water loses all meaning. """
                                ])

    elif terrain_type_code == '2':
        if i>=43 and j<=25: #south desert
            return random.choice(["""As far as the eye can see, rolling dunes stretch across the horizon like waves frozen in time. """,
                                  """The sand gives way to a vast, flat expanse where grains are swept into intricate patterns by the constant wind. """,
                                  """As the sun dips below the horizon, the dunes are painted in shades of deep orange and dusky pink. """])+random.choice(
                                [
                                """Each crest and trough is sculpted by the wind, creating an undulating sea of sand that shimmers under the relentless sun. 
                                  The grains of sand are warm to the touch, and the air is heavy with the dry, earthy scent of the desert. """,
                                """The landscape is punctuated by rocky outcroppings, their weathered surfaces bearing testament to the desert's relentless erosive power. """,
                                """The shifting sands seem to come alive with the changing light, their textures and contours highlighted by the soft glow of twilight. 
                                  The air is cooler now, and the sand carries a subtle chill as you traverse the undulating landscape. """])+random.choice(
                                [
                                """The solitude is both breathtaking and humbling, 
                                  a vast expanse that holds secrets buried beneath the shifting sands of the Kathban Albahr desert. """,
                                """The sky above is a brilliant blue canvas, and the sun bathes the scene in a warm, golden light that casts long shadows across the desert floor. """,
                                """The air is cooler now, and the sand carries a subtle chill as you traverse the undulating landscape. 
                                  Stars begin to twinkle overhead, and the desert becomes a realm of both beauty and mystery under the night sky."""
                                ])

        else: #sandy coastlines 
            return random.choice(["""The sandy coastline stretches out before you, a wide expanse of golden sand that glitters under the brilliant sunlight. """,
                                  """A narrow strip of soft sand hugs the base of towering cliffs, a hidden oasis nestled between land and sea. """,
                                  """The sandy coastline is a meeting place of two worlds – the desert's dunes and the ocean's expanse. """,
                                  """Dark clouds gather overhead as tumultuous waves crash against the rocky shore. """])+random.choice(
                                [
                                """The gentle waves lap at the shore, leaving behind intricate patterns of foam and bubbles. 
                                  Seashells and pebbles are scattered along the sand, remnants of the sea's treasures. """,
                                """The cliffs offer protection from the wind, casting cool shadows that provide relief from the sun's intensity. 
                                  The waves crash against the rocks with a soothing rhythm, and patches of tide pools reveal small ecosystems teeming with colorful marine life. """,
                                """Rolling sand dunes rise and fall like ripples frozen in time, their shapes constantly reshaped by the wind. 
                                  The sea's waves come ashore with a gentle sigh, washing over the edges of the dunes and creating ephemeral patterns in the sand. """,
                                """The sand is damp and gritty underfoot, evidence of the sea's unruly temperament. 
                                  The wind whips your hair and clothes, carrying with it the tang of salt and the promise of a brewing storm. """
                                ])+random.choice([
                                """The air is warm and salty, carrying the sound of seagulls soaring overhead and the distant laughter of beachgoers.""",
                                """It's a serene escape, where the land and ocean converge in perfect harmony.""",
                                """It's a place of transition and contrast, where the forces of nature collide and collaborate.""",
                                """Foam-flecked waves rise with a fierce determination, their power a stark reminder of the ocean's wild and untamed spirit."""
                                ])

    elif terrain_type_code == '3': #plain landscape
        return random.choice(["""The landscape unfolds in a sea of undulating grasses that stretch to the horizon. """,
                              """The plains of """+super_area_title+""" seem to stretch on forever, a vast expanse of open land broken only by occasional clusters of trees. """,
                              """The barren landscape is dominated by arid earth and rocky outcroppings. """,
                              """The steppe is a realm of open skies and endless winds. """,
                              """As far as the eye can see, rows of crops stretch across the fertile plain. """])+random.choice(
                            [
                            """The grasslands in """ + super_area_title+ """ sway in harmony with the breeze, creating a mesmerizing wave-like motion that seems to breathe with the land. 
                              Here and there, wildflowers add vibrant bursts of color, their petals nodding gently in the wind. """,
                            """Tall grasses wave lazily in the wind, their golden heads creating a sea of movement that whispers secrets to anyone who listens. """,
                            """The ground is cracked and dry, and the few tufts of hardy grass that dot the landscape seem like precious oases of life. 
                              The sun beats down relentlessly, casting harsh shadows that stretch across the desolate expanse. """,
                            """ Short grasses carpet the land, bending and swaying as the gusts sweep across the plain. 
                              Herds of animals graze in the distance, their movements harmonizing with the rhythm of the land. """,
                            """ Golden wheat sways like a rippling sea, ready for harvest.
                             Scarecrows stand guard amidst the fields, their outstretched arms warding off unwelcome visitors. """
                            ])+random.choice(
                            [
                            """The sky overhead is an expanse of azure blue, interrupted only by the occasional fluffy cloud.""",
                            """The sun bathes the landscape in a warm glow, and the air is filled with the earthy scent of soil and vegetation.""",
                            """Despite the starkness, there is a certain beauty in the rugged simplicity of the desert plains.""",
                            """The air is cool and invigorating, carrying with it the promise of change and adventure.""",
                            """The air is filled with the earthy scent of freshly turned soil, and the landscape feels alive with the promise of sustenance and growth."""
                            ])

    elif terrain_type_code == '4': #forest
        return random.choice(["""Sunlight filters through the dense canopy, dappling the """+super_area_title+""" floor with patches of golden warmth. """,
                              """A small clearing opens up within the heart of the forest, a haven of tranquility bathed in gentle sunlight. """,
                              """The forest is dominated by a towering canopy of evergreen pines, their needles casting a carpet of fragrant green on the forest floor. """,
                              """As you step into the """+super_area_title+""", a chorus of rustling leaves greets you. """,
                              """The """+super_area_title+""" takes on a different character as dusk descends. """,
                              """A crystal-clear brook winds its way through the forest, its babbling waters creating a soothing backdrop to the symphony of the woods. """])+random.choice(
                            [
                            """Towering trees stand like ancient sentinels, their trunks adorned with gnarled roots and lush moss. 
                              Ferns and undergrowth carpet the ground, creating a soft bed of textures and shades. """,
                            """Tall trees encircle the glade, their branches intertwining overhead to form a natural archway. 
                              Wildflowers bloom at the edges of the clearing, their colors a riotous burst against the sea of green. """,
                            """The air is crisp and invigorating, carrying the aroma of pine and earth. 
                              Sunlight breaks through the branches in slender shafts, illuminating patches of soft moss and fallen needles. """,
                            """The wind weaves its way through the branches, creating a symphony of gentle whispers. 
                              The forest seems alive, each tree and plant swaying in conversation with the breeze. """,
                            """Shadows lengthen and the trees seem to lean in closer, creating an otherworldly atmosphere. 
                              The rustling of leaves becomes more pronounced, accompanied by the occasional hoot of an owl. """,
                            """Stones and pebbles gleam beneath the water's surface, and delicate wildflowers lean over the bank to catch the light. 
                              Birds come to drink and bathe, their ripples creating fleeting patterns on the water. """
                            ])+random.choice(
                            [
                            """The air is cool and fragrant, carrying the earthy scent of damp leaves and the whispers of hidden creatures.""",
                            """Birds sing in harmony, and a sense of magic seems to hang in the air, as if the grove is a doorway to a world beyond reality.""",
                            """The forest is hushed, as if in reverence to the centuries of wisdom held by the ancient trees.""",
                            """Shafts of sunlight pierce the canopy, creating pools of illumination that seem to move in time with the wind's melody.""",
                            """The air is charged with a mixture of anticipation and trepidation, as if the boundaries between the mundane and the magical are beginning to blur.""",
                            """It's a serene and idyllic scene, where nature's harmony is embodied in the gentle flow of the brook."""
                            ])

    elif terrain_type_code == '5': #hill, rocky landscapes
        return random.choice(["""The landscape is dominated by rugged, weathered rock formations that jut out of the earth like ancient sculptures. """,
                              """From the top of a gentle hill, you have a breathtaking view of the land below. """,
                              """You stand on the edge of a towering cliff, overlooking a vast expanse below. """,
                              """You find yourself in the heart of a rocky canyon, its walls rising dramatically on either side. """,
                              """The plateau extends in every direction, a vast expanse of rocky terrain that seems untouched by time. """])+random.choice(
                            [
                            """Each crevice and crag tells a story of time's patient erosion, while moss and lichen add splashes of color to the gray canvas. 
                              Small pools collect in natural basins, reflecting the sky and surrounding terrain. """,
                            """Rolling hills and valleys stretch as far as the eye can see, their contours softened by a veil of mist. 
                              Rocky outcroppings and boulders dot the landscape, standing like silent sentinels amidst the green expanse. """,
                            """The land drops away in a dramatic descent, revealing a mosaic of rock and earth. 
                              Birds soar on thermals, gliding effortlessly through the air, while distant rivers wind their way through the landscape. """,
                            """Sunlight filters through narrow gaps, casting pools of illumination that dance along the canyon floor. 
                              The ground is strewn with smooth river stones, their shapes and colors varying with the eons of water's touch. """,
                            """The ground is uneven, covered in rocky fragments and tufts of hardy grass. The sky stretches overhead, a wide canvas of blue and white. """
                            ])+random.choice(
                            [
                            """The air is crisp and cool, carrying the scent of earth and minerals.""",
                            """The wind whispers secrets as it rustles the grass, and the sky seems infinite overhead.""",
                            """The wind tugs at your clothes and carries the salty tang of the sea, adding an invigorating edge to the view.""",
                            """The air is still and heavy, carrying echoes of silence and the faint trickle of water.""",
                            """It's a place of solitude and open space, where the wind and the land are your only companions."""
                            ]
                            )

    elif terrain_type_code == '6': #mountains
        return random.choice(["""The sun's first rays paint the mountaintops of """+super_area_title+""" in shades of pink and gold, illuminating the rugged terrain with a warm and inviting glow. """,
                              """As you ascend higher into the """+super_area_title+""", the landscape transforms into an alpine wonderland. """,
                              """The path winds through narrow mountain passes, flanked by imposing rock walls that seem to touch the sky. """,
                              """The peak is often obscured by a mystical veil of mist and clouds, adding an air of mystery to the ascent. """,
                              """As you approach the uppermost reaches, the landscape transitions into a rocky desert. """])+random.choice(
                            [
                            """Towering peaks rise like sentinels against the horizon, their jagged silhouettes etched against the sky.""",
                            """Verdant meadows burst with colorful wildflowers, contrasting with the snowy caps of the peaks.
                            Crystal-clear streams babble through the valleys, their waters originating from the melting snow above. """,
                            """ Overhead, eagles circle on the thermals, their wings spread wide against the vast expanse. 
                              The ground is uneven and rocky, requiring careful navigation. """,
                            """As you climb higher, the air becomes damp and cool, and the world around you is cloaked in a soft, diffused light. """,
                            """Harsh winds sweep across the exposed terrain, and the ground is littered with boulders and scree. 
                              Hardy plants cling to the rocky slopes, their adaptations a testament to life's tenacity in even the harshest conditions. """
                            ])+random.choice(
                            [
                            """Valleys below are still shrouded in shadow, while the crisp mountain air carries the promise of adventure and breathtaking vistas.""",
                            """ The air is crisp and invigorating, carrying the scent of pine and the distant call of mountain birds.""",
                            """ With every step, the grandeur of the """+super_area_title+""" becomes more pronounced, 
                              creating a sense of awe and insignificance in the face of nature's grand design.""",
                            """ It's a world of serene beauty, where time seems frozen in the heart of the """+super_area_title+""".""",
                            """The sounds of nature seem muted, as if the """+super_area_title+""" themselves hold their breath in anticipation of your arrival at the summit.""",
                            """The view from this height is panoramic and humbling, offering a glimpse of the world from a unique perspective."""
                            ]
                            )

    else:
        return "town/city description"
    #return "This is a big description of the room, based on terrain type"

def select_short_description(terrain_type_code):
    return "This is a short description"

def select_room_title(terrain_type_code):
    return terrain_types[terrain_type_code]

def save_game_rooms(rooms):
    with open('assets/game_rooms.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)

        # Write the header (column names)
        csv_writer.writerow(["key", "value"])

        # Write the dictionary data as rows
        for key, value in rooms.items():
            csv_writer.writerow([key, value])


game_rooms = {}
final_game_rooms = {}

with open('assets/map_test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        game_rooms[row['key']] = row['value']

for i in range(50):
    for j in range(50):
        
        new_room = {}
        new_room['super area title'] = select_super_area_title(game_rooms[f'({i}, {j})'], i, j)
        new_room['description'] = select_description(game_rooms[f'({i}, {j})'], i, j, new_room['super area title'])
        new_room['title'] = new_room['super area title'] + '-' + select_room_title(game_rooms[f'({i}, {j})'])
        new_room['short description'] = select_short_description(game_rooms[f'({i}, {j})'])
        new_room['continent'] = select_continent(game_rooms[f'({i}, {j})'], i, j)
        new_room['type'] = game_rooms[f'({i}, {j})']
        final_game_rooms[f'({i}, {j})'] = new_room


save_game_rooms(final_game_rooms)
