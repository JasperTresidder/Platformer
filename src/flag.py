from settings import *
import pygame as pg
import pymunk as pm


class Flag(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, space, size, location):
        super().__init__()
        self.space = space
        self.screen = screen
        self.body = pm.Body()  # Create a Body
        self.body.position = (location[0] + size[0]/2, location[1] + size[1]/2)  # Set the position of the body
        self.poly = pm.Poly.create_box(self.body, size)  # Create a box shape and attach to body
        self.poly.color = pg.Color("blue")
        self.poly.mass = 100000 # Set the mass on the shape
        self.poly.elasticity = 0
        self.poly.density = 30
        self.poly.friction = 1
        OBSTACLE = pg.image.load("../data/assets/square_normal.PNG").convert_alpha()
        self.size = 340, 340
        self.img = pg.transform.scale(OBSTACLE, self.size)