import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from point import Point
from config import clock_img, one_life_img


class Clock(Sprite):
    def __init__(self, point):
        Sprite.__init__(self)
        self.name = 'clock'
        self.image = pygame.image.load(clock_img).convert_alpha()
        self.rect = Rect(point.x, point.y, 30, 28)

    def get_name(self):
        return self.name

class OneLife(Sprite):
    def __init__(self, point):
        Sprite.__init__(self)
        self.name = 'onelife'
        self.image = pygame.image.load(one_life_img).convert_alpha()
        self.rect = Rect(point.x, point.y, 30, 28)

    def get_name(self):
        return self.name
