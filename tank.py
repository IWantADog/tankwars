import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from point import Point
from bullet import Bullet
from wall import Brickwall
from config import img_width, img_height, bullet_height, bullet_width, birth_img, boom_img
import sys

class Tank(Sprite):
    def __init__(self,filename, columns, width=img_width, height=img_height):
        Sprite.__init__(self)
        #self.image = pygame.image.load(filename).convert_alpha()
        self.frame = 2
        self.last_time = 0
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.birth_image = pygame.image.load(birth_img).convert_alpha()
        self.boom_image = pygame.image.load(boom_img).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.columns = columns
        self.first_frame = 2
        self.last_frame = self.first_frame + columns - 1

        self.life = 0                        # 生命值为3
        self.birth = 4                       # 诞生动态图片
        self.boom = 7                        # 死亡动态图片
        self.ismoved = False                 # 是否移动
        self.dirct = 'w'                     # 方向
        self.old_dirct = -1                  # 上一次的方向
        self.point = Point(200, 100)         # 位置
        self.speed = 3                       # 速度
        self.rect = Rect(self.point.x, self.point.y, width, height)
        self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}  # 碰撞方向

        #bullet
        self.last_shoot_time = 0

    def get_point(self):
        return self.point

    def set_collide_dirct(self, dirct):
        self.collide_dirct[dirct] = True

    def lost_life(self, n):
        self.life -= n

    def move(self, dire): #direction
        if self.life > 0:
            self.ismoved = True
            self.dirct = dire
            if dire == 'w':
                if not self.collide_dirct['w']:
                    self.point.y -= self.speed
                if dire != self.old_dirct:
                    self.frame = 2
                    self.first_frame = 2
                    self.last_frame = self.frame + self.columns -1
                    self.old_dirct = dire

            elif dire == 's':
                if not self.collide_dirct['s']:
                    self.point.y += self.speed
                if dire != self.old_dirct:
                    self.frame = 6
                    self.first_frame = 6
                    self.last_frame = self.frame + self.columns - 1
                    self.old_dirct = dire

            elif dire == 'a':
                if not self.collide_dirct['a']:
                    self.point.x -= self.speed
                if dire != self.old_dirct:
                    self.frame = 0
                    self.first_frame = 0
                    self.last_frame = self.frame + self.columns - 1
                    self.old_dirct = dire

            elif dire == 'd':
                if not self.collide_dirct['d']:
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

            self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}
            self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)

    def shoot(self, current_time, rate=30):
        if current_time > self.last_shoot_time + rate and self.life > 0:
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
        if self.life > 0 :
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
        elif self.birth > 0:
            frame_x = (4 - self.birth) * self.frame_width
            frame_y = 0
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.birth_image.subsurface(rect)
            self.birth -= 1
            if self.birth == 0:
                self.life = 3           # 当加载完诞生图片时，将life赋为3
        elif self.boom > 0:
            frame_x = (7 - self.boom) * self.frame_width
            frame_y = 0
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.boom_image.subsurface(rect)
            self.boom -= 1


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()
    tt = Tank('tank.png', 2)
    group = Group()
    group.add(tt)

    bullet_group = Group()

    #wall group
    wall_group = Group()
    #brickwall
    bwall = Brickwall(300, 100)

    wall_group.add(bwall)

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

        #wall_group
        wall_group.update()
        wall_group.draw(screen)

        pygame.display.update()