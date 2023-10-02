import math
import time
from src.settings import *
import pygame as pg


class Timer(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.screen = screen
        self.font = pg.font.Font('data/fonts/Grand9K Pixel.ttf', 30)
        self.text0 = self.font.render('Esc - Exit', True, (255, 255, 255))
        self.text0_dest = SCREEN_SIZE[0] - self.text0.get_width() - 40, 40 + 2 * self.text0.get_height()
        self.text1 = self.font.render('R - Retry', True, (255, 255, 255))
        self.text1_dest = SCREEN_SIZE[0] - self.text1.get_width() - 40, 40 + 3 * self.text1.get_height()
        self.text2 = self.font.render('T - Toggle Replay', True, (255, 255, 255))
        self.text2_dest = SCREEN_SIZE[0] - self.text2.get_width() - 40, 40 + self.text1.get_height()
        self.ai_text = self.font.render('RECORD REPLAY', True, (0, 200, 0))
        self.ai_dest = SCREEN_SIZE[0]/2 - self.text1.get_width()/2 - 40, 40




    def draw(self, frames, ai):
        if frames < 0:
            frames = 0
        time_frames = str(round(frames/100, 1)).ljust(3, '0')
        text = self.font.render(time_frames, True, (200, 0, 0))
        self.screen.blit(text,
                        (SCREEN_SIZE[0] - text.get_width() - 40, 40))
        self.screen.blit(self.text0, self.text0_dest)
        self.screen.blit(self.text1, self.text1_dest)
        self.screen.blit(self.text2, self.text2_dest)
        if ai:
            self.screen.blit(self.ai_text, self.ai_dest)


