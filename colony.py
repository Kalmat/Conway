#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
import random
import importlib
import settings
import disputil


###############################################################################
class Colony:
    screen = None

    ####################################################################
    def __init__(self):

        self.screen, self.xmax, self.ymax, self.interpreter, self.archOS = \
                                    disputil.InitDisplay(settings.display_size[0], settings.display_size[1],
                                    hideMouse=False, icon=settings.iconf+settings.icon, caption=settings.caption)
        self.xmin = self.ymin = 0
        self.xmargin = self.xmax * 0.01
        self.xgap = self.xmargin * 3
        self.ymargin = self.ymax * 0.01
        self.ygap = self.ymargin * 3

        self.fauna = settings.fauna
        self.init_bacteria_number = settings.init_bacteria_number
        self.show_icons = settings.show_icons
        self.show_values = settings.show_values
        self.food_activated = settings.food_activated
        self.food_growth_gap = settings.food_growth_gap
        self.show_terrain = settings.show_terrain
        self.logging = settings.logging

        self.fontObj = disputil.LoadFont(settings.values_font, settings.values_font_size, 0)
        self.welcome_fontObj = disputil.LoadFont(settings.welcome_font, settings.welcome_font_size, 0)
        self.title_fontObj = disputil.LoadFont(settings.title_font, settings.title_font_size, 0)
        self.presskey_fontObj = disputil.LoadFont(settings.presskey_font, settings.presskey_font_size, 1)
        self.name_fontObj = disputil.LoadFont(settings.name_font, settings.name_font_size, 0)
        self.info_fontObj = disputil.LoadFont(settings.info_font, settings.info_font_size, 0)

        self.firstRun = True
        self.chosen_fauna = settings.colony_diversity
        self.icon = []
        self.terrain_type = None
        self.terrain_age = None
        self.colony_age = 0
        self.average = 0
        self.keyP = ""

    ####################################################################
    def __del__(self):
        pass

    ####################################################################
    def intro(self):

        self.screen.fill(settings.cBkg)
        pygame.draw.rect(self.screen, settings.cBkg_highlighted, (self.xmax*0.1, self.ymax*0.1, self.xmax*0.8, self.ymax*0.8))

        tx, ty = disputil.DrawText(self.screen, settings.title, self.title_fontObj, settings.title_color,
                                   blit=False)
        disputil.DrawText(self.screen, settings.welcome, self.welcome_fontObj, settings.welcome_color,
                          blit=True, x=self.xmax/2 - tx/2 + self.xgap, y=int(self.ymax*1/3))
        disputil.DrawText(self.screen, settings.title, self.title_fontObj, settings.title_color,
                          blit=True, x=self.xmax/2 - tx/2, y=self.ymax/2 - ty/2)

        icon = disputil.loadIcon(settings.intro, settings.iconf)
        icon = pygame.transform.smoothscale(icon, (settings.intro_size_scale, settings.intro_size_scale))
        self.screen.blit(icon, (self.xmax/2+5, self.ymax/2-32))

        icon = disputil.loadIcon("Virus1_Intro", settings.iconf)
        icon = pygame.transform.smoothscale(icon, (settings.intro_icons_size_scale, settings.intro_icons_size_scale))
        self.screen.blit(icon, (self.xmin - 80, self.ymax - 180))

        icon = disputil.loadIcon("Virus2_Intro", settings.iconf)
        icon = pygame.transform.smoothscale(icon, (settings.intro_icons_size_scale, settings.intro_icons_size_scale))
        self.screen.blit(icon, (self.xmax - 170, self.ymin - 75))

        icon = disputil.loadIcon("Virus3_Intro", settings.iconf)
        icon = pygame.transform.smoothscale(icon, (settings.intro_icons_size_scale, settings.intro_icons_size_scale))
        self.screen.blit(icon, (self.xmin - 120, self.ymin - 80))

        icon = disputil.loadIcon("Virus4_Intro", settings.iconf)
        icon = pygame.transform.smoothscale(icon, (settings.intro_icons_size_scale, settings.intro_icons_size_scale))
        self.screen.blit(icon, (self.xmax - 220, self.ymax - 200))

        pygame.display.update()

        if self.firstRun:
            self.firstRun = False
            time.sleep(1)

        tx, ty = disputil.DrawText(self.screen, settings.presskey, self.presskey_fontObj, settings.presskey_color,
                                   blit=False)
        disputil.DrawText(self.screen, settings.presskey, self.presskey_fontObj, settings.presskey_color,
                          blit=True, x=self.xmax/2 - tx/2, y=self.ymax*0.85)

        pygame.display.update((self.xmax/2 - tx/2, self.ymax*0.85-ty, tx, ty*2))

        event = disputil.event_loop()
        while event.get("Type") not in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            event = disputil.event_loop()
            time.sleep(0.1)

        self.choose_fauna()

        return

    ####################################################################
    def choose_fauna(self):

        self.chosen_fauna = []
        done = False
        chosen_count = 0
        draw_button = True
        changed = [True, True, True, True]
        chosen = [False, False, False, False]
        icon = ["", "", "", ""]
        box = ["", "", "", ""]
        box_bacteria_options = ["", "", "", ""]
        firstRun = True

        self.screen.fill(settings.cBkg_highlighted)
        rect = (self.xmax * 0.1, self.ymax * 0.1, self.xmax * 0.8, self.ymax * 0.8)
        pygame.draw.rect(self.screen, settings.cBkg, rect)

        while not done:

            if firstRun:

                arrow = disputil.loadIcon("Back", settings.iconf)
                arrow = pygame.transform.smoothscale(arrow, (64, 64))
                bx, by = arrow.get_size()
                self.screen.blit(arrow, (self.xmargin, self.ymax - self.ymargin - by))
                disputil.DrawText(self.screen, "Back", self.presskey_fontObj, pygame.Color("white"),
                                  blit=True, x=self.xmargin*2 + bx, y=self.ymax - self.ymargin - by*0.8)
                back_box = pygame.Rect((self.xmargin, self.ymax - self.ymargin - by, bx, by))

                arrow = pygame.transform.rotate(arrow, 180)
                self.screen.blit(arrow, (self.xmax - self.xmargin - bx, self.ymax - self.ymargin - by*0.9))
                tx, ty = disputil.DrawText(self.screen, "Options", self.presskey_fontObj, pygame.Color("white"),
                                           blit=False)
                disputil.DrawText(self.screen, "Options", self.presskey_fontObj, pygame.Color("white"),
                                  blit=True, x=self.xmax - self.xmargin*2 - bx - tx, y=self.ymax - self.ymargin - by*0.8)
                options_box = pygame.Rect((self.xmax - self.xmargin - bx, self.ymax - self.ymargin - by, bx, by))

                logo = disputil.loadIcon("Intro", settings.iconf)
                logo = pygame.transform.smoothscale(logo, (128, 128))

                for i in range(0, len(icon)):
                    icon[i] = disputil.loadIcon("Virus"+str(i+1)+"_Intro", settings.iconf)
                    icon[i] = pygame.transform.smoothscale(icon[i], (156, 156))
                    if i == 0:
                        ix, iy = icon[i].get_size()
                    if i % 2 == 0:
                        box[i] = pygame.Rect(self.xmax*0.1 + self.xgap, self.ymax*0.1 + self.ymargin + iy*i, ix, iy)
                        box_bacteria_options[i] = pygame.Rect(self.xmax*0.1 + self.xgap + ix, self.ymax*0.1 + self.ymargin + iy*i, self.xmax * 0.8 - self.xgap * 4, iy * 0.8)
                    else:
                        box[i] = pygame.Rect(self.xmax*0.9 - ix - self.xgap, self.ymax*0.1 + self.ymargin + iy*i, ix, iy)
                        box_bacteria_options[i] = pygame.Rect(self.xmax*0.1 + self.xgap + ix, self.ymax*0.1 + self.ymargin + iy*i, self.xmax * 0.8 - self.xgap * 4 - ix*1.5, iy * 0.8)

                button = pygame.Rect((self.xmax/2-100, self.ymax - 50 - self.ymargin, 200, 50))

            for i in range(0, len(changed)):
                if changed[i]:
                    xrect = self.xmax*0.1 + self.xgap*2
                    yrect = self.ymax*0.1 + self.ygap + iy*i
                    if chosen[i]:
                        rect_color = pygame.Color("orange")
                    else:
                        rect_color = pygame.Color("black")
                    text_color = pygame.Color("white")
                    pygame.draw.rect(self.screen, rect_color, (xrect, yrect, self.xmax * 0.8 - self.xgap*4, iy*0.8))

                    if i == 0:
                        self.screen.blit(logo, (self.xmax/2 - 64, self.ymin + self.ymargin))
                    self.screen.blit(icon[i], (box[i][0], box[i][1]))

                    name = self.fauna[i]["Name"].capitalize()
                    category = self.fauna[i]["Category"].capitalize()
                    food = self.fauna[i]["Food"].capitalize()
                    reproduction = self.fauna[i]["Reproduction"].capitalize()
                    speed = str(self.fauna[i]["Speed"])
                    longevity = str(self.fauna[i]["Longevity"])
                    max_size = str(self.fauna[i]["Max Size"])

                    tx, ty = disputil.DrawText(self.screen, name, self.name_fontObj, text_color, blit=False)
                    itx, ity = disputil.DrawText(self.screen, "Category: " + category, self.info_fontObj, text_color, blit=False)
                    if i % 2 == 0:
                        xinfo = box[i][0] + ix + self.xgap
                        xname = xinfo + itx + self.xgap*2
                    else:
                        xinfo = box[i][0] - itx - self.xgap
                        xname = xinfo - tx - self.xgap
                    yname = box[i][1] + self.ygap*2
                    yinfo = yrect + self.ymargin
                    disputil.DrawText(self.screen, name, self.name_fontObj, text_color, blit=True, x=xname, y=yname)
                    disputil.DrawText(self.screen, "Category: " + category, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                    yinfo = yinfo + ity
                    disputil.DrawText(self.screen, "Food: " + food, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                    yinfo = yinfo + ity
                    disputil.DrawText(self.screen, "Reproduction: " + reproduction, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                    yinfo = yinfo + ity
                    disputil.DrawText(self.screen, "Speed: " + speed, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                    yinfo = yinfo + ity
                    disputil.DrawText(self.screen, "Longevity: " + longevity, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                    yinfo = yinfo + ity
                    disputil.DrawText(self.screen, "Max Size: " + max_size, self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)

            if firstRun or draw_button or changed[0] or changed[1] or changed[2] or changed[3]:
                if draw_button:
                    if chosen_count:
                        color = pygame.Color("red")
                    else:
                        color = pygame.Color("darkgrey")
                    pygame.draw.rect(self.screen, color, (self.xmax/2-100, self.ymax - 50 - self.ymargin, 200, 50))
                    tx, ty = disputil.DrawText(self.screen, "Start!", self.presskey_fontObj, settings.presskey_color,
                                               blit=False)
                    disputil.DrawText(self.screen, "Start!", self.presskey_fontObj, settings.presskey_color,
                                      blit=True, x=self.xmax / 2 - tx / 2, y=self.ymax - 50 - self.ymargin)
                    draw_button = False

                pygame.display.update()
                changed = [False, False, False, False]
                firstRun = False

            event = disputil.event_loop()
            if event.get("Type") == pygame.MOUSEBUTTONDOWN:
                if back_box.collidepoint(event.get("Pos")):
                    self.intro()
                    return
                if options_box.collidepoint(event.get("Pos")):
                    self.general_options()
                    firstRun = True
                    changed = [True, True, True, True]
                    draw_button = True
                    pygame.draw.rect(self.screen, pygame.Color("cadetblue"),
                                     (self.xmin, self.ymin, self.xmax, self.ymax))
                    pygame.draw.rect(self.screen, pygame.Color("black"),
                                     (self.xmax * 0.1, self.ymax * 0.1, self.xmax * 0.8, self.ymax * 0.8))
                for i in range (0, len(box)):
                    if box[i].collidepoint(event.get("Pos")):
                        changed[i] = True
                        if chosen[i]:
                            chosen[i] = False
                            chosen_count -= 1
                        else:
                            chosen[i] = True
                            chosen_count += 1
                        draw_button = True
                for i in range (0, len(box_bacteria_options)):
                    if box_bacteria_options[i].collidepoint(event.get("Pos")):
                        self.fauna[i] = self.bacteria_options(self.fauna[i])
                        firstRun = True
                        changed = [True, True, True, True]
                        draw_button = True
                        pygame.draw.rect(self.screen, pygame.Color("cadetblue"),
                                         (self.xmin, self.ymin, self.xmax, self.ymax))
                        pygame.draw.rect(self.screen, pygame.Color("black"),
                                         (self.xmax * 0.1, self.ymax * 0.1, self.xmax * 0.8, self.ymax * 0.8))
                if button.collidepoint(event.get("Pos")) and chosen_count:
                    done = True
            elif event.get("Type") == pygame.KEYDOWN:
                if event.get("Key") == pygame.K_RETURN and chosen_count:
                    done = True

            time.sleep(0.05)

        for i in range(0, len(chosen)):
            if chosen[i]:
                self.chosen_fauna.append(i)

        return

    ####################################################################
    def bacteria_options(self, bacteria):

        self.screen.fill(pygame.Color("cadetblue4"))

        icon = disputil.loadIcon(bacteria["Icon File"]+"_Intro", settings.iconf)
        icon = pygame.transform.smoothscale(icon, (128, 128))
        ix, iy = icon.get_size()
        self.screen.blit(icon, (self.xmax / 2 - 64, self.ymin + self.ymargin))

        frame_icon = disputil.loadIcon("Frame", settings.iconf)
        frame_icon = pygame.transform.smoothscale(frame_icon, (32, 32))
        check_icon = disputil.loadIcon("Check", settings.iconf)
        check_icon = pygame.transform.smoothscale(check_icon, (32, 32))

        done = False
        text = ["Category", "Food", "Starvation Limit", "Reproduction", "Gestation Gap", "Speed", "Longevity", "Max Size"]
        value = [bacteria["Category"], bacteria["Food"], bacteria["Starvation Limit"], bacteria["Reproduction"], bacteria["Gestation Gap"], bacteria["Speed"], bacteria["Longevity"], bacteria["Max Size"]]
        changed = [True, True, True, True, True, True, True, True]
        box = ["", "", "", "", "", "", "", ""]
        firstRun = True

        tx, ty = disputil.DrawText(self.screen, bacteria["Name"], self.name_fontObj, settings.cOptions_title,
                                   blit=False)
        disputil.DrawText(self.screen, bacteria["Name"], self.name_fontObj, settings.cOptions_title,
                          blit=True, x=self.xmax/2 - tx/2, y=self.ygap + iy*0.8)

        x = self.xgap * 10
        y = self.ygap + iy*0.8 + ty
        ix = x + self.xgap*10 + self.xgap
        init_iy = y + self.ymargin

        for i in range(0, len(text)):
            tx, ty = disputil.DrawText(self.screen, text[i], self.presskey_fontObj,
                                       settings.cOptions_text, blit=True, x=x, y=y)
            if i == 0:
                disputil.DrawText(self.screen, settings.category_tip, self.info_fontObj, settings.cOptions_text,
                                  blit=True, x=x, y=y+ty*0.8)
            elif i == 1:
                disputil.DrawText(self.screen, settings.food_tip, self.info_fontObj, settings.cOptions_text,
                                  blit=True, x=x, y=y+ty*0.8)
            elif i == 3:
                disputil.DrawText(self.screen, settings.reproduction_tip, self.info_fontObj, settings.cOptions_text,
                                  blit=True, x=x, y=y+ty*0.8)
            y = y + ty + self.ygap

        pygame.draw.rect(self.screen, settings.cButton, (self.xmax / 2 - 100, self.ymax - 50 - self.ymargin, 200, 50))
        tx, ty = disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.cButton_text,
                                   blit=False)
        disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.cButton_text,
                          blit=True, x=self.xmax / 2 - tx / 2, y=self.ymax - 50 - self.ymargin)
        button = pygame.Rect((self.xmax / 2 - 100, self.ymax - 50 - self.ymargin, 200, 50))

        while not done:

            for i in range(0, len(value)):
                if changed[i]:
                    iy = init_iy + (ty + self.ygap) * i
                    if (type(value[i]) is int or
                            type(value[i]) is str) and \
                            (firstRun or changed[i]):
                        disputil.DrawText(self.screen, str(value[i]), self.presskey_fontObj, settings.cOptions_text,
                                          blit=True, x=ix, y=iy)
                        box[i] = pygame.Rect(ix, iy, 100, 50)
                        if not firstRun:
                            value[i] = disputil.get_input_box_value(self.screen, ix, iy, str(value[i]))
                    elif type(value[i]) is bool:
                        pygame.draw.rect(self.screen, pygame.Color("cadetblue4"), (ix, iy, 32, 32))
                        self.screen.blit(frame_icon, (ix, iy))
                        if not firstRun:
                            if value[i]:
                                value[i] = False
                            else:
                                value[i] = True
                        if value[i]:
                            self.screen.blit(check_icon, (ix, iy))
                        box[i] = pygame.Rect(ix, iy, 32, 32)
                    update_disp = True
                    changed[i] = False

            if firstRun or update_disp:
                pygame.display.update()
                firstRun = False
                update_disp = False

            event = disputil.event_loop()
            if event.get("Type") == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(box)):
                    if box[i].collidepoint(event.get("Pos")):
                        changed[i] = True
                if button.collidepoint(event.get("Pos")):
                    done = True
            elif event.get("Type") == pygame.KEYDOWN:
                if event.get("Key") == pygame.K_RETURN:
                    done = True

            time.sleep(0.05)

        bacteria["Category"] = value[0]
        bacteria["Food"] = value[1]
        bacteria["Starvation Limit"] = int(value[2])
        bacteria["Reproduction"] = value[3]
        bacteria["Gestation Gap"] = int(value[4])
        bacteria["Speed"] = int(value[5])
        bacteria["Longevity"] = int(value[6])
        bacteria["Max Size"] = int(value[7])

        return bacteria

    ####################################################################
    def general_options(self):

        self.screen.fill(pygame.Color("cadetblue4"))

        frame_icon = disputil.loadIcon("Frame", settings.iconf)
        frame_icon = pygame.transform.smoothscale(frame_icon, (32, 32))
        check_icon = disputil.loadIcon("Check", settings.iconf)
        check_icon = pygame.transform.smoothscale(check_icon, (32, 32))

        done = False
        text = ["Initial Specimen Number", "Show Icons", "Show Values", "Food Mode Activated", "Food Growth Ratio", "Show Terrain", "Logging"]
        value = [self.init_bacteria_number, self.show_icons, self.show_values, self.food_activated, self.food_growth_gap, self.show_terrain, self.logging]
        changed = [True, True, True, True, True, True, True]
        box = ["", "", "", "", "", "", ""]
        firstRun = True

        tx, ty = disputil.DrawText(self.screen,settings.options, self.title_fontObj, settings.cOptions_title,
                                   blit=False)
        disputil.DrawText(self.screen, settings.options, self.title_fontObj, settings.cOptions_title,
                          blit=True, x=self.xmax/2 - tx/2, y=self.ygap)

        x = self.xgap * 10
        y = ty + self.ygap
        ix = x + tx + self.xgap
        init_iy = y + self.ymargin

        for i in range(0, len(text)):
            tx, ty = disputil.DrawText(self.screen, text[i], self.presskey_fontObj, settings.cOptions_text,
                                       blit=True, x=x, y=y)
            if i == 4:
                disputil.DrawText(self.screen, settings.food_growth_tip, self.info_fontObj, settings.cOptions_text,
                                  blit=True, x=x, y=y+ty*0.8)
            y = y + ty + self.ygap*1.5


        pygame.draw.rect(self.screen, settings.cButton, (self.xmax / 2 - 100, self.ymax - 50 - self.ymargin, 200, 50))
        tx, ty = disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.cButton_text,
                                   blit=False)
        disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.cButton_text,
                          blit=True, x=self.xmax / 2 - tx / 2, y=self.ymax - 50 - self.ymargin)
        button = pygame.Rect((self.xmax / 2 - 100, self.ymax - 50 - self.ymargin, 200, 50))

        while not done:

            for i in range(0, len(value)):
                if changed[i]:
                    iy = init_iy + (ty + self.ygap*1.5) * i
                    if type(value[i]) is int and (firstRun or changed[i]):
                        disputil.DrawText(self.screen, str(value[i]), self.presskey_fontObj, pygame.Color("white"),
                                          blit=True, x=ix, y=iy)
                        box[i] = pygame.Rect(ix, iy, 100, 50)
                        if not firstRun:
                            value[i] = disputil.get_input_box_value(self.screen, ix, iy, str(value[i]))
                    elif type(value[i]) is bool:
                        pygame.draw.rect(self.screen, pygame.Color("cadetblue4"), (ix, iy, 32, 32))
                        self.screen.blit(frame_icon, (ix, iy))
                        if not firstRun:
                            if value[i]:
                                value[i] = False
                            else:
                                value[i] = True
                        if value[i]:
                            self.screen.blit(check_icon, (ix, iy))
                        box[i] = pygame.Rect(ix, iy, 32, 32)
                    update_disp = True
                    changed[i] = False

            if firstRun or update_disp:
                pygame.display.update()
                firstRun = False
                update_disp = False

            event = disputil.event_loop()
            if event.get("Type") == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(box)):
                    if box[i].collidepoint(event.get("Pos")):
                        changed[i] = True
                if button.collidepoint(event.get("Pos")):
                    done = True
            elif event.get("Type") == pygame.KEYDOWN:
                if event.get("Key") == pygame.K_RETURN:
                    done = True

            time.sleep(0.05)

        self.init_bacteria_number = int(value[0])
        self.show_icons = value[1]
        self.show_values = value[2]
        self.food_activated = value[3]
        self.food_growth_gap = int(value[4])
        self.show_terrain = value[5]
        self.logging = value[6]

        return

    ####################################################################
    def create_terrain(self):

        if self.food_activated:
            self.terrain_type = [["organic" for y in range(self.ymax)] for x in range(self.xmax)]
            self.terrain_age = [[0 for y in range(self.ymax)] for x in range(self.xmax)]

        return

    ####################################################################
    def grow_terrain(self):

        if self.food_activated:
            self.screen.fill(pygame.Color("darkslategrey"))

            for i in range(self.xmin, self.xmax):
                for j in range(self.ymin, self.ymax):
                    if self.terrain_type[i][j] == "ground":
                        if self.terrain_age[i][j] > self.food_growth_gap:
                            self.terrain_type[i][j] = "organic"
                        else:
                            self.terrain_age[i][j] += 1
                    if self.food_activated and self.show_terrain and self.terrain_type[i][j] == "ground":
                        self.screen.set_at((i, j), settings.cBkg)

            # pygame.display.update()

        return

    ####################################################################
    def create_colony(self):

        colony = []
        for i in range(0, len(self.chosen_fauna)):
            for j in range(0, int(self.init_bacteria_number / len(self.chosen_fauna))):
                colony.append(myColony.birth(self.fauna[self.chosen_fauna[i]], i))
            self.icon.append(disputil.loadIcon(self.fauna[self.chosen_fauna[i]]["Icon File"], settings.iconf))

        print("COLONY CREATED with %s specimen" % self.init_bacteria_number)
        print("Food mode:", self.food_activated)
        print("Food Growth:", self.food_growth_gap)
        for i in range(0, len(self.chosen_fauna)):
            ratio = int((self.init_bacteria_number / len(self.chosen_fauna)) / self.init_bacteria_number * 100)
            print(self.fauna[self.chosen_fauna[i]]["Name"], ratio, "%", "| Category:", self.fauna[self.chosen_fauna[i]]["Category"], "| Reproduction:", self.fauna[self.chosen_fauna[i]]["Reproduction"], "| Starvation Limit:", self.fauna[self.chosen_fauna[i]]["Starvation Limit"], "| Gestation Gap:",self.fauna[self.chosen_fauna[i]]["Gestation Gap"])
        print()

        return colony

    ####################################################################
    def birth(self, bacteria_settings, icon):

        bacteria = dict(bacteria_settings)
        bacteria["Status"] = "alive"
        if bacteria["Reproduction"] == "sex":
            bacteria["Gender"] = random.choice(settings.genders)
        bacteria["Position"] = random.randint(self.xmin, self.xmax), random.randint(self.ymin, self.ymax)
        bacteria["Size"] = bacteria_settings["Birth Size"]
        bacteria["Speed"] = min(10, bacteria_settings["Speed"])
        bacteria["Last Move"] = 0
        bacteria["Next Run"] = random.randint(0, bacteria["Max Run"])
        bacteria["Last Direction"] = random.choice(settings.directions)
        bacteria["Maturity Init Point"] = int(bacteria["Longevity"] * 0.2)
        bacteria["Maturity End Point"] = int(bacteria["Longevity"] * 0.8)
        bacteria["Age"] = random.randint(0, int(bacteria_settings["Maturity Init Point"]/4))
        bacteria["Growth Gap"] = int((bacteria["Maturity Init Point"] - bacteria["Age"]) / bacteria["Maturity Size"])
        bacteria["Starvation Limit"] = min(bacteria["Starvation Limit"], self.food_growth_gap - 1)
        bacteria["Last Dinner"] = 0
        bacteria["Last Gestation"] = bacteria["Gestation Gap"]
        bacteria["Icon Index"] = icon

        return bacteria

    ####################################################################
    def draw(self, colony):

        if not self.food_activated or not self.show_terrain:
            self.screen.fill(settings.cBkg)

        for i in range(0, len(colony)):
            if colony[i]["Status"] == "alive":
                if not self.show_icons or colony[i]["Icon Index"] is None:
                    pygame.draw.circle(self.screen, colony[i]["Color"], colony[i]["Position"], int(colony[i]["Size"]), 0)
                else:
                    icon = pygame.transform.smoothscale(self.icon[colony[i]["Icon Index"]],
                                                        (int(colony[i]["Size"] * 2), int(colony[i]["Size"] * 2)))
                    if colony[i]["Rotate"]:
                        icon = pygame.transform.rotate(icon, random.choice([0, 90, 180, 270]))
                    self.screen.blit(icon,
                                     (colony[i]["Position"][0] - colony[i]["Size"],
                                      colony[i]["Position"][1] - colony[i]["Size"]))
                if self.show_values:
                    if self.show_icons:
                        x = colony[i]["Position"][0] - colony[i]["Size"]
                        y = colony[i]["Position"][1] - colony[i]["Size"] - settings.values_font_size
                    else:
                        x = colony[i]["Position"][0] - colony[i]["Size"]*2
                        y = colony[i]["Position"][1] - settings.values_font_size / 2
                    disputil.DrawText(self.screen, str(colony[i]["Size"])+", "+str(colony[i]["Age"]),
                                      self.fontObj, pygame.Color("white"), blit=True, x=x, y=y)

        pygame.display.update()

        return

    ####################################################################
    def move(self, colony):

        for i in range(0, len(colony)):
            if colony[i]["Next Run"] <= 0:
                direction = random.choice(settings.directions)
                colony[i]["Last Direction"] = direction
                colony[i]["Next Run"] = random.randint(1, colony[i]["Max Run"])
            else:
                direction = colony[i]["Last Direction"]
                colony[i]["Next Run"] -= 1

            x = int((colony[i]["Position"][0] + direction[0] * colony[i]["Size"] * (colony[i]["Speed"]/10))) % settings.display_size[0]
            y = int((colony[i]["Position"][1] + direction[1] * colony[i]["Size"] * (colony[i]["Speed"]/10))) % settings.display_size[1]
            colony[i]["Position"] = (x, y)

        return colony

    ####################################################################
    def check(self, colony):

        end_colony = []

        for i in range(0, len(colony)):
            son = None
            eaten = False

            colony[i] = self.check_age(colony[i])
            if colony[i]["Status"] == "alive":
                if colony[i]["Reproduction"] == "mitosis":
                    son, colony[i], foo = self.check_reproduction(colony[i])

                if colony[i]["Category"] == "prey":
                    eaten, colony[i], foo = self.check_feed(colony[i])

                if colony[i]["Category"] in ("predator", "both") or \
                   colony[i]["Reproduction"] == "sex":

                    for j in range(0, len(colony)):
                        if i != j:
                            if self.check_collision(colony[i], colony[j]):

                                if colony[i]["Reproduction"] == "sex":
                                    son, colony[i], colony[j] = self.check_reproduction(colony[i], colony[j])

                                if son is None and colony[i]["Category"] in ("predator", "both"):
                                    mark_eaten, colony[i], colony[j] = self.check_feed(colony[i], colony[j])
                                    if mark_eaten: eaten = True

                colony[i] = self.check_starvation(colony[i], eaten)
                colony[i] = self.check_growth(colony[i])
                end_colony = self.check_end_colony(end_colony, colony[i], son)

        self.monitor(end_colony)

        return end_colony

    ####################################################################
    def check_age(self, bacteria):

        if bacteria["Age"] > bacteria["Longevity"]:
            bacteria["Status"] = "dead"
            if settings.logging_verbose:
                print(bacteria["Name"], "died of old at age", bacteria["Age"])
        else:
            bacteria["Age"] += 1

        return bacteria

    ####################################################################
    def check_collision(self, bacteria1, bacteria2):

        rect = (bacteria1["Position"][0] - bacteria1["Size"], bacteria1["Position"][1] - bacteria1["Size"],
                bacteria1["Size"] * 2, bacteria1["Size"] * 2)
        box = pygame.Rect(rect)

        collide = box.collidepoint(bacteria2["Position"])

        return collide

    ####################################################################
    def check_reproduction(self, bacteria1, bacteria2=None):

        son = None

        if bacteria1["Reproduction"] == "mitosis":
            if bacteria1["Maturity Init Point"] <= bacteria1["Age"] <= bacteria1["Maturity End Point"] and \
                    bacteria1["Last Gestation"] >= bacteria1["Gestation Gap"]:
                son = self.birth(bacteria1, bacteria1["Icon Index"])
                bacteria1["Last Gestation"] = 0
                if settings.logging_verbose:
                    print(bacteria1["Name"], "reproduced by mitosis at age:", bacteria1["Age"], "Gestation:",
                          bacteria1["Last Gestation"], "over", bacteria1["Gestation Gap"])
            else:
                bacteria1["Last Gestation"] += 1
            bacteria2 = True
        elif bacteria2 is not None:
            if bacteria1["Name"] == bacteria2["Name"] and \
                    bacteria1["Maturity Init Point"] <= bacteria1["Age"] <= bacteria1["Maturity End Point"] and \
                    bacteria2["Maturity Init Point"] <= bacteria1["Age"] <= bacteria2["Maturity End Point"] and \
                    bacteria1["Last Gestation"] >= bacteria1["Gestation Gap"] and \
                    bacteria2["Last Gestation"] >= bacteria2["Gestation Gap"] and \
                    ((bacteria1["Gender"] == "male" and bacteria2["Gender"] == "female") or \
                     (bacteria1["Gender"] == "female" and bacteria2["Gender"] == "male") or \
                      bacteria1["Gender"] == "both" or bacteria2["Gender"] == "both"):
                son = self.birth(bacteria1, bacteria1["Icon Index"])
                if bacteria1["Gender"] == "female":
                    bacteria1["Last Gestation"] = 0
                if bacteria2["Gender"] == "female":
                    bacteria2["Last Gestation"] = 0
                if settings.logging_verbose:
                    print(bacteria1["Name"], bacteria1["Gender"], ", REPRODUCED by sex at age:", bacteria1["Age"],
                        "After Gestation:", bacteria1["Last Gestation"], "over", bacteria1["Gestation Gap"], "with",
                        bacteria2["Name"], bacteria2["Gender"], "at age:", bacteria2["Age"], "After Gestation:",
                        bacteria2["Last Gestation"], "over", bacteria2["Gestation Gap"])
            else:
                if bacteria1["Gender"] == "female":
                    bacteria1["Last Gestation"] += 1
                if bacteria2["Gender"] == "female":
                    bacteria2["Last Gestation"] += 1
                if settings.logging_verbose:
                    print(bacteria1["Name"], bacteria1["Gender"], ", COULDN'T REPRODUCE by sex at age:", bacteria1["Age"],
                      "After Gestation:", bacteria1["Last Gestation"], "over", bacteria1["Gestation Gap"], "with",
                      bacteria2["Name"], bacteria2["Gender"], "at age:", bacteria2["Age"], "After Gestation:",
                      bacteria2["Last Gestation"], "over", bacteria2["Gestation Gap"])

        return son, bacteria1, bacteria2

    ####################################################################
    def check_feed(self, bacteria1, bacteria2=None):

        eaten = False

        if bacteria1["Category"] in ("predator", "both"):
            if bacteria2 is not None:
                if bacteria2["Status"] == "alive" and \
                        bacteria2["Category"] != "predator" and \
                        (bacteria1["Size"] > bacteria2["Size"] or
                            (bacteria1["Size"] == bacteria2["Size"] and bacteria1["Age"] > bacteria2["Age"])) and \
                        ((bacteria1["Hunt Randomize"] and random.randint(1, bacteria1["Hunt Success"])) != 1 or
                        not bacteria1["Hunt Randomize"]):
                    bacteria2["Status"] = "dead"
                    bacteria1["Size"] = min(bacteria1["Size"] + bacteria2["Size"], bacteria1["Max Size"])
                    if settings.logging_verbose:
                        print(bacteria1["Name"], "Age:", bacteria1["Age"], "Size:", bacteria1["Size"],
                              "Hunt Randomize:", bacteria1["Hunt Randomize"], "Hunt Success:", bacteria1["Hunt Success"],
                              "| ATE |",
                              bacteria2["Name"], "Age:", bacteria1["Age"], "Size:", bacteria1["Size"])
                    eaten = True
                else:
                    if settings.logging_verbose:
                        print(bacteria1["Name"], "Age:", bacteria1["Age"], "Size:", bacteria1["Size"],
                              "Hunt Randomize:", bacteria1["Hunt Randomize"], "Hunt Success:", bacteria1["Hunt Success"],
                              "| COULDN'T EAT |",
                              bacteria2["Name"], "Age:", bacteria1["Age"], "Size:", bacteria1["Size"])

        elif self.food_activated:
            for i in range(0, int(bacteria1["Size"])):
                x = min(bacteria1["Position"][0] - int(bacteria1["Size"]/2) + i, self.xmax-1)
                for j in range(0, int(bacteria1["Size"])):
                    y = min(bacteria1["Position"][1] - int(bacteria1["Size"]/2) + j, self.ymax-1)
                    if self.terrain_type[x][y] == bacteria1["Food"]:
                        self.terrain_type[x][y] = "ground"
                        self.terrain_age[x][y] = 0
                        eaten = True

        return eaten, bacteria1, bacteria2

    ####################################################################
    def check_starvation(self, bacteria, eaten):

        if self.food_activated:
            if eaten or \
                    (bacteria["Category"] in ("predator", "both") and bacteria["Age"] < bacteria["Maturity Init Point"]):
                bacteria["Last Dinner"] = 0
            else:
                bacteria["Last Dinner"] += 1
                if bacteria["Last Dinner"] > bacteria["Starvation Limit"]:
                    bacteria["Status"] = "dead"
                    if settings.logging_verbose:
                        print(bacteria["Name"], "died by starvation at age:", bacteria["Age"], "Size:", bacteria["Size"],
                              "Last dinner:", bacteria["Last Dinner"], "Starvation Limit:", bacteria["Starvation Limit"])

        return bacteria

    ####################################################################
    def check_growth(self, bacteria):

        if bacteria["Age"] <= bacteria["Maturity Init Point"] and \
                float(bacteria["Age"]) % float(bacteria["Growth Gap"]) == 0.0 and \
                bacteria["Size"] < bacteria["Maturity Size"]:
            bacteria["Size"] = bacteria["Size"] + 1

        return bacteria

    ####################################################################
    def check_end_colony(self, colony, bacteria, son):

        if son is not None:
            colony.append(son)

        if bacteria["Status"] == "alive":
            colony.append(bacteria)

        return colony

    ####################################################################
    def monitor(self, colony):

        if not colony:
            print("Your colony died!!!")
        else:
            self.colony_age += 1
            population = len(colony)
            self.average = int(((self.average * max(1, self.colony_age - 1)) + population) / self.colony_age)
            dif = int(((population - self.average) / self.average) * 100)
            if self.logging:
                print("COLONY age: %d | population: %d | average: %d | dif: %d%%" % (self.colony_age, population, self.average, dif))

        return

    #####################################################################
    def catch_action(self, event, colony):

        if event["Key"] is not None and event["Key"] != self.keyP:
            self.keyP = event["Key"]

            if event["Key"] == pygame.K_c:
                icon = disputil.loadIcon("Lightning", settings.iconf)
                ix, iy = icon.get_size()
                icon = pygame.transform.smoothscale(icon, (256, 256))
                x = random.randint(50, self.xmax - 50)
                y = random.randint(50, self.ymax - 50)
                self.screen.blit(icon, (x,y))
                pygame.display.update((x, y, 256, 256))
                for i in range(0, len(colony)):
                    if x <= colony[i]["Position"][0] <= (x + 256*0.8) and \
                            y <= colony[i]["Position"][1] <= (y + 256*0.8):
                        colony[i]["Status"] = "dead"
                time.sleep(1)

            if event["Key"] == pygame.K_r:
                importlib.reload(settings)
                pygame.display.quit()
                self.__init__()
                self.create_colony()

        return colony


####################################################################
myColony = Colony()

if settings.intro: myColony.intro()
myColony.create_terrain()
colony = myColony.create_colony()

while True:

    myColony.grow_terrain()
    myColony.draw(colony)
    colony = myColony.move(colony)
    colony = myColony.check(colony)

    if not colony: break
    colony = myColony.catch_action(disputil.event_loop(), colony)
    time.sleep(0.2)
