#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

display_size = (1280, 800)
init_bacteria_number = 100
show_icons = True
show_values = False
food_activated = True
show_terrain = False
food_growth_gap = 50  # 150 if no predator and mitosis / 25-50 if no predator and sex / 50 if predator present
logging = True
logging_verbose = False
intro = True

categories = ["prey", "predator", "both"]
# genders = ["female", "male", "both"]
genders = ["female", "male"]
metabolism = ["low", "medium", "fast"]
sociability = ["lone", "family", "town", "city"]
reproduction = ["sex", "mitosis"]
foods = ["organic", "inorganic", "preys", "all"]

terrains = ["ground", "organic", "inorganic"]

colony_diversity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3]   # Use this to add more than one of a kind (and don't run intro())

fauna = [
        {"Name": "Green Bacteria",
         "Category": "prey",
         "Gender": "both",
         "Reproduction": "mitosis",
         "Food": "organic",
         "Last Dinner": 0,
         "Starvation Limit": 5,
         "Hunt Randomize": False,
         "Hunt Success": 3,
         "Birth Size": 1,
         "Maturity Size": 20,
         "Growth Gap": 10,
         "Speed": 10,
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
         "Max Size": 20,
         "Size Gap": "addition",
         "Last Move": 0,
         "Icon File": "Virus1",
         "Rotate": False,
         "Icon Index": 0
        },

        {"Name": "Cyan Stick Bacteria",
         "Category": "prey",
         "Gender": "both",
         "Reproduction": "mitosis",
         "Food": "organic",
         "Last Dinner": 0,
         "Starvation Limit": 5,
         "Hunt Randomize": False,
         "Hunt Success": 3,
         "Birth Size": 1,
         "Maturity Size": 20,
         "Growth Gap": 10,
         "Speed": 10,
         "Last Direction": (0,0),
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
         "Max Size": 20,
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
         "Starvation Limit": 5,
         "Hunt Randomize": False,
         "Hunt Success": 3,
         "Birth Size": 1,
         "Maturity Size": 20,
         "Growth Gap": 10,
         "Speed": 10,
         "Last Direction": (0,0),
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
         "Max Size": 20,
         "Size Gap": "addition",
         "Last Move": 0,
         "Icon File": "Virus3",
         "Rotate": False,
         "Icon Index": 2
        },

        {"Name": "Purple Virus",
         "Category": "both",
         "Gender": "both",
         "Reproduction": "mitosis",
         "Food": "prey",
         "Last Dinner": 0,
         "Starvation Limit": 10,
         "Hunt Randomize": False,
         "Hunt Success": 3,
         "Birth Size": 1,
         "Maturity Size": 10,
         "Growth Gap": 10,
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
         "Max Size": 20,
         "Size Gap": "addition",
         "Last Move": 0,
         "Icon File": "Virus4",
         "Rotate": False,
         "Icon Index": 3
        }
        ]

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# ICONS
iconf = "icons/"
icon = "Intro.png"
intro = "Intro"
intro_size = 64
intro_size_scale = int(display_size[0]*intro_size/1280)
intro_icons_prefix = "Virus"
intro_icons_suffix = "_Intro"
intro_icons_size = 300
intro_icons_size_scale = int(display_size[0]*intro_icons_size/1280)

# TEXTS
caption = "Bacteria Jungle"
welcome = "Welcome to..."
title = "BACTERIA   JUNGLE !"
presskey = "press ANY KEY to continue"
food_growth_tip = "150 if no predator and mitosis / 25-50 if no predator and sex / 50 if predator present"
category_tip = "prey / predator / both"
food_tip = "organic / inorganic / preys / all"
reproduction_tip = "mitosis / sex"
options = "OPTIONS"
options_button = "Apply"

# FONTS
welcome_font = "Purisa"
welcome_font_size = 48
welcome_color = pygame.Color("white")
title_font = "ani"
title_font_size = 96
title_color = pygame.Color("orange")
presskey_font = "Waree"
presskey_font_size = 24
presskey_color = pygame.Color("white")
name_font = "Purisa"
name_font_size = 32
info_font = "Waree"
info_font_size = 10
values_font = "freesans"
values_font_size = 10

# COLORS
cBkg = pygame.Color('black')
cBkg_highlighted = pygame.Color("cadetblue4")
cButton = pygame.Color("red")
cButton_text = pygame.Color("white")
cOptions_title = pygame.Color("orange")
cOptions_text = pygame.Color("white")
