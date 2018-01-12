import pygame
from point import Point
from pygame import Rect
from config import bullet_height, bullet_width

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 位置 方向 速度
        self.point = None
        self.dire = None
        self.speed = 8
        self.last_time = None
        self.islive = True

    def load(self, width=bullet_width, height=bullet_height):
        self.master_imge = pygame.image.load('shoot.png').convert_alpha()
        self.frame_width = width
        self.frame_height = height

    def lanch(self , point, dire): # 位置 方向
        self.point = point
        self.dire = dire
        frame = None
        if dire == 'w':
            frame = 0
        elif dire == 's':
            frame = 1
        elif dire == 'd':
            frame = 2
        elif dire == 'a':
            frame = 3

        # print('dire %s, frame %d' % (dire, frame))
        frame_x = frame * self.frame_width
        frame_y = 0
        rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
        self.image = self.master_imge.subsurface(rect)
        self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)


    def move(self):
        if self.dire == 'w':
            self.point.y -= self.speed
        elif self.dire == 's':
            self.point.y += self.speed
        elif self.dire == 'a':
            self.point.x -= self.speed
        elif self.dire == 'd':
            self.point.x += self.speed

        if self.point.x < 0 or self.point.x > 490 or \
                        self.point.y < 0 or self.point.y > 490:
            self.islive = False

        self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)

    def update(self):
        if self.islive:
            self.move()