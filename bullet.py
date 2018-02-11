import pygame
from point import Point
from pygame import Rect
from config import bullet_height, bullet_width, area_width, area_height

def load_bullet_images():
    images_name_list = ['images\\bullet\\up.png', 'images\\bullet\\down.png',
                        'images\\bullet\\right.png', 'images\\bullet\\left.png']
    return [pygame.image.load(item).convert_alpha() for item in images_name_list]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullent_images):
        pygame.sprite.Sprite.__init__(self)
        # 位置 方向 速度
        self.point = None
        self.start_point = None
        self.dire = None
        self.speed = 8
        self.last_time = None
        self.islive = True
        self.master_image = bullent_images
        self.frame = None
        self.width, self.height = None, None

    # def load(self, width=bullet_width, height=bullet_height):
    #     self.master_imge = pygame.image.load(shoot_img).convert_alpha()
    #     self.frame_width = width
    #     self.frame_height = height

    def choose_dire(self, dire):
        self.dire = dire
        if dire == 'w':
            self.frame = 0
        elif dire == 's':
            self.frame = 1
        elif dire == 'd':
            self.frame = 2
        elif dire == 'a':
            self.frame = 3

        self.image = self.master_image[self.frame]
        self.width, self.height = self.image.get_size()

    def lanch(self, point): # 位置 方向
        self.point = Point(point)
        self.start_point = Point(point)
        self.rect = Rect(self.point.x, self.point.y, self.width, self.height)


    def move(self):
        if self.dire == 'w':
            self.point.y -= self.speed
        elif self.dire == 's':
            self.point.y += self.speed
        elif self.dire == 'a':
            self.point.x -= self.speed
        elif self.dire == 'd':
            self.point.x += self.speed

        if self.point.x < 0 or self.point.x > area_width - bullet_width or \
                        self.point.y < 0 or self.point.y > area_height - bullet_height or \
                        self.start_point.get_distance(self.point) >= 300:
            self.islive = False

        self.rect = Rect(self.point.x, self.point.y, self.width, self.height)

    def update(self):
        if self.islive:
            self.move()