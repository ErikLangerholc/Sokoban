import pygame as g
from pygame.locals import *
import sys, time, random, urllib.request


def translatelvl(line, levelnumber):
    r = ""
    line = line.translate("".maketrans("x# $@.!*", ".x.oSZ\nW"))
    l = len(line) - 1
    for i, c in enumerate(line):
        if c == "\n":
            r = r[:-1]
            if i != l: r += "\n"
        else:
            r += c + " "
    qwe = r.split("\n")
    r = str(int((len(qwe[0]) + 1) / 2)) + " " + str(len(qwe)) + "\n" + r
    f = open("levels\\" + str(levelnumber) + ".txt", "w")
    f.write(r)
    f.close()
    return r


def LoadLevel(levelnumber, Wallimg, Boximg, Playerimg, Zoneimg, bgnumber, WindowX, WindowY):
    # ko gremo pol cez level je prvi index za y: level[Y][X] = nas kvadratek ".xoSQZW"
    try:
        levelfile = open("levels\\" + str(levelnumber) + ".txt")
        level = levelfile.read().split("\n")
        levelfile.close()
    except:
        try:
            levelfile = urllib.request.urlopen("http://www.sokoban.info/?1_" + str(levelnumber))
            text = str(levelfile.read())
            levelfile.close()
            level = translatelvl(text.split("\\n")[64][23:-10], levelnumber).split("\n")
        except:
            print("No internet connection.")
            sys.exit()
    levx, levy, level = int(level[0].split()[0]), int(level[0].split()[1]), [x.split() for x in level[1:]]
    squaresize = int(min(WindowX / levx, WindowY / levy))
    s = (squaresize, squaresize)
    Wall = g.transform.scale(Wallimg, s)
    Box = g.transform.scale(Boximg, s)
    Player = g.transform.scale(Playerimg, s)
    Zone = g.transform.scale(Zoneimg, s)
    selected_bg = random.randint(1, bgnumber)
    try:
        BG = g.transform.scale(g.image.load("backgrounds\\bg" + str(selected_bg) + ".jpg"), (WindowX, WindowY))
    except:
        BG = g.transform.scale(g.image.load("backgrounds\\bg" + str(selected_bg) + ".png"), (WindowX, WindowY))

    return (level, levx, levy, squaresize, Wall, Box, Player, Zone, BG)


def GetPlayerXY(level):
    """vrne tuple (x, y, 'Q'/'S'), kjer Q pomeni da stoji na zonu"""
    for row, line in enumerate(level):
        for column, square in enumerate(line):
            if square in "SQ":
                return (column, row, square)


def DrawLevel(surface, Wall, Box, Player, Zone, squaresize, levx, levy, level, WindowX, WindowY):
    # offsets
    x, y = (WindowX - levx * squaresize) / 2, (WindowY - levy * squaresize) / 2
    for row, line in enumerate(level):
        for column, square in enumerate(line):
            if square == "x":
                surface.blit(Wall, (x + column * squaresize, y + row * squaresize))
            elif square == "o":
                surface.blit(Box, (x + column * squaresize, y + row * squaresize))
            elif square == "Z":
                surface.blit(Zone, (x + column * squaresize, y + row * squaresize))
            elif square == "S":
                surface.blit(Player, (x + column * squaresize, y + row * squaresize))
            elif square == "W":
                surface.blit(Zone, (x + column * squaresize, y + row * squaresize))
                surface.blit(Box, (x + column * squaresize, y + row * squaresize))
            elif square == "Q":
                surface.blit(Zone, (x + column * squaresize, y + row * squaresize))
                surface.blit(Player, (x + column * squaresize, y + row * squaresize))


def move(level, direction):
    """level more bit ograjen z zidom ce ne bo error"""
    levx, levy = len(level[0]), len(level)
    X, Y, state = GetPlayerXY(level)
    if direction == "up":
        if level[Y - 1][X] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y - 1][X] = {".": "S", "Z": "Q"}[level[Y - 1][X]]
        elif Y > 1 and level[Y - 1][X] in "oW" and level[Y - 2][X] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y - 1][X] = {"o": "S", "W": "Q"}[level[Y - 1][X]]
            level[Y - 2][X] = {".": "o", "Z": "W"}[level[Y - 2][X]]
    elif direction == "down":
        if level[Y + 1][X] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y + 1][X] = {".": "S", "Z": "Q"}[level[Y + 1][X]]
        elif Y < levy - 2 and level[Y + 1][X] in "oW" and level[Y + 2][X] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y + 1][X] = {"o": "S", "W": "Q"}[level[Y + 1][X]]
            level[Y + 2][X] = {".": "o", "Z": "W"}[level[Y + 2][X]]
    elif direction == "left":
        if level[Y][X - 1] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y][X - 1] = {".": "S", "Z": "Q"}[level[Y][X - 1]]
        elif X > 1 and level[Y][X - 1] in "oW" and level[Y][X - 2] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y][X - 1] = {"o": "S", "W": "Q"}[level[Y][X - 1]]
            level[Y][X - 2] = {".": "o", "Z": "W"}[level[Y][X - 2]]
    elif direction == "right":
        if level[Y][X + 1] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y][X + 1] = {".": "S", "Z": "Q"}[level[Y][X + 1]]
        elif X < levx - 2 and level[Y][X + 1] in "oW" and level[Y][X + 2] in ".Z":
            level[Y][X] = {"S": ".", "Q": "Z"}[state]
            level[Y][X + 1] = {"o": "S", "W": "Q"}[level[Y][X + 1]]
            level[Y][X + 2] = {".": "o", "Z": "W"}[level[Y][X + 2]]


def CheckVictory(level):
    for line in level:
        for square in line:
            if square in "ZQ":
                return False
    return True

def Run():
    g.init()
    FPS = 60
    fpsClock = g.time.Clock()
    fullscrn = False
    upkeytimer = 0
    downkeytimer = 0
    leftkeytimer = 0
    rightkeytimer = 0
    skip = 1
    levelnumber = 1
    bgnumber = 1

    try:
        settingsfile = open("settings.txt.")
        for setting, values in [(x[0], x[1:]) for x in [x.split() for x in settingsfile.read().split("\n")]]:
            try:
                if setting == "Resolution":
                    if values == ["full"]:
                        DisplayInfo = g.display.Info()
                        WindowX = DisplayInfo.current_w
                        WindowY = DisplayInfo.current_h
                        fullscrn = True
                    else:
                        WindowX, WindowY = int(values[0]), int(values[1])
                elif setting == "StartingLevel":
                    levelnumber = int(values[0])
                elif setting == "Backgrounds":
                    bgnumber = int(values[0])
            except:
                print("Invalid values in settings.txt. Using defaults")
                WindowX, WindowY = 1200, 800
        settingsfile.close()
    except:
        print("Error reading settings file")
        WindowX, WindowY  = 1200, 800

    Wallimg = g.image.load("wall.png")
    Boximg = g.image.load("box.png")
    Playerimg = g.image.load("player.png")
    Zoneimg = g.image.load("zone.png")
    Icon = g.image.load("icon.png")

    g.display.set_caption("Sokoban")
    g.display.set_icon(Icon)
    main = g.display.set_mode((WindowX, WindowY), {True: FULLSCREEN, False: 0}[fullscrn])

    #load level:
    level, levx, levy, squaresize, Wall, Box, Player, Zone, BG = LoadLevel(levelnumber, Wallimg, Boximg, Playerimg, Zoneimg,
                                                                           bgnumber, WindowX, WindowY)
    movecount = 0
    oldmovecount = -1

    while 1:
        X, Y, state = GetPlayerXY(level)
        for e in g.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                if movecount > 0:
                    level, levx, levy, squaresize, Wall, Box, Player, Zone, BG = LoadLevel(levelnumber, Wallimg, Boximg,
                                                                                           Playerimg, Zoneimg, bgnumber,
                                                                                           WindowX, WindowY)
                    movecount = 0
                else:
                    g.quit()
                    sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_UP and Y > 0:
                    upkeytimer = time.clock()
                    move(level, "up")
                    movecount += 1
                elif e.key == K_DOWN and Y < levy - 1:
                    downkeytimer = time.clock()
                    move(level, "down")
                    movecount += 1
                elif e.key == K_LEFT and X > 0:
                    leftkeytimer = time.clock()
                    move(level, "left")
                    movecount += 1
                elif e.key ==K_RIGHT and X < levx - 1:
                    rightkeytimer = time.clock()
                    move(level, "right")
                    movecount += 1
            elif e.type == KEYUP:
                if e.key == K_UP:
                    upkeytimer = 0
                elif e.key == K_DOWN:
                    downkeytimer = 0
                elif e.key == K_LEFT:
                    leftkeytimer = 0
                elif e.key == K_RIGHT:
                    rightkeytimer = 0
        t = time.clock()
        skip = (skip + 1) % 3
        for keyindex, keytimer in enumerate([upkeytimer, downkeytimer, leftkeytimer, rightkeytimer]):
            if keytimer != 0 and skip == 0 and t - keytimer > 0.25:
                move(level, {0: "up", 1: "down", 2: "left", 3: "right"}[keyindex])
                movecount += 1

        if oldmovecount != movecount:
            main.blit(BG, (0, 0))
            DrawLevel(main, Wall, Box, Player, Zone, squaresize, levx, levy, level, WindowX, WindowY)
            oldmovecount = movecount

        if CheckVictory(level):
            levelnumber += 1
            try:
                level, levx, levy, squaresize, Wall, Box, Player, Zone, BG = LoadLevel(levelnumber, Wallimg, Boximg,
                                                                                       Playerimg, Zoneimg, bgnumber,
                                                                                       WindowX, WindowY)
                movecount = 0
            except:
                g.quit()
                sys.exit()

        g.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    Run()