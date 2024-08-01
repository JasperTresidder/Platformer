from src.settings import *
import pygame as pg
import pymunk as pm


class Flag(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, space: pm.Space, size: tuple, location: tuple):
        super().__init__()
        self.space = space
        self.screen = screen
        self.flag_size = size
        self.imgs = Flag_Animation
        self.size = (size[0]*2, size[1])
        self.img = [pg.transform.scale(img, self.size) for img in self.imgs]
        self.frame = 0
        self.got = False
        self.rect = pg.Rect(location[0] + size[0]/2 -25, location[1] + size[1]/2 - 40, *size)


    def draw(self, clock, started: bool):
        if clock % int(3 * FRAMERATE / 60) == 0:
            if started:
                self.frame += 1
        if self.frame >= len(self.imgs):
            self.frame = 0
        self.screen.blit(self.img[self.frame], (self.rect.x - self.size[0]/2 + 25, self.rect.y - self.size[1]/2 + 40), self.img[self.frame].get_rect())
        if DEBUG:
            pg.draw.rect(self.screen, (255, 0, 0), self.rect)