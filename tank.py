import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from point import Point
from bullet import Bullet
from config import tank_width,tank_height, bullet_height, bullet_width
import sys

class Tank(Sprite):
    def __init__(self,filename, columns, width=tank_width, height=tank_width):
        Sprite.__init__(self)
        #self.image = pygame.image.load(filename).convert_alpha()
        self.frame = 2
        self.last_time = 0
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(200, 100, width, height)
        self.columns = columns
        self.first_frame = 2
        self.last_frame = self.first_frame + columns - 1

        self.ismoved = False                 # 是否移动
        self.dirct = 'w'                     # 方向
        self.old_dirct = -1                  # 上一次的方向
        self.point = Point(200, 100)         # 位置
        self.speed = 3                       # 速度

        #bullet
        self.last_shoot_time = 0

    def move(self, dire): #direction
        self.ismoved = True
        self.dirct = dire
        if dire == 'w':
            self.point.y -= self.speed
            if dire != self.old_dirct:
                self.frame = 2
                self.first_frame = 2
                self.last_frame = self.frame + self.columns -1
                self.old_dirct = dire

        elif dire == 's':
            self.point.y += self.speed
            if dire != self.old_dirct:
                self.frame = 6
                self.first_frame = 6
                self.last_frame = self.frame + self.columns - 1
                self.old_dirct = dire

        elif dire == 'a':
            self.point.x -= self.speed
            if dire != self.old_dirct:
                self.frame = 0
                self.first_frame = 0
                self.last_frame = self.frame + self.columns - 1
                self.old_dirct = dire

        elif dire == 'd':
            self.point.x += self.speed
            if dire != self.old_dirct:
                self.frame = 4
                self.first_frame = 4
                self.last_frame = self.frame + self.columns - 1
                self.old_dirct = dire

        if self.point.x < 0:
            self.point.x = 0
        elif self.point.x > 460:
            self.point.x = 460

        if self.point.y < 0:
            self.point.y = 0
        elif self.point.y > 460:
            self.point.y = 460

        self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)

    def shoot(self, current_time, rate=30):
        if current_time > self.last_shoot_time + rate:
            bullet = Bullet()
            bullet.load(bullet_width, bullet_height)
            x, y = self.point.get()
            dis_x = (self.frame_width/2) - (bullet_width/2)
            dis_y = (self.frame_height/2) - (bullet_height/2)
            x += dis_x
            y += dis_y
            bullet.lanch(Point(x, y), self.dirct)
            self.last_shoot_time = current_time
            return bullet


    def update(self, current_time, rate=30):

        if self.ismoved and current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
            self.ismoved = False

        frame_x = (self.frame % self.columns) * self.frame_width
        frame_y = (self.frame // self.columns) * self.frame_height
        rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
        self.image = self.master_image.subsurface(rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()
    tt = Tank('tank.png', 2)
    group = Group()
    group.add(tt)

    bullet_group = Group()

    while True:
        framerate.tick(30)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            tt.move('w')
        elif keys[K_s]:
            tt.move('s')
        elif keys[K_a]:
            tt.move('a')
        elif keys[K_d]:
            tt.move('d')

        if keys[K_j]:
            new_bullet = tt.shoot(current_time, 300)
            if new_bullet:
                bullet_group.add(new_bullet)
            # pass

        for bullet in bullet_group.sprites():
            if not bullet.islive:
                bullet_group.remove(bullet)
                # passj

        # print('1111 ', len(bullet_group.sprites()))
        screen.fill((0,0,0))

        group.update(current_time)
        group.draw(screen)


        bullet_group.update()
        bullet_group.draw(screen)



        pygame.display.update()