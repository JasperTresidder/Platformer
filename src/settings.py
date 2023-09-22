from wall import Wall
from push_obstacle import Obstacle
from spike import Spike
import pymunk as pm
import pygame as pg
import numpy as np

#############
DEBUG = False
#############

WALL_JUMP = False



pg.init()
pg.display.init()

screen_s = (1920, 1080)
screen_tiles = (30, 17)

SPACE = pm.Space()
SCREEN_SIZE = (screen_s[0], screen_s[1])
FRAMERATE = 165
PLAYER_SPEED = 6*60/FRAMERATE
SCREEN = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN, vsync=True)
pg.mouse.set_visible(False)

def load_level(filename: str, filename2: str) -> tuple[list[Wall], list[Obstacle], list[Spike]]:
    level = []
    level_box = []
    level_spikes = []
    level.append(Wall(SPACE, (2000, 100), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (SCREEN_SIZE[0], -100), True))
    level.append(Wall(SPACE, (2000, 100), (-100, SCREEN_SIZE[1]), True))
    data = open(filename)
    array = np.loadtxt(data, delimiter=",")
    data = open(filename2)
    array2 = np.loadtxt(data, delimiter=",")
    for j, row in enumerate(array):
        for i, point in enumerate(row):
            if point not in [-1, 0]:
                level.append(Wall(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / screen_tiles[1]),
                                  (i*SCREEN_SIZE[0] / screen_tiles[0] + 0.06, j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if array2[j][i] == 215:
                level_box.append(Obstacle(SCREEN, SPACE, (120, 120), (i*SCREEN_SIZE[0] / screen_tiles[0] + 0.06, j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if point == 0:
                level_spikes.append(Wall(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / (2*screen_tiles[1])),
                                  (i*SCREEN_SIZE[0] / screen_tiles[0] + 0.06, (j * SCREEN_SIZE[1] / screen_tiles[1]) + (SCREEN_SIZE[1] / (2 * screen_tiles[1])) + 0.06)))
    return level, level_box, level_spikes


Level0, Level0_Dynamic, Level0_Spikes = load_level('../data/tiled/level1_Tile Layer 1.csv', '../data/tiled/level1_Tile Layer 2.csv')

# Level0 = [Wall(SPACE, (29 / 150 * SCREEN_SIZE[0], 600), (0, 45 / 85 * SCREEN_SIZE[1])),
#           Wall(SPACE, (2000, 900), (5 / 150 * SCREEN_SIZE[0], 69 * SCREEN_SIZE[1] / 85)),
#           Wall(SPACE, (500, 600), (83 * SCREEN_SIZE[0] / 150, 60 * SCREEN_SIZE[1] / 85)),
#           Wall(SPACE, (1000, 600), (103 * SCREEN_SIZE[0] / 150, 50 * SCREEN_SIZE[1] / 85))]

# Level0_Dynamic = [Obstacle(SCREEN, SPACE, (120, 120), (SCREEN_SIZE[0]/2 -30, SCREEN_SIZE[1] / 1.5))]

CHARACTERS = ['Ninja Frog', 'Mask Dude', 'Pink Man', 'Virtual Guy']
CHARACTER = CHARACTERS[1]

Character_Spritesheets = {
    'idle': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Idle (32x32).png").convert_alpha(),
    'hit': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Hit (32x32).png").convert_alpha(),
    'fall': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Fall (32x32).png").convert_alpha(),
    'jump': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Jump (32x32).png").convert_alpha(),
    'run': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Run (32x32).png").convert_alpha(),
    'double_jump': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Double Jump (32x32).png").convert_alpha(),
    'wall_jump': pg.image.load("../data/assets/Main Characters/" + CHARACTER + "/Wall Jump (32x32).png").convert_alpha(),
}
Frog_Spritesheets2 = dict()
for key, value in Character_Spritesheets.items():
    Frog_Spritesheets2[key + '_left'] = pg.transform.flip(value, True, False)
for key, value in Frog_Spritesheets2.items():
    Character_Spritesheets[key] = value


Frog_Animations = dict()

for key, value in Character_Spritesheets.items():
    animation = []
    for frame in range(int(value.get_size()[0]/32)):
        animation.append(value.subsurface((frame*32, 0, 32, 32)))
    Frog_Animations[key] = animation
