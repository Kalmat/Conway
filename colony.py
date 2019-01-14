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
                                                         hideMouse=False, icon=settings.icons_folder + settings.icon,
                                                         caption=settings.caption)
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

        self.fontObj = disputil.LoadFont(settings.fonts_folder+settings.values_font, settings.values_font_size, 0)
        self.welcome_fontObj = disputil.LoadFont(settings.fonts_folder+settings.welcome_font, settings.welcome_font_size, 0)
        self.title_fontObj = disputil.LoadFont(settings.fonts_folder+settings.title_font, settings.title_font_size, 0)
        self.presskey_fontObj = disputil.LoadFont(settings.fonts_folder+settings.presskey_font, settings.presskey_font_size, 1)
        self.name_fontObj = disputil.LoadFont(settings.fonts_folder+settings.name_font, settings.name_font_size, 0)
        self.info_fontObj = disputil.LoadFont(settings.fonts_folder+settings.info_font, settings.info_font_size, 0)

        self.first_run = True
        self.chosen_fauna = settings.colony_diversity
        self.icon = []
        self.terrain_type = None
        self.terrain_age = None
        self.colony_age = 0
        self.average = 0
        self.keyP = ""

    ####################################################################
    def intro(self):

        self.screen.fill(settings.cBkg)
        pygame.draw.rect(self.screen, settings.cBkg_highlighted, (self.xmax*0.1, self.ymax*0.1, self.xmax*0.8, self.ymax*0.8))

        for i in range(0, 4):
            icon = disputil.loadIcon("Virus"+str(i+1)+"_Intro", settings.icons_folder)
            icon = pygame.transform.smoothscale(icon, (settings.intro_icons_scale, settings.intro_icons_scale))
            x = self.xmax * settings.intro_icon_pos[i][0] - int(self.xmax * settings.intro_icon_gap[i][0] / 1280)
            y = self.ymax * settings.intro_icon_pos[i][1] - int(self.ymax * settings.intro_icon_gap[i][1] / 800)
            self.screen.blit(icon, (x, y))

        disputil.DrawText(self.screen, settings.welcome, self.welcome_fontObj, settings.welcome_color,
                          blit=True, x=self.xmax*0.1 + self.xgap, y=int(self.ymax*1/3.2))

        pygame.display.update()

        tx, ty = disputil.DrawText(self.screen, settings.title, self.title_fontObj, settings.title_color, blit=False)
        if self.first_run:
            disputil.DrawText(self.screen, settings.title, self.title_fontObj, settings.title_color,
                              blit=True, x=self.xmax/2 - tx/2, y=self.ymax/2 - ty/2,
                              outline="FadeIn", ocolor=settings.cBkg_highlighted)
            self.first_run = False
        else:
            disputil.DrawText(self.screen, settings.title, self.title_fontObj, settings.title_color,
                              blit=True, x=self.xmax/2 - tx/2, y=self.ymax/2 - ty/2)
        rect = [(self.xmax/2 - tx/2, self.ymax/2 - ty/2,  tx, ty)]

        icon = disputil.loadIcon(settings.intro_icon, settings.icons_folder)
        icon = pygame.transform.smoothscale(icon, (settings.intro_size_scale, settings.intro_size_scale))
        self.screen.blit(icon, (self.xmax/2+settings.intro_size_scale/10, self.ymax/2-settings.intro_size_scale/2))

        tx, ty = disputil.DrawText(self.screen, settings.presskey, self.presskey_fontObj, settings.presskey_color,
                                   blit=False)
        disputil.DrawText(self.screen, settings.presskey, self.presskey_fontObj, settings.presskey_color,
                          blit=True, x=self.xmax/2 - tx/2, y=self.ymax*0.85)
        rect.append((self.xmax/2 - tx/2, self.ymax*0.85, tx, ty))

        pygame.display.update(rect)

        event = disputil.event_loop()
        while event.get("Type") not in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            event = disputil.event_loop()
            time.sleep(0.01)

        self.choose_fauna()

        return

    ####################################################################
    def choose_fauna(self):

        self.chosen_fauna = []
        done = False
        first_run = True
        chosen_count = 0
        draw_button = True
        changed = [True] * len(settings.fauna)
        chosen = [False] * len(settings.fauna)
        icon = [""] * len(settings.fauna)
        box = [""] * len(settings.fauna)
        box_bacteria_options = [""] * len(settings.fauna)

        self.screen.fill(settings.cBkg_highlighted)
        rect = (self.xmax * 0.1, self.ymax * 0.1, self.xmax * 0.8, self.ymax * 0.8)
        pygame.draw.rect(self.screen, settings.cBkg, rect)

        while not done:

            if first_run:

                arrow = disputil.loadIcon(settings.arrow_icon, settings.icons_folder)
                arrow = pygame.transform.smoothscale(arrow, (settings.arrow_icon_scale, settings.arrow_icon_scale))
                bx, by = arrow.get_size()
                self.screen.blit(arrow, (self.xmargin, self.ymax - self.ymargin - by))
                disputil.DrawText(self.screen, settings.back, self.presskey_fontObj, pygame.Color("white"),
                                  blit=True, x=self.xmargin*2 + bx, y=self.ymax - self.ymargin - by*0.8)
                back_box = pygame.Rect((self.xmargin, self.ymax - self.ymargin - by, bx, by))

                arrow = pygame.transform.rotate(arrow, 180)
                self.screen.blit(arrow, (self.xmax - self.xmargin - bx, self.ymax - self.ymargin - by*0.9))
                tx, ty = disputil.DrawText(self.screen, settings.options.capitalize(), self.presskey_fontObj,
                                          settings.presskey_color, blit=False)
                disputil.DrawText(self.screen, settings.options.capitalize(), self.presskey_fontObj, settings.presskey_color,
                                  blit=True, x=self.xmax - self.xmargin*2 - bx - tx, y=self.ymax - self.ymargin - by*0.8)
                options_box = pygame.Rect((self.xmax - self.xmargin - bx, self.ymax - self.ymargin - by, bx, by))

                logo = disputil.loadIcon(settings.intro_icon, settings.icons_folder)
                logo = pygame.transform.smoothscale(logo, (settings.intro_fauna_icon_scale, settings.intro_fauna_icon_scale))

                for i in range(0, len(icon)):
                    icon[i] = disputil.loadIcon(settings.intro_icons_prefix+str(i+1)+settings.intro_icons_suffix, settings.icons_folder)
                    icon[i] = pygame.transform.smoothscale(icon[i], (settings.fauna_icons_scale, settings.fauna_icons_scale))
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
                        self.screen.blit(logo, (self.xmax/2 - 50, self.ymin + self.ymargin))
                    self.screen.blit(icon[i], (box[i][0], box[i][1]))

                    itx, ity = disputil.DrawText(self.screen, self.fauna[i]["Name"].capitalize(), self.name_fontObj, settings.info_font_color, blit=False)
                    if i % 2 == 0:
                        xinfo = box[i][0] + ix + self.xgap
                        xname = xinfo + self.xgap*4
                    else:
                        xinfo = box[i][0] - ix
                        xname = xinfo - itx - self.xgap
                    yname = box[i][1] + self.ygap*2
                    yinfo = yrect + self.ymargin
                    disputil.DrawText(self.screen, self.fauna[i]["Name"].capitalize(), self.name_fontObj, settings.info_font_color, blit=True, x=xname, y=yname)
                    info_texts = ["Category: ", "Food: ", "Reproduction: ", "Speed: ", "Longevity: ", "Max Size: "]
                    info_values = [self.fauna[i]["Category"].capitalize(), self.fauna[i]["Food"].capitalize(), self.fauna[i]["Reproduction"].capitalize(), str(self.fauna[i]["Speed"]), str(self.fauna[i]["Longevity"]), str(self.fauna[i]["Max Size"])]
                    for i in range(0, len(info_texts)):
                        itx, ity = disputil.DrawText(self.screen, info_texts[i] + info_values[i], self.info_fontObj, text_color, blit=True, x=xinfo, y=yinfo)
                        yinfo = yinfo + ity

            if first_run or draw_button or changed[0] or changed[1] or changed[2] or changed[3]:
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
                first_run = False

            event = disputil.event_loop()
            if event.get("Type") == pygame.MOUSEBUTTONDOWN:
                if back_box.collidepoint(event.get("Pos")):
                    self.intro()
                    return
                if options_box.collidepoint(event.get("Pos")):
                    self.general_options()
                    first_run = True
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
                        first_run = True
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

            time.sleep(0.01)

        for i in range(0, len(chosen)):
            if chosen[i]:
                self.chosen_fauna.append(i)

        return

    ####################################################################
    def bacteria_options(self, bacteria):

        self.screen.fill(pygame.Color("cadetblue4"))

        icon = disputil.loadIcon(bacteria["Icon File"] +"_Intro", settings.icons_folder)
        icon = pygame.transform.smoothscale(icon, (settings.bacteria_options_icon_scale, settings.bacteria_options_icon_scale))
        ix, iy = icon.get_size()
        self.screen.blit(icon, (self.xmax / 2 - ix/2, self.ymin + self.ymargin))

        tx, ty = disputil.DrawText(self.screen, bacteria["Name"], self.name_fontObj, settings.options_title_color, blit=False)
        disputil.DrawText(self.screen, bacteria["Name"], self.name_fontObj, settings.options_title_color, blit=True, x=self.xmax/2 - tx/2, y=self.ygap + iy*0.8)

        text = ["Category", "Food", "Starvation Limit", "Reproduction", "Gestation Gap", "Speed", "Longevity", "Max Size"]
        tip = [settings.category_tip, settings.food_tip, settings.starvation_tip, settings.reproduction_tip, None, None, None, None]
        value = [bacteria["Category"], bacteria["Food"], bacteria["Starvation Limit"], bacteria["Reproduction"], bacteria["Gestation Gap"], bacteria["Speed"], bacteria["Longevity"], bacteria["Max Size"]]
        rect = (self.xgap * 10, iy + ty + self.ygap, self.xmax*0.8, self.ymax*0.8)

        value = self.get_options(text, tip, value, rect)

        bacteria["Category"],  = value[0]
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

        self.screen.fill(settings.cBkg_highlighted)

        tx, ty = disputil.DrawText(self.screen, settings.options, self.title_fontObj, settings.options_title_color,
                                   blit=False)
        disputil.DrawText(self.screen, settings.options, self.title_fontObj, settings.options_title_color, blit=True,
                          x=self.xmax / 2 - tx / 2, y=self.ygap)

        text = ["Initial Specimen Number", "Show Icons", "Show Values", "Food Mode Activated", "Food Growth Ratio", "Show Terrain", "Logging"]
        tip = [None, None, None, None, settings.food_growth_tip, None, None]
        value = [self.init_bacteria_number, self.show_icons, self.show_values, self.food_activated, self.food_growth_gap, self.show_terrain, self.logging]
        rect = (self.xgap * 10, ty + self.ygap, self.xmax*0.8, self.ymax*0.8)

        value = self.get_options(text, tip, value, rect)

        self.init_bacteria_number = int(value[0])
        self.show_icons = value[1]
        self.show_values = value[2]
        self.food_activated = value[3]
        self.food_growth_gap = int(value[4])
        self.show_terrain = value[5]
        self.logging = value[6]

        return

    ####################################################################
    def get_options(self, text, tip, value, rect):

        x, y, ex, ey = rect

        frame_icon = disputil.loadIcon("Frame", settings.icons_folder)
        frame_icon = pygame.transform.smoothscale(frame_icon, (settings.frame_check_scale, settings.frame_check_scale))
        check_icon = disputil.loadIcon("Check", settings.icons_folder)
        check_icon = pygame.transform.smoothscale(check_icon, (settings.frame_check_scale, settings.frame_check_scale))

        done = False
        first_run = True
        event_box = None
        changed = [True] * len(text)
        box = [""] * len(text)

        ix = x + self.xgap*10 + self.xgap
        init_iy = y + self.ymargin

        for i in range(0, len(text)):
            tx, ty = disputil.DrawText(self.screen, text[i], self.presskey_fontObj,
                                       settings.options_color, blit=True, x=x, y=y)

            if tip[i] is not None:
                disputil.DrawText(self.screen, tip[i], self.info_fontObj, settings.options_color,
                                  blit=True, x=x, y=y+ty*0.8)
            y = y + ty + self.ygap

        rect = (self.xmax / 2 - int(self.xmax * 100 / 1280),
                self.ymax - int(self.ymax * 50 / 800) - self.ymargin,
                int(self.xmax * 200 / 1280), int(self.ymax * 50 / 800))
        pygame.draw.rect(self.screen, settings.cButton, rect)
        tx, ty = disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.button_text_color,
                                   blit=False)
        disputil.DrawText(self.screen, settings.options_button, self.presskey_fontObj, settings.button_text_color,
                          blit=True, x=self.xmax / 2 - tx / 2, y=rect[1])
        button = pygame.Rect(rect)

        while not done:

            for i in range(0, len(value)):
                if changed[i]:
                    iy = init_iy + (ty + self.ygap) * i
                    if type(value[i]) is int or type(value[i]) is str:
                        rect = (ix, iy, int(self.xmax * 300 / 1280), int(self.ymax * 50 / 800))
                        if first_run:
                            disputil.DrawText(self.screen, str(value[i]), self.presskey_fontObj, settings.options_color,
                                              blit=True, x=ix, y=iy)
                            box[i] = pygame.Rect(rect)
                        else:
                            value[i], event_box, input_box = disputil.get_input_box_value(self.screen, rect, font=settings.fonts_folder+settings.presskey_font, font_size=settings.presskey_font_size, text=str(value[i]))
                            pygame.draw.rect(self.screen, settings.cBkg_highlighted, rect)
                            disputil.DrawText(self.screen, str(value[i]), self.presskey_fontObj, settings.options_color,
                                              blit=True, x=ix, y=iy)

                    elif type(value[i]) is bool:
                        pygame.draw.rect(self.screen, settings.cBkg_highlighted, (ix-5, iy-5, 32+10, 32+10))
                        self.screen.blit(frame_icon, (ix, iy))
                        if first_run:
                            box[i] = pygame.Rect(ix, iy, 32, 32)
                        else:
                            box[i] = pygame.Rect(ix, iy, 32, 32)
                            if value[i]:
                                value[i] = False
                            else:
                                value[i] = True
                        if value[i]:
                            self.screen.blit(check_icon, (ix + 5, iy - 5))
                        rect = (ix, iy, 32, 32)
                    update_disp = True
                    changed[i] = False

            if first_run or update_disp:
                if not first_run and rect is not None:
                    pygame.display.update(rect)
                else:
                    pygame.display.update()
                first_run = False
                update_disp = False

            if event_box is not None and event_box.get("Type") == pygame.MOUSEBUTTONDOWN:
                event = event_box
                event_box = None
            else:
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

            time.sleep(0.01)

        return value

    ####################################################################
    def create_terrain(self):

        if self.food_activated:
            self.terrain_type = [["organic" for y in range(self.ymax)] for x in range(self.xmax)]
            self.terrain_age = [[0 for y in range(self.ymax)] for x in range(self.xmax)]

        return

    ####################################################################
    def grow_terrain(self):

        if self.food_activated:
            self.screen.fill(settings.cTerrain)

            for i in range(self.xmin, self.xmax):
                for j in range(self.ymin, self.ymax):
                    if self.terrain_type[i][j] == "ground":
                        if self.terrain_age[i][j] > self.food_growth_gap:
                            self.terrain_type[i][j] = "organic"
                        else:
                            self.terrain_age[i][j] += 1
                    if self.food_activated and self.show_terrain and \
                            self.terrain_type[i][j] != "ground":
                        self.screen.set_at((i, j), settings.cBkg)

            # pygame.display.update()

        return

    ####################################################################
    def create(self):

        colony = []
        for i in range(0, len(self.chosen_fauna)):
            for j in range(0, int(self.init_bacteria_number / len(self.chosen_fauna))):
                colony.append(myColony.birth(self.fauna[self.chosen_fauna[i]], i))
            self.icon.append(disputil.loadIcon(self.fauna[self.chosen_fauna[i]]["Icon File"], settings.icons_folder))

        print()
        print("COLONY CREATED with %s specimen" % self.init_bacteria_number)
        print("Food mode:", self.food_activated)
        print("Food Growth:", self.food_growth_gap)
        for i in range(0, len(self.chosen_fauna)):
            ratio = int((self.init_bacteria_number / len(self.chosen_fauna)) / self.init_bacteria_number * 100)
            print(self.fauna[self.chosen_fauna[i]]["Name"], ratio, "%", "| Category:", self.fauna[self.chosen_fauna[i]]["Category"], "| Reproduction:", self.fauna[self.chosen_fauna[i]]["Reproduction"], "| Starvation Limit:", self.fauna[self.chosen_fauna[i]]["Starvation Limit"], "| Gestation Gap:",self.fauna[self.chosen_fauna[i]]["Gestation Gap"])
        print()

        random.shuffle(colony)

        return colony

    ####################################################################
    def birth(self, bacteria_settings, icon):

        bacteria = dict(bacteria_settings)
        bacteria["Status"] = "alive"
        if bacteria["Reproduction"] == "sex":
            bacteria["Gender"] = random.choice(settings.genders)
        else:
            bacteria["Gender"] = "both"
        bacteria["Position"] = random.randint(self.xmin, self.xmax), random.randint(self.ymin, self.ymax)
        bacteria["Size"] = bacteria_settings["Birth Size"]
        bacteria["Speed"] = min(10, bacteria_settings["Speed"])
        bacteria["Last Move"] = 0
        bacteria["Next Run"] = random.randint(0, bacteria["Max Run"])
        bacteria["Last Direction"] = random.choice(settings.directions)
        bacteria["Maturity Init Point"] = int(bacteria["Longevity"] * 0.2)
        bacteria["Maturity End Point"] = int(bacteria["Longevity"] * 0.8)
        bacteria["Age"] = random.randint(0, int(bacteria_settings["Maturity Init Point"]/4))
        if bacteria["Growth Gap"] is None:
            bacteria["Growth Gap"] = int((bacteria["Maturity Init Point"] - bacteria["Age"]) / bacteria["Maturity Size"])
        if bacteria["Category"] == "prey":
            bacteria["Starvation Limit"] = min(bacteria["Starvation Limit"], self.food_growth_gap - 1)
        bacteria["Last Dinner"] = 0
        bacteria["Last Gestation"] = bacteria["Gestation Gap"]
        bacteria["Icon Index"] = icon

        return bacteria

    ####################################################################
    def evolve(self, colony):

        end_colony = []

        for i in range(0, len(colony)):
            son = None
            eaten = False

            self.draw(colony[i], i, len(colony))

            colony[i] = self.check_age(colony[i])

            if colony[i]["Status"] == "alive":

                colony[i] = self.move(colony[i])

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
    def draw(self, bacteria, i, colony_size):

        if i == 0 and (not self.food_activated or not self.show_terrain):
            self.screen.fill(settings.cBkg)

        if bacteria["Status"] == "alive":
            if not self.show_icons or bacteria["Icon Index"] is None:
                pygame.draw.circle(self.screen, bacteria["Color"], bacteria["Position"], int(bacteria["Size"]), 0)
            else:
                icon = self.icon[bacteria["Icon Index"]]
                ix, iy = icon.get_size()
                if int(bacteria["Size"] * 2) != ix or int(bacteria["Size"] * 2) != iy:
                    icon = pygame.transform.smoothscale(icon, (int(bacteria["Size"] * 2), int(bacteria["Size"] * 2)))
                if bacteria["Rotate"]:
                    icon = pygame.transform.rotate(icon, random.choice([0, 30, 60, 90, 120, 150, 180, 210, 240, 270]))
                self.screen.blit(icon, (bacteria["Position"][0] - bacteria["Size"], bacteria["Position"][1] - bacteria["Size"]))
            if self.show_values:
                if self.show_icons:
                    x = bacteria["Position"][0] - bacteria["Size"]
                    y = bacteria["Position"][1] - bacteria["Size"] - settings.values_font_size
                else:
                    x = bacteria["Position"][0] - bacteria["Size"]*2
                    y = bacteria["Position"][1] - settings.values_font_size / 2
                disputil.DrawText(self.screen, str(bacteria["Size"])+", "+str(bacteria["Age"]),
                                  self.fontObj, pygame.Color("white"), blit=True, x=x, y=y)

        if i == (colony_size - 1):
            pygame.display.update()

        return

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
    def move(self, bacteria):

        if bacteria["Next Run"] <= 0:
            direction = random.choice(settings.directions)
            bacteria["Last Direction"] = direction
            bacteria["Next Run"] = random.randint(1, bacteria["Max Run"])
        else:
            direction = bacteria["Last Direction"]
            bacteria["Next Run"] -= 1

        x = int((bacteria["Position"][0] + direction[0] * bacteria["Size"] * (bacteria["Speed"] / 10))) % \
            settings.display_size[0]
        y = int((bacteria["Position"][1] + direction[1] * bacteria["Size"] * (bacteria["Speed"] / 10))) % \
            settings.display_size[1]
        bacteria["Position"] = (x, y)

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
                    if bacteria1["Overgrowth"]:
                        bacteria1["Size"] = min(bacteria1["Size"] + bacteria2["Size"],
                                                max(bacteria1["Max Size"], bacteria1["Maturity Size"]))
                    else:
                        bacteria1["Size"] = min(bacteria1["Size"] + bacteria2["Size"], bacteria1["Maturity Size"])
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
                icon = disputil.loadIcon("Lightning", settings.icons_folder)
                icon = pygame.transform.smoothscale(icon, (settings.cataclism_icon_scale, settings.cataclism_icon_scale))
                x = random.randint(50, self.xmax - 50)
                y = random.randint(50, self.ymax - 50)
                self.screen.blit(icon, (x,y))
                pygame.display.update((x, y, settings.cataclism_icon_scale, settings.cataclism_icon_scale))
                casualties = 0
                for i in range(0, len(colony)):
                    if x <= colony[i]["Position"][0] <= (x + settings.cataclism_icon_scale*0.8) and \
                            y <= colony[i]["Position"][1] <= (y + settings.cataclism_icon_scale*0.8):
                        colony[i]["Status"] = "dead"
                        casualties += 1
                time.sleep(1)
                print("FATAL CATACLISM!!!! caused %s casualties. To be or not to be..." % casualties)

            if event["Key"] == pygame.K_r:
                importlib.reload(settings)
                pygame.display.quit()
                self.__init__()
                self.create()

        return colony


####################################################################
myColony = Colony()

if settings.show_intro: myColony.intro()
myColony.create_terrain()
colony = myColony.create()

while True:

    myColony.grow_terrain()
    colony = myColony.evolve(colony)

    if not colony: break
    colony = myColony.catch_action(disputil.event_loop(), colony)
    time.sleep(0.2)
