import pygame
import random

from .tank import Tank
from .point import Point
from .gift import Clock, OneLife

from config import boss_birth_img, boss_boom_img, ai_tank_path



class RobotTank(Tank):
    master_images_path = ai_tank_path
    def __init__(self, point=None, **kw): #目标坦克坐标，目标boos坐标
        if not point:
            point = (random.uniform(0, 960), 0)
        Tank.__init__(self, point=point, **kw)
        self.state = 'notfind'               # 是否发现目标
        self.speed = kw.get('speed', 2.0)
        self.last_move_time = 0
        self.name = kw.get('name','ai')
        self.distance = kw.get('distance', 150.0)
        self.range = kw.get('range', 40.0)

    def find_aim(self, aim_tank, aim_boss):   # 返回ai需要移动的方向
        tank_x, tank_y = self.point.get()
        aim_tank_x, aim_tank_y = aim_tank.get()
        aim_boss_x, aim_boss_y = aim_boss.get()

        self.state = 'finded'
        if -self.range < tank_x - aim_boss_x < self.range:
            if 0 < aim_boss_y - tank_y <= self.distance:
                return 's'
            elif 0 < tank_y - aim_boss_y <= self.distance:
                return 'w'

        if -self.range < tank_y - aim_boss_y < self.range:
            if 0 < aim_boss_x - tank_x <= self.distance:
                return 'd'
            elif 0 < tank_x - aim_boss_x <= self.distance:
                return 'a'

        if -self.range < tank_x - aim_tank_x < self.range:
            if 0 < aim_tank_y - tank_y <= self.distance:
                return 's'
            elif 0 < tank_y - aim_tank_y <= self.distance:
                return 'w'

        if -self.range < tank_y - aim_tank_y < self.range:
            if 0 < aim_tank_x - tank_x <= self.distance:
                return 'd'
            elif 0 < tank_x - aim_tank_x <= self.distance:
                return 'a'

        self.state = 'notfind'
        return False

    def get_name(self):
        return self.name

    def ai_move(self, current_time, aim_player, aim_boss, group=None, rate=2000):
        if self.state != 'clock':
            dire = self.find_aim(aim_player, aim_boss)
            if not dire:
                if current_time > self.last_move_time + rate:
                    dire = random.choice(['w', 's', 'a', 'd'])
                    self.last_move_time = current_time
                else:
                    dire = self.dirct
            self.move(dire, group)

    def ai_shoot(self, current_time, bullet_images, rate=30):
        if self.state == 'finded':
            return self.shoot(current_time=current_time, bullet_images=bullet_images, rate=rate)

class GiftTank(RobotTank):
    def __init__(self):
        super().__init__(self)
        self.name = 'gift'

    def leave_gift(self):
        gift_list = [Clock(self.point), OneLife(self.point)]
        return random.choice(gift_list)

def create_boss_tank_1():
    return RobotTank(speed=4, life_number=8, name='boss')

def create_boss_tank_2():
    return RobotTank(
        point=(420, 0), speed=4, life_number=10, name='boss', distance=250, range=40
    )





































