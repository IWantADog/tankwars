import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

import sys

from config import *
from tank import Tank
from robot_tank import RobotTank
from point import Point
from wall import Brickwall
from bullet import Bullet
from boss import Boss

MUSCI = 'music/start.ogg'

def get_collide_dirct(ppoint, apoint):
    px, py = ppoint.get()
    ax, ay = apoint.get()
    x = abs(px - ax)
    y = abs(py - ay)

    if x < y:
        if py > ay:
            return 'w', 's'
        else:
            return 's', 'w'
    elif x >= y:
        if px > ax:
            return 'a', 'd'
        else:
            return 'd', 'a'

class Environment:
    def __init__(self):
        self.group_player = Group()
        self.group_robot = Group()
        self.group_bullet_player = Group()
        self.group_bullet_robot = Group()
        self.group_wall = Group()
        self.group_gift = Group()
        self.boss = None
        self.size = (900, 600)
        self.start_time = 0
        
    def bulid(self):
        start_music = pygame.mixer.Sound(MUSCI)
        channel = pygame.mixer.find_channel(True)
        channel.set_volume(0.5)
        channel.play(start_music)

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Tank Wars')

        self.framerate = pygame.time.Clock()

    def add_player(self, player):
        self.group_player.add(player)
    
    def add_robot(self, robot):
        self.group_robot.add(robot)

    def add_player_bullet(self, bullet):
        self.group_bullet_player.add(bullet)

    def add_robot_bullet(self, bullet):
        self.group_bullet_robot.add(bullet)
    
    def add_wall(self, wall):
        self.group_wall.add(wall)
    
    def add_gift(self, gift):
        self.group_gift.add(gift)

    def add_boss(self):
        if not self.boss:
            self.boss = Boss()
        return self.boss
    
    def update(self, current_time):
        self.update_spirtes(current_time)
        self.update_scrren(current_time)

    def update_spirtes(self, current_time):
        # update player bullet
        for bullet in self.group_bullet_player.sprites():
            if not bullet.islive:
                self.group_bullet_player.remove(bullet)

        # update robot tank
        for robot in self.group_robot.sprites():
            if robot.boom == 0:
                if robot.name == 'gift':
                    self.group_gift.add(robot.leave_gift())
                self.group_robot.remove(robot)
            else:
                # TODO robot move rewrite
                # robot.ai_move(current_time, tt.get_point(), ai_t.get_point(), rate=3000)
                robot_tank_bullet = robot.ai_shoot(current_time, 300)
                if robot_tank_bullet:
                    self.group_bullet_robot.add(robot_tank_bullet)
        
        # update robot bullet
        for bullet in self.group_bullet_robot.sprites():
            if not bullet.islive:
                self.group_bullet_robot.remove(bullet)
        
        # update wall
        for wall in self.group_wall.sprites():
            if wall.life <= 0:
                self.group_wall.remove(wall)

    def update_scrren(self, current_time):
        self.screen.fill((0,0,0))

        self.group_player.update(current_time)
        self.group_player.draw(self.screen)

        self.group_robot.update(current_time)
        self.group_robot.draw(self.screen)

        self.group_bullet_player.update()
        self.group_bullet_player.draw(self.screen)

        self.group_bullet_robot.update()
        self.group_bullet_robot.draw(self.screen)

        #wall_group
        self.group_wall.update()
        self.group_wall.draw(self.screen)
    
    def check_collide(self, current_time):
        self.player_bullet_collide()
        self.player_gift_collide(current_time)
        self.robot_bullent_collide()
        self.player_bullet_collide()
        self.tank_wall_collide()
        self.bullet_wall_collide()
        self.tank_boss_collide()
    
    def player_robots_collide(self):
        if not self.group_robot or not self.group_player:
            return
        for robot in self.group_robot.sprites():
            for player in self.group_player:
                if pygame.sprite.collide_rect(player, robot):
                    pp = player.get_point()
                    ip = robot.get_point()
                    pd, ad = get_collide_dirct(pp, ip)
                    player.set_collide_dirct(pd)
                    robot.set_collide_dirct(ad)

    def player_gift_collide(self, current_time):
        collide_list = []
        for player in self.group_player:
            emp_collide_list = pygame.sprite.spritecollide(player, self.group_gift, True)
            collide_list.extend(emp_collide_list)

        for gift in collide_list:
            if gift.name == 'clock':
                self.start_time = current_time
                for ai in self.group_robot.sprites():
                    ai.state = 'clock'
            elif gift.name == 'onelife':
                player.add_life(1)

        for ai in self.group_robot.sprites():
            if ai.state == 'clock':
                if current_time <= self.start_time + 5000:
                    for a in self.group_robot:
                        a.state = 'clock'
                else:
                    for a in self.group_robot:
                        a.state = 'notfind'
                break

    # refactor
    def player_bullet_collide(self):
        for item in self.group_robot.sprites():
            collide_list = pygame.sprite.spritecollide(item, self.group_bullet_player, True)
            item.lost_life(len(collide_list))
    
    def robot_bullent_collide(self):
        for player in self.group_player.sprites():
            collide_list = pygame.sprite.spritecollide(player, self.group_bullet_robot, True)
            player.lost_life(len(collide_list))

    # refactor
    def tank_wall_collide(self):
        player_collide_list = pygame.sprite.groupcollide(self.group_player, self.group_wall, False, False)
        robot_collide_list = pygame.sprite.groupcollide(self.group_robot, self.group_wall, False, False)
        
        for tank, walls in player_collide_list.items():
            for wall in walls:
                tp = tank.get_point()
                wp = wall.get_point()
                td, wd = get_collide_dirct(tp, wp)
                tank.set_collide_dirct(td)

        for tank, walls in robot_collide_list.items():
            for wall in walls:
                tp = tank.get_point()
                wp = wall.get_point()
                td, wd = get_collide_dirct(tp, wp)
                tank.set_collide_dirct(td)

    # refactor
    def bullet_wall_collide(self):
        player_collide_list = pygame.sprite.groupcollide(self.group_wall, self.group_bullet_player, False, True)
        robot_collide_list = pygame.sprite.groupcollide(self.group_wall, self.group_bullet_robot, False, True)
        for wall, bullets in player_collide_list.items():
            if wall.name == 'brickwall':
                wall.lost_life(len(bullets))

        for wall, bullets in robot_collide_list.items():
            if wall.name == 'brickwall':
                wall.lost_life(len(bullets))

    # refactor
    def tank_boss_collide(self):
        if not self.boss:
            return
        
        bp = self.boss.get_point()
        for tank in self.group_robot.sprites():
            if pygame.sprite.collide_rect(tank, self.boss):
                tp = tank.get_point()
                td, _ = get_collide_dirct(tp, bp)
                tank.set_collide_dirct(td)
        
        for tank in self.group_player.sprites():
            if pygame.sprite.collide_rect(tank, self.boss):
                tp = tank.get_point()
                td, _ = get_collide_dirct(tp, bp)
                tank.set_collide_dirct(td)

