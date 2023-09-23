from src.settings import *
import pygame as pg
import pymunk as pm
import math


class Obstacle(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, space, size, location):
        super().__init__()
        self.space = space
        self.screen = screen
        self.body = pm.Body()  # Create a Body
        self.body.position = (location[0] + size[0]/2, location[1] + size[1]/2 + size[1]/8)  # Set the position of the body
        self.initial_position = self.body.position
        self.poly = pm.Poly.create_box(self.body, (size[0], size[1] - size[0]/20), size[0]/10)  # Create a box shape and attach to body
        self.poly.color = pg.Color("blue")
        self.poly.mass = 100000 # Set the mass on the shape
        self.poly.elasticity = 0
        self.poly.density = 100000
        self.poly.friction = 1
        OBSTACLE = pg.image.load(resource_path("data/raw/Pixel Adventure 1/Free/Items/Boxes/Box3/Idle.png")).convert_alpha()
        self.size = 185, 150
        self.size = size[0]*1.7, size[1]*1.39
        self.img = pg.transform.scale(OBSTACLE, self.size)


    def add_to_space(self):
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation


    def draw(self):
        # self.body.angle = 0
        self.blitRotateCenter(self.screen, self.img,(self.body.position.x - self.size[0]/2, self.body.position.y - self.size[1]/2), math.degrees(-self.body.angle))
        #self.screen.blit(self.img, (self.body.position.x - self.size[0]/2, self.body.position.y - self.size[1]/2), self.img.get_rect())

    @staticmethod
    def blitRotateCenter(surf, image, topleft, angle):
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)

