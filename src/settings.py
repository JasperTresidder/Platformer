from wall import Wall
import pymunk as pm
import pygame as pg

pg.init()
pg.display.init()

screen_s = pg.display.get_desktop_sizes()[0]

SPACE = pm.Space()
SCREEN_SIZE = (screen_s[0], screen_s[1])
FRAMERATE = 300
SCREEN = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN, vsync=True)

Level0 = [Wall(SPACE, (29 / 150 * SCREEN_SIZE[0], 600), (0, 45 / 85 * SCREEN_SIZE[1])),
          Wall(SPACE, (2000, 900), (5 / 150 * SCREEN_SIZE[0], 69 * SCREEN_SIZE[1] / 85)),
          Wall(SPACE, (500, 600), (83 * SCREEN_SIZE[0] / 150, 60 * SCREEN_SIZE[1] / 85)),
          Wall(SPACE, (1000, 600), (103 * SCREEN_SIZE[0] / 150, 50 * SCREEN_SIZE[1] / 85)), ]

CHARACTERS = ['Ninja Frog', 'Mask Dude', 'Pink Man', 'Virtual Guy']
CHARACTER = CHARACTERS[0]

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
