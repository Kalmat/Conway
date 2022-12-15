#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os
import random
import sys
import threading
import time

import pygame
import pywinctl
from PyQt5 import QtWidgets, QtGui
from kalmatools import utils
from conway_ui import Ui_Form

# Initial settings
cellSize = 4            # Size of each "cell". It drastically affects performance and consumption
bgcolor = "gray12"       # https://www.pygame.org/docs/ref/color_list.html
fgcolor = "darkorange3"  # https://www.pygame.org/docs/ref/color_list.html
demo = False             # Random board or demo preset
targetTicks = 5          # Target FPS (steps per second). It also affects performance and consumption
fullScreen = False       # Fullscreen or windowed
windowSize = (1000, 1000)  # Ignored if Fulscreen or Wallpaper mode. It has to be fine-tuned together with cellSize and Ticks
asWallpaper = False       # At bottom, no focus, no input (will force Fullscreen even though set to False)
renovate = True          # Completely renew board or "Rain of God" (random drops of "life" or "death")
renovationLap = 10        # Time in minutes to renovate board
sphericBoard = False     # Board has borders (it physically ends) or not (like a sphere)


class ConwayGameOfLife:

    def __init__(self):

        pygame.display.init()
        pygame.display.set_caption("My Conway")
        img = pygame.image.load(utils.resource_path(__file__, "resources/icons") + "colony.ico")
        pygame.display.set_icon(img)

        self.fullscreen = fullScreen
        self.wallpaper = asWallpaper
        self.renovate = renovate
        self.spheric = sphericBoard

        x, y, w, h = pywinctl.getWorkArea()
        self.cellSize = cellSize
        self.addRows = 10
        self.addSize = self.addRows * self.cellSize
        self.screenSize = windowSize
        if self.fullscreen or self.wallpaper:
            if self.fullscreen:
                wx = 0
                wy = 0
                flags = pygame.FULLSCREEN
                self.screenSize = (0, 0)
            else:
                wx = int(x - self.addSize)
                wy = int(y - self.addSize)
                flags = pygame.NOFRAME
            self.screenSize = (w + self.addSize, h + self.addSize)
        else:
            wx = int((w - self.screenSize[0]) / 2)
            wy = int((h - self.screenSize[1]) / 2)
            flags = 0
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (wx, wy)
        self.screen = pygame.display.set_mode(size=self.screenSize, flags=flags)
        self.screenSize = self.screen.get_size()
        self.size = (int(self.screenSize[0] / self.cellSize + self.addRows*2), int(self.screenSize[1] / self.cellSize + self.addRows*2))

        if self.wallpaper:
            self.screenSize = (w + self.addSize, h + self.addSize)
            self.hWnd = pygame.display.get_wm_info()['window']
            self.window = pywinctl.Window(self.hWnd)
            self.window.resizeTo(w + self.addSize, h + self.addSize)
            self.window.sendBehind()

        # https://www.pygame.org/docs/ref/color_list.html
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor

        self.ticks = targetTicks
        targetTime = (1 - ((16 / self.cellSize) * 0.1)) / self.ticks  # 0.1 is the time evolve() takes in my system: res=5120x1440 / cell=16
        self.sleepLap = 0.01
        targetSleeps = targetTime / self.sleepLap
        self.sleepPeriod = int((self.size[0] * self.size[1]) / targetSleeps)
        self.cycles = 0
        self.targetCycles = renovationLap * 60

        self.board = [[] for x in range(self.size[0])]
        self.boardControl = [["" for y in range(self.size[1])] for x in range(self.size[0])]
        self.demo = demo
        if not self.demo:
            # Random initial seed:
            self.randomInitialBoard(True)
        else:
            # Simple initial seed for demo/testing purposes:
            self.demoInitialBoard(random.Random().randint(1, 2))

    def run(self, keep):

        # clock = pygame.time.Clock()

        while keep.is_set():
            pygame.event.pump()
            self.evolve()
            # clock.tick(self.ticks)

        pygame.display.quit()
        pygame.quit()

    def evolve(self):

        self.screen.fill(self.bgcolor)
        count = 0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.spheric:
                    cellsAround = self.cellsAroundSpheric(x, y)
                else:
                    cellsAround = self.cellsAround(x, y)
                color = self.board[x][y]
                if color == self.bgcolor:
                    if cellsAround == 3:
                        color = self.fgcolor
                else:
                    if cellsAround not in (2, 3):
                        color = self.bgcolor
                if color == self.fgcolor:
                    self.screen.fill(self.fgcolor, rect=(x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                self.boardControl[x][y] = color
                count += 1
                # Free CPU to reduce consumption (target = 1 FPS, or as per targetTicks value)
                if count % self.sleepPeriod == 0:
                    time.sleep(self.sleepLap)
        pygame.display.flip()

        self.cycles += 1
        if self.cycles >= self.targetCycles:
            self.cycles = 0
            if self.renovate:
                if not self.demo:
                    self.randomInitialBoard()
                else:
                    self.demoInitialBoard(random.Random().randint(1, 2))
            else:
                self.rainOfGod()
        else:
            self.board = copy.deepcopy(self.boardControl)

    def randomInitialBoard(self, firstRun=False):

        self.screen.fill(self.bgcolor)
        count = 0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                color = random.Random().choice([self.fgcolor, self.bgcolor])
                if firstRun:
                    self.board[x].append(color)
                else:
                    self.board[x][y] = color
                if color == self.fgcolor:
                    self.screen.fill(self.fgcolor, rect=(x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                count += 1
                if count % self.sleepPeriod == 0:
                    time.sleep(self.sleepLap)
        pygame.display.flip()
        time.sleep(1 / self.ticks)

    def demoInitialBoard(self, demo):

        self.screen.fill(self.bgcolor)
        demos = {"demo1":
                     {"set": (int(self.size[0] / 2), int(self.size[1] / 2) - 4),
                      "points": [
                          (-7, -1), (-8, -1), (-9, -1), (-10, 0), (-7, +1), (-8, 1), (-9, +1),
                          (+7, -1), (+8, -1), (+9, -1), (+10, 0), (+7, +1), (+8, 1), (+9, +1),
                          (-1, -15), (-1, -16), (-1, -17), (0, -18), (+1, -15), (+1, -16), (+1, -17),
                          (-1, +15), (-1, +16), (-1, +17), (0, +18), (+1, +15), (+1, +16), (+1, +17)]
                      },
                 "demo2":
                     {"set": (int(self.size[0] / 2), int(self.size[1] / 2) - 4),
                      "points": [
                          (0, 0), (-1, +1), (-1, +2), (0, + 2), (+1, + 2),
                          (-9, +4), (-8, +4), (-10, +5), (-7, +5), (-10, +6), (-7, +6), (-9, +7), (-8, +7)]
                      }
                 }

        initx, inity = demos["demo"+str(demo)]["set"]
        points = demos["demo"+str(demo)]["points"]
        self.board = [[self.bgcolor for y in range(self.size[1])] for x in range(self.size[0])]
        for pos in points:
            x = pos[0] + initx
            y = pos[1] + inity
            self.board[x][y] = self.fgcolor
            self.screen.fill(self.fgcolor, rect=(x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        pygame.display.flip()
        time.sleep(1 / self.ticks)

    def rainOfGod(self):

        self.board = copy.deepcopy(self.boardControl)
        drops = random.Random().randint(0, int(self.size[0] * self.size[1] / 2))
        for i in range(drops):
            x = random.Random().randint(0, self.size[0] - 1)
            y = random.Random().randint(0, self.size[1] - 1)
            deathDrop = random.Random().randint(0, 1) == 0
            color = self.bgcolor if deathDrop else self.fgcolor
            self.board[x][y] = color
            if not deathDrop:
                self.screen.fill(color, rect=(x, y, self.cellSize, self.cellSize))
            time.sleep(max(0.001, self.ticks / drops))

    def cellsAround(self, x, y):

        cells = 0
        for xx in range(max(0, x-1), min(self.size[0], x+2)):
            for yy in range(max(0, y-1), min(self.size[1], y+2)):
                if self.board[xx][yy] == self.fgcolor and (xx, yy) != (x, y):
                    cells += 1
        return cells

    def cellsAroundSpheric(self, x, y):

        cells = 0
        for xx in range(x-1, x+2):
            dx = xx
            if xx < 0:
                dx = self.size[0] - 1
            elif xx >= self.size[0]:
                dx = 0
            for yy in range(max(0, y-1), min(self.size[1], y+2)):
                dy = yy
                if yy < 0:
                    dy = self.size[1] - 1
                elif yy >= self.size[0]:
                    dy = 0
                if self.board[dx][dy] == self.fgcolor and (dx, dy) != (x, y):
                    cells += 1
        return cells


class SettingsWindow(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super(SettingsWindow, self).__init__()

        self.setWindowTitle("Conway's Game of Life")
        self.setWindowIcon(QtGui.QIcon(utils.resource_path(__file__, "resources/icons/colony.ico")))

        self.setupUI()

    def setupUI(self):

        self.setupUi(self)
        self.setLayout(self.gridLayout)

        self.fullscreen_button.clicked.connect(lambda: self.getSettings("fullscreen"))
        self.fullscreen_button.setChecked(fullScreen)
        self.fullscreen_button.setText("ON" if fullScreen else "OFF")

        self.wallpaper_button.clicked.connect(lambda: self.getSettings("wallpaper"))
        self.wallpaper_button.setChecked(asWallpaper)
        self.wallpaper_button.setText("ON" if asWallpaper else "OFF")

        self.spheric_button.clicked.connect(lambda: self.getSettings("spheric"))
        self.spheric_button.setChecked(sphericBoard)
        self.spheric_button.setText("ON" if sphericBoard else "OFF")

        self.cycle_button.clicked.connect(lambda: self.getSettings("cycle"))
        self.cycle_button.setChecked(renovate)
        self.cycle_button.setText("ON" if renovate else "OFF")

        self.go_button.clicked.connect(lambda: self.getSettings("ALL"))
        self.demo_button.clicked.connect(lambda: self.getSettings("ALLDEMO"))

        self.cellsize_edit.setText(str(cellSize))
        self.bgcolor_edit.setText(str(bgcolor))
        self.fgcolor_edit.setText(str(fgcolor))
        self.winsize_w_edit.setText(str(windowSize[0]))
        self.winsize_h_edit.setText(str(windowSize[1]))
        self.steps_edit.setText(str(targetTicks))
        self.cycletime_edit.setText(str(renovationLap))

        self.contextMenu = QtWidgets.QMenu(self)
        self.contextMenu.setStyleSheet("""
            QMenu {border: 1px inset #666; font-size: 18px; background-color: #333; color: #fff; padding: 5; padding-left: 20}
            QMenu:selected {background-color: #666; color: #fff;}""")

        self.contextMenu.addSeparator()
        self.contextMenu.addAction("Quit", lambda: self.execAction("Q"))

        self.trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(utils.resource_path(__file__, "resources/icons/colony.ico")), self)
        self.trayIcon.setContextMenu(self.contextMenu)
        self.trayIcon.setToolTip("Conway's Game of Life")
        self.trayIcon.show()

    def getSettings(self, setting):

        global cellSize
        global windowSize
        global bgcolor
        global fgcolor
        global fullScreen
        global windowSize
        global asWallpaper
        global renovate
        global renovationLap
        global sphericBoard
        global demo
        global targetTicks

        if setting == "fullscreen":
            fullScreen = not fullScreen
            self.fullscreen_button.setChecked(fullScreen)
            self.fullscreen_button.setText("ON" if fullScreen else "OFF")

        elif setting == "wallpaper":
            asWallpaper = not asWallpaper
            self.wallpaper_button.setChecked(asWallpaper)
            self.wallpaper_button.setText("ON" if asWallpaper else "OFF")

        elif setting == "spheric":
            sphericBoard = not sphericBoard
            self.spheric_button.setChecked(sphericBoard)
            self.spheric_button.setText("ON" if sphericBoard else "OFF")

        elif setting == "cycle":
            renovate = not renovate
            self.cycle_button.setChecked(renovate)
            self.cycle_button.setText("ON" if renovate else "OFF")

        elif setting in ("ALL", "ALLDEMO"):

            cellSize = int(self.cellsize_edit.text())
            bgcolor = self.bgcolor_edit.text()
            fgcolor = self.fgcolor_edit.text()
            windowSize = (int(self.winsize_w_edit.text()), int(self.winsize_h_edit.text()))
            targetTicks = int(self.steps_edit.text())
            renovationLap = int(self.cycletime_edit.text())
            demo = setting == "ALLDEMO"
            targetTicks = 5 if demo else targetTicks

            self.hide()
            self.runConway()

    def runConway(self):

        self.keep = threading.Event()
        self.keep.set()
        self.MyBoard = ConwayGameOfLife()
        self.board = threading.Thread(target=self.MyBoard.run, args=(self.keep, ))
        self.board.daemon = True
        self.board.start()

    def execAction(self, option):

        if option == "Q":
            self.keep.clear()
            self.destroy()
            QtWidgets.QApplication.quit()


if __name__ == "__main__":
    # Test initial states here:
    # https://playgameoflife.com/lexicon
    # https://copy.sh/life/

    app = QtWidgets.QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    app.exec_()
