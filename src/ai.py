# 0 nothing, 1 left, 2 right, 3 up, 4 left and up, 5 right and up
# reward time spent, distance to flag.
import pickle

import pygame as pg

class Ai:
    def __init__(self, player):
        self.tick = 0
        file = open('pickle_level', 'rb')
        self.gene = pickle.load(file)

        self.player = player


    def handle_events(self, tick):
        if tick > 0:
            for event in self.gene[tick]:
                if event[0] == pg.KEYUP:
                    self.player.handle_keyup_ai(event[1])
                if event[0] == pg.KEYDOWN:
                    self.player.handle_keydown_ai(event[1])
