from src.settings import *
import pygame as pg
import pymunk as pm


class Item(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, space, size, location):
        super().__init__()
        self.space = space
        self.screen = screen
        self.flag_size = size
        self.location = (location[0] + size[0]/2, location[1] + size[1]/2)  # Set the position of the body
        self.imgs = Item_Animation
        self.size = SCREEN_SIZE[0]/screen_tiles[0], SCREEN_SIZE[1]/screen_tiles[1]
        self.img = [pg.transform.scale(img, self.size) for img in self.imgs]
        self.frame = 0
        self.got = False
        self.rect = pg.Rect(location[0] - size[0]/2, location[1] - size[1]/2, *self.size)

    def draw(self, clock, started):
        if clock % int(3 * FRAMERATE / 60) == 0:
            if started:
                self.frame += 1
        if self.frame >= len(self.imgs):
            self.frame = 0
        #self.body.angle = 0
        self.screen.blit(self.img[self.frame], (self.location[0] - self.size[0]/2, self.location[1] - self.size[1]/2 - self.size[1]/7), self.img[self.frame].get_rect())
        if DEBUG:
            pg.draw.rect(self.screen, (255, 0, 0), self.rect)
