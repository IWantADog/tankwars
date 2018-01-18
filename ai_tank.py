from tank import Tank
from config import ai_tank_img, ai_boss_img, gift_tank_img
import random
from point import Point

class AiTank(Tank):
    def __init__(self, aim_tank, aim_boss, tank_img=ai_tank_img): #目标坦克坐标，目标boos坐标
        point = random.choice([Point(0, 0),  Point(450, 0), Point(860, 0)])
        Tank.__init__(self, tank_img, point=point)
        self.aim_tank = aim_tank
        self.aim_boss = aim_boss
        self.state = False               # 是否发现目标
        self.speed = 2
        self.last_move_time = 0

    def find_aim(self):   # 返回ai需要移动的方向
        tank_x, tank_y = self.point.get()
        aim_tank_x, aim_tank_y = self.aim_tank.get()
        aim_boss_x, aim_boss_y = self.aim_boss.get()

        self.state = True
        if -40 <= tank_x - aim_boss_x <= 40:
            if 0 < aim_boss_y - tank_y <= 150:
                return 's'
            elif 0 < tank_y - aim_boss_y <= 150:
                return 'w'

        if -40 <= tank_y - aim_boss_y <= 40:
            if 0 < aim_boss_x - tank_x <= 150:
                return 'd'
            elif 0 < tank_x - aim_boss_x <= 150:
                return 'a'

        if -40 <= tank_x - aim_tank_x <= 40:
            if 0 < aim_tank_y - tank_y <= 150:
                return 's'
            elif 0 < tank_y - aim_tank_y <= 150:
                return 'w'

        if -40 <= tank_y - aim_tank_y <= 40:
            if 0 < aim_tank_x - tank_x <= 150:
                return 'd'
            elif 0 < tank_x - aim_tank_x <= 150:
                return 'a'

        self.state = False
        return False

    def ai_move(self, current_time, rate=2000):
        dire = self.find_aim()
        if not dire:
            if current_time > self.last_move_time + rate:
                dire = random.choice(['w', 's', 'a', 'd'])
                self.last_move_time = current_time
            else:
                dire = self.dirct
        self.move(dire)

    def ai_shoot(self, current_time, rate):
        if self.state:
            return self.shoot(current_time=current_time, rate=rate)


class GiftTank(AiTank):
    def __init__(self, aim_tank, aim_boss):
        AiTank.__init__(self, aim_tank=aim_tank, aim_boss=aim_boss, tank_img=gift_tank_img)


class BossTank(AiTank):
    def __init__(self, aim_tank, aim_boss):
        AiTank.__init__(self, aim_tank=aim_tank, aim_boss=aim_boss, tank_img=ai_boss_img)
        self.speed = 4









































