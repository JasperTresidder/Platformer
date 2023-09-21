import sys
import pygame as pg
import pymunk as pm
from pymunk.pygame_util import DrawOptions
from character import Character
from wall import Wall
from settings import *

L1 = pg.image.load('../data/map/1/level.PNG').convert_alpha()
L1 = pg.transform.scale(L1, SCREEN_SIZE)

one_pix = SCREEN_SIZE[0]/15



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

        for wall in self.walls:
            wall.add_to_space()

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
            # self.space.debug_draw(options)  # Print the state of the simulation
            self.player.draw(self.game_tick)
            self.player_collide_wall()
            self.update()
            self.space.step(0.02 * 60/FRAMERATE)  # Step the simulation one step forward


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

    def update(self):
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

    def draw_background(self):
        self.screen.blit(L1, (0, 0), L1.get_rect())


    def player_collide_wall(self):
        collisions = []
        velocity_x = self.player.body.velocity.x
        velocity_y = self.player.body.velocity.y
        for wall in self.walls:
            normal = self.player.poly.shapes_collide(wall.poly).normal
            collisions.append((round(normal.x), round(normal.y)))

        if (0, 1) in collisions:  # Touching ground
            self.player.can_jump = True
            self.space.gravity = 0, 0
            if not pg.key.get_pressed()[pg.K_d] and not pg.key.get_pressed()[pg.K_a]:
                self.player.previous_animation = self.player.current_animation
                if 'left' in self.player.previous_animation:
                    self.player.current_animation = 'idle_left'
                else:
                    self.player.current_animation = 'idle'
        else:
            self.space.gravity = 0, 1800
        if (-1, 0) in collisions:  # Touching left wall
            self.player.left = False
            if (0, 1) not in collisions and velocity_y > 0:
                self.player.previous_animation = self.player.current_animation
                self.player.current_animation = 'wall_jump_left'
            if velocity_y > 80:
                self.player.body.velocity = (velocity_x, 80)
        elif pg.key.get_pressed()[pg.K_a]:
            self.player.left = True
            if (0, 1) not in collisions:
                self.player.previous_animation = self.player.current_animation
                if velocity_y > 40:
                    self.player.current_animation = 'fall_left'
                else:
                    self.player.current_animation = 'jump_left'
            else:
                self.player.previous_animation = self.player.current_animation
                self.player.current_animation = 'run_left'

        if (1, 0) in collisions:  # Touching right wall
            self.player.right = False
            if (0, 1) not in collisions and velocity_y > 0:
                self.player.previous_animation = self.player.current_animation
                self.player.current_animation = 'wall_jump'
            if velocity_y > 80:
                self.player.body.velocity = (velocity_x, 80)
        elif pg.key.get_pressed()[pg.K_d]:
            self.player.right = True
            if (0, 1) not in collisions:
                self.player.previous_animation = self.player.current_animation
                if velocity_y > 40:
                    self.player.current_animation = 'fall'
                else:
                    self.player.current_animation = 'jump'
            else:
                self.player.previous_animation = self.player.current_animation
                self.player.current_animation = 'run'

        if (1, 0) not in collisions and (-1, 0) not in collisions and (0, 1) not in collisions and -velocity_y > 1:
            self.player.previous_animation = self.player.current_animation
            if 'left' in self.player.previous_animation:
                if velocity_y > 40:
                    self.player.current_animation = 'fall_left'
                else:
                    self.player.current_animation = 'jump_left'
            else:
                if velocity_y > 40:
                    self.player.current_animation = 'fall'
                else:
                    self.player.current_animation = 'jump'



if __name__ == '__main__':
    app = App(SCREEN, SPACE)
    app.run()
