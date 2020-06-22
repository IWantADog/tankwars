import sys

import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from point import Point
from bullet import Bullet
from wall import Brickwall
from collide import player_ai_collide, tank_wall_collide

from config import *

class Tank(Sprite):
    master_image = None

    def __init__(self, columns=2, point=default_point):
        Sprite.__init__(self)
        self.frame = 2
        self.last_time = 0
        
        self.columns = columns
        self.first_frame = 2
        self.last_frame = self.first_frame + columns - 1

        self.life = 0                        # 生命值为3
        self.life_number = 3
        self.birth = 4                       # 诞生动态图片
        self.boom = 7                        # 死亡动态图片
        self.ismoved = False                 # 是否移动
        self.dirct = 'w'                     # 方向
        self.old_dirct = -1                  # 上一次的方向
        self.point = Point(point)                   # 位置
        self.speed = 3.0                     # 速度
        self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}  # 碰撞方向
        #bullet
        self.last_shoot_time = 0
    
    def load_images(self, images=None, birth_imgs=None, boom_imgs=None):
        if images is None:
            images = player_tank_path

        if birth_imgs is None:
            birth_imgs = birth_img

        if boom_imgs is None:
            boom_imgs = boom_img

        # TODO 减少图片的加入数量，所有的图片仅载入一次
        self.master_image = [pygame.image.load(item).convert_alpha() for item in images]

        self.width, self.height = self.master_image[0].get_size()
        self.birth_image = pygame.image.load(birth_imgs).convert_alpha()
        self.boom_image = pygame.image.load(boom_imgs).convert_alpha()
        self.frame_width = self.birth_image.get_width() // 4
        self.frame_height = self.birth_image.get_height()
        self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)


    def get_point(self):
        return self.point

    def set_collide_dirct(self, dirct):
        self.collide_dirct[dirct] = True

    def add_life(self, n):
        self.life += n

    def lost_life(self, n):
        if self.life > 0:
            self.life -= n

        if self.life < 0:
            self.life = 0

    def get_life(self):
        return self.life

    def get_birth(self):
        return self.birth

    def move(self, dire, group=None): #direction
        if self.life > 0:
            self.ismoved = True
            self.dirct = dire
            if dire == 'w':
                self.point.y -= self.speed
                player_ai_collide(self, group)
                if self.collide_dirct['w']:
                    self.point.y += self.speed

                if dire != self.old_dirct:
                    self.frame = 2
                    self.first_frame = 2
                    self.last_frame = self.frame + self.columns -1
                    self.old_dirct = dire

            elif dire == 's':
                self.point.y += self.speed
                player_ai_collide(self, group)
                if self.collide_dirct['s']:
                    self.point.y -= self.speed

                if dire != self.old_dirct:
                    self.frame = 6
                    self.first_frame = 6
                    self.last_frame = self.frame + self.columns - 1
                    self.old_dirct = dire

            elif dire == 'a':
                self.point.x -= self.speed
                player_ai_collide(self, group)
                if self.collide_dirct['a']:
                    self.point.x += self.speed

                if dire != self.old_dirct:
                    self.frame = 0
                    self.first_frame = 0
                    self.last_frame = self.frame + self.columns - 1
                    self.old_dirct = dire

            elif dire == 'd':
                self.point.x += self.speed
                player_ai_collide(self, group)
                if self.collide_dirct['d']:
                    self.point.x -= self.speed

                if dire != self.old_dirct:
                    self.frame = 4
                    self.first_frame = 4
                    self.last_frame = self.frame + self.columns - 1
                    self.old_dirct = dire

            if self.point.x < 0:
                self.point.x = 0
            elif self.point.x > area_width - self.width:
                self.point.x = area_width - self.width

            if self.point.y < 0:
                self.point.y = 0
            elif self.point.y > area_height - self.height:
                self.point.y = area_height - self.height

            self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}

    def shoot(self, current_time, rate=30):
        if current_time > self.last_shoot_time + rate and self.life > 0:
            bullet = Bullet()
            bullet.load_images()
            bullet.choose_dire(self.dirct)
            x, y = self.point.get()
            dis_x = (self.frame_width/2) - (bullet.width/2)
            dis_y = (self.frame_height/2) - (bullet.height/2)
            x += dis_x
            y += dis_y
            bullet.lanch((x, y))
            self.last_shoot_time = current_time
            return bullet

    def update(self, current_time, rate=30):
        if self.life > 0 :
            if self.ismoved and current_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                    self.last_time = current_time
                    self.ismoved = False

            self.image = self.master_image[self.frame]
            self.width, self.height = self.image.get_size()
            self.rect = Rect(self.point.x, self.point.y, self.width, self.height)

        elif self.birth > 0:
            frame_x = (4 - self.birth) * self.frame_width
            frame_y = 0
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.birth_image.subsurface(rect)
            self.birth -= 1
            if self.birth == 0:
                self.life = self.life_number           # 当加载完诞生图片时，将life赋为3
        elif self.boom > 0:
            frame_x = (7 - self.boom) * self.frame_width
            frame_y = 0
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.boom_image.subsurface(rect)
            self.boom -= 1


class PlayerTank(Tank):
    def controller(self, keys, current_time):
        if keys[K_w]:
            self.move('w')
        elif keys[K_s]:
            self.move('s')
        elif keys[K_a]:
            self.move('a')
        elif keys[K_d]:
            self.move('d')
        else:
            pass

        if keys[K_j]:
            return self.shoot(current_time, 300)

        return None