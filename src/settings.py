from typing import Tuple, List
import pymunk as pm
import pygame as pg
import numpy as np

#############
DEBUG = False
#############

WALL_JUMP = True
LEVEL = 3



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


# Level0 = [Wall(SPACE, (29 / 150 * SCREEN_SIZE[0], 600), (0, 45 / 85 * SCREEN_SIZE[1])),
#           Wall(SPACE, (2000, 900), (5 / 150 * SCREEN_SIZE[0], 69 * SCREEN_SIZE[1] / 85)),
#           Wall(SPACE, (500, 600), (83 * SCREEN_SIZE[0] / 150, 60 * SCREEN_SIZE[1] / 85)),
#           Wall(SPACE, (1000, 600), (103 * SCREEN_SIZE[0] / 150, 50 * SCREEN_SIZE[1] / 85))]

# Level0_Dynamic = [Obstacle(SCREEN, SPACE, (120, 120), (SCREEN_SIZE[0]/2 -30, SCREEN_SIZE[1] / 1.5))]

CHARACTERS = ['Ninja Frog', 'Mask Dude', 'Pink Man', 'Virtual Guy']
CHARACTER = CHARACTERS[3]

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

FLAG = pg.image.load(
            '../data/raw/Pixel Adventure 1/Free/Items/Checkpoints/Checkpoint/Checkpoint (Flag Idle)(64x64).png').convert_alpha()
Flag_Animation = []
for frame in range(int(FLAG.get_size()[0] / 64)):
    Flag_Animation.append(FLAG.subsurface((frame * 64, 0, 64, 64)))

ITEM = pg.image.load(
            '../data/raw/Pixel Adventure 1/Free/Items/Fruits/Cherries.png').convert_alpha()

Item_Animation = []
for frame in range(int(ITEM.get_size()[0] / 32)):
    Item_Animation.append(ITEM.subsurface((frame * 32, 0, 32, 32)))


