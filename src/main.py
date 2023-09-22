import os
import sys
import pygame as pg
import pymunk as pm
from pymunk.pygame_util import DrawOptions
from character import Character
from push_obstacle import Obstacle
from wall import Wall
from settings import *

L1 = pg.image.load('../data/tiled/level1.png').convert_alpha()
L1 = pg.transform.scale(L1, SCREEN_SIZE)

BACKGROUNDS = [
    pg.image.load('../data/raw/Jungle Asset Pack/Jungle Asset Pack/parallax background/' + filename).convert()
    for filename in os.listdir('../data/raw/Jungle Asset Pack/Jungle Asset Pack/parallax background/') if 'png' in filename
]
BACKGROUNDS = [pg.transform.scale(image, SCREEN_SIZE) for image in BACKGROUNDS[0:2]]
BACKGROUND = pg.Surface(SCREEN_SIZE)
for image in BACKGROUNDS:
    BACKGROUND.blit(image, (0, 0), image.get_rect())


one_pix = SCREEN_SIZE[0] / 15


class App:
    def __init__(self, screen, space):
        self.screen = screen
        self.space = space
        self.curr_fps = FRAMERATE
        self.space.gravity = 0, 1800
        self.game_clock = pg.time.Clock()
        self.running = True
        self.player = Character(self.space, self.screen)

        screen_dim = (150, 85)
        self.game_tick = 0

        self.walls = Level0
        self.push_objects = Level0_Dynamic
        self.spikes = Level0_Spikes

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
            if DEBUG:
                self.space.debug_draw(options)  # Print the state of the simulation
            self.player.draw(self.game_tick)
            for object in self.push_objects:
                object.draw()
            self.player_collide_wall()
            self.player_collide_push_object()
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
        self.screen.blit(L1, (0, 0), L1.get_rect())

    def player_collide_wall(self) -> None:
        collisions = []
        for wall in self.walls:
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


if __name__ == '__main__':
    app = App(SCREEN, SPACE)
    app.run()
