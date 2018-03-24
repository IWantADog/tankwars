import pygame
from tank import Tank
from config import boss_birth_img, boss_boom_img
import random
from point import Point
from gift import Clock, OneLife


class AiTank(Tank):
    def __init__(self, tank_img, point=None): #目标坦克坐标，目标boos坐标
        if not point:
            point = random.choice([(0, 0), (450, 0), (860, 0)])
        Tank.__init__(self, tank_img, point=point)
        self.state = 'notfind'               # 是否发现目标
        self.speed = 2
        self.last_move_time = 0
        self.name = 'ai'
        self.distance = 150
        self.range = 40

    def find_aim(self, aim_tank, aim_boss):   # 返回ai需要移动的方向
        tank_x, tank_y = self.point.get()
        aim_tank_x, aim_tank_y = aim_tank.get()
        aim_boss_x, aim_boss_y = aim_boss.get()

        self.state = 'finded'
        if -self.range <= tank_x - aim_boss_x <= self.range:
            if 0 < aim_boss_y - tank_y <= self.distance:
                return 's'
            elif 0 < tank_y - aim_boss_y <= self.distance:
                return 'w'

        if -self.range <= tank_y - aim_boss_y <= self.range:
            if 0 < aim_boss_x - tank_x <= self.distance:
                return 'd'
            elif 0 < tank_x - aim_boss_x <= self.distance:
                return 'a'

        if -self.range <= tank_x - aim_tank_x <= self.range:
            if 0 < aim_tank_y - tank_y <= self.distance:
                return 's'
            elif 0 < tank_y - aim_tank_y <= self.distance:
                return 'w'

        if -self.range <= tank_y - aim_tank_y <= self.range:
            if 0 < aim_tank_x - tank_x <= self.distance:
                return 'd'
            elif 0 < tank_x - aim_tank_x <= self.distance:
                return 'a'

        self.state = 'notfind'
        return False

    def get_name(self):
        return self.name

    def ai_move(self, current_time, aim_player, aim_boss, rate=2000):
        if self.state != 'clock':
            dire = self.find_aim(aim_player, aim_boss)
            if not dire:
                if current_time > self.last_move_time + rate:
                    dire = random.choice(['w', 's', 'a', 'd'])
                    self.last_move_time = current_time
                else:
                    dire = self.dirct
            self.move(dire)

    def ai_shoot(self, current_time, bullet_images, rate):
        if self.state == 'finded':
            return self.shoot(current_time=current_time, bullet_images=bullet_images, rate=rate)


class GiftTank(AiTank):
    def __init__(self, tank_images):
        AiTank.__init__(self, tank_img=tank_images)
        self.name = 'gift'

    def leave_gift(self):
        gift_list = [Clock(self.point), OneLife(self.point)]
        return random.choice(gift_list)

class BossTank_1(AiTank):
    def __init__(self, tank_images):
        AiTank.__init__(self, tank_img=tank_images)
        self.speed = 4
        self.life_number = 8
        self.name = 'boss'

class BossTank_2(AiTank):
    def __init__(self, tank_images):
        AiTank.__init__(self, tank_img=tank_images, point=(420, 0))
        self.speed = 4
        self.life_number = 10
        self.name = 'boss'
        self.birth_image = pygame.image.load(boss_birth_img).convert_alpha()
        self.boom_image = pygame.image.load(boss_boom_img).convert_alpha()
        self.frame_width = self.birth_image.get_width() // 4
        self.frame_height = self.birth_image.get_height()
        self.distance = 250
        self.range = 40





































