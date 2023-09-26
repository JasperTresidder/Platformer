import pygame as pg
from src.settings import *

class Menu:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.get_fonts()
        # self.font = pg.font.SysFont("ariel", 30)
        self.font = pg.font.Font('data/fonts/Grand9K Pixel.ttf', 50)
        self.text = None


    def draw(self, time):
        text = "Level Time: " + time
        text_blit = self.font.render(text, True, (255, 255, 255), (0,0,0))
        self.screen.blit(text_blit,
                         (SCREEN_SIZE[0]/2 - text_blit.get_width()/2, SCREEN_SIZE[1]/2 - text_blit.get_height()))
        text = "Press Enter to Continue..."
        text_blit = self.font.render(text, True, (255, 255, 255), (0,0,0))
        self.screen.blit(text_blit,
                         (SCREEN_SIZE[0] / 2 - text_blit.get_width()/2, SCREEN_SIZE[1] / 2))
        text = "Press R to Retry"
        text_blit = self.font.render(text, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text_blit,
                         (SCREEN_SIZE[0] / 2 - text_blit.get_width() / 2, SCREEN_SIZE[1] / 2 + text_blit.get_height()))

