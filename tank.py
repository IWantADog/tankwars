import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from point import Point
from bullet import Bullet, load_bullet_images
from wall import Brickwall
import sys
from config import img_width, img_height, bullet_height, bullet_width,\
    birth_img, boom_img, windows_height, windows_width, area_height, area_width\
    , default_point, player_tank_path, ai_tank_path, bullet_path

class Tank(Sprite):
    def __init__(self, images_list, columns=2, point=default_point):
        Sprite.__init__(self)
        self.frame = 2
        self.last_time = 0
        self.master_image = images_list
        self.birth_image = pygame.image.load(birth_img).convert_alpha()
        self.boom_image = pygame.image.load(boom_img).convert_alpha()
        self.frame_width = img_width
        self.frame_height = img_height
        self.columns = columns
        self.first_frame = 2
        self.last_frame = self.first_frame + columns - 1

        self.life = 0                        # 生命值为3
        self.birth = 4                       # 诞生动态图片
        self.boom = 7                        # 死亡动态图片
        self.ismoved = False                 # 是否移动
        self.dirct = 'w'                     # 方向
        self.old_dirct = -1                  # 上一次的方向
        self.point = Point(point)                   # 位置
        self.speed = 3                       # 速度
        self.rect = Rect(self.point.x, self.point.y, self.frame_width, self.frame_height)
        self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}  # 碰撞方向

        #bullet
        self.last_shoot_time = 0

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
            elif self.point.x > area_width - img_width:
                self.point.x = area_width - img_width

            if self.point.y < 0:
                self.point.y = 0
            elif self.point.y > area_height - img_height:
                self.point.y = area_height - img_height

            self.collide_dirct = {'w': False, 's': False, 'a': False, 'd': False}

    def shoot(self, current_time, bullet_images, rate=30):
        if current_time > self.last_shoot_time + rate and self.life > 0:
            bullet = Bullet(bullet_images)
            x, y = self.point.get()
            dis_x = (self.frame_width/2) - (bullet_width/2)
            dis_y = (self.frame_height/2) - (bullet_height/2)
            x += dis_x
            y += dis_y
            bullet.lanch((x, y), self.dirct)
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
            width, height = self.image.get_size()
            self.rect = Rect(self.point.x, self.point.y, width, height)

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


def load_images(images_list):
    return [pygame.image.load(item).convert_alpha() for item in images_list]


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    start_music = pygame.mixer.Sound('music\\start.ogg')
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(start_music)

    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    #player
    p_tank = load_images(player_tank_path)
    tt = Tank(p_tank, 2)
    group = Group()
    group.add(tt)

    #ai tank
    ai_tank = load_images(ai_tank_path)
    ai_t = AiTank(ai_tank)
    ai_group = Group()
    ai_group.add(ai_t)

    #player bullent
    bullet_group = Group()

    #ai bullet
    ai_bullet_group = Group()

    #wall group
    wall_group = Group()
    #brickwall
    bwall = Brickwall((300, 100))

    wall_group.add(bwall)

    bullet_images = load_images(bullet_path)

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
            new_bullet = tt.shoot(current_time,bullet_images, 300)
            if new_bullet:
                bullet_group.add(new_bullet)
            # pass

        for bullet in bullet_group.sprites():
            # print(bullet.point, bullet.start_point, bullet.point.get_distance(bullet.start_point))
            if not bullet.islive:
                bullet_group.remove(bullet)
                # passj
        for ai in ai_group.sprites():
            ai.ai_move(current_time, p_tank.get_point(), p_tank.get_point(), rate=3000)
            ai_tank_bullet = ai.ai_shoot(current_time, 300)
            if ai_tank_bullet:
                ai_bullet_group.add(ai_tank_bullet)

        for bullet in ai_bullet_group.sprites():
            if not bullet.islive:
                ai_bullet_group.remove(bullet)

        # print('1111 ', len(bullet_group.sprites()))
        screen.fill((0,0,0))

        group.update(current_time)
        group.draw(screen)

        ai_group.update(current_time)
        ai_group.draw(screen)

        bullet_group.update()
        bullet_group.draw(screen)

        ai_bullet_group.update()
        ai_bullet_group.draw(screen)

        #wall_group
        wall_group.update()
        wall_group.draw(screen)

        pygame.display.update()