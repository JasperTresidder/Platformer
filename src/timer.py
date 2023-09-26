import math
import time
from src.settings import *
import pygame as pg


class Timer(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.screen = screen
        self.font = pg.font.get_fonts()
        #self.font = pg.font.SysFont("ariel", 30)
        self.font = pg.font.Font('data/fonts/Grand9K Pixel.ttf', 30)
        self.start_time = time.time_ns()
        self.end_time = None



    def draw(self):
        self.end_time = time.time_ns()
        time_centi_seconds = str(round((self.end_time - self.start_time) / math.pow(10,9), 1)).ljust(3, '0')
        text = self.font.render(time_centi_seconds, True, (255, 255, 255))
        self.screen.blit(text,
                        (SCREEN_SIZE[0] - text.get_width() - 40, 40))

    def get_ms_time(self) -> str:
        return str(round((self.end_time - self.start_time) / math.pow(10,9), 3)).ljust(6, '0')
    def reset(self):
        self.start_time = time.time_ns()

