import pygame as pg
import pymunk as pm
from settings import *

class Character(pg.sprite.Sprite):
    def __init__(self, space: pm.space.Space, screen: pg.Surface):
        self.space = space
        self.screen = screen
        self.current_animation = 'idle'
        self.previous_animation = 'idle'
        super().__init__()
        self.body = pm.Body()  # Create a Body
        self.body.position = 50, 400  # Set the position of the body

        self.poly = pm.Poly.create_box(self.body, (58, 80))
        self.poly.color = pg.Color("pink")
        self.poly.mass = 10  # Set the mass on the shape
        self.poly.elasticity = 1
        self.poly.density = 1000
        self.poly.friction = 1
        self.body.moment = 100000000000000
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation
        self.left, self.right, self.up, self.down = False, False, False, False
        self.can_jump = False

        self.size = (100, 100)
        # self.img = pg.image.load('../data/assets/square_normal.PNG').convert_alpha()
        self.animations = dict()
        for key, value in Frog_Animations.items():
            self.animations[key] = [pg.transform.scale(img, self.size) for img in value]
        self.frame = 0

    def handle_keydown(self, event: pg.event.Event):
        if event.key == pg.K_d:
            # Right
            self.right = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
        if event.key == pg.K_a:
            # Left
            self.left = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
        if (event.key == pg.K_w or event.key == pg.K_SPACE) and self.can_jump:
            # UP
            self.up = True
            self.previous_animation = self.current_animation
            self.current_animation = 'jump'

    def handle_keyup(self, event: pg.event.Event):
        if event.key == pg.K_d:
            # Right
            self.right = False
        if event.key == pg.K_a:
            # Left
            self.left = False



    def update(self):
        self.body.angle = 0
        if self.right:
            self.body.position += (10*60/FRAMERATE, 0)
        if self.left:
            self.body.position += (-10 * 60/FRAMERATE, 0)
        if not self.left and not self.right:
            self.body.velocity = (0, self.body.velocity.y)
        if self.up:
            self.body.velocity += (0, -800)
            self.up = False
            self.can_jump = False

    def draw(self, clock):
        if clock % int(3*FRAMERATE/60) == 0:
            self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]):
            self.frame = 0
        self.screen.blit(self.animations[self.current_animation][self.frame], (self.body.position.x - self.size[0]/2, self.body.position.y - 6*self.size[1]/10), self.animations[self.current_animation][self.frame].get_rect())







