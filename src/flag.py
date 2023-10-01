from src.settings import *
import pygame as pg
import pymunk as pm


class Flag(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, space, size, location):
        super().__init__()
        self.space = space
        self.screen = screen
        self.body = pm.Body()  # Create a Body
        self.body.position = (location[0] + size[0]/2, location[1] + size[1]/2)  # Set the position of the body
        self.body.body_type = pm.Body.KINEMATIC
        self.flag_size = size
        self.poly = pm.Poly.create_box(self.body, size)  # Create a box shape and attach to body
        self.poly.color = pg.Color("blue")
        self.poly.mass = 0 # Set the mass on the shape
        self.poly.elasticity = 0
        self.poly.density = 0
        self.poly.friction = 0
        self.imgs = Flag_Animation
        self.size = (size[0]*2, size[1])
        self.img = [pg.transform.scale(img, self.size) for img in self.imgs]
        self.frame = 0
        self.got = False

    def add_to_space(self):
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation

    def draw(self, clock, started):
        if clock % int(3 * FRAMERATE / 60) == 0:
            if started:
                self.frame += 1
        if self.frame >= len(self.imgs):
            self.frame = 0
        self.body.angle = 0
        self.screen.blit(self.img[self.frame], (self.body.position.x - self.size[0]/2, self.body.position.y - self.size[1]/2), self.img[self.frame].get_rect())