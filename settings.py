#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame

display_size = (1280, 800)
init_bacteria_number = 100
show_icons = True
show_values = False
food_activated = True
show_terrain = False
food_growth_gap = 50
logging = True
logging_verbose = False
show_intro = True

categories = ["prey", "predator", "both"]
genders = ["male", "female"]
metabolism = ["low", "medium", "fast"]
sociability = ["lone", "family", "town", "city"]
reproduction = ["sex", "mitosis", "hermaphrodite"]
foods = ["organic", "inorganic", "preys", "all"]

terrains = ["ground", "organic", "inorganic"]

fauna = [
    {"Name": "Green Bacteria",
     "Category": "prey",
     "Gender": "both",
     "Reproduction": "mitosis",
     "Food": "organic",
     "Last Dinner": 0,
     "Starvation Limit": 5,   # More starvation limit if sex and predator (e.g. 20)
     "Hunt Randomize": False,
     "Hunt Success": 3,
     "Birth Size": 1,
     "Maturity Size": 20,   # More size than predator if sex
     "Growth Gap": 10,
     "Overgrowth": False,
     "Max Size": 20,
     "Speed": 5,
     "Last Direction": (0,0),
     "Next Run": 0,
     "Max Run": 20,
     "Longevity": 1000,
     "Metabolism": "medium",
     "Sociability": "lone",
     "Maturity Init Point": 200,
     "Maturity End Point": 800,
     "Gestation Time": 1,
     "Gestation Gap": 10,
     "Last Gestation": 0,
     "Gestation Food Level": 3,
     "Color": pygame.Color("chartreuse4"),
     "Position": (0,0),
     "Status": "alive",
     "Age": 0,
     "Size": 1,
     "Size Gap": "addition",
     "Last Move": 0,
     "Icon File": "Virus1",
     "Rotate": True,
     "Icon Index": 0
     },

    {"Name": "Cyan Stick Bacteria",
     "Category": "prey",
     "Gender": "both",
     "Reproduction": "mitosis",
     "Food": "organic",
     "Last Dinner": 0,
     "Starvation Limit": 5,   # More starvation limit if sex and predator (e.g. 20)
     "Hunt Randomize": False,
     "Hunt Success": 3,
     "Birth Size": 1,
     "Maturity Size": 20,   # More size than predator if sex
     "Growth Gap": 10,
     "Overgrowth": False,
     "Max Size": 20,
     "Speed": 5,
     "Last Direction": (0,0),
     "Next Run": 0,
     "Max Run": 20,
     "Longevity": 1000,
     "Metabolism": "medium",
     "Sociability": "lone",
     "Maturity Init Point": 200,
     "Maturity End Point": 800,
     "Gestation Time": 1,
     "Gestation Gap": 10,
     "Last Gestation": 0,
     "Gestation Food Level": 3,
     "Color": pygame.Color("cyan4"),
     "Position": (0,0),
     "Status": "alive",
     "Age": 0,
     "Size": 1,
     "Size Gap": "addition",
     "Last Move": 0,
     "Icon File": "Virus2",
     "Rotate": True,
     "Icon Index": 1
     },

    {"Name": "Green Pseudopodical Virus",
     "Category": "prey",
     "Gender": "both",
     "Reproduction": "mitosis",
     "Food": "organic",
     "Last Dinner": 0,
     "Starvation Limit": 5,   # More starvation limit if sex and predator (e.g. 20)
     "Hunt Randomize": False,
     "Hunt Success": 3,
     "Birth Size": 1,
     "Maturity Size": 20,   # More size than predator if sex
     "Growth Gap": 10,
     "Overgrowth": False,
     "Max Size": 20,
     "Speed": 5,
     "Last Direction": (0,0),
     "Next Run": 0,
     "Max Run": 20,
     "Longevity": 1000,
     "Metabolism": "medium",
     "Sociability": "lone",
     "Maturity Init Point": 200,
     "Maturity End Point": 800,
     "Gestation Time": 1,
     "Gestation Gap": 10,
     "Last Gestation": 0,
     "Gestation Food Level": 3,
     "Color": pygame.Color("orange"),
     "Position": (0,0),
     "Status": "alive",
     "Age": 0,
     "Size": 1,
     "Size Gap": "addition",
     "Last Move": 0,
     "Icon File": "Virus3",
     "Rotate": True,
     "Icon Index": 3
    },

    {"Name": "Purple Virus",
     "Category": "both",
     "Gender": "both",
     "Reproduction": "mitosis",
     "Food": "prey",
     "Last Dinner": 0,
     "Starvation Limit": 10,
     "Hunt Randomize": True,
     "Hunt Success": 3,
     "Birth Size": 1,
     "Maturity Size": 10,
     "Growth Gap": 10,
     "Overgrowth": True,
     "Max Size": 20,
     "Speed": 10,
     "Last Direction": (0,0),
     "Max Run": 50,
     "Longevity": 1000,
     "Metabolism": "medium",
     "Sociability": "lone",
     "Maturity Init Point": 200,
     "Maturity End Point": 800,
     "Gestation Time": 1,
     "Gestation Gap": 10,
     "Last Gestation": 0,
     "Gestation Food Level": 3,
     "Color": pygame.Color("purple"),
     "Position": (0,0),
     "Status": "alive",
     "Age": 0,
     "Size": 1,
     "Size Gap": "addition",
     "Last Move": 0,
     "Icon File": "Virus4",
     "Rotate": True,
     "Icon Index": 3
     }
]

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# ICONS
icons_folder = "icons/"
icon = "Intro.png"
intro_icon = "Intro"
intro_icon_size = 64
intro_size_scale = int(display_size[0] * intro_icon_size / 1280)
arrow_icon = "Arrow"
arrow_icon_size = 64
arrow_icon_scale = int(display_size[0]*arrow_icon_size/1280)
frame_icon = "Frame"
check_icon = "Check"
intro_icons_prefix = "Virus"
intro_icons_suffix = "_Intro"
intro_icons_size = 300
intro_icons_scale = int(display_size[0] * intro_icons_size / 1280)
intro_fauna_icon_size = 100
intro_fauna_icon_scale = int(display_size[0] * intro_fauna_icon_size / 1280)
fauna_icons_size = 156
fauna_icons_scale = int(display_size[0] * fauna_icons_size / 1280)
bacteria_options_icon_size = 128
bacteria_options_icon_scale = int(display_size[0]*bacteria_options_icon_size/1280)
frame_check_size = 32
frame_check_scale = int(display_size[0]*frame_check_size/1280)
cataclism_icon = "Lightning"
cataclism_icon_size = 256
cataclism_icon_scale = int(display_size[0]*cataclism_icon_size/1280)
quit_icon = "Quit"
quit_icon_size = 50
quit_icon_scale = int(display_size[0]*quit_icon_size/1280)
grave_img = "Grave"

# COLORS
cBkg = pygame.Color('black')
cBkg_highlighted = pygame.Color("cadetblue4")
cTerrain = pygame.Color("darkslategrey")
cButton = pygame.Color("red")

# TEXTS AND FONTS
caption = "Bacteria Jungle"
welcome = "Welcome to..."
welcome_font = "Purisa/Purisa.ttf"
welcome_font_size = int(display_size[0]*48/1280)
welcome_color = pygame.Color("white")
title = "BACTERIA   JUNGLE !"
title_font = "ani/ani.ttf"
title_font_size = int(display_size[0]*96/1280)
title_color = pygame.Color("orange")
presskey = "press ANY KEY to continue"
presskey_font = "Waree/Waree.ttf"
presskey_font_size = int(display_size[0]*24/1280)
presskey_color = pygame.Color("white")
options = "OPTIONS"
options_title_color = pygame.Color("orange")
options_color = pygame.Color("white")
food_growth_tip = "150 if no predator and mitosis / 25-50 if no predator and sex / 50 if predator present"
category_tip = "prey / predator / hermaphrodite"
food_tip = "organic / inorganic / preys / all"
reproduction_tip = "mitosis / sex"
starvation_tip = "20+ if only predators and mitosis / 6 if only preys and sex / 5-10 if both"
speed_tip = "(min) 1 to 20 (max)  / 10 for everyone if Food Mode not Activated"
hunt_tip = "1 / N probability to FAIL hunting a prey (0 - NO fail, 1 - ALWAYS fail, 2 - 50% ...)"
colony_diversity_tip = "Set specimens separated by comma (will override Fauna Selection Screen)"
colony_diversity = "e.g.: 0,0,0,3"   # Use this to add more than one of a kind
options_button = "Apply"
button_text_color = pygame.Color("white")
back = "Back"

# OTHER FONTS
fonts_folder = "fonts/"
name_font = "Purisa/Purisa.ttf"
name_font_size = int(display_size[0]*32/1280)
info_font = "Waree/Waree.ttf"
info_font_size = int(display_size[0]*10/1280)
info_font_color = pygame.Color("white")
values_font = "freesans/freesans.ttf"
values_font_size = int(display_size[0]*10/1280)

# POSITIONS
intro_icon_gap = [(80, 180), (170, 75), (120, 80), (220, 200)]
intro_icon_pos = [(0, 1), (1, 0), (0, 0), (1, 1)]

""" OTHER COMBINATIONS:
Previous values work fine and produce (with little adjustments) stable colonies for:

### ALL
Food Growth: 50
All Preys - Mitosis / Starvation 5
Predator - Mitosis / Starvation 10

### JUST PREYS - MITOSIS
Food Growth: 150
All Preys - Mitosis / Starvation 5

### JUST PREYS - SEX
Food Growth: 50
One Prey - Sex / Starvation 6-7

### JUST PREDATORS - MITOSIS
Predator - Mitosis / Starvation 20

### STRANGE
Food Growth: 75
One Prey: Sex / Starvation 20 / Size 21
Predator: Mitosis / Starvation 20 / Size 20

### CATCH ME (IF YOU CAN!!!!)
Init Specimen Number = 2
One Prey: sex / Speed 10 / Size 20 / Starvation 10000000
Predator: sex / Speed 5 / Size 21 (no overgrowth) / Starvation 10000000

### OVERWHELMED (BRING SOME BICARB!!!!)
Food Activated = False
Colony Fauna = 0,0,0,0,0,0,0,0,0,3
One Prey: Reproduction None / Speed 5 / Size 20
Predator: Category: Predator / Reproduction None / Speed 10 / Size 21 (no overgrowth)

## HUNGER NOT
Food Activated = True
Colony Fauna = 0,3,3,3,3,3,3,3,3,3
One Prey: Longevity 100
Predator Category predator / Reproduction none / Hunt Success 0

"""