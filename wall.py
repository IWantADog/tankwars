import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from point import Point
from config import brickwall_img, steelwall_img, img_width, img_height

class Brickwall(Sprite):
    def __init__(self, point):
        Sprite.__init__(self)
        self.life = 3
        self.name = 'brickwall'
        self.point = Point(point)
        self.image = pygame.image.load(brickwall_img).convert_alpha()
        self.rect = Rect(self.point.x, self.point.y, img_width, img_height)

    def lost_life(self, n):
        self.life -= n

    def get_point(self):
        return self.point



class Steelwall(Sprite):
    def __init__(self, point):
        Sprite.__init__(self)
        self.life = 3
        self.name = 'steelwall'
        self.point = Point(point)
        self.image = pygame.image.load(steelwall_img).convert_alpha()
        self.rect = Rect(self.point.x, self.point.y, img_width, img_height)

    def lost_life(self, n):
        self.life -= n

    def get_point(self):
        return self.point