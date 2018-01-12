import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from point import Point
from config import brickwall_img, steelwall_img, boss_img, img_width, img_height

class Boss(Sprite):
    def __init__(self, point_x, point_y):
        Sprite.__init__(self)
        self.life = 1
        self.master_img = pygame.image.load(boss_img).convert_alpha()
        self.point = Point(point_x, point_y)
        self.rect = Rect(point_x, point_y, img_width, img_height)

    def get_point(self):
        return self.point

    def lost_life(self, n):
        self.life -= n

    def update(self, *args):
        if self.life > 0:
            rect = Rect(0, 0, img_width, 36)
        else:
            rect = Rect(40, 0, img_width, 36)

        self.image = self.master_img.subsurface(rect)
