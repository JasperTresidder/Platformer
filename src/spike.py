import pygame as pg
import pymunk as pm


class Spike(pg.sprite.Sprite):
    def __init__(self, space, size, location):
        super().__init__()
        self.space = space
        self.body = pm.Body()  # Create a Body
        self.body.body_type = pm.Body.STATIC
        self.body.position = (location[0] + size[0]/2, location[1] + size[1]/2)  # Set the position of the body

        self.poly = pm.Poly.create_box(self.body, (size[0] - size[1], 0), size[1]/2)  # Create a box shape and attach to body
        self.poly.color = pg.Color("pink")
        self.poly.mass = 100000 # Set the mass on the shape
        self.poly.elasticity = 0
        self.poly.density = 1000000
        self.poly.friction = 0.9

    def add_to_space(self):
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation