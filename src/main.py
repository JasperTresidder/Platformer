import os
import sys
import pygame as pg
import pymunk as pm
from pymunk.pygame_util import DrawOptions
from character import Character
from settings import *
from wall import Wall
from push_obstacle import Obstacle
from spike import Spike
from flag import Flag
from item import Item

BACKGROUNDS = [
    pg.image.load('../data/raw/Jungle Asset Pack/Jungle Asset Pack/parallax background/' + filename).convert()
    for filename in os.listdir('../data/raw/Jungle Asset Pack/Jungle Asset Pack/parallax background/') if
    'png' in filename
]
BACKGROUNDS = [pg.transform.scale(image, SCREEN_SIZE) for image in BACKGROUNDS[0:1]]
BACKGROUND = pg.Surface(SCREEN_SIZE)
for image in BACKGROUNDS:
    BACKGROUND.blit(image, (0, 0), image.get_rect())

one_pix = SCREEN_SIZE[0] / 15


def load_level(level_number: int):

    filename1, filename2 = '../data/tiled/level' + str(level_number) + '_Tile Layer 1.csv', '../data/tiled/level' + str(level_number) + '_Tile Layer 2.csv'
    level = []
    level_box = []
    item = None
    level_spikes = []
    level_flag = None
    level.append(Wall(SPACE, (2000, 100), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (SCREEN_SIZE[0], -100), True))
    level.append(Wall(SPACE, (2000, 100), (-100, SCREEN_SIZE[1]), True))
    data = open(filename1)
    array = np.loadtxt(data, delimiter=",")
    data = open(filename2)
    array2 = np.loadtxt(data, delimiter=",")
    LEVEL_IMAGE = pg.image.load('../data/tiled/level' + str(level_number) + '.png').convert_alpha()
    LEVEL_IMAGE = pg.transform.scale(LEVEL_IMAGE, SCREEN_SIZE)
    for j, row in enumerate(array):
        for i, point in enumerate(row):
            if point not in [-1, 0]:
                level.append(Wall(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / screen_tiles[1]),
                                  (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                   j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if array2[j][i] == 215:
                level_box.append(Obstacle(SCREEN, SPACE, (17*SCREEN_SIZE[0] / (10*screen_tiles[0]) - 0.01, 17*SCREEN_SIZE[1] / (10*screen_tiles[1]) - 0.1), (
                i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06, (j-1) * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if array2[j][i] == 210:
                FLAG_LOCATION_1 = (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                   j * SCREEN_SIZE[1] / screen_tiles[1] - 1.2 * SCREEN_SIZE[1] / screen_tiles[1])
                level_flag = Flag(SCREEN, SPACE, (75, 140), (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                                             j * SCREEN_SIZE[1] / screen_tiles[1] - 1.2 * SCREEN_SIZE[
                                                                 1] / screen_tiles[1]))
            if array2[j][i] == 122:
                FLAG_LOCATION_2 = (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                   j * SCREEN_SIZE[1] / screen_tiles[1] - 1.2 * SCREEN_SIZE[1] / screen_tiles[1])
            if array2[j][i] == 105:
                item = Item(SCREEN, SPACE, (SCREEN_SIZE[0] / (2*screen_tiles[0]), SCREEN_SIZE[1] / (2*screen_tiles[1])), (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                   j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06))
            if point == 0:
                level_spikes.append(
                    Spike(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / (3 * screen_tiles[1])),
                         (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06, (j * SCREEN_SIZE[1] / screen_tiles[1]) + (
                                     2 * SCREEN_SIZE[1] / (3 * screen_tiles[1])) + 0.06)))
    return level, level_box, level_spikes, level_flag, FLAG_LOCATION_1, FLAG_LOCATION_2, item, LEVEL_IMAGE





class App:
    def __init__(self, screen: pg.Surface, space: pm.Space):
        self.screen = screen
        self.space = space
        self.curr_fps = FRAMERATE
        self.space.gravity = 0, 1800*SCREEN_SIZE[1]/1080
        self.game_clock = pg.time.Clock()
        self.running = True
        self.player = Character(self.space, self.screen, WALL_JUMP)
        self.level = 1

        screen_dim = (150, 85)
        self.game_tick = 0
        self.time_hit_flag = 0
        self.walls, self.push_objects, self.spikes, self.flag, self.flag_location_1, self.flag_location_2, self.item, self.level_image = load_level(LEVEL)
        if self.item is not None:
            self.item.add_to_space()
        self.flag.add_to_space()

        for wall in self.walls:
            wall.add_to_space()
        for object in self.push_objects:
            object.add_to_space()
        for object in self.spikes:
            object.add_to_space()

    def run(self) -> None:
        """
        Main game loop
        :return: None
        """
        print_options = pm.SpaceDebugDrawOptions()  # For easy printing
        options = DrawOptions(self.screen)

        while self.running:
            self.handle_game_events()
            self.draw_background()
             # Print the state of the simulation
            self.player.draw(self.game_tick)
            for object in self.push_objects:
                object.draw()
            if self.item is not None:
                if not self.item.got:
                    self.item.draw(self.game_tick)
                    self.player_collide_item()
            self.flag.draw(self.game_tick)
            if DEBUG:
                self.space.debug_draw(options)
            self.player_collide_wall()
            self.player_collide_push_object()
            self.player_collide_flag()
            self.player_collide_spike()
            self.update()
            self.space.step(0.02 * 60 / FRAMERATE)  # Step the simulation one step forward

    def handle_game_events(self) -> None:
        """
        Handle events such as inputs and exit screen
        :return:
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(1)
            if event.type == pg.KEYDOWN:
                self.player.handle_keydown(event)
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(1)
            if event.type == pg.KEYUP:
                self.player.handle_keyup(event)

    def update(self) -> None:
        """
        Flip the screen and tick the clock
        :return:
        """
        self.player.update()
        self.game_clock.tick(FRAMERATE)
        self.game_tick += 1
        self.curr_fps = self.game_clock.get_fps()
        pg.display.set_caption(str(self.curr_fps))
        pg.display.flip()

    def draw_background(self) -> None:
        self.screen.blit(BACKGROUND, (0, 0), BACKGROUND.get_rect())
        self.screen.blit(self.level_image, (0, 0), self.level_image.get_rect())

    def player_collide_wall(self) -> None:
        collisions = []
        for wall in self.walls:
            if not wall.is_boundary:
                normal = self.player.poly.shapes_collide(wall.poly).normal
                collisions.append((round(normal.x), round(normal.y)))

        self.player.update_animation_wall(collisions)

    def player_collide_push_object(self) -> None:
        collisions = []
        collisions_wall = []
        for object in self.push_objects:
            normal = self.player.poly.shapes_collide(object.poly).normal
            collisions.append((round(normal.x), round(normal.y)))
        for wall in self.walls:
            normal = self.push_objects[0].poly.shapes_collide(wall.poly).normal
            collisions_wall.append((round(normal.x), round(normal.y)))

        self.player.update_animation_push_object(collisions, collisions_wall, self.push_objects)

    def player_collide_flag(self) -> None:
        if self.player.poly.shapes_collide(self.flag.poly).points:
            if not self.flag.got and self.game_tick - self.time_hit_flag > 30:
                self.flag.body.position = (
                self.flag_location_2[0] + self.flag.flag_size[0] / 2, self.flag_location_2[1] + self.flag.flag_size[1] / 2)
                self.flag.got = True
                self.time_hit_flag = self.game_tick
            elif self.game_tick - self.time_hit_flag > 30:
                try:
                    self.next_level()
                except:
                    self.level = 0
                    self.next_level()
                # self.flag.body.position = (
                #     self.flag_location_1[0] + self.flag.flag_size[0] / 2, self.flag_location_1[1] + self.flag.flag_size[1] / 2)
                # self.flag.got = False
                # self.time_hit_flag = self.game_tick

    def player_collide_item(self) -> None:
        if self.player.poly.shapes_collide(self.item.poly).points:
            self.item.body.position = (SCREEN_SIZE[0] + 200, 0)
            self.item.got = True
            self.player.wall_jump = True

    def player_collide_spike(self) -> None:
        for spike in self.spikes:
            if self.player.poly.shapes_collide(spike.poly).points:
                self.player.body.position = SCREEN_SIZE[0] / 50, 4*SCREEN_SIZE[1]/10
                for object in self.push_objects:
                    object.body.position = object.initial_position
                if self.flag.got:
                    self.flag.body.position = (
                    self.flag_location_1[0] + self.flag.flag_size[0] / 2, self.flag_location_1[1] + self.flag.flag_size[1] / 2)
                    self.flag.got = False
                if LEVEL == 2:
                    if self.item.got:
                        self.item.body.position = self.item.initial_position
                        self.item.got = False
                        self.player.wall_jump = False

    def next_level(self):
        if self.level == MAX_LEVEL:
            self.level = 0
        for object in self.walls:
            self.space.remove(object.body, object.poly)
        for object in self.push_objects:
            self.space.remove(object.body, object.poly)
        for object in self.spikes:
            self.space.remove(object.body, object.poly)
        self.space.remove(self.flag.body, self.flag.poly)
        self.space.remove(self.player.body, self.player.poly)
        if self.item is not None:
            self.space.remove(self.item.body, self.item.poly)

        self.level += 1
        self.walls, self.push_objects, self.spikes, self.flag, self.flag_location_1, self.flag_location_2, self.item, self.level_image = load_level(
            self.level)
        self.player = Character(self.space, self.screen, self.player.wall_jump)
        if self.item is not None:
            self.item.add_to_space()
        self.flag.add_to_space()

        for wall in self.walls:
            wall.add_to_space()
        for object in self.push_objects:
            object.add_to_space()
        for object in self.spikes:
            object.add_to_space()



if __name__ == '__main__':
    app = App(SCREEN, SPACE)
    app.run()
